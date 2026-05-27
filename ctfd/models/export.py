from __future__ import annotations

from ctfd.models._base import CTFdModel


class Export(CTFdModel):
    """Metadata about a CTFd export archive.

    The ``/exports/raw`` endpoint streams a ZIP file rather than returning JSON,
    so this model only carries optional metadata that may accompany an export
    request (filename, size, content type).
    """

    filename: str | None = None
    size: int | None = None
    content_type: str | None = None
