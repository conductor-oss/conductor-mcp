#  Copyright 2025 Orkes Inc.
#
#  Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
#  the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
#  an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
#  specific language governing permissions and limitations under the License.

from datetime import timedelta

import pytest
import datetime
from freezegun import freeze_time
from pytest_httpx import HTTPXMock
from conductor_mcp.network import token_manager
from conductor_mcp.utils.constants import CONDUCTOR_SERVER_URL, CONDUCTOR_AUTH_KEY, CONDUCTOR_AUTH_SECRET

TEST_URL = "https://orkestest.io/api"
TEST_WORKFLOW_ID = "specialtestworkflowid"
TEST_TOKEN = "specialtesttolkien"


@pytest.mark.asyncio
async def test_get_token(httpx_mock: HTTPXMock, monkeypatch):
    monkeypatch.setenv(CONDUCTOR_SERVER_URL, TEST_URL)
    monkeypatch.setenv(CONDUCTOR_AUTH_KEY, "testAuthKey")
    monkeypatch.setenv(CONDUCTOR_AUTH_SECRET, "testAuthSecretShhhh")
    httpx_mock.add_response(url=TEST_URL + f"/token", json={"token": TEST_TOKEN})

    retrieved_token = await token_manager.get_token()

    assert retrieved_token == TEST_TOKEN


@pytest.mark.asyncio
async def test_refresh_token(httpx_mock: HTTPXMock, monkeypatch):
    monkeypatch.setenv(CONDUCTOR_SERVER_URL, TEST_URL)
    monkeypatch.setenv(CONDUCTOR_AUTH_KEY, "testAuthKey")
    monkeypatch.setenv(CONDUCTOR_AUTH_SECRET, "testAuthSecretShhhh")
    httpx_mock.add_response(url=TEST_URL + f"/token", json={"token": TEST_TOKEN}, is_reusable=True)
    with freeze_time(datetime.datetime.now()) as frozen_datetime:
        await token_manager.get_token()
        await token_manager.get_token()
        await token_manager.get_token()
        first_calls = len(httpx_mock.get_requests())

        # using <= means we allow the tests to be run in any order since the _last_token_retrieval is global
        assert first_calls <= 1

        three_hours_later = datetime.datetime.now() + timedelta(hours=3)
        frozen_datetime.move_to(three_hours_later)
        await token_manager.get_token()

        assert len(httpx_mock.get_requests()) == first_calls + 1
