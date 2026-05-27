from __future__ import annotations

from ctfd.models import Bracket
from ctfd.resources._base import _CreateOps, _DeleteOps, _ListOps, _UpdateOps


class BracketsResource(_ListOps[Bracket], _CreateOps[Bracket], _UpdateOps[Bracket], _DeleteOps):
    """``/brackets`` — no single-bracket GET endpoint is exposed by CTFd."""

    path = '/brackets'
    model = Bracket
