from .celery import app
from epp_client.client import EPPClient
from epp_client.commands.domain import check_domain
import time

@app.task
def add(x, y):
    time.sleep(5)  # Simulate a long-running task
    return x + y

@app.task
def check_domain_task(profile, domain_name):
    """
    Checks a single domain using the given profile.
    """
    client = EPPClient(
        host=profile['host'],
        port=profile['port'],
        username=profile['username'],
        password=profile['password'],
        ssl_certfile=profile.get('ssl_certfile'),
        ssl_keyfile=profile.get('ssl_keyfile')
    )
    try:
        client.connect()
        client.login()
        check_xml = check_domain(domain_name)
        response = client.send_command(check_xml)
        client.logout()
        return response
    except Exception as e:
        return str(e)
