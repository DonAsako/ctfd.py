from __future__ import annotations

from ctfd.models._base import CTFdModel


class Tag(CTFdModel):
    id: int
    challenge_id: int | None = None
    value: str | None = None
