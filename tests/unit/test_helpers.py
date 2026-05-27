from __future__ import annotations

import pytest
from pydantic import BaseModel

from ctfd._http import _clean_params
from ctfd.resources._base import _data, _data_list, _serialize


@pytest.mark.unit
class TestCleanParams:
    def test_none_returns_none(self) -> None:
        assert _clean_params(None) is None

    def test_empty_dict_returns_none(self) -> None:
        assert _clean_params({}) is None

    def test_strips_none_values(self) -> None:
        assert _clean_params({'a': 1, 'b': None, 'c': 'x'}) == {'a': 1, 'c': 'x'}

    def test_keeps_falsy_non_none(self) -> None:
        assert _clean_params({'a': 0, 'b': '', 'c': False}) == {'a': 0, 'b': '', 'c': False}


@pytest.mark.unit
class TestData:
    def test_unwraps_data_envelope(self) -> None:
        assert _data({'success': True, 'data': {'id': 1}}) == {'id': 1}

    def test_returns_payload_without_data_key(self) -> None:
        assert _data({'count': 5}) == {'count': 5}

    def test_non_dict_passthrough(self) -> None:
        assert _data([1, 2, 3]) == [1, 2, 3]

    def test_none_passthrough(self) -> None:
        assert _data(None) is None

    def test_data_key_with_null_value(self) -> None:
        assert _data({'success': True, 'data': None}) is None


@pytest.mark.unit
class TestDataList:
    def test_list_inside_data(self) -> None:
        assert _data_list({'data': [{'id': 1}, {'id': 2}]}) == [{'id': 1}, {'id': 2}]

    def test_non_list_data_returns_empty(self) -> None:
        assert _data_list({'data': {'id': 1}}) == []

    def test_missing_data_returns_empty(self) -> None:
        assert _data_list({}) == []

    def test_none_payload_returns_empty(self) -> None:
        assert _data_list(None) == []


@pytest.mark.unit
class TestSerialize:
    def test_dict_passthrough(self) -> None:
        body = {'name': 'Alice', 'value': 100}
        assert _serialize(body) is body

    def test_basemodel_dumped(self) -> None:
        class Body(BaseModel):
            name: str
            value: int

        result = _serialize(Body(name='Alice', value=100))
        assert result == {'name': 'Alice', 'value': 100}

    def test_basemodel_excludes_none(self) -> None:
        class Body(BaseModel):
            name: str
            note: str | None = None

        result = _serialize(Body(name='Alice'))
        assert result == {'name': 'Alice'}
