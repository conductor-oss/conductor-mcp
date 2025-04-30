from fastmcp import FastMCP

from tools.task import task_mcp
from tools.workflow import workflow_mcp
import sys
import local_development

mcp = FastMCP('orkes-conductor')
mcp.mount('workflow', workflow_mcp)
mcp.mount('task', task_mcp)

if __name__ == '__main__':
    if 'local_dev' in sys.argv:
        local_development.initialize()
    # Initialize and run the server
    mcp.run(transport='stdio')