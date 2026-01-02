#  Copyright 2025 Orkes Inc.
#
#  Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
#  the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
#  an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
#  specific language governing permissions and limitations under the License.

from typing import Dict, Any, List, Literal, Optional
from fastmcp import FastMCP, Context
from conductor_mcp.network.http_proxy import http_get, http_post


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


@task_mcp.tool()
async def get_task_logs(task_id: str) -> str:
    """Gets execution logs for a specific task. Returns log entries generated during task execution.

    Args:
        task_id: The uuid representing the task execution id
    """
    path = f"tasks/{task_id}/log"
    return await http_get(path)


@task_mcp.tool()
async def update_task_status(
    task_id: str,
    workflow_instance_id: str,
    status: Literal["IN_PROGRESS", "FAILED", "FAILED_WITH_TERMINAL_ERROR", "COMPLETED"],
    output_data: Optional[Dict[str, Any]] = None,
    logs: Optional[List[Dict[str, Any]]] = None,
) -> str:
    """Updates the status of a task execution. This is typically used by workers to update task status.

    Args:
        task_id: The uuid representing the task execution id
        workflow_instance_id: The uuid representing the workflow instance id
        status: New task status (IN_PROGRESS, FAILED, FAILED_WITH_TERMINAL_ERROR, COMPLETED)
        output_data: Optional dictionary containing task output data
        logs: Optional list of log entries for the task
    """
    task_update = {
        "workflowInstanceId": workflow_instance_id,
        "taskId": task_id,
        "status": status,
    }
    if output_data is not None:
        task_update["outputData"] = output_data
    if logs is not None:
        task_update["logs"] = logs

    path = "tasks"
    return await http_post(path, data=task_update)


@task_mcp.tool()
async def create_task_definition(task_definition: Dict[str, Any]) -> str:
    """Creates or updates a task definition.

    The task definition should include at minimum:
    - name: The name/type of the task
    - description: A description of what the task does
    - retryCount: Number of retries (default: 3)
    - timeoutSeconds: Task timeout in seconds
    - responseTimeoutSeconds: Response timeout in seconds

    Example task definition:
    {
        "name": "my_custom_task",
        "description": "A custom task that processes data",
        "retryCount": 3,
        "timeoutSeconds": 300,
        "responseTimeoutSeconds": 180,
        "inputKeys": ["input1", "input2"],
        "outputKeys": ["result"]
    }

    Args:
        task_definition: A dictionary containing the task definition
    """
    path = "metadata/taskdefs"
    # API expects an array of task definitions
    return await http_post(path, data=[task_definition])
