from __future__ import annotations

from ctfd.models import Notification
from ctfd.resources._base import _CreateOps, _DeleteOps, _GetOps, _ListOps


class NotificationsResource(_ListOps[Notification], _GetOps[Notification], _CreateOps[Notification], _DeleteOps):
    """``/notifications`` — list, retrieve, create, delete."""

    path = '/notifications'
    model = Notification
