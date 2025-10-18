from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional, List

from security import create_access_token, decode_access_token, get_password_hash, verify_password, Token

app = FastAPI()

# This is a dummy user database. In a real application, this would be a database.
FAKE_USERS_DB = {
    "jules": {
        "username": "jules",
        "full_name": "Jules",
        "email": "jules@example.com",
        "hashed_password": get_password_hash("password"),
        "disabled": False,
    }
}

class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

class UserInDB(User):
    hashed_password: str

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def fake_decode_token(token):
    return decode_access_token(token)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    token_data = fake_decode_token(token)
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = get_user(FAKE_USERS_DB, token_data.username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user(FAKE_USERS_DB, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.get("/health")
def health_check():
    return {"status": "ok"}

# Registry Profiles API
from profiles import RegistryProfile, db, next_id

@app.post("/profiles", response_model=RegistryProfile)
def create_profile(profile: RegistryProfile):
    global next_id
    profile.id = next_id
    db.append(profile)
    next_id += 1
    return profile

@app.get("/profiles", response_model=List[RegistryProfile])
def get_profiles():
    return db

@app.get("/profiles/{profile_id}", response_model=RegistryProfile)
def get_profile(profile_id: int):
    for profile in db:
        if profile.id == profile_id:
            return profile
    raise HTTPException(status_code=404, detail="Profile not found")

@app.put("/profiles/{profile_id}", response_model=RegistryProfile)
def update_profile(profile_id: int, updated_profile: RegistryProfile):
    for i, profile in enumerate(db):
        if profile.id == profile_id:
            updated_profile.id = profile_id
            db[i] = updated_profile
            return updated_profile
    raise HTTPException(status_code=404, detail="Profile not found")

@app.delete("/profiles/{profile_id}")
def delete_profile(profile_id: int):
    for i, profile in enumerate(db):
        if profile.id == profile_id:
            del db[i]
            return {"message": "Profile deleted"}
    raise HTTPException(status_code=404, detail="Profile not found")

from epp_client.client import EPPClient
from epp_client.commands.domain import check_domain

# Pydantic model for the domain check request
class DomainCheckRequest(BaseModel):
    domain_name: str
    profile_id: int

# Pydantic model for the domain check response
class DomainCheckResponse(BaseModel):
    availability: bool
    request_xml: str
    response_xml: str

# Batch Operations API
from fastapi import File, UploadFile
from celery.result import AsyncResult
from worker.tasks import check_domain_task
import csv
import io

@app.post("/jobs/check-domains")
async def create_domain_check_job(profile_id: int, file: UploadFile = File(...)):
    profile = get_profile(profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    contents = await file.read()
    stream = io.StringIO(contents.decode("utf-8"))
    reader = csv.reader(stream)

    tasks = []
    for row in reader:
        domain_name = row[0]
        task = check_domain_task.delay(profile.dict(), domain_name)
        tasks.append(task.id)

    return {"job_ids": tasks}

@app.get("/jobs/{job_id}")
def get_job_status(job_id: str):
    task = AsyncResult(job_id)
    if task.state == 'PENDING':
        response = {
            "state": task.state,
            "status": "Pending..."
        }
    elif task.state != 'FAILURE':
        response = {
            "state": task.state,
            "status": task.info.get('status', ''),
            "result": task.result
        }
    else:
        response = {
            "state": task.state,
            "status": str(task.info),  # this is the exception raised
            "result": None
        }
    return response

# Helper to parse domain availability from XML
def _parse_domain_availability(xml_response: str, domain_name: str) -> bool:
    import xml.etree.ElementTree as ET
    root = ET.fromstring(xml_response)
    ns = {
        'epp': 'urn:ietf:params:xml:ns:epp-1.0',
        'domain': 'urn:ietf:params:xml:ns:domain-1.0'
    }
    # Find the <domain:name> element with the matching domain name
    name_element = root.find(f".//domain:cd[domain:name='{domain_name}']/domain:name", ns)
    if name_element is not None:
        return name_element.attrib.get('avail') == '1'
    return False

@app.post("/api/domains/check", response_model=DomainCheckResponse)
async def domain_check(request: DomainCheckRequest):
    profile = get_profile(request.profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    client = EPPClient(
        host=profile.host,
        port=profile.port,
        username=profile.username,
        password=profile.password,
        ssl_certfile=profile.ssl_certfile,
        ssl_keyfile=profile.ssl_keyfile
    )

    try:
        client.connect()
        client.login()

        request_xml = check_domain(request.domain_name)
        response_xml = client.send_command(request_xml)

        availability = _parse_domain_availability(response_xml, request.domain_name)

        return DomainCheckResponse(
            availability=availability,
            request_xml=request_xml,
            response_xml=response_xml
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if client.sock:
            client.logout()
