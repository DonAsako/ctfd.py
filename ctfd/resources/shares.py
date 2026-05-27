from __future__ import annotations

from typing import Any

from ctfd.models import Share
from ctfd.resources._base import Resource, _data, _serialize


class SharesResource(Resource):
    """Bindings for ``/shares`` (creation only)."""

    async def create(self, body: dict[str, Any]) -> Share:
        payload = await self._http.post_json('/shares', json=_serialize(body))
        return Share.model_validate(_data(payload))
