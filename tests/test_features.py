import pandas as pd

from city_value.features import enrich_linked, floor_area_band, postcode_district


def test_postcode_district() -> None:
    s = pd.Series(["CF10 1AA", "SA1 4DQ", ""])
    assert postcode_district(s).tolist() == ["CF10", "SA1", ""]


def test_floor_area_band() -> None:
    s = pd.Series([40, 60, 80, 120, 200])
    assert list(floor_area_band(s).astype(str)) == [
        "<50",
        "50-70",
        "70-100",
        "100-150",
        "150+",
    ]


def test_enrich_linked_flags() -> None:
    df = pd.DataFrame(
        [
            {
                "postcode_norm": "BS1 4DJ",
                "old_new": "Y",
                "duration": "L",
                "property_type": "F",
                "total_floor_area": 55,
                "number_habitable_rooms": 2,
                "sale_date": "2020-03-15",
                "delta_days": -400,
            }
        ]
    )
    out = enrich_linked(df)
    assert out.loc[0, "postcode_district"] == "BS1"
    assert bool(out.loc[0, "is_new_build"]) is True
    assert bool(out.loc[0, "is_leasehold"]) is True
    assert out.loc[0, "property_type_label"] == "Flat/Maisonette"
    assert out.loc[0, "floor_area_band"] == "50-70"
    assert out.loc[0, "habitable_rooms_band"] == "1-2"
    assert out.loc[0, "sale_quarter"] == "2020Q1"
    assert out.loc[0, "epc_years_before_sale"] == round(400 / 365.25, 2)
