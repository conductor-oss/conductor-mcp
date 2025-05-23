#  Copyright 2025 Orkes Inc.
#
#  Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
#  the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
#  an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
#  specific language governing permissions and limitations under the License.

import os
import logging
from conductor_mcp.utils.constants import CONDUCTOR_SERVER_URL, CONDUCTOR_AUTH_KEY, CONDUCTOR_AUTH_SECRET


def initialize():
    logging.info("Initializing local development")
    os.environ[CONDUCTOR_SERVER_URL] = "https://developer.orkesconductor.io/api"
    os.environ[CONDUCTOR_AUTH_KEY] = "<YOUR_AUTH_KEY>"
    os.environ[CONDUCTOR_AUTH_SECRET] = "<YOUR_AUTH_SECRET>"
