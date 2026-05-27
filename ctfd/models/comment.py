from __future__ import annotations

from datetime import datetime

from ctfd.models._base import CTFdModel


class Comment(CTFdModel):
    id: int
    type: str | None = None
    content: str | None = None
    date: datetime | None = None
    author_id: int | None = None
