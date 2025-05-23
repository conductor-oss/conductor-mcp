#  Copyright 2025 Orkes Inc.
#
#  Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
#  the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
#  an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
#  specific language governing permissions and limitations under the License.

from fastmcp import FastMCP

from conductor_mcp import local_development
from conductor_mcp.tools.task import task_mcp
from conductor_mcp.tools.workflow import workflow_mcp
import sys

mcp = FastMCP("oss-conductor")
mcp.mount("workflow", workflow_mcp)
mcp.mount("task", task_mcp)


def run():
    if "local_dev" in sys.argv:
        local_development.initialize()
    # Initialize and run the server
    mcp.run(transport="stdio")


if __name__ == "__main__":
    run()
