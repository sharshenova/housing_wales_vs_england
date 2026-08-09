# Data notes

Raw and processed files live under `data/` (gitignored). Document every download here.

**Year windows & limitations:** [year_range_analysis.md](year_range_analysis.md) (Option A — locked). Config: [`configs/join.yaml`](../../configs/join.yaml).

## Expected layout

```
data/raw/ppd/          # Price Paid yearly CSVs/TXTs as downloaded
data/raw/epc/          # Domestic EPC extracts
data/interim/          # Filtered four-city Price Paid, cleaned addresses
data/processed/        # Linked PPD–EPC table, Tableau-ready aggregates
data/external/         # Lookups (NSPL, LA codes, IMD/WIMD) if used
```

## Sources

| Dataset | URL | Licence notes |
|---------|-----|---------------|
| Price Paid | https://www.gov.uk/government/statistical-data-sets/price-paid-data-downloads | OGL v3.0; Land Registry attribution required |
| Domestic EPC | https://epc.opendatacommunities.org/ | Open Data Communities terms; may need free API key |
| NSPL / postcode → LA | ONS | OGL |

## Attribution (publish on site / Tableau / README)

Contains HM Land Registry data © Crown copyright and database right. This data is licensed under the Open Government Licence v3.0.

## Join quality log

Record match rates after each join run (date, rows, % matched, method).
