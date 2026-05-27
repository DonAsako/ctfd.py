from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import builtins

from ctfd.models import Config
from ctfd.resources._base import Resource, _data, _data_list, _serialize


class ConfigsResource(Resource):
    """``/configs`` — keyed by string (not integer id), plus the ``/configs/fields`` sub-resource.

    The collection endpoint also accepts ``PATCH`` for bulk updates, which has
    no equivalent in the generic CRUD mixins.
    """

    path = '/configs'

    async def list(self) -> list[Config]:
        payload = await self._http.get_json('/configs')
        return [Config.model_validate(item) for item in _data_list(payload)]

    async def create(self, body: dict[str, Any]) -> Config:
        payload = await self._http.post_json('/configs', json=_serialize(body))
        return Config.model_validate(_data(payload))

    async def bulk_update(self, body: dict[str, Any]) -> dict[str, Any]:
        """Update multiple configuration keys in one call (``PATCH /configs``)."""

        payload = await self._http.patch_json('/configs', json=_serialize(body))
        result = _data(payload)
        return result if isinstance(result, dict) else {}

    async def get(self, config_key: str) -> Config:
        payload = await self._http.get_json(f'/configs/{config_key}')
        return Config.model_validate(_data(payload))

    async def update(self, config_key: str, body: dict[str, Any]) -> Config:
        payload = await self._http.patch_json(f'/configs/{config_key}', json=_serialize(body))
        return Config.model_validate(_data(payload))

    async def delete(self, config_key: str) -> None:
        await self._http.delete_json(f'/configs/{config_key}')

    async def fields(self) -> builtins.list[dict[str, Any]]:
        """List configurable user/team profile fields (``GET /configs/fields``)."""

        payload = await self._http.get_json('/configs/fields')
        return [item for item in _data_list(payload) if isinstance(item, dict)]

    async def create_field(self, body: dict[str, Any]) -> dict[str, Any]:
        payload = await self._http.post_json('/configs/fields', json=_serialize(body))
        result = _data(payload)
        return result if isinstance(result, dict) else {}

    async def get_field(self, field_id: int) -> dict[str, Any]:
        payload = await self._http.get_json(f'/configs/fields/{field_id}')
        result = _data(payload)
        return result if isinstance(result, dict) else {}

    async def update_field(self, field_id: int, body: dict[str, Any]) -> dict[str, Any]:
        payload = await self._http.patch_json(f'/configs/fields/{field_id}', json=_serialize(body))
        result = _data(payload)
        return result if isinstance(result, dict) else {}

    async def delete_field(self, field_id: int) -> None:
        await self._http.delete_json(f'/configs/fields/{field_id}')
