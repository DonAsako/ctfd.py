from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ctfd.models import File

if TYPE_CHECKING:
    import builtins
from ctfd.resources._base import CRUDResource, _data, _data_list


class FilesResource(CRUDResource[File]):
    path = '/files'
    model = File

    async def list(self, **params: Any) -> list[File]:
        payload = await self._http.get_json(self.path, params=params)
        return [File.model_validate(item) for item in _data_list(payload)]

    async def create(self, body: dict[str, Any]) -> builtins.list[File]:  # type: ignore[override]
        """Upload one or more files.

        ``body`` is the multipart form payload as accepted by
        :meth:`httpx.AsyncClient.post` (use the ``files=`` and ``data=`` keys).
        The CTFd API returns the list of created file records.
        """

        files = body.get('files')
        data = {k: v for k, v in body.items() if k != 'files'}
        response = await self._http.request('POST', self.path, files=files, data=data)
        payload = response.json() if response.content else {}
        return [File.model_validate(item) for item in _data_list(payload)]

    async def update(self, resource_id: int | str, body: object) -> File:
        raise NotImplementedError('The CTFd API does not support updating files.')

    async def download(self, file_id: int) -> bytes:
        """Download the raw bytes of a stored file."""

        meta_payload = await self._http.get_json(f'/files/{file_id}')
        meta = _data(meta_payload)
        location = meta.get('location') if isinstance(meta, dict) else None
        if not location:
            raise ValueError(f'File {file_id} has no downloadable location')
        response = await self._http.request('GET', f'/../files/{location}')
        return response.content
