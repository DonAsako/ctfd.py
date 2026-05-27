from __future__ import annotations

from datetime import datetime

from ctfd.models._base import CTFdModel


class Unlock(CTFdModel):
    id: int
    user_id: int | None = None
    team_id: int | None = None
    target: int | None = None
    date: datetime | None = None
    type: str | None = None
