#  Copyright 2025 Orkes Inc.
#
#  Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
#  the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
#  an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
#  specific language governing permissions and limitations under the License.

from datetime import datetime, timedelta
import httpx
import logging
import os
import json
from conductor_mcp.utils.constants import CONDUCTOR_SERVER_URL, CONDUCTOR_AUTH_KEY, CONDUCTOR_AUTH_SECRET


_last_token_retrieval = datetime(1, 1, 1)
TOKEN_LIFE_DURATION = timedelta(hours=2)

_token = "UNASSIGNED"


async def get_token():
    """Retrieves and refreshes a JWT token required for making HTTP requests to Conductor

    :return: JWT token based on auth key and secret pulled from the environment
    """
    current_time = datetime.now()
    global _last_token_retrieval
    time_since_last_retrieval = current_time - _last_token_retrieval
    if time_since_last_retrieval > TOKEN_LIFE_DURATION:
        logging.info("Refreshing token")
        _last_token_retrieval = datetime.now()
        token_url = os.path.join(os.environ[CONDUCTOR_SERVER_URL], "token")
        response = httpx.post(
            token_url,
            headers={"Accept": "application/json", "Content-Type": "application/json"},
            data=json.dumps({"keyId": os.environ[CONDUCTOR_AUTH_KEY], "keySecret": os.environ[CONDUCTOR_AUTH_SECRET]}),
        )
        global _token
        _token = response.json()["token"]
    return _token
