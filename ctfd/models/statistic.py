from __future__ import annotations

from typing import Any

from ctfd.models._base import CTFdModel


class Statistic(CTFdModel):
    """Generic container for the ``/statistics/*`` endpoints.

    The CTFd statistics endpoints return heterogeneous aggregates (counts per
    category, percentages, time-series matrices, ...). Rather than locking a
    single shape, the payload is exposed as a free-form mapping under ``data``.
    """

    data: dict[str, Any] | list[Any] | None = None
