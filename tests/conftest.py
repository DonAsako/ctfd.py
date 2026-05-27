from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

import httpx
import pytest

from ctfd.client import CTFdClient

if TYPE_CHECKING:
    from collections.abc import Callable


def make_response(
    payload: Any,
    *,
    status_code: int = 200,
    content_type: str = 'application/json',
) -> httpx.Response:
    return httpx.Response(
        status_code=status_code,
        headers={'content-type': content_type},
        content=json.dumps(payload).encode(),
    )


def make_transport(
    handler: Callable[[httpx.Request], httpx.Response],
) -> httpx.MockTransport:
    return httpx.MockTransport(handler)


def simple_transport(responses: dict[str, Any]) -> httpx.MockTransport:
    """Build a transport that maps ``"METHOD /path"`` to a JSON response payload."""

    def handler(request: httpx.Request) -> httpx.Response:
        key = f'{request.method} {request.url.path}'
        if key in responses:
            return make_response(responses[key])
        return make_response({'success': False, 'message': f'no mock for {key}'}, status_code=404)

    return make_transport(handler)


@pytest.fixture
def mock_client(request: pytest.FixtureRequest) -> CTFdClient:
    """Return a CTFdClient backed by a mock transport.

    Use the ``responses`` marker to inject route → payload pairs::

        @pytest.mark.responses({'GET /api/v1/challenges': {'success': True, 'data': [...]}})
        async def test_foo(mock_client): ...
    """
    marker = request.node.get_closest_marker('responses')
    responses: dict[str, Any] = marker.args[0] if marker else {}
    transport = simple_transport(responses)
    inner = httpx.AsyncClient(
        base_url='http://ctfd.test/api/v1',
        transport=transport,
    )
    return CTFdClient('http://ctfd.test', client=inner)


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line('markers', 'responses(mapping): mock HTTP responses for mock_client')
