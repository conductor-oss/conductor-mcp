#  Copyright 2025 Orkes Inc.
#
#  Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
#  the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
#  an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
#  specific language governing permissions and limitations under the License.

import pytest
from pytest_httpx import HTTPXMock
from conductor_mcp.network import http_proxy, token_manager
from conductor_mcp.utils.constants import CONDUCTOR_SERVER_URL


TEST_URL = "https://some_test_url/api"


async def mock_token_retriever():
    return "test_tolkien"


@pytest.mark.asyncio
async def test_http_get(httpx_mock: HTTPXMock, monkeypatch):
    monkeypatch.setenv(CONDUCTOR_SERVER_URL, TEST_URL)
    monkeypatch.setattr(token_manager, "get_token", mock_token_retriever)
    httpx_mock.add_response(url=TEST_URL + f"/somegarbagepath", text="test_response")

    result = await http_proxy.http_get("somegarbagepath")

    assert result == "test_response"


@pytest.mark.asyncio
async def test_http_post(httpx_mock: HTTPXMock, monkeypatch):
    monkeypatch.setenv(CONDUCTOR_SERVER_URL, TEST_URL)
    monkeypatch.setattr(token_manager, "get_token", mock_token_retriever)
    httpx_mock.add_response(url=TEST_URL + f"/somegarbageposturl", text="test_post_response")

    result = await http_proxy.http_post(
        "somegarbageposturl", data={"middleEarth": {"shire": "hobbiton"}}, additional_headers={"header1": "header1Val"}
    )

    assert result == "test_post_response"

    request = httpx_mock.get_request()
    assert request.headers["header1"] == "header1Val"
    assert request.content == b'{"middleEarth": {"shire": "hobbiton"}}'
