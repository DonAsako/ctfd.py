from __future__ import annotations

import pytest

from ctfd.client import CTFdClient
from ctfd.models import Bracket

BRACKET = {'id': 1, 'name': 'students', 'type': 'users'}


@pytest.mark.unit
@pytest.mark.responses(
    {
        'GET /api/v1/brackets': {'success': True, 'data': [BRACKET]},
        'POST /api/v1/brackets': {'success': True, 'data': BRACKET},
        'PATCH /api/v1/brackets/1': {'success': True, 'data': {**BRACKET, 'name': 'professionals'}},
        'DELETE /api/v1/brackets/1': {'success': True},
    }
)
class TestBracketsResource:
    async def test_list(self, mock_client: CTFdClient) -> None:
        brackets = await mock_client.brackets.list()
        assert isinstance(brackets[0], Bracket)
        assert brackets[0].name == 'students'

    async def test_create(self, mock_client: CTFdClient) -> None:
        bracket = await mock_client.brackets.create({'name': 'students'})
        assert bracket.id == 1

    async def test_update(self, mock_client: CTFdClient) -> None:
        bracket = await mock_client.brackets.update(1, {'name': 'professionals'})
        assert bracket.name == 'professionals'

    async def test_delete(self, mock_client: CTFdClient) -> None:
        await mock_client.brackets.delete(1)

    async def test_get_raises(self, mock_client: CTFdClient) -> None:
        with pytest.raises(NotImplementedError):
            await mock_client.brackets.get(1)
