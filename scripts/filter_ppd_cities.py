#!/usr/bin/env python3
"""Filter Price Paid yearly CSVs to the four project cities → data/interim.

Usage:
  python scripts/filter_ppd_cities.py
"""

from __future__ import annotations

import argparse
from pathlib import Path

import duckdb
import yaml

from city_value.config import load_yaml
from city_value.paths import project_path
from city_value.ppd import PPD_COLUMNS


def _district_literals(cities_cfg: dict) -> list[str]:
    districts: list[str] = []
    for city in cities_cfg["cities"].values():
        districts.extend(city.get("districts", []))
    return sorted({d.upper() for d in districts})


def filter_files(raw_dir: Path, out_path: Path, districts_upper: list[str]) -> int:
    files = sorted(raw_dir.glob("pp-*.csv"))
    if not files:
        raise FileNotFoundError(f"No pp-YYYY.csv files in {raw_dir}")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect()

    names_sql = "[" + ", ".join(f"'{c}'" for c in PPD_COLUMNS) + "]"
    dist_sql = ", ".join(f"'{d}'" for d in districts_upper)
    file_list = "[" + ", ".join(f"'{f.as_posix()}'" for f in files) + "]"

    con.execute(
        f"""
        COPY (
          SELECT *
          FROM read_csv(
            {file_list},
            header = false,
            names = {names_sql},
            auto_detect = true,
            ignore_errors = true,
            parallel = true
          )
          WHERE upper(trim(district)) IN ({dist_sql})
        ) TO '{out_path.as_posix()}' (FORMAT PARQUET)
        """
    )
    n = con.execute(
        f"SELECT count(*) FROM read_parquet('{out_path.as_posix()}')"
    ).fetchone()[0]
    con.close()
    return int(n)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out",
        type=Path,
        default=project_path("data", "interim", "ppd_four_cities.parquet"),
    )
    args = parser.parse_args()

    cities = load_yaml("cities")
    districts = _district_literals(cities)
    raw = project_path("data", "raw", "ppd")
    n = filter_files(raw, args.out, districts)
    print(f"Wrote {n:,} rows → {args.out}")
    print("District filters:", ", ".join(districts))
    report = project_path("docs", "data", "ppd_filter_report.yaml")
    report.write_text(
        yaml.safe_dump(
            {"rows": n, "districts_upper": districts, "output": str(args.out)},
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
