# Progress

## Current phase

**Phase 1 — Join prototype:** PPD **2015–2025** on disk. Option A year windows **locked**. Next: Domestic EPC + join on prototype window; later backfill **1996–2014**.

## Active goal

Build a reproducible **Price Paid ↔ EPC** pipeline for Swansea, Cardiff, Bristol, Bath that supports £/m² analytics (Project F) and is reusable for Project G.

## Locked windows (Option A)

See [data/year_range_analysis.md](data/year_range_analysis.md) and [decisions/002-year-windows-option-a.md](decisions/002-year-windows-option-a.md).

| Layer | Years | Status |
|-------|-------|--------|
| Price / volume | 1996–2025 | Pending PPD backfill 1996–2014 |
| £/m² + Project G | 2012–2025 | Needs EPC join |
| Join prototype | 2015–2025 | **Current work** — PPD ready |

## Completed

- [x] Create local git project `city_value_housing` (+ agent root)
- [x] Add AGENTS.md, GOALS.md, PROGRESS.md, `.cursor/rules`, pyproject, package skeleton
- [x] Address normalisation helpers + unit tests (2 passed)
- [x] `scripts/download_ppd.py` with correct Land Registry publicdata URL
- [x] Download PPD yearly CSVs **2015–2025**
- [x] Filter → `data/interim/ppd_four_cities.parquet` (four LAs; Vale of Glamorgan excluded)
- [x] Verify district strings: Swansea, Cardiff, City Of Bristol, Bath And North East Somerset
- [x] Decision 001: four cities, F then G
- [x] Decision 002: Option A year windows locked in `configs/join.yaml`

## In progress

- [ ] Attach `city` id in filter output; optional Bath BA1/BA2 restriction
- [ ] Obtain Domestic EPC extracts for the four areas
- [ ] Implement address join on **2015–2025**; report match rate (overall + by year)

## Backlog (do not forget)

- [ ] After join match rate accepted: `python scripts/download_ppd.py --backfill-pending` (**1996–2014**)
- [ ] Re-filter four cities; re-run aggregates; confirm pipeline still works for full price window
- [ ] Clear Tableau/dashboard labels: price-only (1996–2025) vs £/m² (2012–2025)
- [ ] Investigate inflation adjustment — **nominal + real** prices (ONS CPIH or similar); enable `inflation` in `join.yaml` when ready

## Blockers

- EPC bulk download may require free GOV.UK One Login / Open Data registration.

## Next steps

1. Improve filter: attach `city` label from config; optional Bath postcode BA1/BA2 restriction.
2. EPC: register/download for four LAs; draft `scripts/join_ppd_epc.py` on prototype years.
3. Match-rate report in `docs/data/`; accept or iterate join.
4. Then PPD backfill 1996–2014 + full-window price aggregates.

## Key decisions

- [001-four-cities-f-then-g](decisions/001-four-cities-f-then-g.md)
- [002-year-windows-option-a](decisions/002-year-windows-option-a.md)
- Exclude Vale of Glamorgan from core Cardiff KPIs (config updated 2026-08-07).

## Session log

### 2026-08-09

- Accepted Option A: price **1996–2025**, £/m² **2012–2025**, join prototype **2015–2025**.
- Locked in `configs/join.yaml`; decision 002; linked from AGENTS.md, GOALS.md, cursor rules, data README.
- Inflation comparison (nominal + real) added to backlog / `inflation` config stub.
- Download script: `--backfill-pending` and `--prototype` flags.

### 2026-08-07

- Created `city_value_housing` with thesis-style memory: `AGENTS.md` + `docs/PROGRESS.md` + `docs/GOALS.md` + `.cursor/rules` + `docs/decisions/`.
- Career plans stay in `../plans/`.
- Downloaded PPD **2015–2025**; filtered interim parquet **231,526** rows across four LAs.
- Tests: `pytest` 2 passed; `ruff` clean.
- Local git repo ready on `main` (no commits yet; large `data/` ignored). Remote later: `origin` → `sharshenova/housing_wales_vs_england`.
