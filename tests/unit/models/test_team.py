from __future__ import annotations

from datetime import datetime

import pytest

from ctfd.models import Team


@pytest.mark.unit
class TestTeam:
    def test_minimal(self) -> None:
        t = Team(id=1)
        assert t.id == 1

    def test_created_as_datetime(self) -> None:
        t = Team.model_validate({'id': 1, 'created': '2024-06-01T00:00:00Z'})
        assert isinstance(t.created, datetime)

    def test_flags(self) -> None:
        t = Team.model_validate({'id': 1, 'hidden': False, 'banned': False})
        assert t.hidden is False
        assert t.banned is False
