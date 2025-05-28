#  Copyright 2025 Orkes Inc.
#
#  Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
#  the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
#  an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
#  specific language governing permissions and limitations under the License.
import json
import os

from fastmcp import FastMCP
from pygments.lexer import default

from conductor_mcp import local_development
from conductor_mcp.tools.task import task_mcp
from conductor_mcp.tools.workflow import workflow_mcp
import click

from conductor_mcp.utils.constants import CONDUCTOR_SERVER_URL, CONDUCTOR_AUTH_KEY, CONDUCTOR_AUTH_SECRET

mcp = FastMCP("oss-conductor")
mcp.mount("workflow", workflow_mcp)
mcp.mount("task", task_mcp)


@click.command()
@click.option(
    "--local_dev",
    "-l",
    is_flag=True,
    help="Used when the running code directly (i.e. git clone), set Conductor variables in the local_development.py file when using this option.",
)
@click.option(
    "--config",
    "-c",
    default=None,
    help="""
    The location of a JSON config file containing the Conductor variables:
{
    "CONDUCTOR_SERVER_URL": ""https://developer.orkesconductor.io/api"",
    "CONDUCTOR_AUTH_KEY": "<YOUR_AUTH_KEY>",
    "CONDUCTOR_AUTH_SECRET": "<YOUR_AUTH_SECRET>"
}
""",
)
def run(local_dev, config):
    if local_dev and config is not None:
        raise click.UsageError("--local_dev and --config are mutually exclusive, please use just one.")
    elif local_dev:
        local_development.initialize()
    elif config is not None:
        print(f"Initializing Conductor with config file: {config}")
        with open(config, "r") as file:
            data = json.load(file)
            os.environ[CONDUCTOR_SERVER_URL] = data[CONDUCTOR_SERVER_URL]
            os.environ[CONDUCTOR_AUTH_KEY] = data[CONDUCTOR_AUTH_KEY]
            os.environ[CONDUCTOR_AUTH_SECRET] = data[CONDUCTOR_AUTH_SECRET]
    # Initialize and run the server
    mcp.run(transport="stdio")


if __name__ == "__main__":
    run()
