from __future__ import annotations

from ctfd.models import Solution
from ctfd.resources._base import CRUDResource


class SolutionsResource(CRUDResource[Solution]):
    path = '/solutions'
    model = Solution
