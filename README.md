<!--
Copyright 2025 Orkes Inc.

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
-->
# Conductor mcp server
Model Context Protocol server for Conductor.

This package is used to run an MCP server that is capable of interacting with a Conductor instance. It provides tools
for the basic operations that may be needed by an MCP client for Workflow creation, execution, and analysis.

# PyPi Quickstart
## Install package
```commandline
pip install conductor-mcp
```

## Create a JSON config with your Conductor keys
```json
{
  "CONDUCTOR_SERVER_URL": "https://developer.orkescloud.com/api",
  "CONDUCTOR_AUTH_KEY": "<YOUR_APPLICATION_AUTH_KEY>",
  "CONDUCTOR_AUTH_SECRET": "<YOUR_APPLICATION_SECRET_KEY>"
}
```
> Note: the `/api` path is required as part of the CONDUCTOR_SERVER_URL for most applications

## Plug the server into an AI Agent, such as Claude or Cursor
```json
{
  "mcpServers": {
    "conductor": {
      "command": "conductor-mcp",
      "args": [
        "--config",
        "<ABSOLUTE PATH TO A JSON CONFIG FILE>"
      ]
    }
  }
}
```
You should now be able to interact with Conductor via your AI Agent.

### Adding to Claude
You can find instructions for adding to Claude [here](https://modelcontextprotocol.io/quickstart/user#2-add-the-filesystem-mcp-server).
In general, you just add the `mcpServers` config (above) to your Claude config (or create it if it doesn't exist). For
instance, on Mac it might be `~/Library/Application\ Support/Claude/claude_desktop_config.json`.

### Adding to Cursor
The main Cursor instructions are [here](https://docs.cursor.com/context/model-context-protocol).
Go to `Cursor -> Settings -> Cursor Settings -> MCP` and select "+ Add new global MCP server".

Here you can add the exact same configuration file shown in the example for Claude (above).
You can then access the AI chat feature and explore the MCP server in the [sidebar with ⌘+L (Mac) or Ctrl+L (Windows/Linux)](https://docs.cursor.com/chat/overview).

## Example prompts
### Get Flight Risk Info
```text
Create and execute a Conductor Workflow that calls any necessary http endpoints to gather current weather data around
Seattle and outputs the risk factors for flying a small airplane around the South Lake Union area using Visual Flight
Rules today. Only use publicly available endpoints that don't require an API key.
```
### Notify Stocks
(May require API Keys)
```text
Create a Conductor Workflow that runs on a daily schedule, accepts a list of email address and a stock symbol, checks
current stock prices, and sends an email to everyone on the list if they should be happy or sad today based on stock
performance. Name the workflow "NotifyStonks" and use schemaVersion 2.
```

# GitHub Quickstart
## Clone GitHub Repo
```commandline
gh repo clone conductor-oss/conductor-mcp
```

This project relies on `uv` https://docs.astral.sh/uv/getting-started/

## Create venv
(not entirely necessary, since `uv` automatically creates and uses the virtual environment on its own when running other commands)
```commandline
uv sync
source .venv/bin/activate
```
## Define Env Vars
You can continue to use a JSON config file and the `--config` flag, or if the server is running in an environment where
you have control over the environment variables the MCP server will look for them there if a config file is not
provided.
```commandline
export CONDUCTOR_SERVER_URL="YOUR_CONDUCTOR_SERVER_URL"
export CONDUCTOR_AUTH_KEY="<YOUR_APPLICATION_AUTH_KEY>"
export CONDUCTOR_AUTH_SECRET="<YOUR_APPLICATION_SECRET_KEY>"
```
## Configure Your AI Assistant
```json
{
  "mcpServers": {
    "conductor": {
      "command": "uv",
      "args": [
        "--directory",
        "<ABSOLUTE_PATH_TO_THE_PROJECT>",
        "run",
        "conductor-mcp",
        "--config",
        "<ABSOLUTE PATH TO A JSON CONFIG FILE>"
      ]
    }
  }
}
```
### Or Run Server Directly
```commandline
cd <PROJECT_ROOT>
uv run conductor-mcp --config <ABSOLUTE PATH TO A JSON CONFIG FILE>
```
> Note: a `local_development.py` also exists for setting env vars and will be used when the `--local_dev` flag is set.
