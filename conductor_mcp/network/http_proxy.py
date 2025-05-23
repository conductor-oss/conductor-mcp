#  Copyright 2025 Orkes Inc.
#
#  Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
#  the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
#  an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
#  specific language governing permissions and limitations under the License.

import json
import logging
import httpx
import os
from typing import Dict, Any
from conductor_mcp.network import token_manager
from conductor_mcp.utils.constants import CONDUCTOR_SERVER_URL


logging.basicConfig(
    format="%(levelname)s [%(asctime)s] %(name)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S", level=logging.DEBUG
)


async def http_get(resource_path: str):
    """Executes token-authenticated HTTP GET requests to the provided URL

    :param resource_path: The resource path to apply to the server's API endpoint
    :return: The results of the GET request
    """
    full_url = os.path.join(os.environ[CONDUCTOR_SERVER_URL], resource_path)
    logging.debug(f"Requesting url: {full_url}")
    token = await token_manager.get_token()
    response = httpx.get(
        full_url, headers={"X-Authorization": token, "Content-Type": "application/json; charset=utf-8"}
    )
    return response.text


async def http_post(resource_path: str, data: Dict[str, Any] = {}, additional_headers: Dict[str, str] = {}):
    """Executes token-authenticated HTTP POST requests to the provided URL

    :param resource_path: The resource path to apply to the server's API endpoint
    :param data: A dictionary containing any arguments to pass as part of the POST request
    :param additional_headers: A dictionary containing any additional key/values to add to the headers of the request
    :return: The results of the POST request
    """
    full_url = os.path.join(os.environ[CONDUCTOR_SERVER_URL], resource_path)
    logging.debug(f"Requesting url: {full_url}")
    token = await token_manager.get_token()
    response = httpx.post(
        full_url,
        headers={
            "X-Authorization": token,
            "Content-Type": "application/json; charset=utf-8",
            **additional_headers,
        },
        data=json.dumps(data),
    )
    return response.text
