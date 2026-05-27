from __future__ import annotations

from datetime import datetime

import pytest

from ctfd.models import Submission


@pytest.mark.unit
class TestSubmission:
    def test_minimal(self) -> None:
        s = Submission(id=1)
        assert s.id == 1

    def test_type_values(self) -> None:
        for typ in ('correct', 'incorrect', 'unknown'):
            s = Submission.model_validate({'id': 1, 'type': typ})
            assert s.type == typ

    def test_date_parsed(self) -> None:
        s = Submission.model_validate({'id': 1, 'date': '2024-01-01T12:00:00Z'})
        assert isinstance(s.date, datetime)
