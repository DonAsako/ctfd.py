from __future__ import annotations

import pytest

from ctfd.client import CTFdClient
from ctfd.models import File

FILE = {'id': 1, 'type': 'challenge', 'location': 'uploads/abc/file.txt', 'sha1sum': 'abc123'}


@pytest.mark.unit
@pytest.mark.responses(
    {
        'GET /api/v1/files': {'success': True, 'data': [FILE]},
        'GET /api/v1/files/1': {'success': True, 'data': FILE},
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

    async def test_update_raises(self, mock_client: CTFdClient) -> None:
        with pytest.raises(NotImplementedError):
            await mock_client.files.update(1, {})
