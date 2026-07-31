#  Copyright 2025 Orkes Inc.
#
#  Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
#  the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
#  an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
#  specific language governing permissions and limitations under the License.

import pytest

from conductor_mcp.utils.constants import CONDUCTOR_SERVER_URL
from conductor_mcp.utils.urls import build_url

TEST_URL = "https://orkestest.io/api"


@pytest.mark.parametrize(
    "base, resource_path",
    [
        (TEST_URL, "token"),
        (TEST_URL + "/", "token"),
        (TEST_URL, "/token"),
        (TEST_URL + "/", "/token"),
    ],
)
def test_build_url_joins_with_a_single_slash(base, resource_path, monkeypatch):
    monkeypatch.setenv(CONDUCTOR_SERVER_URL, base)

    assert build_url(resource_path) == TEST_URL + "/token"


def test_build_url_preserves_the_base_path(monkeypatch):
    """urllib.parse.urljoin would discard the "/api" segment here."""
    monkeypatch.setenv(CONDUCTOR_SERVER_URL, TEST_URL)

    assert build_url("metadata/workflow") == "https://orkestest.io/api/metadata/workflow"


def test_build_url_keeps_nested_resource_paths_intact(monkeypatch):
    monkeypatch.setenv(CONDUCTOR_SERVER_URL, TEST_URL)

    assert build_url("workflow/123/pause") == "https://orkestest.io/api/workflow/123/pause"


def test_build_url_never_emits_a_backslash(monkeypatch):
    """os.path.join would join with a backslash on Windows, which httpx encodes to %5C.

    Tomcat rejects an encoded backslash in a path with a bare HTTP 400, so every request
    fails there while passing on Linux.
    """
    monkeypatch.setenv(CONDUCTOR_SERVER_URL, TEST_URL)

    assert "\\" not in build_url("metadata/workflow")
