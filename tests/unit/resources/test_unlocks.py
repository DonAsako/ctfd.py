from __future__ import annotations

import pytest

from ctfd.client import CTFdClient
from ctfd.models import Unlock

UNLOCK = {'id': 1, 'user_id': 2, 'target': 5, 'type': 'hints'}


@pytest.mark.unit
@pytest.mark.responses(
    {
        'GET /api/v1/unlocks': {'success': True, 'data': [UNLOCK]},
        'POST /api/v1/unlocks': {'success': True, 'data': UNLOCK},
    }
)
class TestUnlocksResource:
    async def test_list(self, mock_client: CTFdClient) -> None:
        unlocks = await mock_client.unlocks.list()
        assert isinstance(unlocks[0], Unlock)
        assert unlocks[0].type == 'hints'

    async def test_create(self, mock_client: CTFdClient) -> None:
        unlock = await mock_client.unlocks.create({'target': 5, 'type': 'hints'})
        assert unlock.target == 5
