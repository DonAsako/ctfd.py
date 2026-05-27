from __future__ import annotations

from typing import Any

from ctfd.models import Award, Submission, User
from ctfd.resources._base import CRUDResource, _data, _data_list, _serialize


class UsersResource(CRUDResource[User]):
    path = '/users'
    model = User

    async def me(self) -> User:
        payload = await self._http.get_json('/users/me')
        return User.model_validate(_data(payload))

    async def update_me(self, body: dict[str, Any]) -> User:
        payload = await self._http.patch_json('/users/me', json=_serialize(body))
        return User.model_validate(_data(payload))

    async def my_awards(self) -> list[Award]:
        payload = await self._http.get_json('/users/me/awards')
        return [Award.model_validate(item) for item in _data_list(payload)]

    async def my_solves(self) -> list[Submission]:
        payload = await self._http.get_json('/users/me/solves')
        return [Submission.model_validate(item) for item in _data_list(payload)]

    async def my_fails(self) -> list[Submission]:
        payload = await self._http.get_json('/users/me/fails')
        return [Submission.model_validate(item) for item in _data_list(payload)]

    async def my_submissions(self) -> list[Submission]:
        payload = await self._http.get_json('/users/me/submissions')
        return [Submission.model_validate(item) for item in _data_list(payload)]

    async def awards(self, user_id: int) -> list[Award]:
        payload = await self._http.get_json(f'/users/{user_id}/awards')
        return [Award.model_validate(item) for item in _data_list(payload)]

    async def solves(self, user_id: int) -> list[Submission]:
        payload = await self._http.get_json(f'/users/{user_id}/solves')
        return [Submission.model_validate(item) for item in _data_list(payload)]

    async def fails(self, user_id: int) -> list[Submission]:
        payload = await self._http.get_json(f'/users/{user_id}/fails')
        return [Submission.model_validate(item) for item in _data_list(payload)]

    async def email(self, user_id: int, body: dict[str, Any]) -> dict[str, Any]:
        """Send an email to the user identified by ``user_id``."""

        payload = await self._http.post_json(f'/users/{user_id}/email', json=_serialize(body))
        result = _data(payload)
        return result if isinstance(result, dict) else {}
