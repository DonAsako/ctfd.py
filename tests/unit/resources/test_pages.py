from __future__ import annotations

import pytest

from ctfd.client import CTFdClient
from ctfd.models import Page

PAGE = {'id': 1, 'title': 'About', 'route': '/about', 'content': '<p>Hello</p>', 'format': 'html'}


@pytest.mark.unit
@pytest.mark.responses(
    {
        'GET /api/v1/pages': {'success': True, 'data': [PAGE]},
        'GET /api/v1/pages/1': {'success': True, 'data': PAGE},
        'POST /api/v1/pages': {'success': True, 'data': PAGE},
        'PATCH /api/v1/pages/1': {'success': True, 'data': {**PAGE, 'title': 'FAQ'}},
        'DELETE /api/v1/pages/1': {'success': True},
    }
)
class TestPagesResource:
    async def test_list(self, mock_client: CTFdClient) -> None:
        pages = await mock_client.pages.list()
        assert isinstance(pages[0], Page)

    async def test_get(self, mock_client: CTFdClient) -> None:
        page = await mock_client.pages.get(1)
        assert page.route == '/about'

    async def test_create(self, mock_client: CTFdClient) -> None:
        page = await mock_client.pages.create({'title': 'About', 'route': '/about'})
        assert page.id == 1

    async def test_update(self, mock_client: CTFdClient) -> None:
        page = await mock_client.pages.update(1, {'title': 'FAQ'})
        assert page.title == 'FAQ'

    async def test_delete(self, mock_client: CTFdClient) -> None:
        await mock_client.pages.delete(1)
