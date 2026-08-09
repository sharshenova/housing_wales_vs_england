#!/usr/bin/env python3
"""Join PPD sales to EPC certificates (temporal address match).

Usage:
  python scripts/join_ppd_epc.py
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
import yaml

from city_value.address import address_key
from city_value.config import load_yaml
from city_value.join_ppd_epc import JoinParams, join_ppd_epc
from city_value.paths import project_path


def _rebuild_address_keys(df: pd.DataFrame) -> pd.DataFrame:
    """Ensure address_key uses current normalise rules (NaN → empty)."""
    out = df.copy()
    out["address_key"] = [
        address_key(pc, paon, saon, street)
        for pc, paon, saon, street in zip(
            out["postcode"], out["paon"], out["saon"], out["street"], strict=True
        )
    ]
    return out


def _match_rate_table(linked: pd.DataFrame, base: pd.DataFrame, keys: list[str]) -> pd.DataFrame:
    denom = base.groupby(keys, dropna=False).size().rename("sales")
    num = linked.groupby(keys, dropna=False).size().rename("matched")
    out = pd.concat([denom, num], axis=1).fillna(0)
    out["matched"] = out["matched"].astype(int)
    out["sales"] = out["sales"].astype(int)
    out["match_rate"] = (out["matched"] / out["sales"]).round(4)
    return out.reset_index().sort_values(keys)


def write_report(
    stats: dict,
    by_city: pd.DataFrame,
    by_year: pd.DataFrame,
    by_city_year: pd.DataFrame,
    linked: pd.DataFrame,
    unmatched: pd.DataFrame,
    report_path: Path,
    min_match_rate_warn: float,
) -> None:
    lines = [
        (
            f"# PPD ↔ EPC join report "
            f"({int(by_year['sale_year'].min()) if len(by_year) else '?'}–"
            f"{int(by_year['sale_year'].max()) if len(by_year) else '?'})"
        ),
        "",
        f"**Linked output:** `{stats['linked_path']}`",
        f"**Unmatched output:** `{stats['unmatched_path']}`",
        "",
        "## Overall",
        "",
        "| Metric | Value |",
        "|--------|------:|",
        f"| PPD input rows | {stats['ppd_rows_input']:,} |",
        f"| PPD matchable (postcode+PAON) | {stats['ppd_rows_matchable']:,} |",
        f"| Excluded (no postcode/PAON) | {stats['ppd_rows_excluded_no_postcode_or_paon']:,} |",
        f"| EPC rows (area filter applied) | {stats['epc_rows_after_area_filter']:,} |",
        f"| **Matched** | **{stats['matched']:,}** |",
        f"| Unmatched | {stats['unmatched']:,} |",
        f"| **Match rate** | **{100 * stats['match_rate']:.2f}%** |",
        f"| Tier full (address_key) | {stats['tier_full']:,} |",
        f"| Tier loose (postcode\|saon\|paon) | {stats['tier_loose']:,} |",
        f"| £/m² p05 / median / p95 | "
        f"{stats['price_per_m2_p05']:,.0f} / {stats['price_per_m2_median']:,.0f} / "
        f"{stats['price_per_m2_p95']:,.0f} |",
        "",
        f"Threshold (`min_match_rate_warn`): **{100 * min_match_rate_warn:.0f}%**",
        "",
        "## Match rate by city",
        "",
        "| City | Sales | Matched | Match rate |",
        "|------|------:|--------:|-----------:|",
    ]
    for _, r in by_city.iterrows():
        lines.append(
            f"| {r['city']} | {r['sales']:,} | {r['matched']:,} | {100 * r['match_rate']:.1f}% |"
        )

    lines += [
        "",
        "## Match rate by year",
        "",
        "| Year | Sales | Matched | Match rate |",
        "|-----:|------:|--------:|-----------:|",
    ]
    for _, r in by_year.iterrows():
        lines.append(
            f"| {int(r['sale_year'])} | {r['sales']:,} | {r['matched']:,} | "
            f"{100 * r['match_rate']:.1f}% |"
        )

    lines += [
        "",
        "## £/m² median by city (matched)",
        "",
        "| City | Median £/m² | n |",
        "|------|------------:|--:|",
    ]
    if len(linked):
        med = (
            linked.groupby("city")["price_per_m2"]
            .agg(["median", "count"])
            .reset_index()
            .sort_values("city")
        )
        for _, r in med.iterrows():
            lines.append(f"| {r['city']} | £{r['median']:,.0f} | {int(r['count']):,} |")

    lines += [
        "",
        "## Spot checks",
        "",
        "### Sample matched rows (random 8)",
        "",
    ]
    if len(linked):
        sample = linked.sample(n=min(8, len(linked)), random_state=42)
        lines.append("| city | sale_date | price | m² | £/m² | tier | ppd street | epc address1 |")
        lines.append("|---|---|---:|---:|---:|---|---|---|")
        for _, r in sample.iterrows():
            lines.append(
                f"| {r.get('city', '')} | {str(r.get('sale_date', ''))[:10]} | "
                f"£{float(r['price']):,.0f} | {float(r['total_floor_area']):.0f} | "
                f"£{float(r['price_per_m2']):,.0f} | {r.get('join_tier', '')} | "
                f"{r.get('street', '')} | {r.get('epc_address1', '')} |"
            )

    lines += [
        "",
        "### Sample unmatched (random 10)",
        "",
        "| city | sale_date | postcode | paon | street | property_type |",
        "|---|---|---|---|---|---|",
    ]
    if len(unmatched):
        us = unmatched.sample(n=min(10, len(unmatched)), random_state=42)
        for _, r in us.iterrows():
            lines.append(
                f"| {r.get('city', '')} | {str(r.get('date_of_transfer', ''))[:10]} | "
                f"{r.get('postcode_norm', '')} | {r.get('paon', '')} | "
                f"{r.get('street', '')} | {r.get('property_type', '')} |"
            )

    passed = stats["match_rate"] >= min_match_rate_warn
    lines += [
        "",
        "## Verdict",
        "",
    ]
    if passed:
        lines.append(
            f"**Accept (provisional)** — overall match rate "
            f"{100 * stats['match_rate']:.1f}% ≥ {100 * min_match_rate_warn:.0f}%."
        )
        lines.append("Review spot checks above; then mark join accepted in `docs/PROGRESS.md`.")
    else:
        lines.append(
            f"**Below threshold** — overall match rate "
            f"{100 * stats['match_rate']:.1f}% < {100 * min_match_rate_warn:.0f}%."
        )
        lines.append("Iterate address normalisation / keys before accepting.")

    lines += [
        "",
        "## City-year detail",
        "",
        "| City | Year | Sales | Matched | Match rate |",
        "|------|-----:|------:|--------:|-----------:|",
    ]
    for _, r in by_city_year.iterrows():
        lines.append(
            f"| {r['city']} | {int(r['sale_year'])} | {r['sales']:,} | "
            f"{r['matched']:,} | {100 * r['match_rate']:.1f}% |"
        )

    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    join_cfg = load_yaml("join")
    params = JoinParams(
        max_years_before=float(join_cfg["epc"]["max_years_before"]),
        max_years_after=float(join_cfg["epc"]["max_years_after"]),
        min_floor_area_m2=float(join_cfg["epc"]["min_floor_area_m2"]),
        max_floor_area_m2=float(join_cfg["epc"]["max_floor_area_m2"]),
    )
    min_warn = float(join_cfg["join"]["min_match_rate_warn"])

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--ppd",
        type=Path,
        default=project_path("data", "interim", "ppd_join_2012_2025.parquet"),
    )
    parser.add_argument(
        "--epc",
        type=Path,
        default=project_path("data", "interim", "epc_four_cities.parquet"),
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=project_path("data", "processed", "ppd_epc_linked_2012_2025.parquet"),
    )
    parser.add_argument(
        "--unmatched-out",
        type=Path,
        default=project_path("data", "processed", "ppd_epc_unmatched_2012_2025.parquet"),
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=project_path("docs", "data", "join_match_report_2012_2025.md"),
    )
    args = parser.parse_args()

    print("Loading…")
    ppd = _rebuild_address_keys(pd.read_parquet(args.ppd))
    epc = _rebuild_address_keys(pd.read_parquet(args.epc))
    print(f"PPD {len(ppd):,} | EPC {len(epc):,}")

    print("Joining…")
    linked, unmatched, stats = join_ppd_epc(ppd, epc, params)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    linked.to_parquet(args.out, index=False)
    unmatched.to_parquet(args.unmatched_out, index=False)

    # rates use matchable base with rebuilt keys / same filters as join
    from city_value.join_ppd_epc import _prepare_frames

    ppd_p, _ = _prepare_frames(ppd, epc, params)
    base = ppd_p[(ppd_p["postcode_norm"] != "") & (ppd_p["paon"] != "")].copy()
    by_city = _match_rate_table(linked, base, ["city"])
    by_year = _match_rate_table(linked, base, ["sale_year"])
    by_city_year = _match_rate_table(linked, base, ["city", "sale_year"])

    stats["linked_path"] = str(args.out)
    stats["unmatched_path"] = str(args.unmatched_out)
    write_report(
        stats,
        by_city,
        by_year,
        by_city_year,
        linked,
        unmatched,
        args.report,
        min_warn,
    )
    args.report.with_suffix(".yaml").write_text(
        yaml.safe_dump(
            {
                **stats,
                "by_city": by_city.to_dict(orient="records"),
                "by_year": by_year.to_dict(orient="records"),
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )

    print(
        f"Matched {stats['matched']:,} / {stats['ppd_rows_matchable']:,} "
        f"({100 * stats['match_rate']:.1f}%)"
    )
    print(f"Report → {args.report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
