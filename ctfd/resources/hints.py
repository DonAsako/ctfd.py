from __future__ import annotations

from ctfd.models import Hint
from ctfd.resources._base import CRUDResource


class HintsResource(CRUDResource[Hint]):
    path = '/hints'
    model = Hint
