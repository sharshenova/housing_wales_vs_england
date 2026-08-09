# Runbook: PPD ↔ EPC join for £/m² window (2012–2025)

**Date:** 2026-08-09  
**Goal:** Expand the accepted prototype join (2015–2025) to the locked Option A £/m² window (**2012–2025**) and compare stats. Prototype artifacts were removed after comparison; figures below remain the record.

**Primary linked file:** `data/processed/ppd_epc_linked_2012_2025.parquet`  
**Machine-readable summary:** [`join_epc_metrics_2012_2025_run.yaml`](join_epc_metrics_2012_2025_run.yaml)

---

## Step 0 — Confirm EPC interim (no re-download)

**Action:** Reuse existing `data/interim/epc_four_cities.parquet` (from prior ingest).

| Metric | Value |
|--------|------:|
| Rows | 499,054 |
| Lodgement min → max | 2012-01-01 → 2026-07-31 |
| Cities | bath, bristol, cardiff, swansea |

**Outcome:** EPC already covers the £/m² window start year. No second download.

---

## Step 1 — Download missing Price Paid (2012–2014)

**Action:**
```bash
python scripts/download_ppd.py --years 2012 2013 2014
```

| Year | File | Size |
|-----:|------|-----:|
| 2012 | `data/raw/ppd/pp-2012.csv` | 115.5 MB |
| 2013 | `data/raw/ppd/pp-2013.csv` | 140.2 MB |
| 2014 | `data/raw/ppd/pp-2014.csv` | 170.5 MB |

**Outcome:** All three years downloaded successfully. 2015–2025 were already on disk. Pending backfill is now **1996–2011** only (price-only story).

---

## Step 2 — Re-filter four cities

**Action:**
```bash
python scripts/filter_ppd_cities.py
```

| Metric | Value |
|--------|------:|
| Previous interim (2015–2025) | ~231,526 rows |
| New interim (2012–2025) | **285,608** rows |
| Added 2012–2014 | **54,082** rows |

Sales by year (all four LAs, all categories/types in filter):

| Year | Rows | Year | Rows |
|-----:|-----:|-----:|-----:|
| 2012 | 14,772 | 2019 | 21,430 |
| 2013 | 17,617 | 2020 | 17,438 |
| 2014 | 21,693 | 2021 | 25,362 |
| 2015 | 21,677 | 2022 | 22,018 |
| 2016 | 22,240 | 2023 | 18,185 |
| 2017 | 22,718 | 2024 | 18,994 |
| 2018 | 22,454 | 2025 | 19,010 |

**Outcome:** Filter OK. Districts unchanged (Swansea, Cardiff, City Of Bristol, Bath And North East Somerset).

---

## Step 3 — Prepare join table (Category A, D/S/T/F, 2012–2025)

**Action:**
```bash
python scripts/prepare_ppd_join.py
```

| Metric | Value |
|--------|------:|
| Output | `data/interim/ppd_join_2012_2025.parquet` |
| Rows | **251,821** |
| Missing postcode | 88 (0.03%) |
| bath / bristol / cardiff / swansea | 41,478 / 97,101 / 70,163 / 43,079 |

**Outcome:** Pass.

---

## Step 4 — Temporal join + enrich

**Action:**
```bash
python scripts/join_ppd_epc.py \
  --ppd data/interim/ppd_join_2012_2025.parquet \
  --out data/processed/ppd_epc_linked_2012_2025.parquet \
  --unmatched-out data/processed/ppd_epc_unmatched_2012_2025.parquet \
  --report docs/data/join_match_report_2012_2025.md
```

Same join rules as prototype (full `address_key` then loose key; EPC ≤10y before / ≤2y after; floor area 15–500 m²) plus `enrich_linked()`.

| Metric | Value |
|--------|------:|
| PPD matchable | 251,733 |
| **Matched** | **169,100** |
| Unmatched | 82,633 |
| **Match rate** | **67.17%** |
| Tier full / loose | 167,739 / 1,361 |
| £/m² p05 / median / p95 | 1,249 / 2,848 / 5,181 |
| Columns | 47 (same schema as prototype) |

Detail report: [`join_match_report_2012_2025.md`](join_match_report_2012_2025.md).

**Outcome:** Join completed. Overall rate is below the 70% warn threshold because **2012–2014** pull the average down (expected — fewer EPCs before early sales). Overlap years match the prototype exactly (see Step 5).

---

## Step 5 — Comparison vs prototype (2015–2025)

### Overall

| Metric | Prototype 2015–2025 | New 2012–2025 |
|--------|--------------------:|--------------:|
| Matchable sales | 199,359 | 251,733 |
| Matched | 141,661 | 169,100 |
| Match rate | **71.06%** | **67.17%** |
| Tier full | 140,464 | 167,739 |
| Tier loose | 1,197 | 1,361 |
| Median £/m² | 3,037 | 2,848 |

### Sanity check (sale_year ≥ 2015 inside new file)

| Metric | Value |
|--------|------:|
| Matchable (2015–2025 subset) | 199,359 |
| Matched | 141,661 |
| Match rate | **71.06%** |
| Diff vs prototype | **0.00 pp** |

Year-by-year match counts for 2015–2025 are identical to the prototype report. Extending the window did not change the join behaviour on overlapping years.

### Early years only (2012–2014)

| Metric | Value |
|--------|------:|
| Matchable | 52,374 |
| Matched | 27,439 |
| Match rate | **52.39%** |

| Year | Sales | Matched | Match rate |
|-----:|------:|--------:|-----------:|
| 2012 | 14,763 | 5,888 | 39.9% |
| 2013 | 17,196 | 10,025 | 58.3% |
| 2014 | 20,415 | 11,526 | 56.5% |

2012 is weakest (EPC bulk lodgement starts that year → few certificates *before* sale).

### Match rate by city

| City | Proto rate | 2012–2025 rate |
|------|----------:|---------------:|
| bath | 66.1% | 62.4% |
| bristol | 65.9% | 62.4% |
| cardiff | 74.9% | 70.9% |
| swansea | 80.8% | 76.6% |

City ranking unchanged (Swansea highest, Bath/Bristol lowest).

### Median £/m² by city (matched)

| City | Proto 2015–2025 | New 2012–2025 |
|------|----------------:|--------------:|
| bath | £3,768 | £3,571 |
| bristol | £3,590 | £3,370 |
| cardiff | £2,773 | £2,626 |
| swansea | £1,887 | £1,818 |

Slightly lower medians with earlier years included — expected (nominal prices rising over time). City order unchanged.

### Null rates (key EPC fields)

| Column | Proto | 2012–2025 |
|--------|------:|----------:|
| `built_form` | 0.64% | 0.69% |
| `construction_age_band` | 0.0% | 0.0% |
| `current_energy_efficiency` | 0.0% | 0.0% |
| `number_habitable_rooms` | 11.6% | 10.9% |
| `total_floor_area` | 0.0% | 0.0% |
| `current_energy_rating` | 0.0% | 0.0% |

### Verdict

- **Join logic OK** — 2015–2025 overlap matches prototype exactly.
- **Overall 67.2%** is acceptable for the full £/m² window once early-year coverage is understood; for dashboards prefer labelling or filtering years with low match rates (especially **2012**).
- **Primary analysis table** for Project F £/m²: `ppd_epc_linked_2012_2025.parquet`.
- Price-only backfill **1996–2011** remains backlog (no EPC join for those years).

---

## Step 6 — Config / docs updates

- `configs/join.yaml`: `years_pending_ppd_backfill` → 1996–2011 (prototype window keys later removed).
- Schema pointer: [`linked_schema.md`](linked_schema.md); join QA: [`join_match_report_2012_2025.md`](join_match_report_2012_2025.md).
- Progress: [`../PROGRESS.md`](../PROGRESS.md).
- Prototype reports/outputs removed after this comparison was recorded (2026-08-09 cleanup).
