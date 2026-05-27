from __future__ import annotations

import pytest

from ctfd.models import Challenge


@pytest.mark.unit
class TestChallenge:
    def test_minimal(self) -> None:
        ch = Challenge(id=1)
        assert ch.id == 1
        assert ch.name is None

    def test_full(self) -> None:
        ch = Challenge(
            id=1,
            name='Web 101',
            description='desc',
            value=100,
            category='web',
            type='standard',
            state='visible',
            solves=42,
            solved_by_me=False,
        )
        assert ch.name == 'Web 101'
        assert ch.value == 100
        assert ch.solves == 42

    def test_extra_fields_allowed(self) -> None:
        ch = Challenge.model_validate({'id': 1, 'unknown_field': 'x'})
        assert ch.id == 1

    def test_requirements_as_dict(self) -> None:
        ch = Challenge.model_validate({'id': 1, 'requirements': {'prerequisites': [2, 3]}})
        assert ch.requirements == {'prerequisites': [2, 3]}
