from __future__ import annotations

from typing import TYPE_CHECKING, Self

from ctfd._http import DEFAULT_TIMEOUT, DEFAULT_USER_AGENT, AsyncHTTPClient

if TYPE_CHECKING:
    from types import TracebackType

    import httpx
from ctfd.resources import (
    AwardsResource,
    BracketsResource,
    ChallengesResource,
    CommentsResource,
    ConfigsResource,
    ExportsResource,
    FilesResource,
    FlagsResource,
    HintsResource,
    NotificationsResource,
    PagesResource,
    ScoreboardResource,
    SharesResource,
    SolutionsResource,
    StatisticsResource,
    SubmissionsResource,
    TagsResource,
    TeamsResource,
    TokensResource,
    TopicsResource,
    UnlocksResource,
    UsersResource,
)


class CTFdClient:
    """Async client for a CTFd instance.

    Usage::

        async with CTFdClient('https://demo.ctfd.io', token='ctfd_...') as ctfd:
            me = await ctfd.users.me()
            async for challenge in ctfd.challenges.iter():
                print(challenge.name)
    """

    def __init__(  # noqa: PLR0913
        self,
        base_url: str,
        token: str | None = None,
        *,
        timeout: float = DEFAULT_TIMEOUT,
        user_agent: str = DEFAULT_USER_AGENT,
        verify: bool = True,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        self._http = AsyncHTTPClient(
            base_url=base_url,
            token=token,
            timeout=timeout,
            user_agent=user_agent,
            verify=verify,
            client=client,
        )

        self.awards = AwardsResource(self._http)
        self.brackets = BracketsResource(self._http)
        self.challenges = ChallengesResource(self._http)
        self.comments = CommentsResource(self._http)
        self.configs = ConfigsResource(self._http)
        self.exports = ExportsResource(self._http)
        self.files = FilesResource(self._http)
        self.flags = FlagsResource(self._http)
        self.hints = HintsResource(self._http)
        self.notifications = NotificationsResource(self._http)
        self.pages = PagesResource(self._http)
        self.scoreboard = ScoreboardResource(self._http)
        self.shares = SharesResource(self._http)
        self.solutions = SolutionsResource(self._http)
        self.statistics = StatisticsResource(self._http)
        self.submissions = SubmissionsResource(self._http)
        self.tags = TagsResource(self._http)
        self.teams = TeamsResource(self._http)
        self.tokens = TokensResource(self._http)
        self.topics = TopicsResource(self._http)
        self.unlocks = UnlocksResource(self._http)
        self.users = UsersResource(self._http)

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        await self.aclose()

    async def aclose(self) -> None:
        await self._http.aclose()
