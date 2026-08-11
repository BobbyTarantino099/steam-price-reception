# Data dictionary — Steam Games Dataset

Corrected header (see the header bug in `fichas-de-fuente.md`). Nulls calculated over the 125,855
rows after the correction. Columns marked **★** are the ones the Phase 1 analytical question
uses; the rest are documented for completeness but don't enter the analysis.

| Column | Type | Unit | Allowed values | Meaning | Nulls |
|---|---|---|---|---|---|
| AppID ★ | integer | id | unique, > 0 | Unique identifier of the app on Steam | 0.00% |
| Name ★ | text | — | free | Game name | 0.00% (1 row) |
| Release date ★ | date | YYYY-MM-DD | 1997-06-30 to 2026-12-01 | Release date on Steam | 0.00% |
| Estimated owners | categorical (range) | games | e.g. "0 - 20000" | SteamSpy's estimate of the number of owners, in bands | 0.00% |
| Peak CCU | integer | players | ≥ 0 | Historical peak concurrent users | 0.00% |
| Required age | integer | years | 0-21 | Suggested/required minimum age | 0.00% |
| Price ★ | decimal | USD | ≥ 0, up to 999.98 | Current list price | 0.00% |
| Discount | integer | % | 0-100 | Discount active at extraction time | 0.00% |
| DLC count | integer | count | ≥ 0, up to 3703 | Number of downloadable content items | 0.00% |
| About the game | text | — | free | Store description of the game | 6.72% |
| Supported languages | text (list) | — | list e.g. `['English', ...]` | Supported interface languages | 0.00% |
| Full audio languages | text (list) | — | list e.g. `['English', ...]` | Languages with full dubbing/audio | 0.00% |
| Reviews | text | — | free | Featured review quotes (unstructured) | 90.32% |
| Header image | text (URL) | — | URL | Store header image | 0.06% |
| Website | text (URL) | — | URL | Official game website | 59.86% |
| Support url | text (URL) | — | URL | Support URL | 56.06% |
| Support email | text | — | email | Support email | 17.98% |
| Windows | boolean | — | True/False | Available on Windows | 0.00% |
| Mac | boolean | — | True/False | Available on Mac | 0.00% |
| Linux | boolean | — | True/False | Available on Linux | 0.00% |
| Metacritic score | integer | points | 0-97 (0 = no data) | Metacritic score if present | 0.00%* |
| Metacritic url | text (URL) | — | URL | Link to the Metacritic page | 96.62% |
| User score | integer | points | always 0 in this dataset | User score (not populated) | 0.00%* |
| Positive ★ | integer | reviews | ≥ 0 | Count of positive reviews | 0.00% |
| Negative ★ | integer | reviews | ≥ 0 | Count of negative reviews | 0.00% |
| Score rank | decimal | rank | — | Steam's internal ranking (nearly empty) | 99.97% |
| Achievements | integer | count | ≥ 0 | Number of achievements | 0.00% |
| Recommendations | integer | count | ≥ 0 | Steam recommendations | 0.00% |
| Notes | text | — | free | Developer notes/warnings | 81.48% |
| Average playtime forever | integer | minutes | ≥ 0 | Historical average playtime | 0.00% |
| Average playtime two weeks | integer | minutes | ≥ 0 | Average playtime, last 2 weeks | 0.00% |
| Median playtime forever | integer | minutes | ≥ 0 | Historical median playtime | 0.00% |
| Median playtime two weeks | integer | minutes | ≥ 0 | Median playtime, last 2 weeks | 0.00% |
| Developers | text | — | free, comma-separated | Developer studio(s) | 6.71% |
| Publishers | text | — | free, comma-separated | Publisher(s) | 7.09% |
| Categories | text (list) | — | free, comma-separated | Steam categories (e.g. Single-player) | 7.12% |
| Genres ★ | text (list) | — | free, comma-separated | Game genre(s) (1 to 19 per game, median ~3) | 6.69% |
| Tags | text (list) | — | free, comma-separated | Community-assigned tags | 33.77% |
| Screenshots | text (list of URLs) | — | URLs | Screenshots | 4.79% |
| Movies | — | — | — | Empty column (100% null) — candidate to drop in Phase 3 | 100.00% |

\* `Metacritic score` and `User score` have no technical nulls, but use `0` as a sentinel value
for "no data" (only 4,258 rows, 3.38%, have a real Metacritic score > 0). Documented here so
Phase 3 doesn't confuse "0 = bad score" with "0 = no data".

## Note on the header bug

The raw CSV header has 39 names while every data row carries 40 values. This happens because the
name `DiscountDLC count` (position 7) actually corresponds to two columns that were merged by
mistake: `Discount` and `DLC count`. This table already reflects the **corrected** header. The
detail of how it was diagnosed and the code snippet to reproduce the fix are in
`fichas-de-fuente.md`, and it will be repeated as the first step of Phase 3 (Process).
