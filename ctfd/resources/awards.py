from __future__ import annotations

from ctfd.models import Award
from ctfd.resources._base import _CreateOps, _DeleteOps, _GetOps, _ListOps


class AwardsResource(_ListOps[Award], _GetOps[Award], _CreateOps[Award], _DeleteOps):
    """``/awards`` — list, retrieve, create, delete (CTFd does not expose PATCH)."""

    path = '/awards'
    model = Award
