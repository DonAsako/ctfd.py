from __future__ import annotations

from ctfd.models import Comment
from ctfd.resources._base import CRUDResource


class CommentsResource(CRUDResource[Comment]):
    path = '/comments'
    model = Comment

    async def get(self, resource_id: int | str) -> Comment:
        raise NotImplementedError('The CTFd API does not expose a single-comment endpoint.')

    async def update(self, resource_id: int | str, body: object) -> Comment:
        raise NotImplementedError('The CTFd API does not support updating comments.')
