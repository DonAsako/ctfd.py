from __future__ import annotations

from typing import Any

from ctfd.models import Flag
from ctfd.resources._base import _CreateOps, _data, _DeleteOps, _GetOps, _ListOps, _UpdateOps


class FlagsResource(_ListOps[Flag], _GetOps[Flag], _CreateOps[Flag], _UpdateOps[Flag], _DeleteOps):
    path = '/flags'
    model = Flag

    async def types(self) -> dict[str, Any]:
        """List the registered flag types (``GET /flags/types``)."""

        payload = await self._http.get_json('/flags/types')
        result = _data(payload)
        return result if isinstance(result, dict) else {}

    async def type(self, type_name: str) -> dict[str, Any]:
        """Fetch the definition of a single flag type (``GET /flags/types/{name}``)."""

        payload = await self._http.get_json(f'/flags/types/{type_name}')
        result = _data(payload)
        return result if isinstance(result, dict) else {}
