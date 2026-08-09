# EPC downloads

## File on disk

| Field | Value |
|-------|--------|
| Path | `data/raw/epc/9acf114a-6f6d-47e6-8d0f-3f12e194903a.csv` |
| Size | ~512 MB |
| Format | CSV, comma-separated, header row, 93 columns |
| Source | [Get energy performance of buildings data](https://get-energy-performance-data.communities.gov.uk/) (GOV.UK One Login) |
| Checked | 2026-08-09 |

## QA summary (pass)

| Check | Result |
|-------|--------|
| Rows | **499,054** |
| Local authorities | **4 labels** covering our project cities |
| Lodgement dates | **2012-01-01** → **2026-07-31** (covers £/m² window 2012–2025) |
| Missing postcode | **0%** |
| Missing total_floor_area | **0%** |
| Missing current_energy_rating | **0%** |
| Missing UPRN | ~2.0% |
| Missing number_habitable_rooms | ~10.7% (usable; model can allow nulls) |

### Counts by `local_authority_label`

| LA label | Rows | Code(s) |
|----------|------|---------|
| Bristol, City of | 183,021 | E06000023 |
| Cardiff | 152,312 | W06000015 |
| Swansea | 88,907 | W06000011 |
| Bath and North East Somerset | 74,800 + 14 | E06000022 (+ E06000066 for 14 rows) |

The 14 BANES rows with code `E06000066` are a minor coding quirk; keep them under Bath for now.

### Postcode area mix

| Area | Rows |
|------|------|
| BS | 200,117 |
| CF | 152,312 |
| SA | 88,907 |
| BA | 57,718 |

BA &lt; BANES row count is expected (some BANES properties use other postcodes).

## Ingest / join notes

Raw CSV → `data/interim/epc_four_cities.parquet` via `python scripts/ingest_epc.py`.  
Row counts and lodge-date checks are summarised in [join_epc_metrics_2012_2025_run.md](join_epc_metrics_2012_2025_run.md) (Step 0).

## Join-relevant columns present

`postcode`, `address1`–`address3`, `address`, `local_authority` / `local_authority_label`, `lodgement_date`, `inspection_date`, `total_floor_area`, `number_habitable_rooms`, `current_energy_rating`, `current_energy_efficiency`, `built_form`, `construction_age_band`, `property_type`, `uprn`, `certificate_number`

## Verdict

EPC extract accepted for the four cities; used in the **2012–2025** PPD↔EPC join.
