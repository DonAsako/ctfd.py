from __future__ import annotations

from datetime import datetime

from ctfd.models._base import CTFdModel


class Notification(CTFdModel):
    id: int
    title: str | None = None
    content: str | None = None
    date: datetime | None = None
    user_id: int | None = None
    team_id: int | None = None
