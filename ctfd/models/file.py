from __future__ import annotations

from ctfd.models._base import CTFdModel


class File(CTFdModel):
    id: int
    type: str | None = None
    location: str | None = None
    sha1sum: str | None = None
