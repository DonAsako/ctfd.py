from __future__ import annotations

import pytest

from ctfd.client import CTFdClient
from ctfd.models import Share

SHARE = {'id': 1, 'name': 'solve-share', 'type': 'solve', 'user_id': 2, 'value': 'abc123'}


@pytest.mark.unit
@pytest.mark.responses(
    {
        'POST /api/v1/shares': {'success': True, 'data': SHARE},
    }
)
class TestSharesResource:
    async def test_create(self, mock_client: CTFdClient) -> None:
        share = await mock_client.shares.create({'name': 'solve-share', 'type': 'solve'})
        assert isinstance(share, Share)
        assert share.value == 'abc123'
