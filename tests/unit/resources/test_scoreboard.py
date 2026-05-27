from __future__ import annotations

import pytest

from ctfd.client import CTFdClient
from ctfd.models import ScoreboardEntry

ENTRY = {'pos': 1, 'account_id': 42, 'name': 'team_alpha', 'score': 1500}


@pytest.mark.unit
@pytest.mark.responses(
    {
        'GET /api/v1/scoreboard': {
            'success': True,
            'data': [ENTRY, {**ENTRY, 'pos': 2, 'name': 'team_beta', 'score': 1200}],
        },
        'GET /api/v1/scoreboard/top/3': {
            'success': True,
            'data': {
                '1': ENTRY,
                '2': {**ENTRY, 'pos': 2, 'name': 'team_beta'},
                '3': {**ENTRY, 'pos': 3, 'name': 'team_gamma'},
            },
        },
    }
)
class TestScoreboardResource:
    async def test_list_returns_entries(self, mock_client: CTFdClient) -> None:
        entries = await mock_client.scoreboard.list()
        assert len(entries) == 2
        assert all(isinstance(e, ScoreboardEntry) for e in entries)
        assert entries[0].name == 'team_alpha'

    async def test_top_returns_keyed_dict(self, mock_client: CTFdClient) -> None:
        top = await mock_client.scoreboard.top(3)
        assert set(top.keys()) == {'1', '2', '3'}
        assert isinstance(top['1'], ScoreboardEntry)
        assert top['1'].name == 'team_alpha'

    async def test_top_scores_parsed(self, mock_client: CTFdClient) -> None:
        top = await mock_client.scoreboard.top(3)
        assert top['1'].score == 1500
