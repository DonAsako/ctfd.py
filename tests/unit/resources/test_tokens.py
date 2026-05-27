from __future__ import annotations

import pytest

from ctfd.client import CTFdClient
from ctfd.models import Token

TOKEN = {'id': 1, 'user_id': 2, 'value': 'ctfd_abc123', 'type': 'api'}


@pytest.mark.unit
@pytest.mark.responses(
    {
        'GET /api/v1/tokens': {'success': True, 'data': [TOKEN]},
        'GET /api/v1/tokens/1': {'success': True, 'data': TOKEN},
        'POST /api/v1/tokens': {'success': True, 'data': TOKEN},
        'DELETE /api/v1/tokens/1': {'success': True},
    }
)
class TestTokensResource:
    async def test_list(self, mock_client: CTFdClient) -> None:
        tokens = await mock_client.tokens.list()
        assert isinstance(tokens[0], Token)

    async def test_get(self, mock_client: CTFdClient) -> None:
        token = await mock_client.tokens.get(1)
        assert token.value == 'ctfd_abc123'

    async def test_create(self, mock_client: CTFdClient) -> None:
        token = await mock_client.tokens.create({'description': 'ci'})
        assert token.id == 1

    async def test_delete(self, mock_client: CTFdClient) -> None:
        await mock_client.tokens.delete(1)
