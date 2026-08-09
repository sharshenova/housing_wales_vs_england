# 002 — Dual year windows (Option A)

**Date:** 2026-08-09  
**Status:** accepted

## Context

Need a long comparative story for relocators without claiming £/m² where EPC does not exist. See [year_range_analysis.md](../data/year_range_analysis.md).

## Decision

1. **Price / volume analytics:** **1996–2025** (`year_from_price_only` … `year_to`).
2. **£/m² and Project G:** **2012–2025** (`year_from_epc_metrics` … `year_to`).
3. **Join prototyping first:** **2015–2025** (`year_from_join_prototype`) until match rate is accepted.
4. **Then backfill** PPD years **1996–2014** (`years_pending_ppd_backfill`) and re-run filters/aggregates; verify pipeline still works.
5. Dashboard/docs must **label clearly** which charts are price-only vs £/m².
6. **Inflation:** later — show **nominal and real** prices once a deflator method is chosen (`inflation` block in `configs/join.yaml`).

## Consequences

- Do not publish a 30-year £/m² gap chart.
- Scripts/default downloads should eventually cover 1996–2025; join work stays on 2015+ until unlocked.
- Avon breakup (1996) avoided by starting price-only at 1996; postcode filters still recommended as a cross-check.
