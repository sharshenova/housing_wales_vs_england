from city_value.address import address_key, normalise_postcode, normalise_token


def test_normalise_postcode() -> None:
    assert normalise_postcode("sa1 4dq") == "SA1 4DQ"
    assert normalise_postcode("SA14DQ") == "SA1 4DQ"


def test_address_key_stable() -> None:
    k1 = address_key("CF10 1AA", "10", None, "High Street")
    k2 = address_key("cf101aa", "10", "", "HIGH STREET")
    assert k1 == k2
    assert normalise_token("Flat 2!") == "FLAT 2"
