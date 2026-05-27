from __future__ import annotations

from datetime import datetime

import pytest

from ctfd.models import User


@pytest.mark.unit
class TestUser:
    def test_minimal(self) -> None:
        u = User(id=5)
        assert u.id == 5
        assert u.email is None

    def test_created_parsed_as_datetime(self) -> None:
        u = User.model_validate({'id': 1, 'created': '2024-01-15T10:00:00Z'})
        assert isinstance(u.created, datetime)

    def test_boolean_fields(self) -> None:
        u = User.model_validate({'id': 1, 'hidden': True, 'banned': False, 'verified': True})
        assert u.hidden is True
        assert u.banned is False
        assert u.verified is True

    def test_extra_fields_allowed(self) -> None:
        u = User.model_validate({'id': 1, 'score': 500})
        assert u.id == 1
