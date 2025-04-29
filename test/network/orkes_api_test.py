import pytest
from pytest_httpx import HTTPXMock
from network import http_proxy
from network import token_manager
from utils.constants import CONDUCTOR_SERVER_URL


TEST_URL = 'https://some_test_url/api'

async def mock_token_retriever():
    return 'test_tolkien'

@pytest.mark.asyncio
async def test_http_get(httpx_mock: HTTPXMock, monkeypatch):
    monkeypatch.setenv(CONDUCTOR_SERVER_URL, TEST_URL)
    monkeypatch.setattr(token_manager, 'get_token', mock_token_retriever)
    httpx_mock.add_response(url=TEST_URL + f'/somegarbagepath', text='test_response')

    result = await http_proxy.http_get('somegarbagepath')

    assert result == 'test_response'