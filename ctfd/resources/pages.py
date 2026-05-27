from __future__ import annotations

from ctfd.models import Page
from ctfd.resources._base import CRUDResource


class PagesResource(CRUDResource[Page]):
    path = '/pages'
    model = Page
