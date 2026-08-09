# Project goals

## Portfolio outcomes

- One strong **analyst** piece: four-city value-for-money story with Tableau Public.
- One strong **data science** follow-on (same data): sale-price prediction with honest validation.
- Demonstrate problem-solving for Swansea/Cardiff employers (DVLA, NHS Wales, insurers, uni), not tutorial cleaning.

## Project F — City comparison (current)

**Cities:** Swansea, Cardiff, Bristol, Bath.

**Success looks like:**

- Reproducible Price Paid ↔ EPC join with documented match rate and rules.
- Aggregations: median price, £/m², volumes by city / property type / year / postcode district.
- **Dual timelines (Option A):** price/volume **1996–2025**; £/m² **2012–2025** — clearly labelled (see [year_range_analysis.md](data/year_range_analysis.md)).
- Tableau (or equivalent) story with headline KPIs, comparison, drill-down, recommendations.
- Short written insights a relocating professional can act on.
- Later: **nominal + inflation-adjusted (real)** price comparisons.

**Unlock for G:** join quality explicitly accepted in [PROGRESS.md](PROGRESS.md).  
**After join OK:** backfill PPD **1996–2014** and re-verify the pipeline.

## Project G — Price model (later)

- Time-based train/test on the linked table.
- Baseline + stronger model; MAE/MAPE/R²; residual maps.
- Model card with limitations.

## Out of scope (for now)

- Full England & Wales modelling before four cities work.
- Synthetic marketing data.
- SA1 rental scrape as the hero deliverable.
