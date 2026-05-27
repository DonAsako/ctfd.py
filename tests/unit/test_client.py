from __future__ import annotations

import pytest

from ctfd.client import CTFdClient
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


@pytest.mark.unit
class TestCTFdClientAttributes:
    def test_all_resource_attributes_exist(self) -> None:
        client = CTFdClient('http://ctfd.test')
        assert isinstance(client.awards, AwardsResource)
        assert isinstance(client.brackets, BracketsResource)
        assert isinstance(client.challenges, ChallengesResource)
        assert isinstance(client.comments, CommentsResource)
        assert isinstance(client.configs, ConfigsResource)
        assert isinstance(client.exports, ExportsResource)
        assert isinstance(client.files, FilesResource)
        assert isinstance(client.flags, FlagsResource)
        assert isinstance(client.hints, HintsResource)
        assert isinstance(client.notifications, NotificationsResource)
        assert isinstance(client.pages, PagesResource)
        assert isinstance(client.scoreboard, ScoreboardResource)
        assert isinstance(client.shares, SharesResource)
        assert isinstance(client.solutions, SolutionsResource)
        assert isinstance(client.statistics, StatisticsResource)
        assert isinstance(client.submissions, SubmissionsResource)
        assert isinstance(client.tags, TagsResource)
        assert isinstance(client.teams, TeamsResource)
        assert isinstance(client.tokens, TokensResource)
        assert isinstance(client.topics, TopicsResource)
        assert isinstance(client.unlocks, UnlocksResource)
        assert isinstance(client.users, UsersResource)

    async def test_context_manager_closes_cleanly(self) -> None:
        async with CTFdClient('http://ctfd.test') as client:
            assert client is not None

    async def test_aclose_is_idempotent(self) -> None:
        client = CTFdClient('http://ctfd.test')
        await client.aclose()
        await client.aclose()
