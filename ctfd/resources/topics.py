from __future__ import annotations

from ctfd.models import Topic
from ctfd.resources._base import _CreateOps, _DeleteOps, _GetOps, _ListOps


class TopicsResource(_ListOps[Topic], _GetOps[Topic], _CreateOps[Topic], _DeleteOps):
    """``/topics`` — list, retrieve, create, delete by id, plus ``unlink`` on the collection."""

    path = '/topics'
    model = Topic

    async def unlink(self, *, target_id: int, type: str) -> None:  # noqa: A002
        """Detach a topic from a target (challenge, page, ...).

        Maps to ``DELETE /topics?type=...&target_id=...``; the topic record
        itself is preserved.
        """

        await self._http.delete_json(self.path, params={'target_id': target_id, 'type': type})
