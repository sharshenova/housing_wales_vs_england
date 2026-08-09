# Progress

## Current phase

**Phase 1 — £/m² join window ready:** Linked table `ppd_epc_linked_2012_2025.parquet` — **169,100 / 251,733 matched (67.2%)**. Runbook: `docs/data/join_epc_metrics_2012_2025_run.md`. Prototype artifacts removed (comparison retained in runbook). Next: Tableau aggregates; PPD price-only backfill **1996–2011**.

## Active goal

Build a reproducible **Price Paid ↔ EPC** pipeline for Swansea, Cardiff, Bristol, Bath that supports £/m² analytics (Project F) and is reusable for Project G.

## Locked windows (Option A)

See [data/year_range_analysis.md](data/year_range_analysis.md) and [decisions/002-year-windows-option-a.md](decisions/002-year-windows-option-a.md).

| Layer | Years | Status |
|-------|-------|--------|
| Price / volume | 1996–2025 | Pending PPD backfill **1996–2011** |
| £/m² + Project G | 2012–2025 | **Joined** — 67.2% overall (2012 weak) |

## Completed

- [x] Create local git project `city_value_housing` (+ agent root)
- [x] Add AGENTS.md, GOALS.md, PROGRESS.md, `.cursor/rules`, pyproject, package skeleton
- [x] Address normalisation helpers + unit tests (2 passed)
- [x] `scripts/download_ppd.py` with correct Land Registry publicdata URL
- [x] Download PPD yearly CSVs **2012–2025** (2015–2025 first; 2012–2014 on 2026-08-09)
- [x] Filter → `data/interim/ppd_four_cities.parquet` (285,608 rows 2012–2025; Vale of Glamorgan excluded)
- [x] Verify district strings: Swansea, Cardiff, City Of Bristol, Bath And North East Somerset
- [x] Decision 001: four cities, F then G
- [x] Decision 002: Option A year windows locked in `configs/join.yaml`

## In progress

- [x] Obtain Domestic EPC extract for the four areas (single CSV, 499k rows — see `docs/data/epc_downloads.md`)
- [x] EPC ingest → `data/interim/epc_four_cities.parquet` (499,054 rows); provenance `docs/data/epc_downloads.md`
- [x] Enrich linked schema + `enrich_linked()`; schema `docs/data/linked_schema.md`
- [x] Join **2012–2025** → `ppd_epc_linked_2012_2025.parquet` (67.2%); runbook `docs/data/join_epc_metrics_2012_2025_run.md`
- [x] Cleanup: removed prototype reports/outputs and early QA previews
- [ ] Optional Bath BA1/BA2 restriction (sensitivity later)
- [ ] Optional: label/filter low-match years (esp. 2012 at ~40%) in Tableau

## Backlog (do not forget)

- [ ] Price-only: `python scripts/download_ppd.py --backfill-pending` (**1996–2011**)
- [ ] Re-filter four cities; re-run price/volume aggregates; confirm pipeline for full price window
- [ ] Clear Tableau/dashboard labels: price-only (1996–2025) vs £/m² (2012–2025)
- [ ] Investigate inflation adjustment — **nominal + real** prices (ONS CPIH or similar); enable `inflation` in `join.yaml` when ready

## Blockers

- None.

## Next steps

1. Project F Tableau / city value aggregates from `ppd_epc_linked_2012_2025.parquet`.
2. Optionally backfill PPD **1996–2011** for long price/volume series.
3. Project G only after join quality accepted for modelling use.

## Key decisions

- [001-four-cities-f-then-g](decisions/001-four-cities-f-then-g.md)
- [002-year-windows-option-a](decisions/002-year-windows-option-a.md)
- Exclude Vale of Glamorgan from core Cardiff KPIs (config updated 2026-08-07).

## Session log

### 2026-08-09 (prototype code removed)

- Dropped `year_from_join_prototype` / `use_prototype_window` from `configs/join.yaml`.
- Removed `download_ppd.py --prototype` and `prepare_ppd_join.py --window`; prepare defaults to `year_from_epc_metrics`.

### 2026-08-09 (cleanup)

- Deleted prototype reports/parquets, EPC ingest report (kept `epc_four_cities.parquet`), `epc_preview_*`, linked preview sample, `ppd_join_2012_2025_report.*`.
- Join script defaults → 2012–2025 paths; docs retargeted to sole linked table.

### 2026-08-09 (epc-metrics 2012–2025)

- Downloaded PPD **2012–2014**; re-filtered → **285,608** four-city rows.
- Prepared `ppd_join_2012_2025.parquet` (**251,821** Category A); joined → **169,100 / 251,733 (67.2%)**.
- Sanity: sale_year≥2015 inside new file = **exact** prototype match (141,661 / 71.06%).
- Early years 2012–2014 match rate **52.4%** (2012 alone **39.9%**).
- Runbook: `docs/data/join_epc_metrics_2012_2025_run.md`. Pending backfill **1996–2011**.

### 2026-08-09 (enrich)

- Extended join `EPC_COLS` with `built_form`, `construction_age_band`, `current_energy_efficiency`.
- Added `src/city_value/features.py` → `enrich_linked()` (`postcode_district`, `is_new_build`, `is_leasehold`, `property_type_label`, floor/rooms bands, `sale_quarter`, `epc_years_before_sale`).
- Documented linked columns in `docs/data/linked_schema.md`.

### 2026-08-09 (evening)

- EPC Step 0 complete: `data/raw/epc/9acf114a-6f6d-47e6-8d0f-3f12e194903a.csv` (~512 MB, 499,054 rows, all 4 LAs, lodge dates 2012–2026).
- QA note: `docs/data/epc_downloads.md`. Verdict: OK to proceed with ingest + join.
- Prototype join path (since removed): 199,427 Category A sales → 71.1% match; fixed PPD `NAN` SAON bug.

### 2026-08-09

- Accepted Option A: price **1996–2025**, £/m² **2012–2025**, join prototype **2015–2025**.
- Locked in `configs/join.yaml`; decision 002; linked from AGENTS.md, GOALS.md, cursor rules, data README.
- Inflation comparison (nominal + real) added to backlog / `inflation` config stub.
- Download script: `--backfill-pending` flag.

### 2026-08-07

- Created `city_value_housing` with thesis-style memory: `AGENTS.md` + `docs/PROGRESS.md` + `docs/GOALS.md` + `.cursor/rules` + `docs/decisions/`.
- Career plans stay in `../plans/`.
- Downloaded PPD **2015–2025**; filtered interim parquet **231,526** rows across four LAs.
- Tests: `pytest` 2 passed; `ruff` clean.
- Local git repo ready on `main` (no commits yet; large `data/` ignored). Remote later: `origin` → `sharshenova/housing_wales_vs_england`.
