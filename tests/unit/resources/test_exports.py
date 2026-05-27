from __future__ import annotations

import httpx
import pytest

from ctfd.client import CTFdClient
from tests.conftest import make_transport


@pytest.mark.unit
class TestExportsResource:
    async def test_raw_returns_bytes(self) -> None:
        content = b'PK fake zip content'

        def handler(_request: httpx.Request) -> httpx.Response:
            return httpx.Response(200, content=content, headers={'content-type': 'application/zip'})

        inner = httpx.AsyncClient(base_url='http://ctfd.test/api/v1', transport=make_transport(handler))
        client = CTFdClient('http://ctfd.test', client=inner)
        data = await client.exports.raw()
        assert data == content

    async def test_stream_yields_bytes(self) -> None:
        content = b'x' * 200

        def handler(_request: httpx.Request) -> httpx.Response:
            return httpx.Response(200, content=content, headers={'content-type': 'application/zip'})

        inner = httpx.AsyncClient(base_url='http://ctfd.test/api/v1', transport=make_transport(handler))
        client = CTFdClient('http://ctfd.test', client=inner)
        chunks = []
        async for chunk in client.exports.stream(chunk_size=64):
            chunks.append(chunk)
        assert b''.join(chunks) == content
