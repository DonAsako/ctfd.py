from __future__ import annotations

from ctfd.models import Tag
from ctfd.resources._base import CRUDResource


class TagsResource(CRUDResource[Tag]):
    path = '/tags'
    model = Tag
