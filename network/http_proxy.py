import json
import logging
import httpx
import os
from typing import Dict, Any
from network import token_manager
from utils.constants import CONDUCTOR_SERVER_URL


logging.basicConfig(
    format='%(levelname)s [%(asctime)s] %(name)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.DEBUG
)

async def http_get(resource_path: str):
    full_url = os.path.join(os.environ[CONDUCTOR_SERVER_URL], resource_path)
    logging.debug(f'Requesting url: {full_url}')
    token = await token_manager.get_token()
    response = httpx.get(full_url,
                         headers={
                             'X-Authorization': token,
                             'Content-Type': 'application/json; charset=utf-8'
                         })
    return response.text

async def http_post(resource_path: str, data_json_str: Dict[str, Any] = {}):
    full_url = os.path.join(os.environ[CONDUCTOR_SERVER_URL], resource_path)
    logging.debug(f'Requesting url: {full_url}')
    token = await token_manager.get_token()
    response = httpx.post(full_url,
                         headers={
                             'X-Authorization': token,
                             'Content-Type': 'application/json; charset=utf-8'
                         },
                         data=json.dumps(data_json_str))
    return response.text
