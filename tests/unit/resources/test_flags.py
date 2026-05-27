from __future__ import annotations

import pytest

from ctfd.client import CTFdClient
from ctfd.models import Flag

FLAG = {'id': 1, 'challenge_id': 5, 'type': 'static', 'content': 'flag{test}'}


@pytest.mark.unit
@pytest.mark.responses(
    {
        'GET /api/v1/flags': {'success': True, 'data': [FLAG]},
        'GET /api/v1/flags/1': {'success': True, 'data': FLAG},
        'POST /api/v1/flags': {'success': True, 'data': FLAG},
        'PATCH /api/v1/flags/1': {'success': True, 'data': {**FLAG, 'content': 'flag{updated}'}},
        'DELETE /api/v1/flags/1': {'success': True},
        'GET /api/v1/flags/types': {'success': True, 'data': {'static': {}, 'regex': {}}},
        'GET /api/v1/flags/types/static': {'success': True, 'data': {'name': 'static', 'templates': {}}},
    }
)
class TestFlagsResource:
    async def test_list(self, mock_client: CTFdClient) -> None:
        flags = await mock_client.flags.list()
        assert isinstance(flags[0], Flag)

    async def test_get(self, mock_client: CTFdClient) -> None:
        flag = await mock_client.flags.get(1)
        assert flag.content == 'flag{test}'

    async def test_create(self, mock_client: CTFdClient) -> None:
        flag = await mock_client.flags.create({'type': 'static', 'content': 'flag{test}'})
        assert flag.id == 1

    async def test_update(self, mock_client: CTFdClient) -> None:
        flag = await mock_client.flags.update(1, {'content': 'flag{updated}'})
        assert flag.content == 'flag{updated}'

    async def test_delete(self, mock_client: CTFdClient) -> None:
        await mock_client.flags.delete(1)

    async def test_types(self, mock_client: CTFdClient) -> None:
        types = await mock_client.flags.types()
        assert 'static' in types

    async def test_type_by_name(self, mock_client: CTFdClient) -> None:
        t = await mock_client.flags.type('static')
        assert t['name'] == 'static'
