# PPD ↔ EPC join report (2012–2025)

**Linked output:** `/Users/mashukan/Documents/1 Data Analytics/projects/portfolio_projects/city_value_housing/data/processed/ppd_epc_linked_2012_2025.parquet`
**Unmatched output:** `/Users/mashukan/Documents/1 Data Analytics/projects/portfolio_projects/city_value_housing/data/processed/ppd_epc_unmatched_2012_2025.parquet`

## Overall

| Metric | Value |
|--------|------:|
| PPD input rows | 251,821 |
| PPD matchable (postcode+PAON) | 251,733 |
| Excluded (no postcode/PAON) | 88 |
| EPC rows (area filter applied) | 412,680 |
| **Matched** | **169,100** |
| Unmatched | 82,633 |
| **Match rate** | **67.17%** |
| Tier full (address_key) | 167,739 |
| Tier loose (postcode\|saon\|paon) | 1,361 |
| £/m² p05 / median / p95 | 1,249 / 2,848 / 5,181 |

Threshold (`min_match_rate_warn`): **70%**

## Match rate by city

| City | Sales | Matched | Match rate |
|------|------:|--------:|-----------:|
| bath | 41,465 | 25,867 | 62.4% |
| bristol | 97,064 | 60,531 | 62.4% |
| cardiff | 70,139 | 49,723 | 70.9% |
| swansea | 43,065 | 32,979 | 76.6% |

## Match rate by year

| Year | Sales | Matched | Match rate |
|-----:|------:|--------:|-----------:|
| 2012 | 14,763.0 | 5,888.0 | 39.9% |
| 2013 | 17,196.0 | 10,025.0 | 58.3% |
| 2014 | 20,415.0 | 11,526.0 | 56.5% |
| 2015 | 19,927.0 | 11,459.0 | 57.5% |
| 2016 | 19,935.0 | 11,758.0 | 59.0% |
| 2017 | 19,657.0 | 12,181.0 | 62.0% |
| 2018 | 19,228.0 | 12,724.0 | 66.2% |
| 2019 | 18,055.0 | 12,936.0 | 71.7% |
| 2020 | 14,811.0 | 11,198.0 | 75.6% |
| 2021 | 21,733.0 | 16,980.0 | 78.1% |
| 2022 | 18,770.0 | 14,570.0 | 77.6% |
| 2023 | 15,139.0 | 12,044.0 | 79.6% |
| 2024 | 15,836.0 | 12,585.0 | 79.5% |
| 2025 | 16,268.0 | 13,226.0 | 81.3% |

## £/m² median by city (matched)

| City | Median £/m² | n |
|------|------------:|--:|
| bath | £3,571 | 25,867 |
| bristol | £3,370 | 60,531 |
| cardiff | £2,626 | 49,723 |
| swansea | £1,818 | 32,979 |

## Spot checks

### Sample matched rows (random 8)

| city | sale_date | price | m² | £/m² | tier | ppd street | epc address1 |
|---|---|---:|---:|---:|---|---|---|
| bristol | 2021-09-30 | £425,000 | 113 | £3,761 | full | PAINTWORKS | 313, Paintworks |
| cardiff | 2022-07-22 | £227,500 | 65 | £3,500 | full | LOFTUS STREET | 35 Loftus Street |
| cardiff | 2021-09-29 | £195,000 | 110 | £1,773 | full | LEAD STREET | 17 LEAD STREET |
| swansea | 2021-08-27 | £227,000 | 98 | £2,316 | full | MEGAN CLOSE | 6 MEGAN CLOSE |
| cardiff | 2024-07-26 | £150,000 | 51 | £2,941 | full | HENKE COURT | 100, Henke Court |
| swansea | 2021-01-22 | £290,995 | 112 | £2,598 | full | FFORDD MORIAH | 6, Ffordd Moriah |
| bath | 2019-11-22 | £199,950 | 63 | £3,174 | full | ABBEY VIEW | 4, Abbey View |
| swansea | 2023-09-25 | £190,000 | 131 | £1,450 | full | MILL STREET | 35, Mill Street |

### Sample unmatched (random 10)

| city | sale_date | postcode | paon | street | property_type |
|---|---|---|---|---|---|
| bristol | 2024-07-10 | BS3 1FT | REGENT HOUSE | LOMBARD STREET | F |
| swansea | 2016-08-19 | SA4 8QN | GRAIG FAWR |  | D |
| bath | 2017-10-25 | BA2 3DQ | WATERFRONT HOUSE 211 | LOWER BRISTOL ROAD | F |
| cardiff | 2015-05-05 | CF10 2FF | ALTOLUSSO | BUTE TERRACE | F |
| swansea | 2018-01-05 | SA4 9ZQ | 1 | FFORDD GER Y LLYN | T |
| bristol | 2019-02-01 | BS1 1UA | THE STEPS 17 | ST NICHOLAS STREET | F |
| cardiff | 2016-03-31 | CF14 5AZ | HOME LONG HOUSE | HEOL HIR | F |
| cardiff | 2013-06-28 | CF5 3DX | 291 | ST FAGANS ROAD | S |
| swansea | 2017-06-30 | SA5 4QE | 44 | CAMROSE DRIVE | T |
| cardiff | 2012-06-13 | CF10 4NQ | 89 | ADVENTURERS QUAY | F |

## Verdict

**Below threshold** — overall match rate 67.2% < 70%.
Iterate address normalisation / keys before accepting.

## City-year detail

| City | Year | Sales | Matched | Match rate |
|------|-----:|------:|--------:|-----------:|
| bath | 2012 | 2,526 | 931 | 36.9% |
| bath | 2013 | 2,931 | 1,540 | 52.5% |
| bath | 2014 | 3,362 | 1,823 | 54.2% |
| bath | 2015 | 3,392 | 1,820 | 53.7% |
| bath | 2016 | 3,301 | 1,866 | 56.5% |
| bath | 2017 | 3,012 | 1,826 | 60.6% |
| bath | 2018 | 3,092 | 2,001 | 64.7% |
| bath | 2019 | 2,871 | 1,941 | 67.6% |
| bath | 2020 | 2,564 | 1,764 | 68.8% |
| bath | 2021 | 3,723 | 2,612 | 70.2% |
| bath | 2022 | 2,943 | 2,058 | 69.9% |
| bath | 2023 | 2,442 | 1,806 | 74.0% |
| bath | 2024 | 2,567 | 1,833 | 71.4% |
| bath | 2025 | 2,739 | 2,046 | 74.7% |
| bristol | 2012 | 5,942 | 2,379 | 40.0% |
| bristol | 2013 | 6,856 | 3,826 | 55.8% |
| bristol | 2014 | 8,233 | 4,217 | 51.2% |
| bristol | 2015 | 7,992 | 4,269 | 53.4% |
| bristol | 2016 | 7,682 | 4,145 | 54.0% |
| bristol | 2017 | 7,691 | 4,342 | 56.5% |
| bristol | 2018 | 7,181 | 4,408 | 61.4% |
| bristol | 2019 | 6,582 | 4,398 | 66.8% |
| bristol | 2020 | 5,672 | 4,020 | 70.9% |
| bristol | 2021 | 8,487 | 6,200 | 73.0% |
| bristol | 2022 | 7,020 | 5,120 | 72.9% |
| bristol | 2023 | 5,764 | 4,230 | 73.4% |
| bristol | 2024 | 5,881 | 4,317 | 73.4% |
| bristol | 2025 | 6,081 | 4,660 | 76.6% |
| cardiff | 2012 | 3,942 | 1,567 | 39.8% |
| cardiff | 2013 | 4,646 | 2,923 | 62.9% |
| cardiff | 2014 | 5,717 | 3,424 | 59.9% |
| cardiff | 2015 | 5,410 | 3,222 | 59.6% |
| cardiff | 2016 | 5,529 | 3,346 | 60.5% |
| cardiff | 2017 | 5,470 | 3,555 | 65.0% |
| cardiff | 2018 | 5,617 | 3,821 | 68.0% |
| cardiff | 2019 | 5,446 | 4,067 | 74.7% |
| cardiff | 2020 | 3,983 | 3,236 | 81.2% |
| cardiff | 2021 | 5,733 | 4,875 | 85.0% |
| cardiff | 2022 | 5,488 | 4,478 | 81.6% |
| cardiff | 2023 | 4,193 | 3,544 | 84.5% |
| cardiff | 2024 | 4,481 | 3,814 | 85.1% |
| cardiff | 2025 | 4,484 | 3,851 | 85.9% |
| swansea | 2012 | 2,353 | 1,011 | 43.0% |
| swansea | 2013 | 2,763 | 1,736 | 62.8% |
| swansea | 2014 | 3,103 | 2,062 | 66.5% |
| swansea | 2015 | 3,133 | 2,148 | 68.6% |
| swansea | 2016 | 3,423 | 2,401 | 70.1% |
| swansea | 2017 | 3,484 | 2,458 | 70.5% |
| swansea | 2018 | 3,338 | 2,494 | 74.7% |
| swansea | 2019 | 3,156 | 2,530 | 80.2% |
| swansea | 2020 | 2,592 | 2,178 | 84.0% |
| swansea | 2021 | 3,790 | 3,293 | 86.9% |
| swansea | 2022 | 3,319 | 2,914 | 87.8% |
| swansea | 2023 | 2,740 | 2,464 | 89.9% |
| swansea | 2024 | 2,907 | 2,621 | 90.2% |
| swansea | 2025 | 2,964 | 2,669 | 90.0% |
