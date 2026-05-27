from __future__ import annotations

from ctfd.models import Solution
from ctfd.resources._base import _CreateOps, _DeleteOps, _GetOps, _ListOps, _UpdateOps


class SolutionsResource(
    _ListOps[Solution],
    _GetOps[Solution],
    _CreateOps[Solution],
    _UpdateOps[Solution],
    _DeleteOps,
):
    path = '/solutions'
    model = Solution
