import json

from fastmcp import FastMCP
from network.http_proxy import http_get, http_post

workflow_mcp = FastMCP("Workflow Service")


@workflow_mcp.tool()
async def get_workflow_by_id(workflow_id: str) -> str:
    """Gets a conductor workflow metadata in json format based on that workflow's id

    Args:
        workflow_id: The uuid representing the workflow id
    """
    path = f'workflow/{workflow_id}?includeTasks=true&summarize=false'
    return await http_get(path)

@workflow_mcp.tool()
async def start_workflow_by_name(workflow_name: str, data={}) -> str:
    """Starts a new execution of a conductor workflow by its name

    Args:
        workflow_name: The name of the workflow definition to create a new execution for
        data: A dictionary containing any arguments to pass into the workflow for creation
    """
    path = f'workflow/{workflow_name}?priority=0'
    return await http_post(path, data)
