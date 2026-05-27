from __future__ import annotations

import json

import httpx
import pytest

from ctfd._http import AsyncHTTPClient
from ctfd.exceptions import (
    CTFdAuthenticationError,
    CTFdNotFoundError,
    CTFdServerError,
    CTFdValidationError,
)


def _make_transport(responses: dict[str, tuple[int, object]]) -> httpx.MockTransport:
    def handler(request: httpx.Request) -> httpx.Response:
        key = f'{request.method} {request.url.path}'
        if key not in responses:
            return httpx.Response(404, content=b'{"message":"not found"}', headers={'content-type': 'application/json'})
        status, body = responses[key]
        return httpx.Response(
            status,
            content=json.dumps(body).encode(),
            headers={'content-type': 'application/json'},
        )

    return httpx.MockTransport(handler)


@pytest.fixture
def http_client() -> AsyncHTTPClient:
    inner = httpx.AsyncClient(
        base_url='http://ctfd.test/api/v1',
        transport=_make_transport(
            {
                'GET /api/v1/challenges': (200, {'success': True, 'data': [{'id': 1}]}),
                'POST /api/v1/challenges': (200, {'success': True, 'data': {'id': 2}}),
                'PATCH /api/v1/challenges/1': (200, {'success': True, 'data': {'id': 1, 'name': 'updated'}}),
                'DELETE /api/v1/challenges/1': (200, {'success': True}),
                'GET /api/v1/bad_json': (200, {'success': True}),
                'GET /api/v1/error_400': (
                    400,
                    {'success': False, 'message': 'bad input', 'errors': {'name': ['required']}},
                ),
                'GET /api/v1/error_401': (401, {'success': False, 'message': 'auth required'}),
                'GET /api/v1/error_403': (403, {'success': False, 'message': 'forbidden'}),
                'GET /api/v1/error_404': (404, {'success': False, 'message': 'not found'}),
                'GET /api/v1/error_500': (500, {'success': False, 'message': 'server error'}),
                'GET /api/v1/login_redirect': (302, {'location': '/login?next=/'}),
            }
        ),
    )
    return AsyncHTTPClient('http://ctfd.test', client=inner)


@pytest.mark.unit
class TestAsyncHTTPClientInit:
    def test_api_root_appended_when_missing(self) -> None:
        c = AsyncHTTPClient('http://example.com')
        assert c._api_root() == 'http://example.com/api/v1'

    def test_api_root_not_double_appended(self) -> None:
        c = AsyncHTTPClient('http://example.com/api/v1')
        assert c._api_root() == 'http://example.com/api/v1'

    def test_trailing_slash_stripped(self) -> None:
        c = AsyncHTTPClient('http://example.com/')
        assert c._api_root() == 'http://example.com/api/v1'


@pytest.mark.unit
class TestHTTPMethods:
    async def test_get_json_returns_parsed_payload(self, http_client: AsyncHTTPClient) -> None:
        data = await http_client.get_json('/challenges')
        assert data == {'success': True, 'data': [{'id': 1}]}

    async def test_post_json_returns_parsed_payload(self, http_client: AsyncHTTPClient) -> None:
        data = await http_client.post_json('/challenges', json={'name': 'test'})
        assert data['data']['id'] == 2

    async def test_patch_json_returns_updated_resource(self, http_client: AsyncHTTPClient) -> None:
        data = await http_client.patch_json('/challenges/1', json={'name': 'updated'})
        assert data['data']['name'] == 'updated'

    async def test_delete_json_succeeds(self, http_client: AsyncHTTPClient) -> None:
        data = await http_client.delete_json('/challenges/1')
        assert data['success'] is True


@pytest.mark.unit
class TestHTTPErrors:
    async def test_400_raises_validation_error(self, http_client: AsyncHTTPClient) -> None:
        with pytest.raises(CTFdValidationError) as exc_info:
            await http_client.get_json('/error_400')
        assert exc_info.value.errors == {'name': ['required']}
        assert exc_info.value.message == 'bad input'

    async def test_401_raises_authentication_error(self, http_client: AsyncHTTPClient) -> None:
        with pytest.raises(CTFdAuthenticationError):
            await http_client.get_json('/error_401')

    async def test_404_raises_not_found_error(self, http_client: AsyncHTTPClient) -> None:
        with pytest.raises(CTFdNotFoundError):
            await http_client.get_json('/error_404')

    async def test_500_raises_server_error(self, http_client: AsyncHTTPClient) -> None:
        with pytest.raises(CTFdServerError):
            await http_client.get_json('/error_500')
