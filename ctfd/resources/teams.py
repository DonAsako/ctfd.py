from __future__ import annotations

from typing import Any

from ctfd.models import Award, Submission, Team
from ctfd.resources._base import CRUDResource, _data, _data_list, _serialize


class TeamsResource(CRUDResource[Team]):
    path = '/teams'
    model = Team

    async def me(self) -> Team:
        payload = await self._http.get_json('/teams/me')
        return Team.model_validate(_data(payload))

    async def update_me(self, body: dict[str, Any]) -> Team:
        payload = await self._http.patch_json('/teams/me', json=_serialize(body))
        return Team.model_validate(_data(payload))

    async def delete_me(self) -> None:
        await self._http.delete_json('/teams/me')

    async def my_awards(self) -> list[Award]:
        payload = await self._http.get_json('/teams/me/awards')
        return [Award.model_validate(item) for item in _data_list(payload)]

    async def my_solves(self) -> list[Submission]:
        payload = await self._http.get_json('/teams/me/solves')
        return [Submission.model_validate(item) for item in _data_list(payload)]

    async def my_fails(self) -> list[Submission]:
        payload = await self._http.get_json('/teams/me/fails')
        return [Submission.model_validate(item) for item in _data_list(payload)]

    async def add_my_member(self, body: dict[str, Any]) -> dict[str, Any]:
        payload = await self._http.post_json('/teams/me/members', json=_serialize(body))
        result = _data(payload)
        return result if isinstance(result, dict) else {}

    async def awards(self, team_id: int) -> list[Award]:
        payload = await self._http.get_json(f'/teams/{team_id}/awards')
        return [Award.model_validate(item) for item in _data_list(payload)]

    async def solves(self, team_id: int) -> list[Submission]:
        payload = await self._http.get_json(f'/teams/{team_id}/solves')
        return [Submission.model_validate(item) for item in _data_list(payload)]

    async def fails(self, team_id: int) -> list[Submission]:
        payload = await self._http.get_json(f'/teams/{team_id}/fails')
        return [Submission.model_validate(item) for item in _data_list(payload)]

    async def members(self, team_id: int) -> list[int]:
        payload = await self._http.get_json(f'/teams/{team_id}/members')
        data = _data(payload)
        return list(data) if isinstance(data, list) else []

    async def add_member(self, team_id: int, user_id: int) -> dict[str, Any]:
        payload = await self._http.post_json(f'/teams/{team_id}/members', json={'user_id': user_id})
        result = _data(payload)
        return result if isinstance(result, dict) else {}

    async def remove_member(self, team_id: int, user_id: int) -> None:
        await self._http.delete_json(f'/teams/{team_id}/members', params={'user_id': user_id})
