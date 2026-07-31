#  Copyright 2025 Orkes Inc.
#
#  Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
#  the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
#  an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
#  specific language governing permissions and limitations under the License.

import os

from conductor_mcp.utils.constants import CONDUCTOR_SERVER_URL


def build_url(resource_path: str) -> str:
    """Joins a resource path onto the configured Conductor server URL.

    Deliberately not os.path.join: on Windows that joins with a backslash, which httpx
    percent-encodes to %5C, and Tomcat rejects an encoded backslash in a path with a bare
    HTTP 400. Nor urllib.parse.urljoin, which drops the base's own path ("/api").

    :param resource_path: The resource path to apply to the server's API endpoint
    :return: The absolute URL to request
    """
    return f"{os.environ[CONDUCTOR_SERVER_URL].rstrip('/')}/{resource_path.lstrip('/')}"
