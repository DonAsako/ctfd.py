from __future__ import annotations

from datetime import datetime
from typing import Any

from ctfd.models._base import CTFdModel


class Award(CTFdModel):
    id: int
    user_id: int | None = None
    team_id: int | None = None
    type: str | None = None
    name: str | None = None
    description: str | None = None
    date: datetime | None = None
    value: int | None = None
    category: str | None = None
    icon: str | None = None
    requirements: dict[str, Any] | None = None
