# orkes-conductor-mcp
Model Context Protocol server for Orkes Conductor.

# Running the server
This project relies on `uv` https://docs.astral.sh/uv/getting-started/

Create venv (not entirely necessary, since `uv` automatically creates and uses the virtual environment on its own when running other commands)
```commandline
uv sync
source .venv/bin/activate
```
Run Server
```commandline
uv run server.py
```
---
For local development, a `local_development.py` file is provided for convenience for setting environment variables explicitly.

This is particularly useful where you don't have control over the environment, i.e. running in Claude.
```
    os.environ[CONDUCTOR_SERVER_URL] = 'https://developer.orkescloud.com/api'
    os.environ[CONDUCTOR_AUTH_KEY] = '<YOUR_APPLICATION_AUTH_KEY>'
    os.environ[CONDUCTOR_AUTH_SECRET] = '<YOUR_APPLICATION_SECRET_KEY>'
```
To run with local development add 'local_dev' to the server arguments:
```commandline
uv run server.py local_dev
```
> Note: the `/api` path is required as part of the CONDUCTOR_SERVER_URL for most applications
# Adding to Claude
Follow [this tutorial](https://modelcontextprotocol.io/quickstart/user) for adding the mcp server to claude, and use the following
configuration, with or without the `local_dev` argument:
```json
{
  "mcpServers": {
    "orkes-conductor": {
      "command": "uv",
      "args": [
        "--directory",
        "/<YOUR ABSOLUTE PATH TO THE DIRECTORY CONTAINING server.py>",
        "run",
        "server.py",
        "local_dev"
      ]
    }
  }
}
```