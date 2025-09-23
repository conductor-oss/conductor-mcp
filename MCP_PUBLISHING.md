# MCP Registry Publishing

This document explains how the conductor MCP server is published to the Model Context Protocol (MCP) registry.

## Automated Publishing

The server is automatically published to the MCP registry whenever you:

1. **Create a release** on GitHub
2. **Push a version tag** (e.g., `v1.0.0`)

The GitHub Actions workflow (`.github/workflows/publish-mcp.yml`) will:
- Extract the version from `pyproject.toml`
- Update `server.json` with the current version
- Validate the configuration against the MCP schema
- Publish to the MCP registry using GitHub OIDC authentication

## Manual Version Sync

If you need to manually sync the version during development:

```bash
# Using the project script
uv run sync-version

# Or directly with Python
python sync_version.py
```

This will update `server.json` to match the version in `pyproject.toml`.

## Version Management

**Important**: You only need to update the version in `pyproject.toml`. The `server.json` file will be automatically updated during the publishing process.

### Workflow:
1. Update version in `pyproject.toml`
2. Commit and push changes
3. Create a release or tag
4. GitHub Actions automatically publishes to MCP registry

## Files

- `server.json` - MCP server definition (auto-updated during publishing)
- `sync_version.py` - Script to manually sync versions
- `.github/workflows/publish-mcp.yml` - Automated publishing workflow

## Registry URL

Once published, your server will be available at:
https://mcp.registry.io/io.github.conductor-oss/conductor-mcp
