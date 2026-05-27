from __future__ import annotations

from ctfd.models import Submission
from ctfd.resources._base import CRUDResource


class SubmissionsResource(CRUDResource[Submission]):
    path = '/submissions'
    model = Submission
