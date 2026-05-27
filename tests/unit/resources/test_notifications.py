from __future__ import annotations

import pytest

from ctfd.client import CTFdClient
from ctfd.models import Notification

NOTIF = {'id': 1, 'title': 'CTF starts soon', 'content': '5 mins left', 'user_id': None, 'team_id': None}


@pytest.mark.unit
@pytest.mark.responses(
    {
        'GET /api/v1/notifications': {'success': True, 'data': [NOTIF]},
        'GET /api/v1/notifications/1': {'success': True, 'data': NOTIF},
        'POST /api/v1/notifications': {'success': True, 'data': NOTIF},
        'DELETE /api/v1/notifications/1': {'success': True},
    }
)
class TestNotificationsResource:
    async def test_list(self, mock_client: CTFdClient) -> None:
        notifs = await mock_client.notifications.list()
        assert isinstance(notifs[0], Notification)

    async def test_get(self, mock_client: CTFdClient) -> None:
        n = await mock_client.notifications.get(1)
        assert n.title == 'CTF starts soon'

    async def test_create(self, mock_client: CTFdClient) -> None:
        n = await mock_client.notifications.create({'title': 'CTF starts soon', 'content': '5 mins left'})
        assert n.id == 1

    async def test_delete(self, mock_client: CTFdClient) -> None:
        await mock_client.notifications.delete(1)

    async def test_update_raises(self, mock_client: CTFdClient) -> None:
        with pytest.raises(NotImplementedError):
            await mock_client.notifications.update(1, {})
