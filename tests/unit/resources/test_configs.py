from __future__ import annotations

import pytest

from ctfd.client import CTFdClient
from ctfd.models import Config

CONFIG = {'id': 1, 'key': 'ctf_name', 'value': 'My CTF'}
FIELD = {'id': 1, 'name': 'affiliation', 'type': 'text', 'required': False}


@pytest.mark.unit
@pytest.mark.responses(
    {
        'GET /api/v1/configs': {'success': True, 'data': [CONFIG]},
        'POST /api/v1/configs': {'success': True, 'data': CONFIG},
        'PATCH /api/v1/configs': {'success': True, 'data': {}},
        'GET /api/v1/configs/ctf_name': {'success': True, 'data': CONFIG},
        'PATCH /api/v1/configs/ctf_name': {'success': True, 'data': {**CONFIG, 'value': 'New CTF'}},
        'DELETE /api/v1/configs/ctf_name': {'success': True},
        'GET /api/v1/configs/fields': {'success': True, 'data': [FIELD]},
        'POST /api/v1/configs/fields': {'success': True, 'data': FIELD},
        'GET /api/v1/configs/fields/1': {'success': True, 'data': FIELD},
        'PATCH /api/v1/configs/fields/1': {'success': True, 'data': {**FIELD, 'required': True}},
        'DELETE /api/v1/configs/fields/1': {'success': True},
    }
)
class TestConfigsResource:
    async def test_list(self, mock_client: CTFdClient) -> None:
        configs = await mock_client.configs.list()
        assert isinstance(configs[0], Config)
        assert configs[0].key == 'ctf_name'

    async def test_create(self, mock_client: CTFdClient) -> None:
        cfg = await mock_client.configs.create({'key': 'ctf_name', 'value': 'My CTF'})
        assert isinstance(cfg, Config)

    async def test_bulk_update(self, mock_client: CTFdClient) -> None:
        result = await mock_client.configs.bulk_update({'ctf_name': 'New CTF'})
        assert isinstance(result, dict)

    async def test_get_by_key(self, mock_client: CTFdClient) -> None:
        cfg = await mock_client.configs.get('ctf_name')
        assert cfg.value == 'My CTF'

    async def test_update_by_key(self, mock_client: CTFdClient) -> None:
        cfg = await mock_client.configs.update('ctf_name', {'value': 'New CTF'})
        assert cfg.value == 'New CTF'

    async def test_delete_by_key(self, mock_client: CTFdClient) -> None:
        await mock_client.configs.delete('ctf_name')

    async def test_fields(self, mock_client: CTFdClient) -> None:
        fields = await mock_client.configs.fields()
        assert fields[0]['name'] == 'affiliation'

    async def test_create_field(self, mock_client: CTFdClient) -> None:
        field = await mock_client.configs.create_field({'name': 'affiliation'})
        assert field['id'] == 1

    async def test_get_field(self, mock_client: CTFdClient) -> None:
        field = await mock_client.configs.get_field(1)
        assert field['name'] == 'affiliation'

    async def test_update_field(self, mock_client: CTFdClient) -> None:
        field = await mock_client.configs.update_field(1, {'required': True})
        assert field['required'] is True

    async def test_delete_field(self, mock_client: CTFdClient) -> None:
        await mock_client.configs.delete_field(1)
