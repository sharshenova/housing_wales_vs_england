# 001 — Four cities, Project F then G

**Date:** 2026-08-07  
**Status:** accepted

## Context

Portfolio needs a strong housing analytics project. SA1 rental scrape is geographically biased. Price Paid + EPC enables £/m² and later modelling.

## Decision

1. Compare **Swansea, Cardiff, Bristol, Bath** (two popular Welsh + two popular English cities).
2. Ship **Idea F** (value-for-money analytics + dashboards) first.
3. Design the Price Paid ↔ EPC join so **Idea G** (price prediction) can reuse it.
4. Do not start G until join quality is documented and accepted in PROGRESS.

## Consequences

- Scope stays manageable vs all-Wales / all-England.
- Join quality is the critical path; match-rate reporting is mandatory.
- Tableau story is the F deliverable; modelling is explicitly phase two.
