"""Temporal Price Paid ↔ EPC address join."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from city_value.address import normalise_token
from city_value.features import enrich_linked


@dataclass(frozen=True)
class JoinParams:
    max_years_before: float = 10.0
    max_years_after: float = 2.0
    min_floor_area_m2: float = 15.0
    max_floor_area_m2: float = 500.0


EPC_COLS = [
    "certificate_number",
    "epc_date",
    "total_floor_area",
    "number_habitable_rooms",
    "current_energy_rating",
    "current_energy_efficiency",
    "built_form",
    "construction_age_band",
    "property_type",
    "uprn",
    "address1",
    "address2",
]


def loose_address_key(postcode_norm: pd.Series, paon: pd.Series, saon: pd.Series) -> pd.Series:
    return (
        postcode_norm.fillna("").astype(str)
        + "|"
        + saon.map(normalise_token)
        + "|"
        + paon.map(normalise_token)
    )


def _prepare_frames(
    ppd: pd.DataFrame, epc: pd.DataFrame, params: JoinParams
) -> tuple[pd.DataFrame, pd.DataFrame]:
    ppd = ppd.copy()
    epc = epc.copy()
    ppd["sale_date"] = pd.to_datetime(ppd["date_of_transfer"], errors="coerce")
    epc["epc_date"] = pd.to_datetime(epc["epc_date"], errors="coerce")
    epc["total_floor_area"] = pd.to_numeric(epc["total_floor_area"], errors="coerce")
    epc = epc[
        epc["total_floor_area"].between(params.min_floor_area_m2, params.max_floor_area_m2)
    ].copy()

    ppd["saon"] = ppd["saon"].map(normalise_token)
    ppd["paon"] = ppd["paon"].map(normalise_token)
    ppd["street"] = ppd["street"].map(normalise_token)
    ppd["postcode_norm"] = ppd["postcode_norm"].fillna("").astype(str)
    epc["saon"] = epc["saon"].map(normalise_token)
    epc["paon"] = epc["paon"].map(normalise_token)
    epc["street"] = epc["street"].map(normalise_token)
    epc["postcode_norm"] = epc["postcode_norm"].fillna("").astype(str)

    ppd["loose_key"] = loose_address_key(ppd["postcode_norm"], ppd["paon"], ppd["saon"])
    epc["loose_key"] = loose_address_key(epc["postcode_norm"], epc["paon"], epc["saon"])
    return ppd, epc


def _pick_temporal(
    merged: pd.DataFrame, params: JoinParams, sale_id_col: str = "transaction_id"
) -> pd.DataFrame:
    """From sale×EPC candidate rows, keep one EPC per sale by temporal rules."""
    if merged.empty:
        return merged

    df = merged.copy()
    df["delta_days"] = (df["epc_date"] - df["sale_date"]).dt.days
    max_before = int(params.max_years_before * 365.25)
    max_after = int(params.max_years_after * 365.25)

    before = df[(df["delta_days"] <= 0) & (df["delta_days"] >= -max_before)].copy()
    after = df[(df["delta_days"] > 0) & (df["delta_days"] <= max_after)].copy()

    picks: list[pd.DataFrame] = []
    if not before.empty:
        before = before.sort_values(
            [sale_id_col, "epc_date", "certificate_number"],
            ascending=[True, False, True],
        )
        picks.append(before.groupby(sale_id_col, as_index=False, sort=False).head(1))

    chosen_ids = set(picks[0][sale_id_col]) if picks else set()
    if not after.empty:
        after = after[~after[sale_id_col].isin(chosen_ids)]
        if not after.empty:
            after = after.sort_values(
                [sale_id_col, "epc_date", "certificate_number"],
                ascending=[True, True, True],
            )
            picks.append(after.groupby(sale_id_col, as_index=False, sort=False).head(1))

    if not picks:
        return df.iloc[0:0].copy()
    return pd.concat(picks, ignore_index=True)


def _attach_epc_fields(picked: pd.DataFrame, tier: str) -> pd.DataFrame:
    out = picked.copy()
    out["join_tier"] = tier
    out["price_per_m2"] = out["price"].astype(float) / out["total_floor_area"].astype(float)
    out = out.rename(
        columns={
            "property_type_epc": "epc_property_type",
            "uprn": "epc_uprn",
            "address1": "epc_address1",
            "address2": "epc_address2",
        }
    )
    return out


def join_ppd_epc(
    ppd: pd.DataFrame,
    epc: pd.DataFrame,
    params: JoinParams,
) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    """Join sales to EPCs: full address_key first, then loose key fallback."""
    ppd, epc = _prepare_frames(ppd, epc, params)

    matchable = ppd[(ppd["postcode_norm"] != "") & (ppd["paon"] != "")].copy()
    epc_ok = epc[(epc["postcode_norm"] != "") & (epc["paon"] != "")].copy()

    epc_keep = ["address_key", "loose_key", *[c for c in EPC_COLS if c in epc_ok.columns]]
    epc_join = epc_ok[epc_keep].rename(columns={"property_type": "property_type_epc"})

    # Tier 1: full address_key
    m_full = matchable.merge(epc_join, on="address_key", how="inner", suffixes=("", "_epc"))
    n_multi_full = int(
        m_full.groupby("transaction_id").size().gt(1).sum()
    ) if not m_full.empty else 0
    pick_full = _pick_temporal(m_full, params)
    linked_full = _attach_epc_fields(pick_full, "full") if not pick_full.empty else pick_full

    matched_ids = set(linked_full["transaction_id"]) if len(linked_full) else set()
    remaining = matchable[~matchable["transaction_id"].isin(matched_ids)].copy()

    # Tier 2: loose key for unmatched
    m_loose = remaining.merge(
        epc_join.drop(columns=["address_key"]),
        on="loose_key",
        how="inner",
        suffixes=("", "_epc"),
    )
    n_multi_loose = int(
        m_loose.groupby("transaction_id").size().gt(1).sum()
    ) if not m_loose.empty else 0
    pick_loose = _pick_temporal(m_loose, params)
    linked_loose = (
        _attach_epc_fields(pick_loose, "loose") if not pick_loose.empty else pick_loose
    )

    linked = pd.concat([linked_full, linked_loose], ignore_index=True)
    if len(linked):
        if "current_energy_efficiency" in linked.columns:
            linked["current_energy_efficiency"] = pd.to_numeric(
                linked["current_energy_efficiency"], errors="coerce"
            )
        linked = enrich_linked(linked)
    final_ids = set(linked["transaction_id"]) if len(linked) else set()
    unmatched = matchable[~matchable["transaction_id"].isin(final_ids)].copy()

    n_sales = len(matchable)
    n_matched = len(linked)
    stats = {
        "ppd_rows_input": int(len(ppd)),
        "ppd_rows_matchable": int(n_sales),
        "ppd_rows_excluded_no_postcode_or_paon": int(len(ppd) - n_sales),
        "epc_rows_after_area_filter": int(len(epc_ok)),
        "matched": int(n_matched),
        "unmatched": int(len(unmatched)),
        "match_rate": round(n_matched / n_sales, 4) if n_sales else 0.0,
        "tier_full": int((linked["join_tier"] == "full").sum()) if n_matched else 0,
        "tier_loose": int((linked["join_tier"] == "loose").sum()) if n_matched else 0,
        "sales_with_multi_epc_candidates_full": n_multi_full,
        "sales_with_multi_epc_candidates_loose": n_multi_loose,
        "price_per_m2_median": float(linked["price_per_m2"].median()) if n_matched else None,
        "price_per_m2_p05": float(linked["price_per_m2"].quantile(0.05)) if n_matched else None,
        "price_per_m2_p95": float(linked["price_per_m2"].quantile(0.95)) if n_matched else None,
    }
    return linked, unmatched, stats
