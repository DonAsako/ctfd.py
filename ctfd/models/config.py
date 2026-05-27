from __future__ import annotations

from ctfd.models._base import CTFdModel


class Config(CTFdModel):
    id: int
    key: str | None = None
    value: str | None = None
