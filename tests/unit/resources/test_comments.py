from __future__ import annotations

import pytest

from ctfd.client import CTFdClient
from ctfd.models import Comment

COMMENT = {'id': 1, 'type': 'challenge', 'content': 'Nice challenge!', 'author_id': 3}


@pytest.mark.unit
@pytest.mark.responses(
    {
        'GET /api/v1/comments': {'success': True, 'data': [COMMENT]},
        'POST /api/v1/comments': {'success': True, 'data': COMMENT},
        'DELETE /api/v1/comments/1': {'success': True},
    }
)
class TestCommentsResource:
    async def test_list(self, mock_client: CTFdClient) -> None:
        comments = await mock_client.comments.list()
        assert isinstance(comments[0], Comment)

    async def test_create(self, mock_client: CTFdClient) -> None:
        comment = await mock_client.comments.create({'content': 'Nice challenge!', 'type': 'challenge'})
        assert comment.id == 1

    async def test_delete(self, mock_client: CTFdClient) -> None:
        await mock_client.comments.delete(1)

    async def test_get_raises(self, mock_client: CTFdClient) -> None:
        with pytest.raises(NotImplementedError):
            await mock_client.comments.get(1)

    async def test_update_raises(self, mock_client: CTFdClient) -> None:
        with pytest.raises(NotImplementedError):
            await mock_client.comments.update(1, {})
