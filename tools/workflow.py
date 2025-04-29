
from fastmcp import FastMCP, Context
from network.http_proxy import http_get


workflow_mcp = FastMCP("Workflow Service")


@workflow_mcp.tool()
async def get_workflow_metadata(workflow_id: str, ctx: Context) -> str:
    """Gets a conductor workflow metadata in json format based on that workflow's id

    Args:
        workflow_id: The uuid representing the workflow id
    """
    path = f'workflow/{workflow_id}?includeTasks=true&summarize=false'
    return await http_get(path)
