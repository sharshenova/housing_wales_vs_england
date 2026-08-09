"""Address normalisation for Price Paid ↔ EPC matching."""

from __future__ import annotations

import re

_SPACE = re.compile(r"\s+")
_NON_ALNUM = re.compile(r"[^A-Z0-9 ]+")


def _is_missing(value: object) -> bool:
    if value is None:
        return True
    try:
        # pandas / numpy NaN
        if value != value:  # noqa: PLR0124
            return True
    except Exception:
        pass
    text = str(value).strip().upper()
    return text in {"", "NAN", "NONE", "<NA>", "NAT", "NULL"}


def normalise_postcode(postcode: str | None) -> str:
    """Uppercase postcode with a single space before the inward code when possible."""
    if _is_missing(postcode):
        return ""
    pc = _SPACE.sub("", str(postcode).upper())
    if len(pc) > 3:
        return f"{pc[:-3]} {pc[-3:]}"
    return pc


def normalise_token(value: str | None) -> str:
    """Uppercase, strip punctuation, collapse whitespace."""
    if _is_missing(value):
        return ""
    text = str(value).upper().strip()
    text = _NON_ALNUM.sub(" ", text)
    return _SPACE.sub(" ", text).strip()


def address_key(
    postcode: str | None,
    paon: str | None,
    saon: str | None = None,
    street: str | None = None,
) -> str:
    """Build a stable join key: postcode|saon|paon|street."""
    parts = [
        normalise_postcode(postcode),
        normalise_token(saon),
        normalise_token(paon),
        normalise_token(street),
    ]
    return "|".join(parts)
