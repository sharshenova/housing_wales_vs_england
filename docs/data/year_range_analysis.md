# Which year range should we use?

**Date:** 2026-08-09  
**Status:** **accepted** — locked in [`configs/join.yaml`](../../configs/join.yaml) and [decision 002](../decisions/002-year-windows-option-a.md)

## Why we currently have 2015–2025 only

That was a **bootstrap choice**, not a research conclusion:

- Faster first pipeline (download + filter) while scaffolding the repo
- `configs/join.yaml` originally aimed at ~2010+; we started mid-decade for speed
- Enough years for a first Tableau story, but **not** the best final window for Project F/G

We can extend easily: yearly PPD files download in minutes; four-city filtered parquet stays small.

---

## Factor 1 — EPC availability (binds £/m² and Project G)

| Fact | Implication |
|------|-------------|
| EPCs became mandatory on sale/rent around **2007–08** | Almost no floor-area data for sales before then |
| Official stats / register open data quality from **Q4 2008** (1 Oct 2008+) | Pre-2008 EPC open data is weak or unpublished |
| Current MHCLG bulk service copy often says certificates **since 2012** | Practical bulk download for us may start **2012**, not 1995 |
| Match rule: EPC near sale date (we prefer before sale) | Sales in 2010 can use a 2008–12 certificate; sales in 2000 cannot get a contemporary EPC |

**Hard constraint for £/m² and modelling:**

- Credible **£/m² time series** ≈ sales from **~2012 (or late 2008 if we obtain those certificates)** onward  
- **1995–2008/11 sales:** Price Paid only (no reliable size adjustment)

Do **not** promise a 30-year £/m² gap chart. Promise a **long price gap** + a **shorter £/m² gap**.

---

## Factor 2 — Data consistency (PPD, geography, definitions)

### Price Paid

- Exists from **1 Jan 1995**; methodology is stable enough for medians by type/area.
- **Category B** (additional PPD: some BTL, repossessions, “Other”, etc.) only from **Oct 2013**. Prefer **Category A** for clean residential comps across the whole period.
- Recent months are incomplete (registration lag) — treat latest year cautiously.
- Postcodes are as at transaction time; they are not retro-corrected.

### Local authority names (important for our four cities)

- **Bath and North East Somerset** and current **City of Bristol** geography come from the **abolition of Avon on 1 Apr 1996**.
- PPD keeps the **district name at the time of sale** and does **not** rewrite history when boundaries change.
- Filtering only on today’s district strings (`CITY OF BRISTOL`, `BATH AND NORTH EAST SOMERSET`) will **miss or mis-assign 1995–early 1996** (and any renamed periods).
- **Swansea** / **Cardiff** as unitary names are more stable in the modern period, but long history still benefits from **postcode-area filters** (SA*, CF*, BS*, BA*) as a cross-check.

**Practical rule:** for anything before ~2000 (especially Bath/Bristol), prefer **postcode-based city assignment**, not district name alone.

### EPC field consistency

- Floor area / room definitions and SAP methodology have evolved; early certificates are noisier.
- Expired certificates are valid for joining historical sales if dated near the sale.
- Always document match rate **by sale year** — expect lower match rates in the earliest £/m² years.

---

## Factor 3 — History worth showing (story, not noise)

Useful “regime” markers for a relocator / investor narrative:

| Period | Why it matters |
|--------|----------------|
| **1995–2007** | Long boom into GFC — **price-only** story if we extend PPD |
| **2008–09** | Global financial crisis; volumes/prices dip |
| **2013+** | Help to Buy / post-crisis recovery; Category B appears |
| **2016** | Brexit referendum — regional divergence interesting |
| **2020–21** | COVID + **stamp duty holiday** — volume spike, distorted comps |
| **2022–23** | Rate shock / cost-of-living — cooling; energy crisis links to EPC story |
| **2024–25** | Newer “normal” — good for “today’s value” KPIs |

For **Swansea vs Cardiff vs Bristol vs Bath**, the interesting comparative story in industry commentary is often **post-2015** Bristol/BANES premium vs Wales — but a longer price series makes the dashboard look more “official statistics” grade.

---

## Factor 4 — Space and compute

| Dataset | Rough size | On a MacBook |
|---------|------------|--------------|
| PPD yearly 2015–2025 (what we have) | ~1.9 GB raw | Fine |
| PPD full 1995–2025 | ~5 GB raw (official single file ~5.3 GB) | Fine if filtered year-by-year with DuckDB |
| Four-city filtered PPD 2015–2025 | ~0.2M rows / few MB parquet | Trivial |
| Four-city PPD 1995–2025 | ~2× rows order of magnitude still small | Trivial |
| Domestic EPC for 4 LAs | Largest extra download; still usually manageable if **LA-level** zips, not all-England | Fine if we don’t keep all-England unzipped forever |

**Bottleneck is not 30 years of PPD** — it is **EPC download + address join**, which does not get much harder if PPD goes back to 1995, because pre-EPC years simply won’t match.

---

## Factor 5 — Other issues

1. **Inflation:** compare **real** prices (CPIH/CPI deflator) for long gaps, not only nominal £.
2. **Composition bias:** city medians move if more flats sell one year — always split by property type; £/m² helps but needs EPC.
3. **BANES ≠ “Bath city”:** LA includes rural surrounds — for “Bath” branding, consider **BA1/BA2** (and maybe exclude far BA posts) as a sensitivity.
4. **Bristol urban area** spills into South Gloucestershire / North Somerset — out of scope unless we explicitly expand.
5. **Licence / address use:** OGL for PPD prices; address fields have Royal Mail/OS constraints for some reuses — fine for portfolio analytics with attribution.
6. **Tableau Public:** prefer yearly/city aggregates, not 200k+ raw rows in the extract.

---

## Recommended options

### Option A — Dual window (recommended)

| Layer | Years | Metrics |
|-------|-------|---------|
| **Price story (long)** | **1996–2025** (or 1995 with postcode filters) | Median price, volumes, YoY, gaps between cities (nominal + inflation-adjusted) |
| **£/m² & modelling** | **2012–2025** (fallback **2009–2025** if early EPCs available) | £/m², size bands, Project G features |

**Why best:** honest about EPC limits; still answers “30-year gap?” for **prices**; keeps F and G strong where size exists.

Start geography from **1996** to avoid Avon breakup mess, unless we invest in postcode mapping for 1995.

### Option B — EPC-era only (simpler)

**2009 or 2012 → 2025** for everything.

- Pros: one consistent period; every chart can mention size/EPC  
- Cons: weaker “long history” wow; misses 1990s–2000s boom/bust context  

Good if we want fastest path to one clean Tableau story.

### Option C — Truly 1995–2025 single narrative (not recommended as sole approach)

Possible for **price-only**. Misleading if we imply £/m² for the whole period.

### Option D — What we have now (2015–2025)

Fine for MVP dashboards and join prototyping; **too short** as the final “how gaps changed” answer once EPC works. Extend before polishing Tableau.

---

## Suggested decision for this portfolio

1. **Keep building the join on 2015–2025** (already on disk) until match rate looks good.  
2. **Then download PPD 1996–2014** (and 1995 if postcode filter is ready).  
3. **Publish two timeline lengths in the dashboard:**  
   - Page/section 1: price gaps **1996–2025**  
   - Page/section 2: £/m² gaps **2012–2025** (or first year with match rate ≥ warning threshold)  
4. **Project G training window:** sales with successful EPC join, likely **~2015–2023 train / 2024–25 test** (time-based), not 1995.

### Config (locked)

See `configs/join.yaml`: `year_from_price_only: 1996`, `year_from_epc_metrics: 2012`, `year_from_join_prototype: 2015`, `years_pending_ppd_backfill: 1996–2014`.

**Inflation:** planned later — nominal + real (deflator TBD, likely ONS CPIH); `inflation.enabled: false` until investigated.

---

## Bottom line

- **30-year £/m²:** not realistic — EPC doesn’t support it.  
- **~30-year price gaps:** yes, and disk/CPU are fine if we filter to four cities.  
- **Best combo:** **1996–2025 prices** + **2012–2025 £/m² (and G)** , with clear labels so recruiters see you understand data limitations.
