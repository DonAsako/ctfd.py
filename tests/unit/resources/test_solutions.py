from __future__ import annotations

import pytest

from ctfd.client import CTFdClient
from ctfd.models import Solution

SOL = {'id': 1, 'challenge_id': 5, 'content': 'The flag is in the cookies.', 'state': 'visible'}


@pytest.mark.unit
@pytest.mark.responses(
    {
        'GET /api/v1/solutions': {'success': True, 'data': [SOL]},
        'GET /api/v1/solutions/1': {'success': True, 'data': SOL},
        'POST /api/v1/solutions': {'success': True, 'data': SOL},
        'PATCH /api/v1/solutions/1': {'success': True, 'data': {**SOL, 'state': 'hidden'}},
        'DELETE /api/v1/solutions/1': {'success': True},
    }
)
class TestSolutionsResource:
    async def test_list(self, mock_client: CTFdClient) -> None:
        sols = await mock_client.solutions.list()
        assert isinstance(sols[0], Solution)

    async def test_get(self, mock_client: CTFdClient) -> None:
        sol = await mock_client.solutions.get(1)
        assert sol.state == 'visible'

    async def test_create(self, mock_client: CTFdClient) -> None:
        sol = await mock_client.solutions.create({'content': 'in cookies', 'challenge_id': 5})
        assert sol.id == 1

    async def test_update(self, mock_client: CTFdClient) -> None:
        sol = await mock_client.solutions.update(1, {'state': 'hidden'})
        assert sol.state == 'hidden'

    async def test_delete(self, mock_client: CTFdClient) -> None:
        await mock_client.solutions.delete(1)
