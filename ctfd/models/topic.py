from __future__ import annotations

from ctfd.models._base import CTFdModel


class Topic(CTFdModel):
    id: int
    value: str | None = None
