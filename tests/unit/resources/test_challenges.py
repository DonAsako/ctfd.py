from __future__ import annotations

import pytest

from ctfd.client import CTFdClient
from ctfd.models import Challenge, File, Flag, Hint, Solution, Submission, Tag, Topic

CHALLENGE = {'id': 1, 'name': 'Web 101', 'value': 100, 'category': 'web', 'state': 'visible'}
CHALLENGE_2 = {'id': 2, 'name': 'Crypto', 'value': 200}


@pytest.mark.unit
@pytest.mark.responses(
    {
        'GET /api/v1/challenges': {'success': True, 'data': [CHALLENGE, CHALLENGE_2]},
        'GET /api/v1/challenges/1': {'success': True, 'data': CHALLENGE},
        'POST /api/v1/challenges': {'success': True, 'data': CHALLENGE},
        'PATCH /api/v1/challenges/1': {'success': True, 'data': {**CHALLENGE, 'name': 'updated'}},
        'DELETE /api/v1/challenges/1': {'success': True},
        'POST /api/v1/challenges/attempt': {'success': True, 'data': {'status': 'correct', 'message': 'Correct!'}},
        'GET /api/v1/challenges/types': {'success': True, 'data': {'standard': {}, 'dynamic': {}}},
        'GET /api/v1/challenges/1/files': {
            'success': True,
            'data': [{'id': 10, 'type': 'challenge', 'location': 'f.txt'}],
        },
        'GET /api/v1/challenges/1/flags': {
            'success': True,
            'data': [{'id': 5, 'type': 'static', 'content': 'flag{x}'}],
        },
        'GET /api/v1/challenges/1/hints': {'success': True, 'data': [{'id': 3, 'cost': 10}]},
        'GET /api/v1/challenges/1/tags': {'success': True, 'data': [{'id': 7, 'value': 'beginner'}]},
        'GET /api/v1/challenges/1/topics': {'success': True, 'data': [{'id': 9, 'value': 'networking'}]},
        'GET /api/v1/challenges/1/solves': {'success': True, 'data': [{'id': 20, 'type': 'correct'}]},
        'GET /api/v1/challenges/1/solution': {'success': True, 'data': {'id': 1, 'content': 'solution text'}},
        'GET /api/v1/challenges/1/requirements': {'success': True, 'data': {'prerequisites': [2]}},
        'GET /api/v1/challenges/1/ratings': {'success': True, 'data': {'avg': 4.5}},
        'PUT /api/v1/challenges/1/ratings': {'success': True, 'data': {'score': 5}},
    }
)
class TestChallengesResource:
    async def test_list_returns_challenges(self, mock_client: CTFdClient) -> None:
        challenges = await mock_client.challenges.list()
        assert len(challenges) == 2
        assert all(isinstance(c, Challenge) for c in challenges)
        assert challenges[0].name == 'Web 101'

    async def test_get_returns_single(self, mock_client: CTFdClient) -> None:
        ch = await mock_client.challenges.get(1)
        assert isinstance(ch, Challenge)
        assert ch.id == 1
        assert ch.value == 100

    async def test_create_returns_challenge(self, mock_client: CTFdClient) -> None:
        ch = await mock_client.challenges.create({'name': 'Web 101', 'value': 100})
        assert ch.id == 1

    async def test_update_returns_updated(self, mock_client: CTFdClient) -> None:
        ch = await mock_client.challenges.update(1, {'name': 'updated'})
        assert ch.name == 'updated'

    async def test_delete_succeeds(self, mock_client: CTFdClient) -> None:
        await mock_client.challenges.delete(1)

    async def test_attempt_returns_result(self, mock_client: CTFdClient) -> None:
        result = await mock_client.challenges.attempt(1, 'flag{test}')
        assert result['status'] == 'correct'

    async def test_types_returns_dict(self, mock_client: CTFdClient) -> None:
        types = await mock_client.challenges.types()
        assert 'standard' in types

    async def test_files_returns_list(self, mock_client: CTFdClient) -> None:
        files = await mock_client.challenges.files(1)
        assert len(files) == 1
        assert isinstance(files[0], File)

    async def test_flags_returns_list(self, mock_client: CTFdClient) -> None:
        flags = await mock_client.challenges.flags(1)
        assert len(flags) == 1
        assert isinstance(flags[0], Flag)
        assert flags[0].content == 'flag{x}'

    async def test_hints_returns_list(self, mock_client: CTFdClient) -> None:
        hints = await mock_client.challenges.hints(1)
        assert len(hints) == 1
        assert isinstance(hints[0], Hint)

    async def test_tags_returns_list(self, mock_client: CTFdClient) -> None:
        tags = await mock_client.challenges.tags(1)
        assert len(tags) == 1
        assert isinstance(tags[0], Tag)
        assert tags[0].value == 'beginner'

    async def test_topics_returns_list(self, mock_client: CTFdClient) -> None:
        topics = await mock_client.challenges.topics(1)
        assert isinstance(topics[0], Topic)

    async def test_solves_returns_submissions(self, mock_client: CTFdClient) -> None:
        solves = await mock_client.challenges.solves(1)
        assert isinstance(solves[0], Submission)

    async def test_solution_returns_solution(self, mock_client: CTFdClient) -> None:
        sol = await mock_client.challenges.solution(1)
        assert isinstance(sol, Solution)
        assert sol.content == 'solution text'

    async def test_requirements_returns_dict(self, mock_client: CTFdClient) -> None:
        reqs = await mock_client.challenges.requirements(1)
        assert reqs['prerequisites'] == [2]

    async def test_ratings_returns_dict(self, mock_client: CTFdClient) -> None:
        ratings = await mock_client.challenges.ratings(1)
        assert ratings['avg'] == 4.5

    async def test_rate_returns_dict(self, mock_client: CTFdClient) -> None:
        result = await mock_client.challenges.rate(1, {'score': 5})
        assert result['score'] == 5
