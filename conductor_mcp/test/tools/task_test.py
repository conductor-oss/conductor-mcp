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
from conductor_mcp.tools import task
from conductor_mcp.network import http_proxy


@pytest.mark.asyncio
async def test_get_task_by_id(monkeypatch):
    mock_get = AsyncMock(return_value='{"taskId": "task-123"}')
    monkeypatch.setattr(http_proxy, "http_get", mock_get)

    result = await task.get_task_by_id("task-123")

    mock_get.assert_awaited_once_with("tasks/task-123")
    assert result == '{"taskId": "task-123"}'


@pytest.mark.asyncio
async def test_get_task_queue_details(monkeypatch):
    mock_get = AsyncMock(return_value='{"queue": "details"}')
    monkeypatch.setattr(http_proxy, "http_get", mock_get)

    result = await task.get_task_queue_details()

    mock_get.assert_awaited_once_with("tasks/queue/all")
    assert result == '{"queue": "details"}'


@pytest.mark.asyncio
async def test_get_all_task_definitions(monkeypatch):
    mock_get = AsyncMock(return_value='[{"name": "task_1"}]')
    monkeypatch.setattr(http_proxy, "http_get", mock_get)

    result = await task.get_all_task_definitions()

    mock_get.assert_awaited_once_with("metadata/taskdefs?access=READ&metadata=false")
    assert result == '[{"name": "task_1"}]'


@pytest.mark.asyncio
async def test_get_task_definition_for_tasktype(monkeypatch):
    mock_get = AsyncMock(return_value='{"name": "custom_task"}')
    monkeypatch.setattr(http_proxy, "http_get", mock_get)

    result = await task.get_task_definition_for_tasktype("custom_task")

    mock_get.assert_awaited_once_with("metadata/taskdefs/custom_task?metadata=false")
    assert result == '{"name": "custom_task"}'


@pytest.mark.asyncio
async def test_get_task_logs(monkeypatch):
    mock_get = AsyncMock(return_value='[{"log": "executed"}]')
    monkeypatch.setattr(http_proxy, "http_get", mock_get)

    result = await task.get_task_logs("task-123")

    mock_get.assert_awaited_once_with("tasks/task-123/log")
    assert result == '[{"log": "executed"}]'


@pytest.mark.asyncio
async def test_update_task_status(monkeypatch):
    mock_post = AsyncMock(return_value='{"status": "COMPLETED"}')
    monkeypatch.setattr(http_proxy, "http_post", mock_post)

    result = await task.update_task_status(
        task_id="task-123",
        workflow_instance_id="wf-456",
        status="COMPLETED",
        output_data={"result": "success"},
    )

    mock_post.assert_awaited_once_with(
        "tasks",
        data={
            "workflowInstanceId": "wf-456",
            "taskId": "task-123",
            "status": "COMPLETED",
            "outputData": {"result": "success"},
        },
    )
    assert result == '{"status": "COMPLETED"}'


@pytest.mark.asyncio
async def test_create_task_definition(monkeypatch):
    mock_post = AsyncMock(return_value='{"name": "new_task"}')
    monkeypatch.setattr(http_proxy, "http_post", mock_post)

    task_def = {"name": "new_task", "retryCount": 3}
    result = await task.create_task_definition(task_def)

    mock_post.assert_awaited_once_with("metadata/taskdefs", data=[task_def])
    assert result == '{"name": "new_task"}'
