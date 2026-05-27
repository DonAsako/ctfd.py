from __future__ import annotations

from ctfd.models._base import CTFdModel


class Flag(CTFdModel):
    id: int
    challenge_id: int | None = None
    type: str | None = None
    content: str | None = None
    data: str | None = None
