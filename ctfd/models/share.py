from __future__ import annotations

from datetime import datetime

from ctfd.models._base import CTFdModel


class Share(CTFdModel):
    """A shareable link to a CTFd resource (e.g. a solve, a profile).

    Not formally defined in the public swagger; fields are inferred from the
    CTFd source and kept fully optional.
    """

    id: int
    name: str | None = None
    type: str | None = None
    user_id: int | None = None
    value: str | None = None
    expiration: datetime | None = None
    created: datetime | None = None
