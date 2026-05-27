from __future__ import annotations

from ctfd.models import Page
from ctfd.resources._base import _CreateOps, _DeleteOps, _GetOps, _ListOps, _UpdateOps


class PagesResource(_ListOps[Page], _GetOps[Page], _CreateOps[Page], _UpdateOps[Page], _DeleteOps):
    path = '/pages'
    model = Page
