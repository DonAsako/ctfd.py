from __future__ import annotations

from typing import Any

from ctfd.models._base import CTFdModel


class Hint(CTFdModel):
    id: int
    title: str | None = None
    type: str | None = None
    challenge_id: int | None = None
    content: str | None = None
    cost: int | None = None
    requirements: dict[str, Any] | None = None
