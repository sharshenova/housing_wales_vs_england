# City Value Housing

Compare **Swansea, Cardiff, Bristol, and Bath** for relocating professionals: what do you get for your money in house sales, especially on a **£/m²** basis?

Built as a portfolio project (Python + DuckDB/SQL + Tableau Public), with a reusable **Price Paid ↔ EPC** join aimed at a later price-prediction model.

## Audience & questions

**Audience:** people relocating for work comparing two Welsh and two English cities.

1. For terraced / semi (and by size via EPC), what do you get in each city?
2. How has the price / £/m² gap changed over ~10–15 years?
3. Which postcode districts punch above their weight on value?

## Status

See [docs/PROGRESS.md](docs/PROGRESS.md). Goals and agent workflow: [AGENTS.md](AGENTS.md), [docs/GOALS.md](docs/GOALS.md).

**Analysis windows (Option A):** price/volume **1996–2025**; £/m² **2012–2025** (join prototype on **2015–2025** first). Details and limitations: [docs/data/year_range_analysis.md](docs/data/year_range_analysis.md).

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Data sources

- [HM Land Registry Price Paid Data](https://www.gov.uk/government/statistical-data-sets/price-paid-data-downloads) (Open Government Licence)
- [Domestic Energy Performance Certificates](https://epc.opendatacommunities.org/)
- Optional later: ONS affordability, WIMD/IMD

Attribution (Price Paid): Contains HM Land Registry data © Crown copyright and database right. Licensed under the Open Government Licence v3.0.

## Repo layout

| Path | Role |
|------|------|
| `src/city_value/` | Reusable pipeline code |
| `scripts/` | Download / join / aggregate CLIs |
| `configs/` | Cities and join parameters |
| `docs/` | Progress, goals, decisions |
| `notebooks/` | Exploration only |
| `data/` | Local data (gitignored) |

## Related plans

- [Portfolio career strategy](../plans/portfolio_career_strategy.md)
- [Housing idea brainstorm](../plans/uk_wales_housing_project_ideas.md)
