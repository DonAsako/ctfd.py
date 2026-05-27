from __future__ import annotations

from typing import Any

from ctfd.resources._base import Resource, _data


class StatisticsResource(Resource):
    """``/statistics/*`` — aggregate counters and matrices.

    These endpoints return heterogeneous payloads (per-category counters,
    percentages, time-series matrices, ...), so they are exposed as raw
    mappings rather than strongly-typed models.
    """

    async def challenge_solves(self) -> dict[str, Any]:
        return await self._json('/statistics/challenges/solves')

    async def challenge_solves_percentages(self) -> dict[str, Any]:
        return await self._json('/statistics/challenges/solves/percentages')

    async def challenges(self, column: str) -> dict[str, Any]:
        return await self._json(f'/statistics/challenges/{column}')

    async def progression_matrix(self) -> dict[str, Any]:
        return await self._json('/statistics/progression/matrix')

    async def scores_distribution(self) -> dict[str, Any]:
        return await self._json('/statistics/scores/distribution')

    async def submissions(self, column: str) -> dict[str, Any]:
        return await self._json(f'/statistics/submissions/{column}')

    async def teams(self) -> dict[str, Any]:
        return await self._json('/statistics/teams')

    async def users(self, column: str | None = None) -> dict[str, Any]:
        path = '/statistics/users' if column is None else f'/statistics/users/{column}'
        return await self._json(path)

    async def _json(self, path: str) -> dict[str, Any]:
        payload = await self._http.get_json(path)
        result = _data(payload)
        return result if isinstance(result, dict) else {}
