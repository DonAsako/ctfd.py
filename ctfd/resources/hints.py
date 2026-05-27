from __future__ import annotations

from ctfd.models import Hint
from ctfd.resources._base import _CreateOps, _DeleteOps, _GetOps, _ListOps, _UpdateOps


class HintsResource(_ListOps[Hint], _GetOps[Hint], _CreateOps[Hint], _UpdateOps[Hint], _DeleteOps):
    path = '/hints'
    model = Hint
