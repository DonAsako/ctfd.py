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


@pytest.mark.unit
class TestLoginRedirectGuard:
    """When CTFd answers a /api/v1/... request with 302 → /login, treat it as auth-required."""

    @staticmethod
    def _client(location: str, *, status: int = 302) -> AsyncHTTPClient:
        def handler(_request: httpx.Request) -> httpx.Response:
            return httpx.Response(status, headers={'location': location})

        inner = httpx.AsyncClient(base_url='http://ctfd.test/api/v1', transport=httpx.MockTransport(handler))
        return AsyncHTTPClient('http://ctfd.test', client=inner)

    async def test_login_redirect_raises_authentication_error(self) -> None:
        client = self._client('/login?next=%2Fapi%2Fv1%2Fchallenges%3F')
        with pytest.raises(CTFdAuthenticationError) as exc_info:
            await client.get_json('/challenges')
        assert '/login' in exc_info.value.message

    async def test_non_login_redirect_is_not_intercepted(self) -> None:
        client = self._client('/somewhere-else')
        # Non-login 3xx is not raised; the response is returned as-is and
        # _decode_json reads its (empty) body without crashing.
        result = await client.get_json('/challenges')
        assert result is None

    async def test_site_root_strips_api_v1_suffix(self) -> None:
        c1 = AsyncHTTPClient('http://example.com/api/v1')
        c2 = AsyncHTTPClient('http://example.com')
        assert c1.site_root == 'http://example.com'
        assert c2.site_root == 'http://example.com'
