# Price Paid downloads

Base URL: `https://price-paid-data.publicdata.landregistry.gov.uk/pp-{year}.csv`  
Script: `scripts/download_ppd.py`

| Date | Years on disk | Notes |
|------|---------------|-------|
| 2026-08-07 | 2015–2025 | All yearly complete CSVs in `data/raw/ppd/` |

## Filtered interim

`data/interim/ppd_four_cities.parquet` — **231,526** rows (2015–2025), districts:

- SWANSEA  
- CARDIFF  
- CITY OF BRISTOL  
- BATH AND NORTH EAST SOMERSET  

Vale of Glamorgan excluded from core Cardiff filter.

## Attribution

Contains HM Land Registry data © Crown copyright and database right. Licensed under the Open Government Licence v3.0.
