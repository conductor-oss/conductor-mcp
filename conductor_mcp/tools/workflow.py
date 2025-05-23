#  Copyright 2025 Orkes Inc.
#
#  Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
#  the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
#  an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
#  specific language governing permissions and limitations under the License.
from typing import Literal, Dict, Any
from fastmcp import FastMCP
from conductor_mcp.network import http_proxy

workflow_mcp = FastMCP("Workflow Service")


@workflow_mcp.tool()
async def create_workflow_definition(workflow_definition: Dict[str, Any]) -> str:
    """Creates a workflow definition from the provided workflow_definition dict param.

    These are the main constructs that should be considered:
    1. Do_while : to run through a list (input _items as the input parameters to iterate)
    2. Switch: decision task
    3. Inline: Executes javascript inline

    In order to access workflow variables in javascript functions, they must first be assigned a value via inputParameters,
    for example:
        if there's a task named "analyze_market_data" then to access its output in javascript you need to create an inputParameter to assign it a value that can be used:
            "inputParameters": {
                "marketData": "${analyze_market_data.output}"
              }
        Then the "${analyze_market_data.output}" value can be accessed in javascript as "marketData" like so:
            "(function () {\\n  console.log("Market Data: " + $.marketData);\\n})();"

    In switch cases, an expression field must be defined using the same input method as above. You can construct the expression field like this:
            "inputParameters": {
                "marketData": "${analyze_market_data.output}"
            }
            "expression": "(function () {\\n  $.marketData.includes("NASDAQ");\\n})();"

    Here are some examples to help:
        ## Example of a switch task to run conditional tasks
        {
          "name": "switch_case_example",
          "description": "switch_case_example",
          "version": 1,
          "tasks": [
            {
              "name": "switch",
              "taskReferenceName": "switch_ref",
              "inputParameters": {
                "switchCaseValue": "${workflow.input.case_param}"
              },
              "type": "SWITCH",
              "decisionCases": {
                "case_a": [
                  {
                    "name": "simple_1",
                    "taskReferenceName": "simple_ref_1",
                    "type": "SIMPLE"
                  }
                ],
                "case_b": [
                  {
                    "name": "simple",
                    "taskReferenceName": "simple_ref",
                    "type": "SIMPLE"
                  }
                ]
              },
              "defaultCase": [
                {
                  "name": "simple_2",
                  "taskReferenceName": "simple_ref_2",
                  "type": "SIMPLE"
                }
              ],
              "evaluatorType": "value-param"
            }
          ]
        }

        ## Example of a do_while for iterating over a list
        {
          "createTime": 1740724130693,
          "name": "for_each_example",
          "description": "for_each_example",
          "version": 1,
          "tasks": [
            {
              "name": "do_while",
              "taskReferenceName": "do_while_ref",
              "inputParameters": {
                "items": "$ {workflow.input.items_list}"
              },
              "type": "DO_WHILE",
              "loopOver": [
                {
                  "name": "simple",
                  "taskReferenceName": "simple_ref",
                  "inputParameters": {
                    "item": "$ {do_while_ref.output.item}"
                  },
                  "type": "SIMPLE"
                },
                {
                  "name": "simple_1",
                  "taskReferenceName": "simple_ref_1",
                  "inputParameters": {
                    "item_to_process": "$ {do_while_ref.output.item}"
                  },
                  "type": "SIMPLE"
                }
              ],
              "evaluatorType": "value-param"
            }
          ]
        }

        ## Example of an inline javascript execution
        {
          "name": "inline_javascript_execution",
          "version": 1,
          "tasks": [
            {
              "name": "inline",
              "taskReferenceName": "inline_ref",
              "type": "INLINE",
              "inputParameters": {
                "invoker": "$ {workflow.input.invoker_name}"
              },
              "inputParameters": {
                "expression": "(function () {\\n  return "Hello " + $.invoker;\\n})();",
                "evaluatorType": "graaljs",
                "value1": 1,
                "value2": 2
              }
            }
          ]
        }

        notice, that the javscript function is written as:
        (function () {
          return $.value1 + $.value2;
        })();
        and value1 and value2 are the input to the task.

        ## Important Rules
        taskReferenceName MUST be unique in the workflow JSON.
        When using INLINE task, all the variables in the script MUST be the input parameters to the task.  Only task's input parameters can be accessed inside the script.
        When trying to update a workflow that's already been created you must increment the version number, otherwise you need to pick a unique name for the workflow.
        It's best not to use loopCondition, instead, iterate over the list of items using items input parameter. Nest SWITCH task if you want to do conditional processing.

        ### SWITCH task rules:
        When using SWITCH task, the switchCaseValue _cannot_ contain expressions, scripts or methods.  It has to be simple map.  Use expression field to execute a script if required.
        Remember, switchCaseValue and expression fields in SWITCH are mutually exclusive.  ONLY one of them can be used. expression is NOT an input field, it is set as a property to the task.
        expression MUST be a javascript function that returns a single string.  Similar to INLINE task.  The function is IIFE type, which is a JavaScript function that is defined and executed immediately.
        When writing SWITCH task remember to consider all the cases, if required use defaultCase to handle default cases and the ones for which no clear branches are defined.
        one more thing -- SWITCH task does not produce output, so do not use the output of a switch as an input to any task.

        ## Inline javascript rules
        We use GraalVM to evaluate javascript code.
        It's best not to use concat function to merge arrays or maps etc.
        You can ONLY use the variables defined as input to the task in the javascript code.  Access them as $.var.
        Note, you _CANNOT_ use ${task.output.var} in javascript. neither in inline or Switch task expressions. Only $.var and var MUST be an input parameter to the task.
        In order to address any inputs to the workflow or tasks, you must be sure to first assign that input to an input parameter, which then can be referenced -
            for instance, in order to use ${workflow.input.case_param} in javascript, you must make sure the inputParameters assigns that to a variable in the task definition,
            such as:
              "inputParameters": {
                "switchCaseValue": "${workflow.input.case_param}"
              },
            once that value is assigned to switchCaseValue via the inputParameters section of the task definition, it can be addressed in javascript as $.switchCaseValue

        ## Input mapping rules
        * The task's input and output is always a Map data type.  If a task's schema returns List or a single value as output, it is wrapped in a map with key "result"
        * For HTTP task's the output is in "response" key

    Args:
        workflow_definition: A nested dictionary representing a workflow definition
    """
    path = f"metadata/workflow?overwrite=false"
    return await http_proxy.http_post(path, data=workflow_definition)


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
    """
    path = f"workflow/search?query={query}"
    return await http_proxy.http_get(path)


@workflow_mcp.tool()
async def get_workflow_by_id(workflow_id: str) -> str:
    """Gets a conductor workflow execution in json format based on the workflow's execution id

    Args:
        workflow_id: The uuid representing the execution of the workflow
    """
    path = f"workflow/{workflow_id}?includeTasks=true&summarize=false"
    return await http_proxy.http_get(path)


@workflow_mcp.tool()
async def start_workflow_by_name(
    workflow_name: str,
    correlation_id: str = None,
    priority=0,
    idempotency_strategy: Literal["RETURN_EXISTING", "FAIL", "FAIL_ON_RUNNING"] = "RETURN_EXISTING",
    idempotency_key: str = None,
    data={},
) -> str:
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
        additional_headers["X-Idempotency-key"] = idempotency_key
        additional_headers["X-on-conflict"] = idempotency_strategy
    correlation_id_val = "" if correlation_id is None else f"&correlationId={correlation_id}"
    path = f"workflow/{workflow_name}?priority={priority}{correlation_id_val}"

    return await http_proxy.http_post(path, data, additional_headers=additional_headers)


@workflow_mcp.tool()
async def get_workflow_by_name(workflow_name: str) -> str:
    """Gets the metadata for a conductor workflow in json format based on that workflow's name

    Args:
        workflow_name: The name of the workflow
    """
    path = f"metadata/workflow?access=READ&metadata=true&name={workflow_name}&short=false"
    return await http_proxy.http_get(path)


@workflow_mcp.tool()
async def get_all_workflows() -> str:
    """Gets a short description of all existing conductor workflows."""
    path = "metadata/workflow?short=true&metadata=true"
    return await http_proxy.http_get(path)
