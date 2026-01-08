#  Copyright 2025 Orkes Inc.
#
#  Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
#  the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
#  an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
#  specific language governing permissions and limitations under the License.

"""
MCP Prompts for Conductor.

Prompts provide reusable templates for common Conductor operations,
guiding LLMs through troubleshooting, analysis, and workflow management tasks.
"""

from typing import Optional
from fastmcp import FastMCP


prompt_mcp = FastMCP("Conductor Prompts")


@prompt_mcp.prompt()
def troubleshoot_workflow(workflow_id: str) -> str:
    """Troubleshoot a failed or stuck workflow.

    Args:
        workflow_id: The workflow execution ID to troubleshoot
    """
    return f"""I need help troubleshooting workflow {workflow_id}. Please:
1. Get the current status of the workflow using get_workflow_by_id
2. Identify any failed tasks and their error messages
3. Check the task logs for detailed errors using get_task_logs
4. Analyze the workflow definition to understand the expected flow
5. Suggest possible solutions based on the error messages
6. Recommend next steps to resolve the issue

Start by fetching the workflow status."""


@prompt_mcp.prompt()
def analyze_failures(workflow_name: Optional[str] = None, hours: int = 24) -> str:
    """Analyze recent workflow failures and identify patterns.

    Args:
        workflow_name: Optional workflow name to filter by
        hours: Number of hours to look back (default: 24)
    """
    filter_text = f' for workflow type "{workflow_name}"' if workflow_name else ""
    return f"""Analyze all failed workflows in the last {hours} hours{filter_text}.

Please:
1. Use query_workflow_executions to find failed workflows with query: status="FAILED"
2. For each failed workflow, examine the failed tasks and error messages
3. Identify common error patterns and group failures by root cause
4. Determine the most frequently failing tasks
5. Analyze potential root causes (configuration issues, external dependencies, timeouts, etc.)
6. Provide recommendations to prevent future failures
7. Prioritize fixes based on failure frequency and impact

Start by querying for failed workflows."""


@prompt_mcp.prompt()
def create_workflow(workflow_name: str, description: str) -> str:
    """Guide to create a new workflow definition.

    Args:
        workflow_name: Name for the new workflow
        description: Description of what the workflow does
    """
    return f"""I want to create a new workflow called "{workflow_name}".
Description: {description}

Please help me:
1. First, use get_all_workflows to show me existing workflow definitions as examples
2. Based on the description, design the workflow structure with appropriate tasks
3. Guide me through creating the workflow definition JSON
4. Ensure all task types are valid (SIMPLE, HTTP, INLINE, SWITCH, DO_WHILE, etc.)
5. Create any necessary task definitions using create_task_definition
6. Register the workflow definition using create_workflow_definition
7. Verify the workflow was created successfully

Remember the key rules:
- taskReferenceName must be unique within the workflow
- INLINE tasks can only access variables via inputParameters
- SWITCH tasks cannot have both switchCaseValue and expression
- Version numbers must be incremented when updating existing workflows

Start by showing me existing workflows for reference."""


@prompt_mcp.prompt()
def monitor_workflow(workflow_id: str) -> str:
    """Monitor a running workflow execution.

    Args:
        workflow_id: The workflow execution ID to monitor
    """
    return f"""Please monitor workflow {workflow_id} and provide a detailed status report.

Steps:
1. Use get_workflow_by_id to fetch the current workflow status
2. List all completed tasks with their execution times
3. Identify the currently running task(s) and their progress
4. Show pending tasks that are yet to execute
5. Check for any warnings or potential issues (slow tasks, retries, etc.)
6. If the workflow is stuck, investigate possible causes
7. Estimate time to completion based on task durations (if possible)

Provide a clear summary of the workflow's health and progress."""


@prompt_mcp.prompt()
def optimize_workflow(workflow_name: str) -> str:
    """Analyze a workflow for optimization opportunities.

    Args:
        workflow_name: Name of the workflow to optimize
    """
    return f"""Analyze the workflow "{workflow_name}" for optimization opportunities.

Please:
1. Use get_workflow_by_name to fetch the workflow definition
2. Review the task structure and identify potential improvements:
   - Tasks that could run in parallel (using FORK/JOIN)
   - Unnecessary sequential dependencies
   - Tasks with excessive timeouts
   - Opportunities for batching similar operations
3. Check recent executions for performance patterns using query_workflow_executions
4. Identify bottleneck tasks that take the longest
5. Suggest specific changes to improve workflow efficiency
6. Provide before/after estimates if applicable

Start by fetching the workflow definition."""
