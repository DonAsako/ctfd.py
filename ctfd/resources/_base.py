from __future__ import annotations

from typing import TYPE_CHECKING, Any, ClassVar

from pydantic import BaseModel

from ctfd.pagination import AsyncPaginator

if TYPE_CHECKING:
    from ctfd._http import AsyncHTTPClient


class Resource:
    """Common base for every resource binding.

    Subclasses receive the shared :class:`AsyncHTTPClient` instance and use it
    to issue requests against the CTFd API.
    """

    def __init__(self, http: AsyncHTTPClient) -> None:
        self._http = http


class CRUDResource[T: BaseModel](Resource):
    """CRUD helper for the standard ``/path``, ``/path/{id}`` endpoint pair.

    Subclasses set :attr:`path` and :attr:`model`; the helpers below cover the
    HTTP shapes used by the vast majority of CTFd resources.
    """

    path: ClassVar[str]
    model: ClassVar[type[BaseModel]]

    async def list(self, **params: Any) -> list[T]:
        """Fetch the first page of the collection as a list."""

        payload = await self._http.get_json(self.path, params=params)
        return [self._parse(item) for item in _data_list(payload)]

    def iter(self, **params: Any) -> AsyncPaginator[T]:
        """Return an async iterator that walks every page of the collection."""

        return AsyncPaginator(self._http, self.path, self.model, params=params)  # type: ignore[arg-type]

    async def get(self, resource_id: int | str) -> T:
        """Fetch a single resource by its identifier."""

        payload = await self._http.get_json(f'{self.path}/{resource_id}')
        return self._parse(_data(payload))

    async def create(self, body: dict[str, Any] | BaseModel) -> T:
        """Create a new resource from the given body."""

        payload = await self._http.post_json(self.path, json=_serialize(body))
        return self._parse(_data(payload))

    async def update(self, resource_id: int | str, body: dict[str, Any] | BaseModel) -> T:
        """Partially update a resource."""

        payload = await self._http.patch_json(f'{self.path}/{resource_id}', json=_serialize(body))
        return self._parse(_data(payload))

    async def delete(self, resource_id: int | str) -> None:
        """Delete a resource by its identifier."""

        await self._http.delete_json(f'{self.path}/{resource_id}')

    def _parse(self, item: Any) -> T:
        return self.model.model_validate(item)  # type: ignore[return-value]


def _data(payload: Any) -> Any:
    if isinstance(payload, dict) and 'data' in payload:
        return payload['data']
    return payload


def _data_list(payload: Any) -> list[Any]:
    data = _data(payload)
    if isinstance(data, list):
        return data
    return []


def _serialize(body: dict[str, Any] | BaseModel) -> dict[str, Any]:
    if isinstance(body, BaseModel):
        return body.model_dump(exclude_none=True, by_alias=True)
    return body
