#!/usr/bin/env python3
"""Prepare Price Paid rows for the EPC join window.

Filters to Category A, property types D/S/T/F, attaches city labels, and adds
postcode_norm + address_key. Default years: year_from_epc_metrics … year_to.

Usage:
  python scripts/prepare_ppd_join.py
  python scripts/prepare_ppd_join.py --year-from 2015 --year-to 2025
"""

from __future__ import annotations

import argparse
from pathlib import Path

import duckdb
import pandas as pd
import yaml

from city_value.address import address_key, normalise_postcode
from city_value.cities import city_label, district_to_city_map
from city_value.config import load_yaml
from city_value.paths import project_path


def prepare(
    source: Path,
    out_path: Path,
    year_from: int,
    year_to: int,
    property_types: list[str],
    ppd_category: str,
    cities_cfg: dict,
) -> tuple[pd.DataFrame, dict]:
    district_map = district_to_city_map(cities_cfg)
    types_sql = ", ".join(f"'{t}'" for t in property_types)

    con = duckdb.connect()
    df = con.execute(
        f"""
        SELECT *
        FROM read_parquet(?)
        WHERE year(CAST(date_of_transfer AS DATE)) BETWEEN ? AND ?
          AND upper(trim(CAST(ppd_category_type AS VARCHAR))) = ?
          AND upper(trim(CAST(property_type AS VARCHAR))) IN ({types_sql})
        """,
        [str(source), year_from, year_to, ppd_category.upper()],
    ).df()
    con.close()

    df["district_u"] = df["district"].astype(str).str.upper().str.strip()
    df["city"] = df["district_u"].map(district_map)
    unknown = int(df["city"].isna().sum())
    if unknown:
        raise ValueError(f"{unknown} rows have district not in cities.yaml mapping")

    df["city_label"] = df["city"].map(lambda c: city_label(cities_cfg, c))
    df["sale_year"] = pd.to_datetime(df["date_of_transfer"]).dt.year
    df["postcode_norm"] = df["postcode"].map(normalise_postcode)
    df["address_key"] = [
        address_key(pc, paon, saon, street)
        for pc, paon, saon, street in zip(
            df["postcode"], df["paon"], df["saon"], df["street"], strict=True
        )
    ]

    df = df.drop(columns=["district_u"])
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(out_path, index=False)

    missing_pc = int((df["postcode_norm"] == "").sum())

    by_city_year = (
        df.groupby(["city", "sale_year"], observed=True)
        .size()
        .reset_index(name="n")
        .sort_values(["city", "sale_year"])
    )
    by_city = df.groupby("city", observed=True).size().to_dict()
    by_type = df.groupby("property_type", observed=True).size().to_dict()

    stats = {
        "source": str(source),
        "output": str(out_path),
        "year_from": year_from,
        "year_to": year_to,
        "ppd_category": ppd_category,
        "property_types": property_types,
        "rows": int(len(df)),
        "rows_by_city": {str(k): int(v) for k, v in by_city.items()},
        "rows_by_property_type": {str(k): int(v) for k, v in by_type.items()},
        "missing_postcode": missing_pc,
        "pct_missing_postcode": round(missing_pc / len(df), 4) if len(df) else None,
        "unique_address_keys": int(df["address_key"].nunique()),
        "price_min": float(df["price"].min()),
        "price_median": float(df["price"].median()),
        "price_max": float(df["price"].max()),
        "by_city_year": by_city_year.to_dict(orient="records"),
    }
    return df, stats


def write_report(stats: dict, report_path: Path) -> None:
    y0, y1 = stats["year_from"], stats["year_to"]
    lines = [
        f"# PPD join prep report ({y0}–{y1})",
        "",
        f"**Output:** `{stats['output']}`",
        f"**Source:** `{stats['source']}`",
        "",
        "## Filters applied",
        "",
        f"- Years: **{y0}–{y1}**",
        f"- PPD category: **{stats['ppd_category']}**",
        f"- Property types: `{', '.join(stats['property_types'])}`",
        "",
        "## Totals",
        "",
        "| Metric | Value |",
        "|--------|------:|",
        f"| Rows | **{stats['rows']:,}** |",
        f"| Unique address_key | {stats['unique_address_keys']:,} |",
    ]
    pct_missing = 100 * (stats["pct_missing_postcode"] or 0)
    lines.append(f"| Missing postcode | {stats['missing_postcode']:,} ({pct_missing:.2f}%) |")
    lines.append(
        "| Price min / median / max | "
        f"£{stats['price_min']:,.0f} / £{stats['price_median']:,.0f} / "
        f"£{stats['price_max']:,.0f} |"
    )
    lines += [
        "",
        "## Rows by city",
        "",
        "| City | Rows |",
        "|------|-----:|",
    ]
    for city, n in sorted(stats["rows_by_city"].items()):
        lines.append(f"| {city} | {n:,} |")

    lines += [
        "",
        "## Rows by property type",
        "",
        "| Type | Rows |",
        "|------|-----:|",
    ]
    for ptype, n in sorted(stats["rows_by_property_type"].items()):
        lines.append(f"| {ptype} | {n:,} |")

    lines += [
        "",
        "## Rows by city and year",
        "",
        "| City | Year | Rows |",
        "|------|-----:|-----:|",
    ]
    for row in stats["by_city_year"]:
        lines.append(f"| {row['city']} | {row['sale_year']} | {row['n']:,} |")

    lines += [
        "",
        "## Columns added",
        "",
        "- `city`, `city_label`, `sale_year`",
        "- `postcode_norm`, `address_key`",
        "",
        "## Verdict",
        "",
    ]
    ok = stats["rows"] > 0 and (stats["pct_missing_postcode"] or 0) < 0.05
    if ok:
        lines.append(f"**Pass** — PPD join table ({y0}–{y1}) is ready for EPC join.")
    else:
        lines.append("**Fail** — investigate empty output or high missing-postcode rate.")

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    join_cfg = load_yaml("join")
    cities_cfg = load_yaml("cities")
    ppd = join_cfg["ppd"]

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--year-from",
        type=int,
        default=None,
        help="Inclusive start year (default: ppd.year_from_epc_metrics)",
    )
    parser.add_argument(
        "--year-to",
        type=int,
        default=None,
        help="Inclusive end year (default: ppd.year_to)",
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=project_path("data", "interim", "ppd_four_cities.parquet"),
        help="Filtered four-city Price Paid parquet",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Output parquet (default: data/interim/ppd_join_{from}_{to}.parquet)",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=None,
        help="Markdown report path (default: docs/data/ppd_join_{from}_{to}_report.md)",
    )
    args = parser.parse_args()

    year_from = int(args.year_from if args.year_from is not None else ppd["year_from_epc_metrics"])
    year_to = int(args.year_to if args.year_to is not None else ppd["year_to"])
    out_path = args.out or project_path(
        "data", "interim", f"ppd_join_{year_from}_{year_to}.parquet"
    )
    report_path = args.report or project_path(
        "docs", "data", f"ppd_join_{year_from}_{year_to}_report.md"
    )

    property_types = list(ppd["property_types"])
    category = str(ppd["ppd_category"])

    _df, stats = prepare(
        source=args.source,
        out_path=out_path,
        year_from=year_from,
        year_to=year_to,
        property_types=property_types,
        ppd_category=category,
        cities_cfg=cities_cfg,
    )
    write_report(stats, report_path)

    yaml_path = report_path.with_suffix(".yaml")
    yaml_path.write_text(yaml.safe_dump(stats, sort_keys=False), encoding="utf-8")

    print(f"Wrote {stats['rows']:,} rows → {out_path}")
    print(f"Report → {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
