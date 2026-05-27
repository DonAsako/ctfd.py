from __future__ import annotations

from ctfd.models import Bracket
from ctfd.resources._base import CRUDResource


class BracketsResource(CRUDResource[Bracket]):
    path = '/brackets'
    model = Bracket

    async def get(self, resource_id: int | str) -> Bracket:
        raise NotImplementedError('The CTFd API does not expose a single-bracket endpoint.')
