"""HM Land Registry Price Paid helpers."""

from __future__ import annotations

# Standard column order for Price Paid CSV (no header in official downloads).
# https://www.gov.uk/guidance/about-the-price-paid-data
PPD_COLUMNS: list[str] = [
    "transaction_id",
    "price",
    "date_of_transfer",
    "postcode",
    "property_type",
    "old_new",
    "duration",
    "paon",
    "saon",
    "street",
    "locality",
    "town_city",
    "district",
    "county",
    "ppd_category_type",
    "record_status",
]
