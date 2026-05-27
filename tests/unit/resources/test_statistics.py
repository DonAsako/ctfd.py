from __future__ import annotations

import pytest

from ctfd.client import CTFdClient


@pytest.mark.unit
@pytest.mark.responses(
    {
        'GET /api/v1/statistics/challenges/solves': {'success': True, 'data': {'1': 42, '2': 15}},
        'GET /api/v1/statistics/challenges/solves/percentages': {'success': True, 'data': {'1': 84.0}},
        'GET /api/v1/statistics/challenges/category': {'success': True, 'data': {'web': 5}},
        'GET /api/v1/statistics/progression/matrix': {'success': True, 'data': {}},
        'GET /api/v1/statistics/scores/distribution': {'success': True, 'data': {'bins': []}},
        'GET /api/v1/statistics/submissions/type': {'success': True, 'data': {'correct': 100}},
        'GET /api/v1/statistics/teams': {'success': True, 'data': {'count': 20}},
        'GET /api/v1/statistics/users': {'success': True, 'data': {'count': 50}},
        'GET /api/v1/statistics/users/country': {'success': True, 'data': {'FR': 10}},
    }
)
class TestStatisticsResource:
    async def test_challenge_solves(self, mock_client: CTFdClient) -> None:
        data = await mock_client.statistics.challenge_solves()
        assert data['1'] == 42

    async def test_challenge_solves_percentages(self, mock_client: CTFdClient) -> None:
        data = await mock_client.statistics.challenge_solves_percentages()
        assert isinstance(data, dict)

    async def test_challenges_by_column(self, mock_client: CTFdClient) -> None:
        data = await mock_client.statistics.challenges('category')
        assert data['web'] == 5

    async def test_progression_matrix(self, mock_client: CTFdClient) -> None:
        data = await mock_client.statistics.progression_matrix()
        assert isinstance(data, dict)

    async def test_scores_distribution(self, mock_client: CTFdClient) -> None:
        data = await mock_client.statistics.scores_distribution()
        assert 'bins' in data

    async def test_submissions_by_column(self, mock_client: CTFdClient) -> None:
        data = await mock_client.statistics.submissions('type')
        assert data['correct'] == 100

    async def test_teams(self, mock_client: CTFdClient) -> None:
        data = await mock_client.statistics.teams()
        assert data['count'] == 20

    async def test_users_no_column(self, mock_client: CTFdClient) -> None:
        data = await mock_client.statistics.users()
        assert data['count'] == 50

    async def test_users_with_column(self, mock_client: CTFdClient) -> None:
        data = await mock_client.statistics.users('country')
        assert data['FR'] == 10
