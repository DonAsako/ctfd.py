from __future__ import annotations

from datetime import datetime

import pytest

from ctfd.models import Token


@pytest.mark.unit
class TestToken:
    def test_minimal(self) -> None:
        t = Token(id=1)
        assert t.id == 1

    def test_dates_parsed(self) -> None:
        t = Token.model_validate(
            {
                'id': 1,
                'created': '2024-01-01T00:00:00Z',
                'expiration': '2025-01-01T00:00:00Z',
            }
        )
        assert isinstance(t.created, datetime)
        assert isinstance(t.expiration, datetime)

    def test_value_field(self) -> None:
        t = Token.model_validate({'id': 1, 'value': 'ctfd_abc123'})
        assert t.value == 'ctfd_abc123'
