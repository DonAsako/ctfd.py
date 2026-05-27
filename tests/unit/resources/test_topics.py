from __future__ import annotations

import pytest

from ctfd.client import CTFdClient
from ctfd.models import Topic

TOPIC = {'id': 1, 'value': 'SQL injection'}


@pytest.mark.unit
@pytest.mark.responses(
    {
        'GET /api/v1/topics': {'success': True, 'data': [TOPIC]},
        'GET /api/v1/topics/1': {'success': True, 'data': TOPIC},
        'POST /api/v1/topics': {'success': True, 'data': TOPIC},
        'DELETE /api/v1/topics': {'success': True},
        'DELETE /api/v1/topics/1': {'success': True},
    }
)
class TestTopicsResource:
    async def test_list(self, mock_client: CTFdClient) -> None:
        topics = await mock_client.topics.list()
        assert isinstance(topics[0], Topic)
        assert topics[0].value == 'SQL injection'

    async def test_get(self, mock_client: CTFdClient) -> None:
        topic = await mock_client.topics.get(1)
        assert topic.id == 1

    async def test_create(self, mock_client: CTFdClient) -> None:
        topic = await mock_client.topics.create({'value': 'SQL injection'})
        assert topic.id == 1

    async def test_delete_by_id(self, mock_client: CTFdClient) -> None:
        await mock_client.topics.delete(1)

    async def test_unlink(self, mock_client: CTFdClient) -> None:
        await mock_client.topics.unlink(topic_id=1, challenge_id=5)
