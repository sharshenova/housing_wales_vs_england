"""Map Price Paid district names to project city ids."""

from __future__ import annotations

from typing import Any


def district_to_city_map(cities_cfg: dict[str, Any]) -> dict[str, str]:
    """Return UPPER(district) → city_id from configs/cities.yaml."""
    mapping: dict[str, str] = {}
    for city_id, meta in cities_cfg["cities"].items():
        for district in meta.get("districts", []):
            mapping[str(district).upper().strip()] = city_id
    return mapping


def city_label(cities_cfg: dict[str, Any], city_id: str) -> str:
    return str(cities_cfg["cities"][city_id]["label"])
