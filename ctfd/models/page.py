from __future__ import annotations

from ctfd.models._base import CTFdModel


class Page(CTFdModel):
    id: int
    title: str | None = None
    route: str | None = None
    content: str | None = None
    draft: bool | None = None
    hidden: bool | None = None
    auth_required: bool | None = None
    format: str | None = None
    link_target: str | None = None
