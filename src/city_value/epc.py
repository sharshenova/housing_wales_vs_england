"""Domestic EPC ingest helpers."""

from __future__ import annotations

from typing import Any

# Columns kept for join / £/m² / Project G
EPC_KEEP_COLUMNS: list[str] = [
    "certificate_number",
    "address1",
    "address2",
    "address3",
    "address",
    "postcode",
    "posttown",
    "local_authority",
    "local_authority_label",
    "inspection_date",
    "lodgement_date",
    "total_floor_area",
    "number_habitable_rooms",
    "current_energy_rating",
    "current_energy_efficiency",
    "property_type",
    "built_form",
    "construction_age_band",
    "uprn",
]

# EPC local_authority_label → project city id
EPC_LA_TO_CITY: dict[str, str] = {
    "Swansea": "swansea",
    "Cardiff": "cardiff",
    "Bristol, City of": "bristol",
    "Bath and North East Somerset": "bath",
}


def city_id_from_epc_la(label: str | None, cities_cfg: dict[str, Any] | None = None) -> str | None:
    if label is None:
        return None
    text = str(label).strip()
    if text in EPC_LA_TO_CITY:
        return EPC_LA_TO_CITY[text]
    # optional override from config later
    if cities_cfg:
        for city_id, meta in cities_cfg.get("cities", {}).items():
            for epc_label in meta.get("epc_la_labels", []):
                if str(epc_label).strip() == text:
                    return str(city_id)
    return None
