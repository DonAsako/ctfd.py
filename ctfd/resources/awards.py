from __future__ import annotations

from ctfd.models import Award
from ctfd.resources._base import CRUDResource


class AwardsResource(CRUDResource[Award]):
    path = '/awards'
    model = Award

    async def update(self, resource_id: int | str, body: object) -> Award:
        raise NotImplementedError('The CTFd API does not support updating awards.')
