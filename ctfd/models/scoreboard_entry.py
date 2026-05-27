from __future__ import annotations

from typing import Any

from ctfd.models._base import CTFdModel


class ScoreboardEntry(CTFdModel):
    """A single row of the scoreboard.

    Not formally defined in the public swagger; fields are inferred from the
    CTFd source and kept fully optional.
    """

    pos: int | None = None
    account_id: int | None = None
    account_url: str | None = None
    account_type: str | None = None
    oauth_id: int | None = None
    name: str | None = None
    score: int | None = None
    bracket_id: int | None = None
    bracket_name: str | None = None
    members: list[dict[str, Any]] | None = None
