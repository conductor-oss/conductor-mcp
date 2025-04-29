from fastmcp import FastMCP
from tools.workflow import workflow_mcp

mcp = FastMCP('orkes-conductor')
mcp.mount('workflow', workflow_mcp)

if __name__ == '__main__':
    # Initialize and run the server
    mcp.run(transport='stdio')