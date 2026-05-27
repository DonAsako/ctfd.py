from __future__ import annotations

import pytest

from ctfd.models import ScoreboardEntry


@pytest.mark.unit
class TestScoreboardEntry:
    def test_minimal(self) -> None:
        e = ScoreboardEntry()
        assert e.pos is None

    def test_full(self) -> None:
        e = ScoreboardEntry.model_validate(
            {
                'pos': 1,
                'account_id': 42,
                'name': 'team_alpha',
                'score': 1500,
                'bracket_id': 2,
                'bracket_name': 'students',
            }
        )
        assert e.pos == 1
        assert e.score == 1500
        assert e.bracket_name == 'students'

    def test_members_list(self) -> None:
        e = ScoreboardEntry.model_validate({'members': [{'id': 1}, {'id': 2}]})
        assert e.members is not None
        assert len(e.members) == 2
