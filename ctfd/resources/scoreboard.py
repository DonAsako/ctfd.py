from __future__ import annotations

from ctfd.models import ScoreboardEntry
from ctfd.resources._base import Resource, _data_list


class ScoreboardResource(Resource):
    async def list(self) -> list[ScoreboardEntry]:
        """Return the full scoreboard."""

        payload = await self._http.get_json('/scoreboard')
        return [ScoreboardEntry.model_validate(item) for item in _data_list(payload)]

    async def top(self, count: int) -> dict[str, ScoreboardEntry]:
        """Return the top ``count`` entries of the scoreboard.

        CTFd returns this endpoint as a mapping keyed by position (e.g.
        ``"1": {...}, "2": {...}``); the mapping is preserved here.
        """

        payload = await self._http.get_json(f'/scoreboard/top/{count}')
        data = payload.get('data', {}) if isinstance(payload, dict) else {}
        if not isinstance(data, dict):
            return {}
        return {key: ScoreboardEntry.model_validate(value) for key, value in data.items()}
