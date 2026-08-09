import pandas as pd

from city_value.join_ppd_epc import JoinParams, join_ppd_epc


def test_prefers_epc_before_sale() -> None:
    ppd = pd.DataFrame(
        [
            {
                "transaction_id": "t1",
                "price": 200_000,
                "date_of_transfer": "2020-06-01",
                "postcode": "CF10 1AA",
                "postcode_norm": "CF10 1AA",
                "paon": "10",
                "saon": "",
                "street": "HIGH STREET",
                "address_key": "CF10 1AA||10|HIGH STREET",
                "property_type": "T",
                "city": "cardiff",
                "sale_year": 2020,
            }
        ]
    )
    epc = pd.DataFrame(
        [
            {
                "certificate_number": "old",
                "epc_date": "2018-01-01",
                "total_floor_area": 80,
                "number_habitable_rooms": 4,
                "current_energy_rating": "D",
                "current_energy_efficiency": 55,
                "built_form": "Mid-Terrace",
                "construction_age_band": "1900-1929",
                "property_type": "House",
                "uprn": "1",
                "address1": "10 High Street",
                "address2": None,
                "postcode_norm": "CF10 1AA",
                "paon": "10",
                "saon": "",
                "street": "HIGH STREET",
                "address_key": "CF10 1AA||10|HIGH STREET",
            },
            {
                "certificate_number": "new",
                "epc_date": "2019-05-01",
                "total_floor_area": 82,
                "number_habitable_rooms": 4,
                "current_energy_rating": "C",
                "current_energy_efficiency": 72,
                "built_form": "Mid-Terrace",
                "construction_age_band": "1900-1929",
                "property_type": "House",
                "uprn": "1",
                "address1": "10 High Street",
                "address2": None,
                "postcode_norm": "CF10 1AA",
                "paon": "10",
                "saon": "",
                "street": "HIGH STREET",
                "address_key": "CF10 1AA||10|HIGH STREET",
            },
        ]
    )
    linked, unmatched, stats = join_ppd_epc(ppd, epc, JoinParams())
    assert stats["matched"] == 1
    assert linked.iloc[0]["certificate_number"] == "new"
    assert abs(linked.iloc[0]["price_per_m2"] - 200_000 / 82) < 1e-6
    assert linked.iloc[0]["built_form"] == "Mid-Terrace"
    assert linked.iloc[0]["current_energy_efficiency"] == 72
    assert linked.iloc[0]["property_type_label"] == "Terraced"
    assert linked.iloc[0]["floor_area_band"] == "70-100"
    assert len(unmatched) == 0
