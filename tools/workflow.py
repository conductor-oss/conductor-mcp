#  Copyright 2025 Orkes Inc.
#
#  Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
#  the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
#  an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
#  specific language governing permissions and limitations under the License.
from typing import Literal

from fastmcp import FastMCP
from network import http_proxy

workflow_mcp = FastMCP("Workflow Service")

@workflow_mcp.tool()
async def query_workflow_executions(query: str) -> str:
    """Search for workflow (executions) based on payload and other parameters.
    The query parameter accepts exact matches using = and AND operators on the following fields: workflowId, correlationId, workflowType, and status.
    Matches using = can be written as taskType = HTTP. Matches using IN are written as status IN (SCHEDULED, IN_PROGRESS).
    The 'startTime' and 'modifiedTime' field uses unix timestamps and accepts queries using < and >, for example startTime < 1696143600000.
    Queries can be combined using AND, for example taskType = HTTP AND status = SCHEDULED

    If no query kwargs are provided, all workflow executions will be returned.

    Example call to this function to query for a status of FAILED and start time after Thu May 01 2025 22:20:59 GMT+0000:
        query_workflow_executions('status="FAILED" AND startTime > 1746138025 ')

    Searching for a range of time does not work, i.e. "startTime > 0 AND startTime < 1746138025"

    Example call for FAILED or COMPLETED status and workflow named "SimpleWorkflow":
        query_workflow_executions('status IN (FAILED, COMPLETED) AND workflowType="SimpleWorkflow"')

    Args:
        query: A query string, utilizing any of the following fields.
            workflowId: The id of a workflow execution.
            correlationId: The correlationId used to create any workflow executions.
            workflowType: Synonymous with workflow name.
            createTime: The creation unix timestamp of a workflow.
            startTime: The start unix timestamp of a workflow.
            status: The status of a workflow execution. One of [RUNNING, PAUSED, COMPLETED, TIMED_OUT, TERMINATED, FAILED].
            endTime: The end unix timestamp of a workflow.
            priority: The priority (integer) of a workflow.
    """
    path = f'workflow/search?query={query}'
    return await http_proxy.http_get(path)


@workflow_mcp.tool()
async def get_workflow_by_id(workflow_id: str) -> str:
    """Gets a conductor workflow execution in json format based on the workflow's execution id

    Args:
        workflow_id: The uuid representing the execution of the workflow
    """
    path = f'workflow/{workflow_id}?includeTasks=true&summarize=false'
    return await http_proxy.http_get(path)

@workflow_mcp.tool()
async def start_workflow_by_name(workflow_name: str, correlation_id: str = None, priority=0 , idempotency_strategy: Literal['RETURN_EXISTING', 'FAIL', 'FAIL_ON_RUNNING'] = 'RETURN_EXISTING', idempotency_key:str = None, data={}) -> str:
    """Starts a new execution of a conductor workflow by its name

    Args:
        workflow_name: The name of the workflow definition to create a new execution for
        correlation_id: An integer used as unique identifier for the workflow execution, used to correlate the current workflow instance with other workflows.
        priority: A number starting at 0 representing the priority of the execution of the workflow. Lower numbers mean higher priority.
        idempotency_key: An arbitrary, user-provided string used to ensure idempotency when calling this endpoint multiple times.
        idempotency_strategy: A string representing one of the following three strategies:
            RETURN_EXISTING: Return the workflowId of the workflow instance with the same idempotency key.
            FAIL: Start a new workflow instance only if there are no workflow executions with the same idempotency key.
            FAIL_ON_RUNNING: Start a new workflow instance only if there are no RUNNING or PAUSED workflows with the same idempotency key. Completed workflows can run again.
        data: A dictionary containing any arguments to pass into the workflow for creation
    """
    additional_headers = {}
    if idempotency_key is not None:
        additional_headers['X-Idempotency-key'] = idempotency_key
        additional_headers['X-on-conflict'] = idempotency_strategy
    correlation_id_val = '' if correlation_id is None else f'&correlationId={correlation_id}'
    path = f'workflow/{workflow_name}?priority={priority}{correlation_id_val}'

    return await http_proxy.http_post(path, data, additional_headers=additional_headers)


@workflow_mcp.tool()
async def get_workflow_by_name(workflow_name: str) -> str:
    """Gets the metadata for a conductor workflow in json format based on that workflow's name

    Args:
        workflow_name: The name of the workflow
    """
    path = f'metadata/workflow?access=READ&metadata=true&name={workflow_name}&short=false'
    return await http_proxy.http_get(path)


@workflow_mcp.tool()
async def get_all_workflows() -> str:
    """Gets a short description of all existing conductor workflows.
    """
    path = 'metadata/workflow?short=true&metadata=true'
    return await http_proxy.http_get(path)

