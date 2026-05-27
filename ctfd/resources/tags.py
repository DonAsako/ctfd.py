from __future__ import annotations

from ctfd.models import Tag
from ctfd.resources._base import _CreateOps, _DeleteOps, _GetOps, _ListOps, _UpdateOps


class TagsResource(_ListOps[Tag], _GetOps[Tag], _CreateOps[Tag], _UpdateOps[Tag], _DeleteOps):
    path = '/tags'
    model = Tag
