# Price Paid downloads

Base URL: `https://price-paid-data.publicdata.landregistry.gov.uk/pp-{year}.csv`  
Script: `scripts/download_ppd.py`

| Date | Years on disk | Notes |
|------|---------------|-------|
| 2026-08-07 | 2015–2025 | All yearly complete CSVs in `data/raw/ppd/` |
| 2026-08-09 | 2012–2014 | Backfill for £/m² window (`pp-2012.csv` … `pp-2014.csv`) |

Still pending for price-only story: **1996–2011** (`years_pending_ppd_backfill` in `configs/join.yaml`).

## Filtered interim

`data/interim/ppd_four_cities.parquet` — **285,608** rows (2012–2025), districts:

- SWANSEA  
- CARDIFF  
- CITY OF BRISTOL  
- BATH AND NORTH EAST SOMERSET  

Vale of Glamorgan excluded from core Cardiff filter.

## Attribution

Contains HM Land Registry data © Crown copyright and database right. Licensed under the Open Government Licence v3.0.
