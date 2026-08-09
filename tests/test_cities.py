from city_value.cities import district_to_city_map
from city_value.config import load_yaml


def test_district_map_covers_four_cities() -> None:
    mapping = district_to_city_map(load_yaml("cities"))
    assert mapping["SWANSEA"] == "swansea"
    assert mapping["CARDIFF"] == "cardiff"
    assert mapping["CITY OF BRISTOL"] == "bristol"
    assert mapping["BATH AND NORTH EAST SOMERSET"] == "bath"
