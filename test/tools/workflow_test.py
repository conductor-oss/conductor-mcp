import pytest
from unittest.mock import AsyncMock
from tools import workflow
from network import http_proxy

# workflow_name: str, correlation_id: str = None, priority=0 , idempotency_strategy: Literal['RETURN_EXISTING', 'FAIL', 'FAIL_ON_RUNNING'] = 'RETURN_EXISTING', idempotency_key:str = None, data={}) -> str:
@pytest.mark.parametrize("args,expected", [
    ({'workflow_name': 'test1'}, ('workflow/test1?priority=0', {})),
    ({'workflow_name': 'test2', 'priority': '13'}, ('workflow/test2?priority=13', {})),
    ({'workflow_name': 'test3', 'idempotency_strategy': 'FAIL'}, ('workflow/test3?priority=0', {})),
    ({'workflow_name': 'test4', 'priority': '9', 'idempotency_key': 'azog'}, ('workflow/test4?priority=9', {'X-Idempotency-key': 'azog', 'X-on-conflict': 'RETURN_EXISTING'})),
    ({'workflow_name': 'test5', 'priority': '11', 'idempotency_key': 'azog', 'idempotency_strategy': 'FAIL'}, ('workflow/test5?priority=11', {'X-Idempotency-key': 'azog', 'X-on-conflict': 'FAIL'})),
    ({'workflow_name': 'test6', 'correlation_id': '42'}, ('workflow/test6?priority=0;correlationId=42', {})),
])
@pytest.mark.asyncio
async def test_start_workflow_by_name(args, expected, monkeypatch):
    mock_function = AsyncMock(return_value="mocked result")
    monkeypatch.setattr(http_proxy, 'http_post', mock_function)

    await workflow.start_workflow_by_name(**args)

    mock_function.assert_called_with(expected[0], {}, additional_headers=expected[1])
