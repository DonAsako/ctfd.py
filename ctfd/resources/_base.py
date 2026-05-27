from __future__ import annotations

from typing import TYPE_CHECKING, Any, ClassVar, cast

from pydantic import BaseModel

from ctfd.pagination import AsyncPaginator

if TYPE_CHECKING:
    from ctfd._http import AsyncHTTPClient


class Resource:
    """Base for every resource binding.

    Concrete resources set :attr:`path` and :attr:`model` as class-level
    constants and compose any subset of the :class:`_ListOps`,
    :class:`_GetOps`, :class:`_CreateOps`, :class:`_UpdateOps`,
    :class:`_DeleteOps` mixins to expose the operations that the CTFd API
    actually supports for that resource.
    """

    path: ClassVar[str] = ''
    model: ClassVar[type[BaseModel]] = BaseModel

    def __init__(self, http: AsyncHTTPClient) -> None:
        self._http = http


class _ListOps[T: BaseModel](Resource):
    """Mixin: ``GET /<path>`` collection listing and pagination."""

    async def list(self, **params: Any) -> list[T]:
        """Fetch the first page of the collection as a list."""

        payload = await self._http.get_json(self.path, params=params)
        return [cast('T', self.model.model_validate(item)) for item in _data_list(payload)]

    def iter(self, **params: Any) -> AsyncPaginator[T]:
        """Return an async iterator that walks every page of the collection."""

        return cast('AsyncPaginator[T]', AsyncPaginator(self._http, self.path, self.model, params=params))


class _GetOps[T: BaseModel](Resource):
    """Mixin: ``GET /<path>/{id}`` single-resource retrieval."""

    async def get(self, resource_id: int | str) -> T:
        payload = await self._http.get_json(f'{self.path}/{resource_id}')
        return cast('T', self.model.model_validate(_data(payload)))


class _CreateOps[T: BaseModel](Resource):
    """Mixin: ``POST /<path>`` resource creation."""

    async def create(self, body: dict[str, Any] | BaseModel) -> T:
        payload = await self._http.post_json(self.path, json=_serialize(body))
        return cast('T', self.model.model_validate(_data(payload)))


class _UpdateOps[T: BaseModel](Resource):
    """Mixin: ``PATCH /<path>/{id}`` partial update."""

    async def update(self, resource_id: int | str, body: dict[str, Any] | BaseModel) -> T:
        payload = await self._http.patch_json(f'{self.path}/{resource_id}', json=_serialize(body))
        return cast('T', self.model.model_validate(_data(payload)))


class _DeleteOps(Resource):
    """Mixin: ``DELETE /<path>/{id}``."""

    async def delete(self, resource_id: int | str) -> None:
        await self._http.delete_json(f'{self.path}/{resource_id}')


def _data(payload: Any) -> Any:
    """Return the ``data`` field of a CTFd response envelope, or the payload itself."""

    if isinstance(payload, dict) and 'data' in payload:
        return payload['data']
    return payload


def _data_list(payload: Any) -> list[Any]:
    """Return ``payload['data']`` if it is a list, otherwise an empty list."""

    data = _data(payload)
    if isinstance(data, list):
        return data
    return []


def _serialize(body: dict[str, Any] | BaseModel) -> dict[str, Any]:
    """Coerce a request body to a JSON-serialisable dict.

    Pydantic models are dumped with ``exclude_none=True`` and ``by_alias=True``
    so the wire payload matches the CTFd field names.
    """

    if isinstance(body, BaseModel):
        return body.model_dump(exclude_none=True, by_alias=True)
    return body
