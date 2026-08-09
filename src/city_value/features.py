"""Derived analysis columns for the linked PPD–EPC table."""

from __future__ import annotations

import pandas as pd

PROPERTY_TYPE_LABELS: dict[str, str] = {
    "D": "Detached",
    "S": "Semi-detached",
    "T": "Terraced",
    "F": "Flat/Maisonette",
    "O": "Other",
}


def postcode_district(postcode_norm: pd.Series) -> pd.Series:
    """Outward postcode code, e.g. CF10 from CF10 1AA."""
    pc = postcode_norm.fillna("").astype(str).str.upper().str.strip()
    return pc.map(lambda x: x.split(" ")[0] if x else "")


def floor_area_band(area: pd.Series) -> pd.Series:
    bins = [0, 50, 70, 100, 150, float("inf")]
    labels = ["<50", "50-70", "70-100", "100-150", "150+"]
    return pd.cut(area, bins=bins, labels=labels, right=False)


def habitable_rooms_band(rooms: pd.Series) -> pd.Series:
    out = pd.Series(index=rooms.index, dtype="object")
    r = pd.to_numeric(rooms, errors="coerce")
    out[r.isna()] = "Unknown"
    out[r <= 2] = "1-2"
    out[r == 3] = "3"
    out[r == 4] = "4"
    out[r == 5] = "5"
    out[r >= 6] = "6+"
    return out


def sale_quarter(sale_date: pd.Series) -> pd.Series:
    dt = pd.to_datetime(sale_date, errors="coerce")
    q = dt.dt.quarter
    y = dt.dt.year
    return y.astype("Int64").astype(str) + "Q" + q.astype("Int64").astype(str)


def enrich_linked(df: pd.DataFrame) -> pd.DataFrame:
    """Add derived columns used by Project F (Tableau) and Project G (modelling)."""
    out = df.copy()

    if "postcode_norm" in out.columns:
        out["postcode_district"] = postcode_district(out["postcode_norm"])
    elif "postcode" in out.columns:
        from city_value.address import normalise_postcode

        out["postcode_district"] = postcode_district(
            out["postcode"].map(normalise_postcode)
        )

    if "old_new" in out.columns:
        out["is_new_build"] = out["old_new"].astype(str).str.upper().eq("Y")
    if "duration" in out.columns:
        out["is_leasehold"] = out["duration"].astype(str).str.upper().eq("L")
    if "property_type" in out.columns:
        out["property_type_label"] = (
            out["property_type"].astype(str).str.upper().map(PROPERTY_TYPE_LABELS)
        )

    if "total_floor_area" in out.columns:
        out["floor_area_band"] = floor_area_band(
            pd.to_numeric(out["total_floor_area"], errors="coerce")
        ).astype("string")
    if "number_habitable_rooms" in out.columns:
        out["habitable_rooms_band"] = habitable_rooms_band(out["number_habitable_rooms"])

    sale_src = out["sale_date"] if "sale_date" in out.columns else out.get("date_of_transfer")
    if sale_src is not None:
        out["sale_quarter"] = sale_quarter(sale_src)

    if "delta_days" in out.columns:
        # Positive when EPC lodged before sale (usual case)
        delta = pd.to_numeric(out["delta_days"], errors="coerce")
        out["epc_years_before_sale"] = (-delta / 365.25).round(2)

    return out
