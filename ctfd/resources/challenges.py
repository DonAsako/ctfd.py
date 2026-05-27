from __future__ import annotations

from typing import Any

from ctfd.models import Challenge, File, Flag, Hint, Solution, Submission, Tag, Topic
from ctfd.resources._base import CRUDResource, _data, _data_list


class ChallengesResource(CRUDResource[Challenge]):
    path = '/challenges'
    model = Challenge

    async def attempt(self, challenge_id: int, submission: str) -> dict[str, Any]:
        """Submit an attempt against a challenge and return the raw API result."""

        payload = await self._http.post_json(
            '/challenges/attempt',
            json={'challenge_id': challenge_id, 'submission': submission},
        )
        result = _data(payload)
        return result if isinstance(result, dict) else {}

    async def types(self) -> dict[str, Any]:
        """List the challenge types registered on the server."""

        payload = await self._http.get_json('/challenges/types')
        result = _data(payload)
        return result if isinstance(result, dict) else {}

    async def files(self, challenge_id: int) -> list[File]:
        payload = await self._http.get_json(f'/challenges/{challenge_id}/files')
        return [File.model_validate(item) for item in _data_list(payload)]

    async def flags(self, challenge_id: int) -> list[Flag]:
        payload = await self._http.get_json(f'/challenges/{challenge_id}/flags')
        return [Flag.model_validate(item) for item in _data_list(payload)]

    async def hints(self, challenge_id: int) -> list[Hint]:
        payload = await self._http.get_json(f'/challenges/{challenge_id}/hints')
        return [Hint.model_validate(item) for item in _data_list(payload)]

    async def tags(self, challenge_id: int) -> list[Tag]:
        payload = await self._http.get_json(f'/challenges/{challenge_id}/tags')
        return [Tag.model_validate(item) for item in _data_list(payload)]

    async def topics(self, challenge_id: int) -> list[Topic]:
        payload = await self._http.get_json(f'/challenges/{challenge_id}/topics')
        return [Topic.model_validate(item) for item in _data_list(payload)]

    async def solves(self, challenge_id: int) -> list[Submission]:
        payload = await self._http.get_json(f'/challenges/{challenge_id}/solves')
        return [Submission.model_validate(item) for item in _data_list(payload)]

    async def solution(self, challenge_id: int) -> Solution | None:
        payload = await self._http.get_json(f'/challenges/{challenge_id}/solution')
        data = _data(payload)
        if data is None:
            return None
        return Solution.model_validate(data)

    async def requirements(self, challenge_id: int) -> dict[str, Any]:
        payload = await self._http.get_json(f'/challenges/{challenge_id}/requirements')
        result = _data(payload)
        return result if isinstance(result, dict) else {}

    async def ratings(self, challenge_id: int) -> dict[str, Any]:
        payload = await self._http.get_json(f'/challenges/{challenge_id}/ratings')
        result = _data(payload)
        return result if isinstance(result, dict) else {}

    async def rate(self, challenge_id: int, body: dict[str, Any]) -> dict[str, Any]:
        payload = await self._http.put_json(f'/challenges/{challenge_id}/ratings', json=body)
        result = _data(payload)
        return result if isinstance(result, dict) else {}
