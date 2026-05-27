from __future__ import annotations

from ctfd.models import Comment
from ctfd.resources._base import _CreateOps, _DeleteOps, _ListOps


class CommentsResource(_ListOps[Comment], _CreateOps[Comment], _DeleteOps):
    """``/comments`` — collection list/create + per-id delete. CTFd exposes no GET-by-id or PATCH."""

    path = '/comments'
    model = Comment
