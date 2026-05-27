from __future__ import annotations

from datetime import datetime

from ctfd.models._base import CTFdModel


class Token(CTFdModel):
    id: int
    type: str | None = None
    user_id: int | None = None
    created: datetime | None = None
    expiration: datetime | None = None
    description: str | None = None
    value: str | None = None
