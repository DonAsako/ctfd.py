from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel

if TYPE_CHECKING:
    from collections.abc import AsyncIterator

    from ctfd._http import AsyncHTTPClient


@dataclass(slots=True)
class PageMeta:
    """Pagination metadata as exposed by the CTFd API.

    The CTFd API returns these counters under the ``meta.pagination`` key on
    list endpoints. Any of them may be missing on legacy versions, in which
    case the field stays ``None``.
    """

    page: int | None = None
    next: int | None = None
    prev: int | None = None
    pages: int | None = None
    per_page: int | None = None
    total: int | None = None

    @classmethod
    def from_payload(cls, payload: Any) -> PageMeta:
        if not isinstance(payload, dict):
            return cls()
        meta = payload.get('meta') or {}
        pagination = meta.get('pagination') if isinstance(meta, dict) else None
        if not isinstance(pagination, dict):
            return cls()
        return cls(
            page=pagination.get('page'),
            next=pagination.get('next'),
            prev=pagination.get('prev'),
            pages=pagination.get('pages'),
            per_page=pagination.get('per_page'),
            total=pagination.get('total'),
        )


class AsyncPaginator[T: BaseModel]:
    """Async iterator over a paginated CTFd list endpoint.

    Iterating yields parsed model instances one by one, transparently
    requesting the next page when the current one is exhausted.
    """

    def __init__(
        self,
        http: AsyncHTTPClient,
        path: str,
        model: type[T],
        *,
        params: dict[str, Any] | None = None,
    ) -> None:
        self._http = http
        self._path = path
        self._model = model
        self._params: dict[str, Any] = dict(params or {})
        self._buffer: list[T] = []
        self._meta = PageMeta()
        self._exhausted = False
        self._loaded_once = False

    def __aiter__(self) -> AsyncIterator[T]:
        return self

    async def __anext__(self) -> T:
        while not self._buffer:
            if self._exhausted:
                raise StopAsyncIteration
            await self._load_next_page()
        return self._buffer.pop(0)

    async def _load_next_page(self) -> None:
        if not self._loaded_once:
            page = self._params.get('page', 1)
        elif self._meta.next is not None:
            page = self._meta.next
        else:
            self._exhausted = True
            return

        request_params = {**self._params, 'page': page}
        payload = await self._http.get_json(self._path, params=request_params)
        self._loaded_once = True
        self._meta = PageMeta.from_payload(payload)

        data = payload.get('data', []) if isinstance(payload, dict) else []
        self._buffer.extend(self._model.model_validate(item) for item in data)

        if self._meta.next is None:
            self._exhausted = True

    async def all(self) -> list[T]:
        """Drain the paginator and return every remaining item as a list."""

        return [item async for item in self]

    @property
    def meta(self) -> PageMeta:
        """Metadata of the most recently fetched page (empty before the first fetch)."""

        return self._meta
