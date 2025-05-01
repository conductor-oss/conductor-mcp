from datetime import datetime, timedelta
import httpx
import logging
import os
import json
from utils.constants import CONDUCTOR_SERVER_URL, CONDUCTOR_AUTH_KEY, CONDUCTOR_AUTH_SECRET


_last_token_retrieval = datetime(1,1,1)
TOKEN_LIFE_DURATION = timedelta(hours=2)

_token = 'UNASSIGNED'

async def get_token():
    """Retrieves and refreshes a JWT token required for making HTTP requests to Conductor

    :return: JWT token based on auth key and secret pulled from the environment
    """
    current_time = datetime.now()
    global _last_token_retrieval
    time_since_last_retrieval = current_time - _last_token_retrieval
    if time_since_last_retrieval > TOKEN_LIFE_DURATION:
        logging.info('Refreshing token')
        _last_token_retrieval = datetime.now()
        token_url = os.path.join(os.environ[CONDUCTOR_SERVER_URL], 'token')
        response = httpx.post(token_url,
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            data=json.dumps({
                'keyId': os.environ[CONDUCTOR_AUTH_KEY],
                'keySecret': os.environ[CONDUCTOR_AUTH_SECRET]
            }))
        global _token
        _token = response.json()['token']
    return _token
