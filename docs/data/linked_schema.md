# Linked PPD–EPC schema (analysis table)

**File:** `data/processed/ppd_epc_linked_2012_2025.parquet`  
**Grain:** one row = one matched Price Paid sale + one chosen EPC  
**Window:** £/m² metrics **2012–2025** (Category A, types D/S/T/F)  
**Runbook:** [join_epc_metrics_2012_2025_run.md](join_epc_metrics_2012_2025_run.md) · join QA: [join_match_report_2012_2025.md](join_match_report_2012_2025.md)

| Column | Source | Meaning | Project F (Tableau) | Project G (model) |
|--------|--------|---------|---------------------|-------------------|
| `transaction_id` | PPD | Sale record id | Join key / counts | ID |
| `price` | PPD | Sale price (£) | KPIs, distributions | Target (or log) |
| `date_of_transfer` / `sale_date` | PPD | Completion date | Time filters | Time split |
| `sale_year` | derived | Calendar year | Trends | Feature |
| `sale_quarter` | derived | e.g. `2020Q1` | Seasonality | Feature |
| `postcode` / `postcode_norm` | PPD | Postcode | Detail | — |
| `postcode_district` | derived | Outward code (e.g. CF10) | Maps / drill-down | Feature |
| `property_type` | PPD | D/S/T/F/O code | Filter | Feature |
| `property_type_label` | derived | Readable type label | Charts | — |
| `old_new` | PPD | Y new-build / N existing | Filter | — |
| `is_new_build` | derived | Boolean from `old_new` | Filter | Feature |
| `duration` | PPD | F freehold / L leasehold | Filter | — |
| `is_leasehold` | derived | Boolean from `duration` | Filter | Feature |
| `paon` / `saon` / `street` | PPD | Address parts | QA | — |
| `city` / `city_label` | derived | Project city | Core breakdown | Feature |
| `district` / `town_city` | PPD | LA / town at sale | Context | — |
| `ppd_category_type` | PPD | A/B (we use A) | QA | — |
| `total_floor_area` | EPC | Internal floor area m² | Size context | Feature |
| `floor_area_band` | derived | &lt;50 … 150+ m² | Segmented £/m² | Feature |
| `number_habitable_rooms` | EPC | Habitable rooms (nullable) | Size context | Feature |
| `habitable_rooms_band` | derived | 1–2 … 6+ / Unknown | Segmented value | Feature |
| `price_per_m2` | derived | `price / total_floor_area` | **Core KPI** | Optional target |
| `current_energy_rating` | EPC | A–G letter | EPC breakdowns | Feature |
| `current_energy_efficiency` | EPC | 1–100 numeric score | Finer EPC view | Feature |
| `built_form` | EPC | e.g. Mid-Terrace, Detached | Typology | Feature |
| `construction_age_band` | EPC | Building age band | Stock mix | Feature |
| `epc_property_type` | EPC | House/Flat/Bungalow/… | Cross-check vs PPD | Feature |
| `epc_date` | EPC | Certificate date used in join | Freshness | — |
| `delta_days` | derived | EPC date − sale date (days) | QA | — |
| `epc_years_before_sale` | derived | Years EPC precedes sale | Freshness filter | Feature |
| `join_tier` | derived | `full` or `loose` match | QA / sensitivity | — |
| `certificate_number` | EPC | Certificate id | Traceability | — |
| `epc_uprn` | EPC | UPRN if present | Future joins | — |
| `epc_address1` / `epc_address2` | EPC | EPC address lines | Spot checks | — |
| `address_key` / `loose_key` | derived | Join keys | QA | — |

## Notes

- Prefer **£/m² within `floor_area_band` / `property_type_label`** for fairer city comparisons.
- `number_habitable_rooms` is missing for ~11% of EPCs → use `habitable_rooms_band = Unknown`.
- Do not claim £/m² for unmatched sales; price-only series uses PPD without these EPC fields.
