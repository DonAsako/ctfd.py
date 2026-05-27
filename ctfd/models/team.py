from __future__ import annotations

from datetime import datetime

from ctfd.models._base import CTFdModel


class Team(CTFdModel):
    id: int
    oauth_id: int | None = None
    name: str | None = None
    email: str | None = None
    password: str | None = None
    secret: str | None = None
    website: str | None = None
    affiliation: str | None = None
    country: str | None = None
    bracket_id: int | None = None
    hidden: bool | None = None
    banned: bool | None = None
    captain_id: int | None = None
    created: datetime | None = None
