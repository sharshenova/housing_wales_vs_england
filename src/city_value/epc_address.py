"""Parse EPC address fields into PAON / SAON / street for PPD-compatible keys."""

from __future__ import annotations

import re

from city_value.address import address_key, normalise_postcode, normalise_token

_FLAT = re.compile(
    r"^(FLAT|APARTMENT|APT|UNIT|ROOM|STUDIO)\s+([A-Z0-9\-]+)\b[,]?\s*(.*)$",
    re.IGNORECASE,
)
_LEADING_PAON = re.compile(
    r"^([0-9]+[A-Z]?|[A-Z]?[0-9]+[A-Z]?)\s*[,.]?\s+(.*)$",
    re.IGNORECASE,
)


def _clean(value: str | None) -> str:
    if value is None:
        return ""
    text = str(value).strip()
    if text.lower() in {"nan", "none", "<na>"}:
        return ""
    return text


def parse_epc_address(
    address1: str | None,
    address2: str | None = None,
    address3: str | None = None,
) -> tuple[str, str, str]:
    """Return (saon, paon, street) best-effort from EPC address lines."""
    a1 = _clean(address1)
    a2 = _clean(address2)
    a3 = _clean(address3)

    # Flat / apartment in address1; building number+street often in address2
    m_flat = _FLAT.match(a1)
    if m_flat:
        saon = normalise_token(f"{m_flat.group(1)} {m_flat.group(2)}")
        rest = _clean(m_flat.group(3))
        building = rest or a2
        saon2, paon, street = _parse_number_street(building)
        if not street and a2 and not rest:
            # address2 may be only a building name; try address3 as street-ish
            if a3 and not paon:
                _, paon3, street3 = _parse_number_street(a3)
                paon = paon or paon3
                street = street or street3 or normalise_token(a3)
            elif a2:
                street = street or normalise_token(a2)
        elif not street and a2:
            street = normalise_token(a2)
        return saon, paon, street

    # Bare house number in address1, street in address2
    if re.fullmatch(r"[0-9]+[A-Z]?", a1, flags=re.IGNORECASE) and a2:
        return "", normalise_token(a1), normalise_token(a2)

    saon, paon, street = _parse_number_street(a1)
    if not street and a2:
        street = normalise_token(a2)
    return saon, paon, street


def _parse_number_street(text: str) -> tuple[str, str, str]:
    text = _clean(text)
    if not text:
        return "", "", ""
    m = _LEADING_PAON.match(text)
    if m:
        return "", normalise_token(m.group(1)), normalise_token(m.group(2))
    return "", "", normalise_token(text)


def epc_address_key(
    postcode: str | None,
    address1: str | None,
    address2: str | None = None,
    address3: str | None = None,
) -> tuple[str, str, str, str, str]:
    """Return postcode_norm, saon, paon, street, address_key."""
    saon, paon, street = parse_epc_address(address1, address2, address3)
    pc = normalise_postcode(postcode)
    key = address_key(pc, paon, saon, street)
    return pc, saon, paon, street, key
