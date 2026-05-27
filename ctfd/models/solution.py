from __future__ import annotations

from ctfd.models._base import CTFdModel


class Solution(CTFdModel):
    id: int
    challenge_id: int | None = None
    content: str | None = None
    state: str | None = None
