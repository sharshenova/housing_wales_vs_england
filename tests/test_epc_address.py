from city_value.epc_address import epc_address_key, parse_epc_address


def test_simple_house() -> None:
    saon, paon, street = parse_epc_address("74, Blaise Place", None, None)
    assert saon == ""
    assert paon == "74"
    assert "BLAISE" in street


def test_flat_with_building() -> None:
    saon, paon, street = parse_epc_address("Flat 3", "210 Newport Road", None)
    assert saon == "FLAT 3"
    assert paon == "210"
    assert "NEWPORT" in street


def test_epc_key_matches_ppd_style() -> None:
    pc, saon, paon, street, key = epc_address_key(
        "cf241dn", "Flat 3", "210 Newport Road", None
    )
    assert pc == "CF24 1DN"
    assert key.startswith("CF24 1DN|FLAT 3|210|")
