#  Copyright 2025 Orkes Inc.
#
#  Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
#  the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
#  an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
#  specific language governing permissions and limitations under the License.

import pytest
from unittest.mock import AsyncMock
from conductor_mcp.tools import workflow
from conductor_mcp.network import http_proxy


# workflow_name: str, correlation_id: str = None, priority=0 , idempotency_strategy: Literal['RETURN_EXISTING', 'FAIL', 'FAIL_ON_RUNNING'] = 'RETURN_EXISTING', idempotency_key:str = None, data={}) -> str:
@pytest.mark.parametrize(
    "args,expected",
    [
        ({"workflow_name": "test1"}, ("workflow/test1?priority=0", {})),
        ({"workflow_name": "test2", "priority": "13"}, ("workflow/test2?priority=13", {})),
        ({"workflow_name": "test3", "idempotency_strategy": "FAIL"}, ("workflow/test3?priority=0", {})),
        (
            {"workflow_name": "test4", "priority": "9", "idempotency_key": "azog"},
            ("workflow/test4?priority=9", {"X-Idempotency-key": "azog", "X-on-conflict": "RETURN_EXISTING"}),
        ),
        (
            {"workflow_name": "test5", "priority": "11", "idempotency_key": "azog", "idempotency_strategy": "FAIL"},
            ("workflow/test5?priority=11", {"X-Idempotency-key": "azog", "X-on-conflict": "FAIL"}),
        ),
        ({"workflow_name": "test6", "correlation_id": "42"}, ("workflow/test6?priority=0&correlationId=42", {})),
    ],
)
@pytest.mark.asyncio
async def test_start_workflow_by_name(args, expected, monkeypatch):
    mock_function = AsyncMock(return_value="mocked result")
    monkeypatch.setattr(http_proxy, "http_post", mock_function)

    await workflow.start_workflow_by_name(**args)

    mock_function.assert_called_with(expected[0], {}, additional_headers=expected[1])
