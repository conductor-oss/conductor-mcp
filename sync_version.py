#!/usr/bin/env python3
"""
Sync version from pyproject.toml to server.json
Run this script whenever you update the version in pyproject.toml
"""
import json
import tomllib
import sys


def sync_version():
    try:
        # Read version from pyproject.toml
        with open("pyproject.toml", "rb") as f:
            pyproject = tomllib.load(f)
        version = pyproject["project"]["version"]

        # Update server.json
        with open("server.json", "r") as f:
            server_config = json.load(f)

        old_version = server_config["version"]
        server_config["version"] = version
        server_config["packages"][0]["version"] = version

        with open("server.json", "w") as f:
            json.dump(server_config, f, indent=2)

        print(f"Updated server.json: {old_version} → {version}")
        return True

    except Exception as e:
        print(f"Error syncing version: {e}")
        return False


def main():
    success = sync_version()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
