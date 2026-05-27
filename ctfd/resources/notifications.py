from __future__ import annotations

from ctfd.models import Notification
from ctfd.resources._base import CRUDResource


class NotificationsResource(CRUDResource[Notification]):
    path = '/notifications'
    model = Notification

    async def update(self, resource_id: int | str, body: object) -> Notification:
        raise NotImplementedError('The CTFd API does not support updating notifications.')
