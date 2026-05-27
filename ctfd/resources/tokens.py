from __future__ import annotations

from ctfd.models import Token
from ctfd.resources._base import CRUDResource


class TokensResource(CRUDResource[Token]):
    path = '/tokens'
    model = Token

    async def update(self, resource_id: int | str, body: object) -> Token:
        raise NotImplementedError('The CTFd API does not support updating tokens.')
