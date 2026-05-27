from __future__ import annotations

from typing import IO, Any

from ctfd.models import File
from ctfd.resources._base import Resource, _data, _data_list, _DeleteOps, _GetOps, _ListOps


class FilesResource(_ListOps[File], _GetOps[File], _DeleteOps, Resource):
    """``/files`` — list, retrieve, delete, plus multipart ``upload`` and raw ``download``.

    Per the CTFd swagger, ``POST /files`` is multipart and uses the ``file``
    form field (singular) plus optional ``type``, ``location``,
    ``challenge_id``, ``page_id`` and ``solution_id`` companions; it is exposed
    as :meth:`upload` rather than ``create`` because the return type is a list
    of created records, not a single one.
    """

    path = '/files'
    model = File

    async def upload(  # noqa: PLR0913
        self,
        file: IO[bytes] | bytes | tuple[str, IO[bytes] | bytes, str | None],
        *,
        type: str | None = None,  # noqa: A002
        location: str | None = None,
        challenge_id: int | None = None,
        page_id: int | None = None,
        solution_id: int | None = None,
    ) -> list[File]:
        """Upload a file and return the created :class:`File` records.

        ``file`` accepts any value supported by httpx's ``files=`` argument:
        a raw bytes blob, a binary file-like object, or a ``(filename, content,
        content_type)`` tuple.
        """

        data = _drop_none(
            {
                'type': type,
                'location': location,
                'challenge_id': challenge_id,
                'page_id': page_id,
                'solution_id': solution_id,
            }
        )
        response = await self._http.request('POST', self.path, files={'file': file}, data=data)
        payload = response.json() if response.content else {}
        return [File.model_validate(item) for item in _data_list(payload)]

    async def download(self, file_id: int) -> bytes:
        """Download the raw bytes of a stored file.

        Fetches the file record to resolve its ``location``, then requests the
        site-root URL ``{site}/files/{location}`` (CTFd serves uploads outside
        of ``/api/v1``).
        """

        meta_payload = await self._http.get_json(f'/files/{file_id}')
        meta = _data(meta_payload)
        location = meta.get('location') if isinstance(meta, dict) else None
        if not isinstance(location, str) or not location:
            msg = f'File {file_id} has no downloadable location'
            raise ValueError(msg)
        return await self._http.get_bytes(f'{self._http.site_root}/files/{location}')


def _drop_none(mapping: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in mapping.items() if v is not None}
