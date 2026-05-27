from __future__ import annotations

from typing import Any

from ctfd.models import Flag
from ctfd.resources._base import CRUDResource, _data


class FlagsResource(CRUDResource[Flag]):
    path = '/flags'
    model = Flag

    async def types(self) -> dict[str, Any]:
        """List the registered flag types."""

        payload = await self._http.get_json('/flags/types')
        result = _data(payload)
        return result if isinstance(result, dict) else {}

    async def type(self, type_name: str) -> dict[str, Any]:
        """Fetch the definition of a single flag type."""

        payload = await self._http.get_json(f'/flags/types/{type_name}')
        result = _data(payload)
        return result if isinstance(result, dict) else {}
