from __future__ import annotations

from ctfd.models import Share
from ctfd.resources._base import _CreateOps


class SharesResource(_CreateOps[Share]):
    """``/shares`` — creation only."""

    path = '/shares'
    model = Share
