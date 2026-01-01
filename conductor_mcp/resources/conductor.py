#  Copyright 2025 Orkes Inc.
#
#  Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
#  the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
#  an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
#  specific language governing permissions and limitations under the License.

"""
MCP Resources for Conductor.

Resources provide read-only access to Conductor data, allowing LLMs to query
workflow definitions, task definitions, and workflow execution states.
"""

from fastmcp import FastMCP
from conductor_mcp.network.http_proxy import http_get


resource_mcp = FastMCP("Conductor Resources")


@resource_mcp.resource("conductor://workflows/definitions")
async def get_workflow_definitions() -> str:
    """List of all registered workflow definitions in Conductor.
    
    Returns metadata about all workflows registered in Conductor, including
    workflow names, versions, descriptions, and task configurations.
    """
    path = "metadata/workflow?short=false&metadata=true"
    return await http_get(path)


@resource_mcp.resource("conductor://tasks/definitions")
async def get_task_definitions() -> str:
    """List of all registered task definitions in Conductor.
    
    Returns metadata about all tasks registered in Conductor, including
    task names, descriptions, retry policies, and timeout configurations.
    """
    path = "metadata/taskdefs?access=READ&metadata=false"
    return await http_get(path)


@resource_mcp.resource("conductor://workflows/running")
async def get_running_workflows() -> str:
    """List of currently running workflow executions.
    
    Returns workflow executions that are currently in RUNNING status,
    including workflow IDs, names, start times, and current progress.
    """
    path = "workflow/search?query=status%3D%22RUNNING%22"
    return await http_get(path)


@resource_mcp.resource("conductor://workflows/failed")
async def get_failed_workflows() -> str:
    """List of recently failed workflow executions.
    
    Returns workflow executions that have failed, including workflow IDs,
    names, failure reasons, and failed task information.
    """
    path = "workflow/search?query=status%3D%22FAILED%22"
    return await http_get(path)


@resource_mcp.resource("conductor://workflows/paused")
async def get_paused_workflows() -> str:
    """List of currently paused workflow executions.
    
    Returns workflow executions that are currently in PAUSED status,
    including workflow IDs, names, and pause timestamps.
    """
    path = "workflow/search?query=status%3D%22PAUSED%22"
    return await http_get(path)


@resource_mcp.resource("conductor://tasks/queue")
async def get_task_queue_status() -> str:
    """Current status of all task queues.
    
    Returns the current queue status for all task types, including
    the number of pending tasks in each queue.
    """
    path = "tasks/queue/all"
    return await http_get(path)

