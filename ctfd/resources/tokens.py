from __future__ import annotations

from ctfd.models import Token
from ctfd.resources._base import _CreateOps, _DeleteOps, _GetOps, _ListOps


class TokensResource(_ListOps[Token], _GetOps[Token], _CreateOps[Token], _DeleteOps):
    """``/tokens`` — list, retrieve, create, delete (no PATCH on tokens)."""

    path = '/tokens'
    model = Token
