#  Copyright 2025 Orkes Inc.
#
#  Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
#  the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
#  an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
#  specific language governing permissions and limitations under the License.

from fastmcp import FastMCP, Context
from conductor_mcp.network.http_proxy import http_get


task_mcp = FastMCP("Task Service")


@task_mcp.tool()
async def get_task_by_id(task_id: str, ctx: Context) -> str:
    """Gets the metadata for a conductor workflow task in json format based on that task's id

    Args:
        task_id: The uuid representing the task id
    """
    path = f"tasks/{task_id}"
    return await http_get(path)


@task_mcp.tool()
async def get_task_queue_details() -> str:
    """Gets the current status details for all conductor workflow task queues"""
    path = "tasks/queue/all"
    return await http_get(path)


@task_mcp.tool()
async def get_all_task_definitions() -> str:
    """Gets all task definitions"""
    path = "metadata/taskdefs?access=READ&metadata=false"
    return await http_get(path)


@task_mcp.tool()
async def get_task_definition_for_tasktype(taskType: str) -> str:
    """Gets the task definition for the given taskType.

        "taskType" is synonymous with "task name".

        This API refers to only user-defined tasks.

    Args:
        taskType: The string representing the desired tasks' taskType
    """
    path = f"metadata/taskdefs/{taskType}?metadata=false"
    return await http_get(path)
