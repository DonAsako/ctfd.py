from __future__ import annotations

import io

import httpx
import pytest

from ctfd.client import CTFdClient
from ctfd.models import File
from tests.conftest import make_transport

FILE = {'id': 1, 'type': 'challenge', 'location': 'uploads/abc/file.txt', 'sha1sum': 'abc123'}


@pytest.mark.unit
@pytest.mark.responses(
    {
        'GET /api/v1/files': {'success': True, 'data': [FILE]},
        'GET /api/v1/files/1': {'success': True, 'data': FILE},
        'POST /api/v1/files': {'success': True, 'data': [FILE]},
        'DELETE /api/v1/files/1': {'success': True},
    }
)
class TestFilesResource:
    async def test_list(self, mock_client: CTFdClient) -> None:
        files = await mock_client.files.list()
        assert isinstance(files[0], File)
        assert files[0].sha1sum == 'abc123'

    async def test_get(self, mock_client: CTFdClient) -> None:
        f = await mock_client.files.get(1)
        assert f.location == 'uploads/abc/file.txt'

    async def test_delete(self, mock_client: CTFdClient) -> None:
        await mock_client.files.delete(1)

    async def test_upload_returns_list(self, mock_client: CTFdClient) -> None:
        files = await mock_client.files.upload(b'payload', type='challenge', challenge_id=42)
        assert len(files) == 1
        assert isinstance(files[0], File)


@pytest.mark.unit
class TestFilesDownload:
    async def test_download_hits_site_root(self) -> None:
        captured: list[str] = []

        def handler(request: httpx.Request) -> httpx.Response:
            captured.append(str(request.url))
            if request.url.path == '/api/v1/files/1':
                return httpx.Response(
                    200,
                    json={'success': True, 'data': FILE},
                    headers={'content-type': 'application/json'},
                )
            return httpx.Response(200, content=b'binary blob')

        inner = httpx.AsyncClient(base_url='http://ctfd.test/api/v1', transport=make_transport(handler))
        client = CTFdClient('http://ctfd.test', client=inner)
        data = await client.files.download(1)
        assert data == b'binary blob'
        assert captured[-1] == 'http://ctfd.test/files/uploads/abc/file.txt'

    async def test_download_raises_when_no_location(self) -> None:
        def handler(_request: httpx.Request) -> httpx.Response:
            return httpx.Response(
                200,
                json={'success': True, 'data': {'id': 1, 'location': None}},
                headers={'content-type': 'application/json'},
            )

        inner = httpx.AsyncClient(base_url='http://ctfd.test/api/v1', transport=make_transport(handler))
        client = CTFdClient('http://ctfd.test', client=inner)
        with pytest.raises(ValueError, match='no downloadable location'):
            await client.files.download(1)


@pytest.mark.unit
class TestFilesUploadShape:
    async def test_upload_sends_multipart_with_file_field(self) -> None:
        seen: dict[str, bytes] = {}

        def handler(request: httpx.Request) -> httpx.Response:
            seen['content_type'] = request.headers.get('content-type', '').encode()
            seen['body'] = request.content
            return httpx.Response(
                200,
                json={'success': True, 'data': [FILE]},
                headers={'content-type': 'application/json'},
            )

        inner = httpx.AsyncClient(base_url='http://ctfd.test/api/v1', transport=make_transport(handler))
        client = CTFdClient('http://ctfd.test', client=inner)
        await client.files.upload(
            ('payload.bin', io.BytesIO(b'binary content'), 'application/octet-stream'),
            type='challenge',
            challenge_id=42,
        )
        assert seen['content_type'].startswith(b'multipart/form-data')
        assert b'name="file"' in seen['body']
        assert b'binary content' in seen['body']
        assert b'name="type"' in seen['body']
        assert b'challenge' in seen['body']
        assert b'name="challenge_id"' in seen['body']
