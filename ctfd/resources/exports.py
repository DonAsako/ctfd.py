from __future__ import annotations

from typing import TYPE_CHECKING

from ctfd.resources._base import Resource

if TYPE_CHECKING:
    from collections.abc import AsyncIterator

DEFAULT_CHUNK_SIZE = 64 * 1024


class ExportsResource(Resource):
    """Bindings for the ``/exports/raw`` endpoint.

    The endpoint streams a ZIP archive of the entire CTFd instance, so the
    methods exposed here return raw bytes rather than parsed models.
    """

    async def raw(self) -> bytes:
        """Download the export archive and return it entirely in memory."""

        response = await self._http.request('POST', '/exports/raw')
        return response.content

    async def stream(self, chunk_size: int = DEFAULT_CHUNK_SIZE) -> AsyncIterator[bytes]:
        """Stream the export archive in chunks of ``chunk_size`` bytes."""

        response = await self._http.request('POST', '/exports/raw')
        async for chunk in response.aiter_bytes(chunk_size):
            yield chunk
