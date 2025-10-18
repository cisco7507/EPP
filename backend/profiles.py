from pydantic import BaseModel
from typing import List, Optional

class RegistryProfile(BaseModel):
    id: Optional[int] = None
    name: str
    host: str
    port: int
    username: str
    password: str
    ssl_certfile: Optional[str] = None
    ssl_keyfile: Optional[str] = None

# In-memory database
db: List[RegistryProfile] = []
next_id = 1
