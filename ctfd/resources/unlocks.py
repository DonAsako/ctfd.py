from __future__ import annotations

from ctfd.models import Unlock
from ctfd.resources._base import _CreateOps, _ListOps


class UnlocksResource(_ListOps[Unlock], _CreateOps[Unlock]):
    """``/unlocks`` — list and create only (no per-id endpoints)."""

    path = '/unlocks'
    model = Unlock
