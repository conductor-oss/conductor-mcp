#  Copyright 2025 Orkes Inc.
#
#  Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
#  the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
#  an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
#  specific language governing permissions and limitations under the License.

from typing import Optional
from fastmcp import FastMCP
from conductor_mcp.network.http_proxy import http_get


event_mcp = FastMCP("Event Service")


@event_mcp.tool()
async def get_event_handlers(event: Optional[str] = None, active_only: bool = True) -> str:
    """Gets all event handlers or filters by event name and active status.

    Event handlers define how Conductor responds to external events. They can trigger
    workflow executions or perform other actions when specific events occur.

    Args:
        event: Optional event name to filter by
        active_only: If True, return only active event handlers (default: True)
    """
    params = []
    if event:
        params.append(f"event={event}")
    params.append(f"activeOnly={str(active_only).lower()}")
    
    query_string = "&".join(params)
    path = f"event?{query_string}"
    return await http_get(path)

