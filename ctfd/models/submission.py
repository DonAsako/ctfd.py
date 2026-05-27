from __future__ import annotations

from datetime import datetime

from ctfd.models._base import CTFdModel


class Submission(CTFdModel):
    id: int
    challenge_id: int | None = None
    user_id: int | None = None
    team_id: int | None = None
    ip: str | None = None
    provided: str | None = None
    type: str | None = None
    date: datetime | None = None
