# Cleaning log — Steam case (price and reception)

**Input dataset:** `datos/crudos/steam_fronkongames_catalogo-historico_2026-07-28.csv` — 125,855 rows
**Output datasets:**
- `datos/limpios/steam_juegos_limpios.csv` — 117,430 rows (1 row = 1 game)
- `datos/limpios/steam_juegos_por_genero.csv` — 338,575 rows (1 row = 1 game × genre)

**Tool:** Python (pandas), justified in Phase 0: reproducibility over a 400 MB file with a
structural flaw (header bug) that requires a script, not manual review.

**Second source incorporated:** BLS annual CPI-U
(`datos/crudos/bls_cpi-u_anual_1997-2026_2026-07-28.csv`), approved in Phase 2, used for the
inflation adjustment.

Full script: `notebooks/procesar.py`.

## Transformations

### T1 — Fixed the header bug
- **What:** the raw header declares 39 column names; every row carries 40 values. The name
  `DiscountDLC count` (position 7) merges two real columns: `Discount` and `DLC count`.
- **Why:** without fixing this, every column from `About the game` onward is misaligned with its
  real data (confirmed in Phase 2: `About the game` showed `'0'` instead of descriptive text).
- **How:** inserted the missing name into the column list before loading the CSV
  (`header=None, names=cols_fixed, skiprows=1`), instead of letting pandas infer the header.
- **Rows affected:** all 125,855, every one was misaligned.
- **Alternative discarded:** trimming the `About the game` column (long text) to "realign" —
  discarded because it doesn't address the root cause and breaks on any row with unescaped
  commas.

### T2 — Date typing and exclusion of future releases
- **What:** `Release date` from text to `datetime`; exclusion of games with a release date after
  the download date (2026-07-28).
- **Why:** 2 games have a future (planned) release date and 0 reviews — they don't yet represent
  a real "reception" case and shouldn't count as observed population.
- **How:** `pd.to_datetime(errors='coerce')` + filter `Release date <= download_date`.
- **Rows affected:** 2 removed (0 unparseable dates).
- **Alternative discarded:** keeping them with 0 reviews — discarded because it would skew any
  average % of positive reviews downward for no real reason.

### T3 — Dropped out-of-scope columns
- **What:** dropped 15 columns: `Movies`, `Score rank`, `Metacritic url`, `Reviews`, `Notes`,
  `Website`, `Support url`, `Support email`, `About the game`, `Supported languages`,
  `Full audio languages`, `Screenshots`, `Header image`, `Categories`, `Tags`.
- **Why:** either they don't contribute to the question (price, genre, reviews), or have nulls
  between 34% and 100% (`Movies` 100%, `Score rank` 99.97%), or are unstructured free text this
  case doesn't analyse.
- **How:** `df.drop(columns=[...])`.
- **Rows affected:** none (this drops columns, not rows).
- **Alternative discarded:** keeping `Tags` for a text analysis — discarded as out of scope
  (outside the Phase 1 question); left as a "desirable additional data" item for Phase 6.

### T4 — Duplicates by `AppID`
- **What:** duplicate check using `AppID` as the key.
- **Why:** `AppID` is Steam's declared unique identifier; 0 duplicates had already been verified
  in Phase 2, reconfirmed after the transformations above.
- **How:** `duplicated(subset=['AppID'])`.
- **Rows affected:** 0.
- **Alternative discarded:** N/A, no duplicates to resolve.

### T5 — Excluded games with no genre
- **What:** 8,423 games (6.69% of the catalogue after T2) have no genre assigned on Steam.
- **Why:** the analytical question requires classifying by genre; a game with no genre can't be
  placed in any genre × price-band combination.
- **How:** `df[df['Genres'].notna()]`.
- **Rows affected:** 8,423 removed.
- **Alternative discarded:** imputing a generic genre ("Unclassified") — discarded because it
  would invent a category Steam never assigned and distort that category's count.

### T6 — Enrichment with CPI-U (BLS) and inflation-adjusted price
- **What:** joined the catalogue with BLS's annual CPI-U index by release year, and calculated
  `precio_ajustado_usd = Price × (CPI_2026 / CPI_release_year)`, with base year = 2026 (the most
  recent in the dataset, per the metric defined in Phase 1).
- **Why:** without this adjustment, comparing a 1997 game's price with a 2026 game's price
  understates the real value paid for the older games.
- **How:** `merge` by year + a vectorised formula; verified with an `assert` that the merge
  didn't duplicate rows (confirmed: 0 games were left without a matching CPI value).
- **Rows affected:** the remaining 117,430, all received an adjusted price.
- **Declared limitation:** the 2026 CPI (base year) is a **partial average** of only 4 months
  (January-April), the only data available as of the download date. The 2025 figure uses 11
  months (October wasn't published due to a US government shutdown). This introduces a minor
  margin of imprecision in the adjusted prices of the most recent games; declared in the case's
  README.
- **Alternative discarded:** waiting for BLS to publish the full 2026 year — discarded due to
  project timeline; declaring the limitation was preferred.

### T7 — Calculated % positive reviews
- **What:** `pct_resenas_positivas = Positive / (Positive + Negative) × 100`, as defined in
  Phase 1.
- **Why:** it's the case's central "reception" metric.
- **How:** vectorised calculation; the 34,589 games with 0 total reviews are left as `NaN`
  instead of 0%, to avoid confusing "no data" with "neutral reception".
- **Rows affected:** all 117,430, of which 34,589 are left without a value (correctly, as null).
- **Alternative discarded:** assigning 0% to games with no reviews — discarded because 0% would
  imply "negative reception", when in reality it's "no evidence".

### T8 — Exploded by genre (derived dataset)
- **What:** generated `steam_juegos_por_genero.csv`, where each game with N genres produces N
  rows (one per genre), from `steam_juegos_limpios.csv`.
- **Why:** decision confirmed with the user to answer the "genre and price-band combinations"
  question — a game with several genres contributes evidence to each one.
- **How:** `Genres.str.split(',')` + `explode()`.
- **Rows affected:** 117,430 games produce 338,575 game-genre rows (the same game can appear in
  several genres — they are not mutually exclusive, and this is explicitly stated so Phase 4
  doesn't interpret per-genre counts as a unique-game population).
- **Alternative discarded:** keeping only the primary genre or only mono-genre games — both
  evaluated and discarded by the user in Phase 2.

## Note for Phase 4 (does not block closing this phase)

Steam's `Genres` column mixes, under the same label, actual genres (`Action`, `RPG`, `Strategy`)
with content descriptors/business model tags (`Violent`, `Gore`, `Free To Play`, `Early Access`,
`Nudity`). There are 33 unique values in total. This isn't a data error — it's Steam's real
taxonomy — but Phase 4 will need to decide whether to exclude or handle separately the tags that
aren't genres in the strict sense, to avoid comparing apples to oranges when recommending "which
genre to invest in".

## Reconciliation
| Item | Rows |
|---|---|
| Initial (after fixing the header) | 125,855 |
| Removed for future release date | 2 |
| Removed for `AppID` duplicates | 0 |
| Removed for no genre assigned | 8,423 |
| **Final (`steam_juegos_limpios.csv`)** | **117,430** |
| Rows after exploding by genre (`steam_juegos_por_genero.csv`) | 338,575 |

Verified with an `assert` in the script: `125,855 − 2 − 0 − 8,423 == 117,430`. ✅

## Post-cleaning verification
- [x] Counts check out (`assert` in `procesar.py`).
- [x] Standardised categories (genres) are the 33 expected from Steam's taxonomy.
- [x] Plausible numeric ranges: no negative prices or reviews; `AppID` remains unique.
- [x] Process reproducible from the raw file (`procesar.py` runs end to end with no manual
      editing).
- [x] The clean dataset still answers the question: 117,430 games remain with genre, price and
      reviews; 10,479 pass the ≥500-review filter to be applied in Phase 4, and 99,085 are paid
      (`Price > 0`) — enough volume for price quartiles.
