from __future__ import annotations

import pytest

from ctfd.client import CTFdClient
from ctfd.models import Hint

HINT = {'id': 1, 'challenge_id': 5, 'content': 'look at headers', 'cost': 10}


@pytest.mark.unit
@pytest.mark.responses(
    {
        'GET /api/v1/hints': {'success': True, 'data': [HINT]},
        'GET /api/v1/hints/1': {'success': True, 'data': HINT},
        'POST /api/v1/hints': {'success': True, 'data': HINT},
        'PATCH /api/v1/hints/1': {'success': True, 'data': {**HINT, 'cost': 20}},
        'DELETE /api/v1/hints/1': {'success': True},
    }
)
class TestHintsResource:
    async def test_list(self, mock_client: CTFdClient) -> None:
        hints = await mock_client.hints.list()
        assert isinstance(hints[0], Hint)

    async def test_get(self, mock_client: CTFdClient) -> None:
        hint = await mock_client.hints.get(1)
        assert hint.cost == 10

    async def test_create(self, mock_client: CTFdClient) -> None:
        hint = await mock_client.hints.create({'content': 'look at headers', 'challenge_id': 5})
        assert hint.id == 1

    async def test_update(self, mock_client: CTFdClient) -> None:
        hint = await mock_client.hints.update(1, {'cost': 20})
        assert hint.cost == 20

    async def test_delete(self, mock_client: CTFdClient) -> None:
        await mock_client.hints.delete(1)
