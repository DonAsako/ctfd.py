from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class CTFdModel(BaseModel):
    """Base model for every CTFd resource.

    The CTFd API regularly adds fields between releases, so unknown keys are
    tolerated rather than rejected.
    """

    model_config = ConfigDict(extra='allow', populate_by_name=True)
