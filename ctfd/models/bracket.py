from __future__ import annotations

from ctfd.models._base import CTFdModel


class Bracket(CTFdModel):
    """A scoring bracket grouping users or teams (e.g. ``students`` vs ``staff``).

    Not formally defined in the public swagger; fields are inferred from the
    CTFd source and kept fully optional.
    """

    id: int
    name: str | None = None
    description: str | None = None
    type: str | None = None
