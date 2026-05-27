from __future__ import annotations

from ctfd.models import Submission
from ctfd.resources._base import _CreateOps, _DeleteOps, _GetOps, _ListOps, _UpdateOps


class SubmissionsResource(
    _ListOps[Submission],
    _GetOps[Submission],
    _CreateOps[Submission],
    _UpdateOps[Submission],
    _DeleteOps,
):
    path = '/submissions'
    model = Submission
