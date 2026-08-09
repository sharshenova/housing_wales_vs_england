#!/usr/bin/env python3
"""Ingest Domestic EPC CSV(s) for the four cities → interim parquet.

Usage:
  python scripts/ingest_epc.py
"""

from __future__ import annotations

import argparse
from pathlib import Path

import duckdb
import pandas as pd
import yaml

from city_value.cities import city_label
from city_value.config import load_yaml
from city_value.epc import EPC_KEEP_COLUMNS, city_id_from_epc_la
from city_value.epc_address import epc_address_key
from city_value.paths import project_path


def _find_epc_files(raw_dir: Path) -> list[Path]:
    files = sorted(raw_dir.glob("*.csv")) + sorted(raw_dir.glob("*.CSV"))
    return [f for f in files if f.is_file() and f.stat().st_size > 0]


def ingest(raw_dir: Path, out_path: Path, cities_cfg: dict) -> dict:
    files = _find_epc_files(raw_dir)
    if not files:
        raise FileNotFoundError(f"No EPC CSV files in {raw_dir}")

    con = duckdb.connect()
    file_list = "[" + ", ".join(f"'{f.as_posix()}'" for f in files) + "]"
    cols = ", ".join(EPC_KEEP_COLUMNS)
    df = con.execute(
        f"""
        SELECT {cols}
        FROM read_csv(
          {file_list},
          header = true,
          auto_detect = true,
          ignore_errors = true,
          parallel = true,
          sample_size = -1
        )
        """
    ).df()
    con.close()

    df["city"] = df["local_authority_label"].map(
        lambda x: city_id_from_epc_la(x, cities_cfg)
    )
    unknown = int(df["city"].isna().sum())
    if unknown:
        bad = (
            df.loc[df["city"].isna(), "local_authority_label"]
            .astype(str)
            .value_counts()
            .head(10)
            .to_dict()
        )
        raise ValueError(f"{unknown} EPC rows have unmapped LA labels: {bad}")

    df["city_label"] = df["city"].map(lambda c: city_label(cities_cfg, c))

    parsed = [
        epc_address_key(pc, a1, a2, a3)
        for pc, a1, a2, a3 in zip(
            df["postcode"], df["address1"], df["address2"], df["address3"], strict=True
        )
    ]
    df["postcode_norm"] = [p[0] for p in parsed]
    df["saon"] = [p[1] for p in parsed]
    df["paon"] = [p[2] for p in parsed]
    df["street"] = [p[3] for p in parsed]
    df["address_key"] = [p[4] for p in parsed]

    df["inspection_date"] = pd.to_datetime(df["inspection_date"], errors="coerce")
    df["lodgement_date"] = pd.to_datetime(df["lodgement_date"], errors="coerce")
    df["epc_date"] = df["lodgement_date"].fillna(df["inspection_date"])
    df["total_floor_area"] = pd.to_numeric(df["total_floor_area"], errors="coerce")
    df["number_habitable_rooms"] = pd.to_numeric(
        df["number_habitable_rooms"], errors="coerce"
    )
    df["current_energy_efficiency"] = pd.to_numeric(
        df["current_energy_efficiency"], errors="coerce"
    )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(out_path, index=False)

    join_cfg = load_yaml("join")
    min_area = float(join_cfg["epc"]["min_floor_area_m2"])
    max_area = float(join_cfg["epc"]["max_floor_area_m2"])
    area_ok = df["total_floor_area"].between(min_area, max_area)

    stats = {
        "source_files": [str(f) for f in files],
        "output": str(out_path),
        "rows": int(len(df)),
        "rows_by_city": {str(k): int(v) for k, v in df.groupby("city").size().items()},
        "rows_by_la_label": {
            str(k): int(v)
            for k, v in df.groupby("local_authority_label").size().items()
        },
        "missing_postcode": int((df["postcode_norm"] == "").sum()),
        "pct_missing_postcode": round(float((df["postcode_norm"] == "").mean()), 4),
        "missing_floor_area": int(df["total_floor_area"].isna().sum()),
        "pct_missing_floor_area": round(float(df["total_floor_area"].isna().mean()), 4),
        "floor_area_in_config_range": int(area_ok.sum()),
        "pct_floor_area_in_config_range": round(float(area_ok.mean()), 4),
        "missing_rooms": int(df["number_habitable_rooms"].isna().sum()),
        "pct_missing_rooms": round(float(df["number_habitable_rooms"].isna().mean()), 4),
        "missing_rating": int(
            df["current_energy_rating"].isna().sum()
            + (df["current_energy_rating"].astype(str).str.strip() == "").sum()
        ),
        "missing_uprn": int(df["uprn"].isna().sum()),
        "pct_missing_uprn": round(float(df["uprn"].isna().mean()), 4),
        "missing_epc_date": int(df["epc_date"].isna().sum()),
        "min_lodgement": str(df["lodgement_date"].min()),
        "max_lodgement": str(df["lodgement_date"].max()),
        "min_inspection": str(df["inspection_date"].min()),
        "max_inspection": str(df["inspection_date"].max()),
        "unique_address_keys": int(df["address_key"].nunique()),
        "pct_empty_paon": round(float((df["paon"] == "").mean()), 4),
        "pct_nonempty_saon": round(float((df["saon"] != "").mean()), 4),
        "floor_area_median": float(df["total_floor_area"].median()),
        "floor_area_p05": float(df["total_floor_area"].quantile(0.05)),
        "floor_area_p95": float(df["total_floor_area"].quantile(0.95)),
        "rating_counts": {
            str(k): int(v)
            for k, v in df["current_energy_rating"].value_counts(dropna=False).items()
        },
    }
    return stats


def write_report(stats: dict, report_path: Path) -> None:
    lines = [
        "# EPC ingest report (Step 2)",
        "",
        f"**Output:** `{stats['output']}`",
        "",
        "## Source files",
        "",
    ]
    for f in stats["source_files"]:
        lines.append(f"- `{f}`")

    lines += [
        "",
        "## Totals",
        "",
        "| Metric | Value |",
        "|--------|------:|",
        f"| Rows | **{stats['rows']:,}** |",
        f"| Unique address_key | {stats['unique_address_keys']:,} |",
        f"| Missing postcode | {stats['missing_postcode']:,} "
        f"({100 * stats['pct_missing_postcode']:.2f}%) |",
        f"| Missing floor area | {stats['missing_floor_area']:,} "
        f"({100 * stats['pct_missing_floor_area']:.2f}%) |",
        f"| Floor area in config range | {stats['floor_area_in_config_range']:,} "
        f"({100 * stats['pct_floor_area_in_config_range']:.2f}%) |",
        f"| Missing rooms | {stats['missing_rooms']:,} "
        f"({100 * stats['pct_missing_rooms']:.2f}%) |",
        f"| Missing UPRN | {stats['missing_uprn']:,} "
        f"({100 * stats['pct_missing_uprn']:.2f}%) |",
        f"| Missing EPC date | {stats['missing_epc_date']:,} |",
        f"| Empty parsed PAON | {100 * stats['pct_empty_paon']:.2f}% |",
        f"| Non-empty SAON (flats etc.) | {100 * stats['pct_nonempty_saon']:.2f}% |",
        f"| Floor area p05 / median / p95 | "
        f"{stats['floor_area_p05']:.0f} / {stats['floor_area_median']:.0f} / "
        f"{stats['floor_area_p95']:.0f} m² |",
        "",
        "## Date range",
        "",
        f"- Lodgement: {stats['min_lodgement']} → {stats['max_lodgement']}",
        f"- Inspection: {stats['min_inspection']} → {stats['max_inspection']}",
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
        "## Rows by EPC LA label",
        "",
        "| LA label | Rows |",
        "|----------|-----:|",
    ]
    for label, n in sorted(stats["rows_by_la_label"].items(), key=lambda x: -x[1]):
        lines.append(f"| {label} | {n:,} |")

    lines += [
        "",
        "## Energy rating counts",
        "",
        "| Rating | Rows |",
        "|--------|-----:|",
    ]
    for rating, n in sorted(stats["rating_counts"].items(), key=lambda x: str(x[0])):
        lines.append(f"| {rating} | {n:,} |")

    lines += [
        "",
        "## Columns added for join",
        "",
        "- `city`, `city_label`",
        "- `saon`, `paon`, `street` (parsed from EPC address lines)",
        "- `postcode_norm`, `address_key` (same scheme as PPD)",
        "- `epc_date` = lodgement_date, else inspection_date",
        "",
        "## Verdict",
        "",
    ]
    ok = (
        stats["rows"] > 0
        and stats["pct_missing_postcode"] < 0.01
        and stats["pct_missing_floor_area"] < 0.01
        and stats["missing_epc_date"] == 0
        and set(stats["rows_by_city"]) >= {"swansea", "cardiff", "bristol", "bath"}
    )
    if ok:
        lines.append(
            "**Pass** — EPC interim table is ready for temporal join (Step 3)."
        )
    else:
        lines.append("**Fail** — investigate missing fields or city coverage.")

    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    cities_cfg = load_yaml("cities")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--raw-dir",
        type=Path,
        default=project_path("data", "raw", "epc"),
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=project_path("data", "interim", "epc_four_cities.parquet"),
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=project_path("docs", "data", "epc_ingest_report.md"),
    )
    args = parser.parse_args()

    stats = ingest(args.raw_dir, args.out, cities_cfg)
    write_report(stats, args.report)
    args.report.with_suffix(".yaml").write_text(
        yaml.safe_dump(stats, sort_keys=False), encoding="utf-8"
    )
    print(f"Wrote {stats['rows']:,} rows → {args.out}")
    print(f"Report → {args.report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
