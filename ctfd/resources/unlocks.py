from __future__ import annotations

from typing import Any

from ctfd.models import Unlock
from ctfd.resources._base import Resource, _data, _data_list, _serialize


class UnlocksResource(Resource):
    """Bindings for ``/unlocks`` (no detail or destructive endpoints)."""

    async def list(self, **params: Any) -> list[Unlock]:
        payload = await self._http.get_json('/unlocks', params=params)
        return [Unlock.model_validate(item) for item in _data_list(payload)]

    async def create(self, body: dict[str, Any]) -> Unlock:
        payload = await self._http.post_json('/unlocks', json=_serialize(body))
        return Unlock.model_validate(_data(payload))
