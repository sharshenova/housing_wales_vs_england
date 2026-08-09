# AGENTS.md — City Value Housing

Portfolio project for Maria Sharshenova: compare **Swansea, Cardiff, Bristol, Bath** house-sale value for relocating professionals, then (if the join is strong) predict prices.

Career context and full portfolio list: [`../plans/portfolio_career_strategy.md`](../plans/portfolio_career_strategy.md).  
Housing idea brainstorm (A–H): [`../plans/uk_wales_housing_project_ideas.md`](../plans/uk_wales_housing_project_ideas.md).  
**Year windows & data limitations (must keep in mind):** [`docs/data/year_range_analysis.md`](docs/data/year_range_analysis.md) — locked in [`configs/join.yaml`](configs/join.yaml) / [decision 002](docs/decisions/002-year-windows-option-a.md).

## Goals (do not lose these)

1. **Project F (primary, now):** analytics + Tableau story answering value-for-money across the four cities, using **£/m²** from Price Paid ↔ EPC — not raw medians alone. Label price-only vs £/m² charts clearly.
2. **Project G (next):** reuse the same linked dataset for a time-aware sale-price model — only after join quality is documented and acceptable.
3. Showcase **Python + SQL/DuckDB pipelines**, clear business recommendations, and reproducible open-data work for Swansea/Cardiff hiring.

## Locked analysis windows (Option A)

| Layer | Years | Config keys |
|-------|-------|-------------|
| Price / volume | **1996–2025** | `year_from_price_only` … `year_to` |
| £/m² + modelling | **2012–2025** | `year_from_epc_metrics` … `year_to` |
| Join prototype (now) | **2015–2025** | `year_from_join_prototype`; `use_prototype_window: true` |
| PPD still to download | **1996–2014** | `years_pending_ppd_backfill` |

**Workflow:** prove EPC join on 2015–2025 → accept match rate → backfill 1996–2014 → re-filter / re-aggregate → confirm everything still works.  
**Inflation (later):** nominal **and** real prices (`inflation` in `join.yaml`; method TBD, likely ONS CPIH).

## Agent workflow

### Start of each session

1. Read [docs/PROGRESS.md](docs/PROGRESS.md) — phase, blockers, next steps.
2. Skim [docs/data/year_range_analysis.md](docs/data/year_range_analysis.md) when touching years, £/m², or dashboard labels.
3. Read [docs/GOALS.md](docs/GOALS.md) if scope is unclear.
4. Treat `docs/` as source of truth — do not assume prior chat context.

### End of each session

1. Update [docs/PROGRESS.md](docs/PROGRESS.md) (what changed, next steps).
2. If a major decision was made, add `docs/decisions/NNN-title.md`.
3. If a data download/join run finished, note match rates and file paths in PROGRESS or `docs/data/`.

## Commands

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

pytest
ruff check src/ tests/
ruff format src/ tests/
```

## Project structure

```
src/city_value/   # Importable package — reusable logic
configs/          # Cities, paths, join parameters
scripts/          # CLI entry points (download, join, aggregate)
notebooks/        # Exploration only
data/raw|interim|processed|external  # Gitignored data
docs/             # Progress, goals, decisions, data notes
tests/
tableau/          # Exports / notes for Tableau Public (no huge extracts in git)
```

## Code conventions

- Type hints on public functions.
- No hardcoded absolute paths — use `pathlib` relative to project root / config.
- Logic in `src/city_value/`; scripts are thin wrappers; notebooks are exploratory.
- `snake_case` files/functions; `PascalCase` classes.
- Add dependencies to `pyproject.toml` before importing new packages.
- Fixed seed `SEED=42` for any modelling (Project G).

## Data and licensing (non-negotiable)

- **Never commit** full Price Paid / EPC dumps (large). Keep `data/` gitignored.
- Document provenance and **Open Government Licence** attribution for HM Land Registry Price Paid.
- EPC open data: follow EPC Open Data Communities terms; document in `docs/data/`.
- Prefer yearly Price Paid files filtered to the four cities over the full 5GB dump when possible.

## What NOT to do

- Do not invent match rates or price statistics — compute or cite.
- Do not claim £/m² (or size-based insights) for years before `year_from_epc_metrics` (2012).
- Do not forget PPD backfill **1996–2014** after the join prototype is accepted.
- Do not start Project G modelling until Project F join quality is accepted in PROGRESS.
- Do not commit unless the user explicitly asks.
- Do not expand to all of England/Wales until the four-city pipeline works.
