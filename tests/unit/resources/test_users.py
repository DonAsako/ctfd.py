from __future__ import annotations

import pytest

from ctfd.client import CTFdClient
from ctfd.models import Award, Submission, User

USER = {'id': 1, 'name': 'Alice', 'email': 'alice@example.com', 'type': 'user'}
SUBMISSION = {'id': 10, 'type': 'correct', 'challenge_id': 5}
AWARD = {'id': 3, 'name': 'First Blood', 'value': 50}


@pytest.mark.unit
@pytest.mark.responses(
    {
        'GET /api/v1/users': {'success': True, 'data': [USER]},
        'GET /api/v1/users/1': {'success': True, 'data': USER},
        'POST /api/v1/users': {'success': True, 'data': USER},
        'PATCH /api/v1/users/1': {'success': True, 'data': {**USER, 'name': 'Bob'}},
        'DELETE /api/v1/users/1': {'success': True},
        'GET /api/v1/users/me': {'success': True, 'data': USER},
        'PATCH /api/v1/users/me': {'success': True, 'data': {**USER, 'website': 'https://alice.dev'}},
        'GET /api/v1/users/me/awards': {'success': True, 'data': [AWARD]},
        'GET /api/v1/users/me/solves': {'success': True, 'data': [SUBMISSION]},
        'GET /api/v1/users/me/fails': {'success': True, 'data': []},
        'GET /api/v1/users/me/submissions': {'success': True, 'data': [SUBMISSION]},
        'GET /api/v1/users/1/awards': {'success': True, 'data': [AWARD]},
        'GET /api/v1/users/1/solves': {'success': True, 'data': [SUBMISSION]},
        'GET /api/v1/users/1/fails': {'success': True, 'data': []},
        'POST /api/v1/users/1/email': {'success': True},
    }
)
class TestUsersResource:
    async def test_list(self, mock_client: CTFdClient) -> None:
        users = await mock_client.users.list()
        assert len(users) == 1
        assert isinstance(users[0], User)

    async def test_get(self, mock_client: CTFdClient) -> None:
        user = await mock_client.users.get(1)
        assert user.name == 'Alice'

    async def test_create(self, mock_client: CTFdClient) -> None:
        user = await mock_client.users.create({'name': 'Alice', 'email': 'alice@example.com'})
        assert user.id == 1

    async def test_update(self, mock_client: CTFdClient) -> None:
        user = await mock_client.users.update(1, {'name': 'Bob'})
        assert user.name == 'Bob'

    async def test_delete(self, mock_client: CTFdClient) -> None:
        await mock_client.users.delete(1)

    async def test_me(self, mock_client: CTFdClient) -> None:
        me = await mock_client.users.me()
        assert isinstance(me, User)
        assert me.name == 'Alice'

    async def test_update_me(self, mock_client: CTFdClient) -> None:
        me = await mock_client.users.update_me({'website': 'https://alice.dev'})
        assert me.website == 'https://alice.dev'

    async def test_my_awards(self, mock_client: CTFdClient) -> None:
        awards = await mock_client.users.my_awards()
        assert isinstance(awards[0], Award)

    async def test_my_solves(self, mock_client: CTFdClient) -> None:
        solves = await mock_client.users.my_solves()
        assert isinstance(solves[0], Submission)

    async def test_my_fails_empty(self, mock_client: CTFdClient) -> None:
        fails = await mock_client.users.my_fails()
        assert fails == []

    async def test_my_submissions(self, mock_client: CTFdClient) -> None:
        subs = await mock_client.users.my_submissions()
        assert len(subs) == 1

    async def test_awards_by_id(self, mock_client: CTFdClient) -> None:
        awards = await mock_client.users.awards(1)
        assert isinstance(awards[0], Award)

    async def test_solves_by_id(self, mock_client: CTFdClient) -> None:
        solves = await mock_client.users.solves(1)
        assert isinstance(solves[0], Submission)

    async def test_fails_by_id(self, mock_client: CTFdClient) -> None:
        fails = await mock_client.users.fails(1)
        assert fails == []

    async def test_email(self, mock_client: CTFdClient) -> None:
        result = await mock_client.users.email(1, {'text': 'Hello'})
        assert isinstance(result, dict)
