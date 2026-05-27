from __future__ import annotations

import pytest

from ctfd.client import CTFdClient
from ctfd.models import Tag

TAG = {'id': 1, 'challenge_id': 5, 'value': 'web'}


@pytest.mark.unit
@pytest.mark.responses(
    {
        'GET /api/v1/tags': {'success': True, 'data': [TAG]},
        'GET /api/v1/tags/1': {'success': True, 'data': TAG},
        'POST /api/v1/tags': {'success': True, 'data': TAG},
        'PATCH /api/v1/tags/1': {'success': True, 'data': {**TAG, 'value': 'crypto'}},
        'DELETE /api/v1/tags/1': {'success': True},
    }
)
class TestTagsResource:
    async def test_list(self, mock_client: CTFdClient) -> None:
        tags = await mock_client.tags.list()
        assert isinstance(tags[0], Tag)

    async def test_get(self, mock_client: CTFdClient) -> None:
        tag = await mock_client.tags.get(1)
        assert tag.value == 'web'

    async def test_create(self, mock_client: CTFdClient) -> None:
        tag = await mock_client.tags.create({'value': 'web', 'challenge_id': 5})
        assert tag.id == 1

    async def test_update(self, mock_client: CTFdClient) -> None:
        tag = await mock_client.tags.update(1, {'value': 'crypto'})
        assert tag.value == 'crypto'

    async def test_delete(self, mock_client: CTFdClient) -> None:
        await mock_client.tags.delete(1)
