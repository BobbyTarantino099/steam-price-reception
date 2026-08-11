# Data source records — Steam case

## Source 1: Steam Games Dataset (fronkongames)

- **Origin:** third party — aggregator (Kaggle), built from the official Steam Web API +
  SteamSpy (unofficial "owners" estimates).
- **URL or location:** kaggle.com/datasets/fronkongames/steam-games-dataset
- **Download date:** 2026-07-28
- **Licence:** CC BY 4.0 — allows use and redistribution with attribution. Cited in the public
  README.
- **Period covered:** 1997-06-30 to 2026-12-01 (includes 2 games with a future release date, not
  yet published as of the download date).
- **Granularity:** one row = one game (unique `AppID`) listed on the Steam store.
- **Volume:** 125,855 rows × 40 real columns (the raw header declares 39 — see bug below).
- **Format:** CSV, ~400 MB.

### ROCCC
| Letter | Assessment | Detail |
|---|---|---|
| **R**eliable | Medium | `price`, `positive`/`negative` come from the official Steam API (reliable). `estimated_owners` comes from SteamSpy, which estimates algorithmically, not from real sales confirmed by Valve. |
| **O**riginal | Medium-low | It's a third-party source (aggregator), not a direct download from Valve. It's traceable: the dataset itself documents that it combines the Steam Web API + SteamSpy. |
| **C**omprehensive | High for this question | Contains `price`, `genres`, `positive`, `negative`, which is everything the Phase 1 question requires. Missing: dated individual reviews (only the per-game cumulative total). |
| **C**urrent | High | Downloaded the same day as the analysis; the dataset is updated periodically at the source. |
| **C**ited | High | Public Kaggle listing with methodology, author and licence declared. |

**Declared failures:** Originality (third party, not straight from Valve) and partial reliability
of `estimated_owners` (an estimated range, not a Valve-confirmed exact figure). Both are
documented as limitations in the report; neither disqualifies the source.

- **PII present:** No. This is game catalogue metadata, no personal user data.
- **Security:** static downloaded file, lives locally in `datos/crudos/`, no credentials or live
  API involved.
- **Accessibility / reproducibility:** the raw file (~400 MB) is not uploaded to the public
  portfolio repository. The public README links directly to the Kaggle source so anyone can
  reproduce the download. Decision confirmed with the user.

**Known limitations:**
1. **Confirmed header bug:** the raw header declares 39 column names, but every data row carries
   40 fields. The name `DiscountDLC count` at position 7 actually corresponds to two merged
   columns (`Discount` and `DLC count`), which misaligned everything after it. Fixed in this
   phase by inserting the missing name before loading (detail in the integrity check below).
   **This fix must be repeated identically in Phase 3 when loading the raw file — it is not
   fixed in the file itself, only diagnosed.**
2. `estimated_owners` comes in categorical ranges (e.g. "0 - 20000"), not a point figure.
3. No review text or individual review dates — this prevents measuring the real time evolution of
   sentiment; Phase 1 already adopted "game age" as a proxy.

---

## Source 2: CPI-U — US Bureau of Labor Statistics

- **Origin:** first party — US government agency (Bureau of Labor Statistics).
- **URL or location:** bls.gov/cpi/data.htm — series `CUUR0000SA0` (CPI-U, US city average, not
  seasonally adjusted, base 1982-84=100).
- **Download date:** pending — will be downloaded in Phase 3 when applying the adjustment.
- **Licence:** public domain (US government work).
- **Period covered:** 1913 to date (June 2026 available as of this record); comfortably covers
  the Steam catalogue's 1997-2026 range.
- **Granularity:** monthly index and annual average, aggregated US urban.
- **Volume:** one row per month/year published.
- **Format:** downloadable HTML table / plain text from BLS; also accessible via a public API.

### ROCCC
| Letter | Assessment | Detail |
|---|---|---|
| **R**eliable | High | Official, public, audited US government methodology. |
| **O**riginal | High | Direct primary source, not an aggregator. |
| **C**omprehensive | High for this use | Only the general annual index is needed to deflate prices; CPI-U covers it. |
| **C**urrent | High | Published monthly; the most recent figure is April 2026. |
| **C**ited | High | Public methodology documentation at bls.gov. |

**Approved by the user on 2026-07-28** as the second source for the Phase 1 inflation adjustment
(inflation-adjusted price). Fails no ROCCC letter.

- **PII present:** No.
- **Licence / privacy / security / accessibility:** no restrictions — public domain, freely
  downloadable, anyone can reproduce the access.
