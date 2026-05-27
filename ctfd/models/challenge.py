from __future__ import annotations

from typing import Any

from ctfd.models._base import CTFdModel


class Challenge(CTFdModel):
    id: int
    name: str | None = None
    description: str | None = None
    attribution: str | None = None
    connection_info: str | None = None
    next_id: int | None = None
    max_attempts: int | None = None
    value: int | None = None
    category: str | None = None
    type: str | None = None
    state: str | None = None
    logic: str | None = None
    initial: int | None = None
    minimum: int | None = None
    decay: int | None = None
    position: int | None = None
    function: str | None = None
    requirements: dict[str, Any] | None = None
    solves: int | None = None
    solved_by_me: bool | None = None
