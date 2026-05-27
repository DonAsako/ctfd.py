from __future__ import annotations

from ctfd.models import Topic
from ctfd.resources._base import CRUDResource


class TopicsResource(CRUDResource[Topic]):
    path = '/topics'
    model = Topic

    async def unlink(self, *, topic_id: int | None = None, challenge_id: int | None = None) -> None:
        """Detach a topic from a challenge.

        The CTFd API exposes deletion on the collection itself via query
        parameters (rather than ``/topics/{id}``) to support unlinking a topic
        from a specific challenge without removing the topic record.
        """

        params = {'topic_id': topic_id, 'challenge_id': challenge_id}
        await self._http.delete_json(self.path, params=params)
