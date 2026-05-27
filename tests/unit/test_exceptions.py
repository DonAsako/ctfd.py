from __future__ import annotations

import pytest

from ctfd.exceptions import (
    CTFdAPIError,
    CTFdAuthenticationError,
    CTFdNotFoundError,
    CTFdPermissionError,
    CTFdRateLimitError,
    CTFdServerError,
    CTFdValidationError,
    error_for_status,
)


@pytest.mark.unit
class TestErrorForStatus:
    def test_400_returns_validation_error(self) -> None:
        err = error_for_status(400, message='bad input')
        assert isinstance(err, CTFdValidationError)
        assert err.status_code == 400
        assert err.message == 'bad input'

    def test_401_returns_authentication_error(self) -> None:
        assert isinstance(error_for_status(401), CTFdAuthenticationError)

    def test_403_returns_permission_error(self) -> None:
        assert isinstance(error_for_status(403), CTFdPermissionError)

    def test_404_returns_not_found_error(self) -> None:
        assert isinstance(error_for_status(404), CTFdNotFoundError)

    def test_429_returns_rate_limit_error(self) -> None:
        assert isinstance(error_for_status(429), CTFdRateLimitError)

    def test_500_returns_server_error(self) -> None:
        assert isinstance(error_for_status(500), CTFdServerError)

    def test_503_returns_server_error(self) -> None:
        assert isinstance(error_for_status(503), CTFdServerError)

    def test_422_returns_generic_api_error(self) -> None:
        err = error_for_status(422)
        assert type(err) is CTFdAPIError

    def test_errors_dict_preserved(self) -> None:
        err = error_for_status(400, errors={'field': ['required']})
        assert err.errors == {'field': ['required']}

    def test_payload_preserved(self) -> None:
        payload = {'success': False, 'message': 'oops'}
        err = error_for_status(400, payload=payload)
        assert err.payload == payload

    def test_str_includes_status_and_message(self) -> None:
        err = error_for_status(404, message='not found')
        assert '404' in str(err)
        assert 'not found' in str(err)

    def test_str_without_message(self) -> None:
        err = error_for_status(500)
        assert '500' in str(err)

    def test_all_subclasses_are_api_errors(self) -> None:
        for code in (400, 401, 403, 404, 429, 500):
            assert isinstance(error_for_status(code), CTFdAPIError)
