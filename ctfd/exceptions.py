from __future__ import annotations

from typing import Any


class CTFdError(Exception):
    """Base exception for every error raised by this client."""


class CTFdAPIError(CTFdError):
    """The CTFd API returned a non-success HTTP response.

    Attributes:
        status_code: HTTP status code returned by the server.
        message: Human-readable error message extracted from the response body.
        errors: Per-field validation errors, when CTFd returns them.
        payload: Raw decoded response body, when available.
    """

    def __init__(
        self,
        status_code: int,
        message: str = '',
        errors: dict[str, Any] | None = None,
        payload: Any = None,
    ) -> None:
        self.status_code = status_code
        self.message = message
        self.errors = errors or {}
        self.payload = payload
        super().__init__(f'CTFd API error {status_code}: {message}' if message else f'CTFd API error {status_code}')


class CTFdAuthenticationError(CTFdAPIError):
    """Returned when the API rejects the credentials (HTTP 401)."""


class CTFdPermissionError(CTFdAPIError):
    """Returned when the API forbids the operation (HTTP 403)."""


class CTFdNotFoundError(CTFdAPIError):
    """Returned when the requested resource does not exist (HTTP 404)."""


class CTFdValidationError(CTFdAPIError):
    """Returned when the API rejects the request body (HTTP 400)."""


class CTFdRateLimitError(CTFdAPIError):
    """Returned when the API rate-limits the client (HTTP 429)."""


class CTFdServerError(CTFdAPIError):
    """Returned for HTTP 5xx responses."""


def error_for_status(
    status_code: int,
    message: str = '',
    errors: dict[str, Any] | None = None,
    payload: Any = None,
) -> CTFdAPIError:
    """Map an HTTP status code to the most specific exception subclass."""

    mapping: dict[int, type[CTFdAPIError]] = {
        400: CTFdValidationError,
        401: CTFdAuthenticationError,
        403: CTFdPermissionError,
        404: CTFdNotFoundError,
        429: CTFdRateLimitError,
    }
    cls = mapping.get(status_code)
    if cls is None:
        cls = CTFdServerError if status_code >= 500 else CTFdAPIError
    return cls(status_code=status_code, message=message, errors=errors, payload=payload)
