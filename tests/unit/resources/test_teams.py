from __future__ import annotations

import pytest

from ctfd.client import CTFdClient
from ctfd.models import Award, Submission, Team

TEAM = {'id': 1, 'name': 'PwnCats', 'email': 'team@example.com'}
SUBMISSION = {'id': 10, 'type': 'correct', 'challenge_id': 5}
AWARD = {'id': 3, 'name': 'Speed', 'value': 25}


@pytest.mark.unit
@pytest.mark.responses(
    {
        'GET /api/v1/teams': {'success': True, 'data': [TEAM]},
        'GET /api/v1/teams/1': {'success': True, 'data': TEAM},
        'POST /api/v1/teams': {'success': True, 'data': TEAM},
        'PATCH /api/v1/teams/1': {'success': True, 'data': {**TEAM, 'affiliation': 'CTF Club'}},
        'DELETE /api/v1/teams/1': {'success': True},
        'GET /api/v1/teams/me': {'success': True, 'data': TEAM},
        'PATCH /api/v1/teams/me': {'success': True, 'data': {**TEAM, 'website': 'https://team.dev'}},
        'DELETE /api/v1/teams/me': {'success': True},
        'GET /api/v1/teams/me/awards': {'success': True, 'data': [AWARD]},
        'GET /api/v1/teams/me/solves': {'success': True, 'data': [SUBMISSION]},
        'GET /api/v1/teams/me/fails': {'success': True, 'data': []},
        'POST /api/v1/teams/me/members': {'success': True, 'data': {}},
        'GET /api/v1/teams/1/awards': {'success': True, 'data': [AWARD]},
        'GET /api/v1/teams/1/solves': {'success': True, 'data': [SUBMISSION]},
        'GET /api/v1/teams/1/fails': {'success': True, 'data': []},
        'GET /api/v1/teams/1/members': {'success': True, 'data': [2, 3, 4]},
        'POST /api/v1/teams/1/members': {'success': True, 'data': {}},
        'DELETE /api/v1/teams/1/members': {'success': True},
    }
)
class TestTeamsResource:
    async def test_list(self, mock_client: CTFdClient) -> None:
        teams = await mock_client.teams.list()
        assert isinstance(teams[0], Team)

    async def test_get(self, mock_client: CTFdClient) -> None:
        team = await mock_client.teams.get(1)
        assert team.name == 'PwnCats'

    async def test_create(self, mock_client: CTFdClient) -> None:
        team = await mock_client.teams.create({'name': 'PwnCats'})
        assert team.id == 1

    async def test_update(self, mock_client: CTFdClient) -> None:
        team = await mock_client.teams.update(1, {'affiliation': 'CTF Club'})
        assert team.affiliation == 'CTF Club'

    async def test_delete(self, mock_client: CTFdClient) -> None:
        await mock_client.teams.delete(1)

    async def test_me(self, mock_client: CTFdClient) -> None:
        me = await mock_client.teams.me()
        assert isinstance(me, Team)

    async def test_update_me(self, mock_client: CTFdClient) -> None:
        me = await mock_client.teams.update_me({'website': 'https://team.dev'})
        assert me.website == 'https://team.dev'

    async def test_delete_me(self, mock_client: CTFdClient) -> None:
        await mock_client.teams.delete_me()

    async def test_my_awards(self, mock_client: CTFdClient) -> None:
        awards = await mock_client.teams.my_awards()
        assert isinstance(awards[0], Award)

    async def test_my_solves(self, mock_client: CTFdClient) -> None:
        solves = await mock_client.teams.my_solves()
        assert isinstance(solves[0], Submission)

    async def test_my_fails(self, mock_client: CTFdClient) -> None:
        fails = await mock_client.teams.my_fails()
        assert fails == []

    async def test_add_my_member(self, mock_client: CTFdClient) -> None:
        result = await mock_client.teams.add_my_member({'user_id': 5})
        assert isinstance(result, dict)

    async def test_awards_by_id(self, mock_client: CTFdClient) -> None:
        awards = await mock_client.teams.awards(1)
        assert isinstance(awards[0], Award)

    async def test_solves_by_id(self, mock_client: CTFdClient) -> None:
        solves = await mock_client.teams.solves(1)
        assert isinstance(solves[0], Submission)

    async def test_members(self, mock_client: CTFdClient) -> None:
        members = await mock_client.teams.members(1)
        assert members == [2, 3, 4]

    async def test_add_member(self, mock_client: CTFdClient) -> None:
        result = await mock_client.teams.add_member(1, 5)
        assert isinstance(result, dict)

    async def test_remove_member(self, mock_client: CTFdClient) -> None:
        await mock_client.teams.remove_member(1, 5)
