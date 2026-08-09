# PPD join prep report (2012–2025)

**Output:** `/Users/mashukan/Documents/1 Data Analytics/projects/portfolio_projects/city_value_housing/data/interim/ppd_join_2012_2025.parquet`
**Source:** `/Users/mashukan/Documents/1 Data Analytics/projects/portfolio_projects/city_value_housing/data/interim/ppd_four_cities.parquet`

## Filters applied

- Years: **2012–2025**
- PPD category: **A**
- Property types: `D, S, T, F`

## Totals

| Metric | Value |
|--------|------:|
| Rows | **251,821** |
| Unique address_key | 190,724 |
| Missing postcode | 88 (0.03%) |
| Price min / median / max | £500 / £239,950 / £20,000,000 |

## Rows by city

| City | Rows |
|------|-----:|
| bath | 41,478 |
| bristol | 97,101 |
| cardiff | 70,163 |
| swansea | 43,079 |

## Rows by property type

| Type | Rows |
|------|-----:|
| D | 35,213 |
| F | 62,286 |
| S | 61,695 |
| T | 92,627 |

## Rows by city and year

| City | Year | Rows |
|------|-----:|-----:|
| bath | 2012 | 2,527 |
| bath | 2013 | 2,932 |
| bath | 2014 | 3,365 |
| bath | 2015 | 3,393 |
| bath | 2016 | 3,302 |
| bath | 2017 | 3,012 |
| bath | 2018 | 3,092 |
| bath | 2019 | 2,872 |
| bath | 2020 | 2,565 |
| bath | 2021 | 3,723 |
| bath | 2022 | 2,943 |
| bath | 2023 | 2,442 |
| bath | 2024 | 2,568 |
| bath | 2025 | 2,742 |
| bristol | 2012 | 5,942 |
| bristol | 2013 | 6,858 |
| bristol | 2014 | 8,237 |
| bristol | 2015 | 7,994 |
| bristol | 2016 | 7,692 |
| bristol | 2017 | 7,691 |
| bristol | 2018 | 7,184 |
| bristol | 2019 | 6,585 |
| bristol | 2020 | 5,674 |
| bristol | 2021 | 8,488 |
| bristol | 2022 | 7,020 |
| bristol | 2023 | 5,765 |
| bristol | 2024 | 5,885 |
| bristol | 2025 | 6,086 |
| cardiff | 2012 | 3,942 |
| cardiff | 2013 | 4,646 |
| cardiff | 2014 | 5,721 |
| cardiff | 2015 | 5,413 |
| cardiff | 2016 | 5,531 |
| cardiff | 2017 | 5,472 |
| cardiff | 2018 | 5,618 |
| cardiff | 2019 | 5,447 |
| cardiff | 2020 | 3,987 |
| cardiff | 2021 | 5,735 |
| cardiff | 2022 | 5,490 |
| cardiff | 2023 | 4,193 |
| cardiff | 2024 | 4,483 |
| cardiff | 2025 | 4,485 |
| swansea | 2012 | 2,355 |
| swansea | 2013 | 2,765 |
| swansea | 2014 | 3,104 |
| swansea | 2015 | 3,134 |
| swansea | 2016 | 3,423 |
| swansea | 2017 | 3,486 |
| swansea | 2018 | 3,340 |
| swansea | 2019 | 3,157 |
| swansea | 2020 | 2,593 |
| swansea | 2021 | 3,791 |
| swansea | 2022 | 3,319 |
| swansea | 2023 | 2,740 |
| swansea | 2024 | 2,907 |
| swansea | 2025 | 2,965 |

## Columns added

- `city`, `city_label`, `sale_year`
- `postcode_norm`, `address_key`

## Verdict

**Pass** — PPD join table (2012–2025) is ready for EPC join.
