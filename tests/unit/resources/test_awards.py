from __future__ import annotations

import pytest

from ctfd.client import CTFdClient
from ctfd.models import Award

AWARD = {'id': 1, 'user_id': 2, 'name': 'First Blood', 'value': 100}


@pytest.mark.unit
@pytest.mark.responses(
    {
        'GET /api/v1/awards': {'success': True, 'data': [AWARD]},
        'GET /api/v1/awards/1': {'success': True, 'data': AWARD},
        'POST /api/v1/awards': {'success': True, 'data': AWARD},
        'DELETE /api/v1/awards/1': {'success': True},
    }
)
class TestAwardsResource:
    async def test_list(self, mock_client: CTFdClient) -> None:
        awards = await mock_client.awards.list()
        assert isinstance(awards[0], Award)

    async def test_get(self, mock_client: CTFdClient) -> None:
        award = await mock_client.awards.get(1)
        assert award.name == 'First Blood'

    async def test_create(self, mock_client: CTFdClient) -> None:
        award = await mock_client.awards.create({'name': 'First Blood', 'value': 100})
        assert award.id == 1

    async def test_delete(self, mock_client: CTFdClient) -> None:
        await mock_client.awards.delete(1)

    async def test_update_raises(self, mock_client: CTFdClient) -> None:
        with pytest.raises(NotImplementedError):
            await mock_client.awards.update(1, {})
