from __future__ import annotations

import json

import httpx
import pytest

from ctfd._http import AsyncHTTPClient
from ctfd.models import Challenge
from ctfd.pagination import AsyncPaginator, PageMeta


def _paged_transport(pages: list[list[dict]]) -> httpx.MockTransport:
    """Return a transport that serves pages by the ``page`` query parameter."""

    def handler(request: httpx.Request) -> httpx.Response:
        page = int(request.url.params.get('page', 1))
        idx = page - 1
        if idx >= len(pages):
            data: list[dict] = []
            nxt = None
        else:
            data = pages[idx]
            nxt = page + 1 if page < len(pages) else None

        payload = {
            'success': True,
            'data': data,
            'meta': {
                'pagination': {
                    'page': page,
                    'next': nxt,
                    'prev': page - 1 if page > 1 else None,
                    'pages': len(pages),
                    'per_page': 50,
                    'total': sum(len(p) for p in pages),
                }
            },
        }
        return httpx.Response(200, content=json.dumps(payload).encode(), headers={'content-type': 'application/json'})

    return httpx.MockTransport(handler)


@pytest.fixture
def multi_page_http() -> AsyncHTTPClient:
    pages = [
        [{'id': 1, 'name': 'ch1'}, {'id': 2, 'name': 'ch2'}],
        [{'id': 3, 'name': 'ch3'}],
    ]
    inner = httpx.AsyncClient(base_url='http://ctfd.test/api/v1', transport=_paged_transport(pages))
    return AsyncHTTPClient('http://ctfd.test', client=inner)


@pytest.fixture
def single_page_http() -> AsyncHTTPClient:
    pages = [[{'id': 10, 'name': 'only'}]]
    inner = httpx.AsyncClient(base_url='http://ctfd.test/api/v1', transport=_paged_transport(pages))
    return AsyncHTTPClient('http://ctfd.test', client=inner)


@pytest.fixture
def empty_http() -> AsyncHTTPClient:
    pages: list[list[dict]] = [[]]
    inner = httpx.AsyncClient(base_url='http://ctfd.test/api/v1', transport=_paged_transport(pages))
    return AsyncHTTPClient('http://ctfd.test', client=inner)


@pytest.mark.unit
class TestPageMeta:
    def test_from_payload_full(self) -> None:
        payload = {'meta': {'pagination': {'page': 2, 'next': 3, 'prev': 1, 'pages': 5, 'per_page': 50, 'total': 250}}}
        meta = PageMeta.from_payload(payload)
        assert meta.page == 2
        assert meta.next == 3
        assert meta.prev == 1
        assert meta.pages == 5
        assert meta.per_page == 50
        assert meta.total == 250

    def test_from_payload_missing_meta(self) -> None:
        meta = PageMeta.from_payload({})
        assert meta.page is None
        assert meta.next is None

    def test_from_payload_non_dict(self) -> None:
        meta = PageMeta.from_payload([])
        assert meta.page is None

    def test_from_payload_no_pagination_key(self) -> None:
        meta = PageMeta.from_payload({'meta': {}})
        assert meta.total is None


@pytest.mark.unit
class TestAsyncPaginator:
    async def test_iterates_all_pages(self, multi_page_http: AsyncHTTPClient) -> None:
        pager = AsyncPaginator(multi_page_http, '/challenges', Challenge)
        items = await pager.all()
        assert len(items) == 3
        assert [c.id for c in items] == [1, 2, 3]

    async def test_single_page(self, single_page_http: AsyncHTTPClient) -> None:
        pager = AsyncPaginator(single_page_http, '/challenges', Challenge)
        items = await pager.all()
        assert len(items) == 1
        assert items[0].name == 'only'

    async def test_empty_response(self, empty_http: AsyncHTTPClient) -> None:
        pager = AsyncPaginator(empty_http, '/challenges', Challenge)
        items = await pager.all()
        assert items == []

    async def test_meta_starts_empty(self, multi_page_http: AsyncHTTPClient) -> None:
        pager = AsyncPaginator(multi_page_http, '/challenges', Challenge)
        assert pager.meta.page is None

    async def test_meta_updated_after_first_page(self, multi_page_http: AsyncHTTPClient) -> None:
        pager = AsyncPaginator(multi_page_http, '/challenges', Challenge)
        await pager.__anext__()
        assert pager.meta.page == 1
        assert pager.meta.next == 2

    async def test_async_for_loop(self, multi_page_http: AsyncHTTPClient) -> None:
        ids = []
        async for ch in AsyncPaginator(multi_page_http, '/challenges', Challenge):
            ids.append(ch.id)
        assert ids == [1, 2, 3]

    async def test_models_are_parsed(self, multi_page_http: AsyncHTTPClient) -> None:
        pager = AsyncPaginator(multi_page_http, '/challenges', Challenge)
        items = await pager.all()
        assert all(isinstance(c, Challenge) for c in items)

    async def test_extra_params_forwarded(self, multi_page_http: AsyncHTTPClient) -> None:
        pager = AsyncPaginator(multi_page_http, '/challenges', Challenge, params={'q': 'web'})
        assert pager._params['q'] == 'web'

    async def test_stop_async_iteration_when_exhausted(self, single_page_http: AsyncHTTPClient) -> None:
        pager = AsyncPaginator(single_page_http, '/challenges', Challenge)
        await pager.all()
        with pytest.raises(StopAsyncIteration):
            await pager.__anext__()
