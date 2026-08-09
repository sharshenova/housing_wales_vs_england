#!/usr/bin/env python3
"""Download HM Land Registry Price Paid yearly files into data/raw/ppd.

Usage (after pip install -e .):
  python scripts/download_ppd.py --years 2020 2021 2022
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import httpx
from tqdm import tqdm

from city_value.config import load_yaml
from city_value.paths import project_path

# Yearly complete CSV (URL host confirmed from GOV.UK Price Paid page, Aug 2026).
BASE = "https://price-paid-data.publicdata.landregistry.gov.uk/pp-{year}.csv"


def download_year(year: int, dest_dir: Path, client: httpx.Client) -> Path:
    dest_dir.mkdir(parents=True, exist_ok=True)
    out = dest_dir / f"pp-{year}.csv"
    if out.exists() and out.stat().st_size > 0:
        print(f"skip existing {out}")
        return out
    url = BASE.format(year=year)
    with client.stream("GET", url, follow_redirects=True) as resp:
        resp.raise_for_status()
        total = int(resp.headers.get("content-length", 0))
        with out.open("wb") as f, tqdm(
            total=total or None, unit="B", unit_scale=True, desc=str(year)
        ) as bar:
            for chunk in resp.iter_bytes():
                f.write(chunk)
                bar.update(len(chunk))
    return out


def main(argv: list[str] | None = None) -> int:
    join_cfg = load_yaml("join")
    ppd = join_cfg["ppd"]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--years",
        nargs="+",
        type=int,
        default=None,
        help="Years to download (default: full price-only window from join.yaml)",
    )
    parser.add_argument(
        "--backfill-pending",
        action="store_true",
        help="Download only years listed in ppd.years_pending_ppd_backfill",
    )
    parser.add_argument(
        "--prototype",
        action="store_true",
        help="Download join-prototype window only (year_from_join_prototype..year_to)",
    )
    args = parser.parse_args(argv)

    if args.years is not None:
        years = args.years
    elif args.backfill_pending:
        years = list(ppd["years_pending_ppd_backfill"])
    elif args.prototype:
        years = list(
            range(int(ppd["year_from_join_prototype"]), int(ppd["year_to"]) + 1)
        )
    else:
        years = list(range(int(ppd["year_from_price_only"]), int(ppd["year_to"]) + 1))

    dest = project_path("data", "raw", "ppd")
    with httpx.Client(timeout=120.0) as client:
        for year in years:
            try:
                path = download_year(year, dest, client)
                print(f"ok {path}")
            except httpx.HTTPError as exc:
                print(f"FAILED {year}: {exc}", file=sys.stderr)
                print(
                    "Check the current URL on "
                    "https://www.gov.uk/government/statistical-data-sets/price-paid-data-downloads",
                    file=sys.stderr,
                )
                return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
