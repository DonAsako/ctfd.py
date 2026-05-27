from __future__ import annotations

from typing import TYPE_CHECKING, Any, Self

import httpx

if TYPE_CHECKING:
    from types import TracebackType

from ctfd.exceptions import CTFdAuthenticationError, error_for_status

DEFAULT_TIMEOUT = 30.0
DEFAULT_USER_AGENT = 'ctfd.py'


class AsyncHTTPClient:
    """Thin async wrapper around :class:`httpx.AsyncClient`.

    Centralises base-URL resolution, authentication, JSON decoding and error
    mapping so resource classes can stay focused on endpoint semantics.
    """

    def __init__(  # noqa: PLR0913
        self,
        base_url: str,
        token: str | None = None,
        *,
        timeout: float = DEFAULT_TIMEOUT,
        user_agent: str = DEFAULT_USER_AGENT,
        verify: bool = True,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        self._base_url = base_url.rstrip('/')
        self._token = token
        self._owns_client = client is None
        headers = {
            'Accept': 'application/json',
            'User-Agent': user_agent,
        }
        if token:
            headers['Authorization'] = f'Token {token}'
        self._client = client or httpx.AsyncClient(
            base_url=self._api_root(),
            headers=headers,
            timeout=timeout,
            verify=verify,
        )

    def _api_root(self) -> str:
        if self._base_url.endswith('/api/v1'):
            return self._base_url
        return f'{self._base_url}/api/v1'

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        await self.aclose()

    async def aclose(self) -> None:
        if self._owns_client:
            await self._client.aclose()

    async def request(  # noqa: PLR0913
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: Any = None,
        data: Any = None,
        files: Any = None,
        headers: dict[str, str] | None = None,
    ) -> httpx.Response:
        response = await self._client.request(
            method,
            path,
            params=_clean_params(params),
            json=json,
            data=data,
            files=files,
            headers=headers,
        )
        if 300 <= response.status_code < 400:
            location = response.headers.get('location', '')
            if '/login' in location:
                raise CTFdAuthenticationError(
                    status_code=response.status_code,
                    message=f'CTFd redirected to {location!r}; the request was likely unauthenticated.',
                )
        if response.status_code >= 400:
            raise _exception_from_response(response)
        return response

    async def get_json(self, path: str, *, params: dict[str, Any] | None = None) -> Any:
        response = await self.request('GET', path, params=params)
        return _decode_json(response)

    async def post_json(
        self,
        path: str,
        *,
        json: Any = None,
        params: dict[str, Any] | None = None,
    ) -> Any:
        response = await self.request('POST', path, json=json, params=params)
        return _decode_json(response)

    async def patch_json(
        self,
        path: str,
        *,
        json: Any = None,
        params: dict[str, Any] | None = None,
    ) -> Any:
        response = await self.request('PATCH', path, json=json, params=params)
        return _decode_json(response)

    async def delete_json(self, path: str, *, params: dict[str, Any] | None = None) -> Any:
        response = await self.request('DELETE', path, params=params)
        return _decode_json(response)

    async def put_json(
        self,
        path: str,
        *,
        json: Any = None,
        params: dict[str, Any] | None = None,
    ) -> Any:
        response = await self.request('PUT', path, json=json, params=params)
        return _decode_json(response)


def _clean_params(params: dict[str, Any] | None) -> dict[str, Any] | None:
    if not params:
        return None
    return {k: v for k, v in params.items() if v is not None}


def _decode_json(response: httpx.Response) -> Any:
    if not response.content:
        return None
    return response.json()


def _exception_from_response(response: httpx.Response) -> Exception:
    payload: Any = None
    message = ''
    errors: dict[str, Any] = {}
    try:
        payload = response.json()
    except ValueError:
        message = response.text
    else:
        if isinstance(payload, dict):
            raw_errors = payload.get('errors')
            if isinstance(raw_errors, dict):
                errors = raw_errors
            message = str(payload.get('message') or payload.get('error') or '')
    return error_for_status(
        status_code=response.status_code,
        message=message,
        errors=errors,
        payload=payload,
    )
