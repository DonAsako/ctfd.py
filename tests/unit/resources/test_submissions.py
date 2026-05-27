from __future__ import annotations

import pytest

from ctfd.client import CTFdClient
from ctfd.models import Submission

SUB = {'id': 1, 'challenge_id': 5, 'user_id': 2, 'type': 'correct', 'provided': 'flag{x}'}


@pytest.mark.unit
@pytest.mark.responses(
    {
        'GET /api/v1/submissions': {'success': True, 'data': [SUB]},
        'GET /api/v1/submissions/1': {'success': True, 'data': SUB},
        'POST /api/v1/submissions': {'success': True, 'data': SUB},
        'PATCH /api/v1/submissions/1': {'success': True, 'data': {**SUB, 'type': 'incorrect'}},
        'DELETE /api/v1/submissions/1': {'success': True},
    }
)
class TestSubmissionsResource:
    async def test_list(self, mock_client: CTFdClient) -> None:
        subs = await mock_client.submissions.list()
        assert isinstance(subs[0], Submission)

    async def test_get(self, mock_client: CTFdClient) -> None:
        sub = await mock_client.submissions.get(1)
        assert sub.type == 'correct'

    async def test_create(self, mock_client: CTFdClient) -> None:
        sub = await mock_client.submissions.create({'challenge_id': 5, 'provided': 'flag{x}'})
        assert sub.id == 1

    async def test_update(self, mock_client: CTFdClient) -> None:
        sub = await mock_client.submissions.update(1, {'type': 'incorrect'})
        assert sub.type == 'incorrect'

    async def test_delete(self, mock_client: CTFdClient) -> None:
        await mock_client.submissions.delete(1)
