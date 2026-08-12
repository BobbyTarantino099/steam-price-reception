# Case: Price and reception on Steam (video game investment case)

**Status:** Phase 7 — Portfolio (case published; presentation rehearsal pending)
**Last updated:** 2026-08-10

## 0. Choose (decision sheet)

**Date:** 2026-07-28

### The case
- **Sector / fictional client:** Investment fund evaluating entry into the video game sector,
  using the Steam market as a proxy for the PC/digital market.
- **Business problem in one sentence:** Which genre and price-band combinations on Steam achieve
  the best reception (reviews) without sacrificing price, and which genres are therefore the
  better investment candidates?
- **Concrete decision this enables:** Recommend which genre(s) the fund should prioritise for its
  investment thesis (e.g. studios or publishers in that genre).
- **Presentation audience:** Portfolio / recruiters (skill-demonstration case).

### The data
- **Candidate source:** Steam Games Dataset (fronkongames), Kaggle / Hugging Face.
- **Licence:** CC BY 4.0 — requires attribution in the public README.
- **Period and volume:** 125,855 games published on Steam, full historical catalogue up to the
  collection date (dataset with periodic updates).
- **Initial integrity check:** ⚠️ verified only at the metadata level (columns, licence, volume,
  provenance via official API + SteamSpy). Real null counts, duplicates and key uniqueness are
  pending the full check in Phase 2, once the file is loaded. Two known caveats up front:
  1. The raw CSV has a header bug that misaligns the columns after `Discount`/`DLC count`.
  2. `estimated_owners` comes in ranges, not an exact figure.
- **Does it contain the fields the question requires?** Yes — `price`, `genres`,
  `positive`/`negative` (reviews). Missing: dated individual reviews (only a per-game aggregate),
  so "sustaining price over time" will be analysed via game age, not the real evolution of
  reviews.

### Calibration
- **Effort estimate:** ~1 week of focused work.
- **Does it support a 30-minute presentation?** Yes.
- **Is there real cleaning to document?** Yes — header bug, zero prices for F2P to handle
  separately, possible nulls in tags/genres, potential duplicates from re-releases.

### Fit in the portfolio
- **What it demonstrates that my other cases don't:** It's the first case, so it sets the
  baseline: turning an investment question into a pricing + sentiment analysis, with
  Python/pandas, on a dataset with a real structural flaw (not just trivial nulls).
- **Main tool:** Python (pandas).
- **Dataset saturation level:** Medium.

### Decision
- [x] Proceed
- [ ] Discarded — reason:

**Phase 0 exit gate:** ✅ complete (approved by the user on 2026-07-28).

---

## 1. Ask

**Status:** ✅ closed (approved by the user on 2026-07-28)

- **Business problem:** A video-game-focused investment fund has no data-driven basis for
  deciding which genre to prioritise for its investment thesis in the PC/Steam market.
- **Analytical question (SMART):** Which genre and price-band combinations (inflation-adjusted
  price quartiles, calculated on paid games with ≥500 reviews) in Steam's historical catalogue
  show the most consistent pattern of high positive-review %, controlling for game age?
- **Decision this unlocks:** Recommend 2-3 genres where the committee should prioritise
  investment due diligence, with evidence of which price band sustains the best reception in
  each.
- **Problem type:** Find patterns.

- **Stakeholders:**

| Who | What they decide / need | Format |
|---|---|---|
| Investment committee (primary) | Decides where to prioritise due diligence; needs a clear recommendation with evidence and risks | ~30 min presentation + executive summary |
| Senior analyst (secondary) | Validates method, cleaning and assumptions | Cleaning log + technical documentation (notebook) |

- **Metrics:**

| Metric | Formula | Unit | Granularity | Window |
|---|---|---|---|---|
| % positive reviews | `positive / (positive + negative) × 100` | Percentage | Per game | Historical cumulative as of the dataset collection date |
| Steam category (presentation only) | Recalculated with Steam's public thresholds on volume and % positive | Categorical (Overwhelmingly Positive…Negative) | Per game | Same as above |
| Inclusion filter | `positive + negative ≥ 500` | Count | Per game | — |
| Inflation-adjusted price | `price × (CPI_base / CPI_release_year)`, base = dataset's most recent year | Real USD | Per game | Requires a CPI index (external US source) — pending validation in Phase 2 |
| Game age | `base_year − release_year` | Years | Per game | Control variable, not a filter |
| Price band | Quartiles of **adjusted** price on paid games (price > 0) passing the review filter | Real-USD range | Per game | Static (full catalogue) |

⚠️ Pending (doesn't block this phase, resolved in Process): how to disaggregate games with
multiple genres.

⚠️ Conditional: the inflation adjustment depends on the external CPI source passing the Phase 2
integrity check. If it doesn't, this point downgrades to a "declared limitation" and the reason
is documented instead of applying it silently.

- **Out of scope:**
  - PC/Steam only — no consoles or mobile.
  - F2P games are excluded from the price-band analysis (documented as separate context).
  - Does not establish causality, only a descriptive pattern/correlation.
  - Does not allocate investment budget, only prioritises genres for due diligence.
  - Excludes the long tail with <500 reviews (indie/niche) — left as an "additional deliverable
    to explore" in Phase 6.

**Phase 1 exit gate:** ✅ complete
- [x] Business problem in 1-2 sentences, jargon-free.
- [x] SMART and fair analytical question.
- [x] Concrete decision written down.
- [x] Problem type identified.
- [x] Stakeholders mapped with what each one needs.
- [x] Metrics with operational definitions.
- [x] Scope with what is explicitly excluded.

## 2. Prepare

**Status:** ✅ closed (approved by the user on 2026-07-28)

- **Sources:** full records in `documentacion/fichas-de-fuente.md`.
  1. **Steam Games Dataset** (Kaggle, fronkongames) — downloaded 2026-07-28. 125,855 rows × 40
     real columns (the raw header only declares 39, see bug below). CC BY 4.0.
  2. **CPI-U** (US Bureau of Labor Statistics, series `CUUR0000SA0`) — approved on 2026-07-28 as
     the second source for the Phase 1 inflation adjustment. Public domain. Will be downloaded in
     Phase 3 when the adjustment is applied.

- **ROCCC assessment:** full detail in `documentacion/fichas-de-fuente.md`.
  - Steam Games Dataset: partially fails **O**riginal (it's a third-party aggregator, not
    straight from Valve) and the reliability component of `estimated_owners` (a SteamSpy
    estimate, not real sales). Not disqualified; declared as a limitation.
  - CPI-U: fails no letter — first-party, current, comprehensive for the intended use,
    documented.

- **Identified biases:**
  - **Survivorship bias:** the dataset only contains games that made it to publication on Steam;
    it doesn't capture rejected or delisted games, nor the industry outside PC/Steam.
  - **Sampling bias (long tail):** 42,899 games (34.1%) have 0 reviews (positive + negative). The
    ≥500-review filter already decided in Phase 1 deliberately excludes this tail; the final
    sample skews toward successful/visible games. This is a documented scoping decision, not a
    hidden bias.
  - **Measurement bias in `estimated_owners`:** it comes in categorical ranges estimated by
    SteamSpy, not a Valve-confirmed figure. It will not be used as the analysis's main metric,
    only as context.
  - **Unresolved multi-genre:** 6.69% of games have no genre assigned; the rest have between 1
    and 19 genres (median ~3). How to disaggregate multiple genres is left for Phase 3 (already
    flagged in Phase 1).

- **Licence / privacy / security / accessibility:**
  - Steam Games Dataset: CC BY 4.0, requires attribution in the public README. No PII. Static
    local file, no credentials involved.
  - CPI-U: public domain, no restrictions, no PII.
  - **Accessibility decision:** the raw file (~400 MB) is not uploaded to the portfolio's public
    repository; the README will link directly to the Kaggle source. Confirmed with the user.

- **Initial integrity check:**
  - Rows × columns: 125,855 × 40 (the raw header declares 39 columns; every row carries 40
    fields). **Header bug confirmed and diagnosed:** the name `DiscountDLC count` (position 7)
    merges two real columns, `Discount` and `DLC count`. Fixed by inserting the missing name
    before loading the file — the procedure is documented in `documentacion/fichas-de-fuente.md`
    and will need to be repeated identically at the start of Phase 3.
  - Real date range: 1997-06-30 to 2026-12-01. Only 2 rows with a future release date (not yet
    published, 0 reviews) — will be excluded in Phase 3.
  - Nulls per column: high and expected in columns not used by the question (`Movies` 100%,
    `Score rank` 99.97%, `Metacritic url` 96.6%, `Reviews` 90.3%). The columns the question does
    use have low nulls: `Genres` 6.69%, `Price` 0%, `Positive`/`Negative` 0%.
  - Key uniqueness: `AppID` has 125,855 unique values across 125,855 rows → 0 exact duplicates. 0
    fully duplicated rows.
  - Numeric ranges: no negatives in `Price`, `Positive`, `Negative`. `DLC count` reaches 3,703 in
    one case (Fantasy Grounds VTT, verified as real — it has thousands of tabletop DLCs). `Price`
    maxes out at $999.98, no impossible values. `Metacritic score` uses `0` as a "no data"
    sentinel (only 3.38% of games have a real score) — documented in the dictionary so Phase 3/4
    doesn't mistake it for a real score.
  - Column-by-column detail in `documentacion/diccionario-de-datos.md`.

- **Confirmation:** this data does answer the Phase 1 question. `price`, `genres`, `positive`
  and `negative` are present with manageable nulls. The one gap (dated individual reviews) was
  already anticipated and resolved with the game-age proxy.

- **Exit gate:** ✅ complete
  - [x] Every source has its full record.
  - [x] ROCCC assessed per source, with failures declared.
  - [x] Potential biases identified in writing.
  - [x] Licence, privacy, security and accessibility resolved.
  - [x] Data dictionary written.
  - [x] Immutable copy of the raw file saved, with naming convention
        (`datos/crudos/steam_fronkongames_catalogo-historico_2026-07-28.csv`).
  - [x] Initial integrity check run, with results noted.
  - [x] Confirmed that this data can answer the Phase 1 question.

## 3. Process

**Status:** ✅ closed (approved by the user on 2026-07-28)

- **Tool and rationale:** Python (pandas) — decided in Phase 0. Confirmed in this phase: the
  process requires reproducibility over a 400 MB file with a structural header bug, something
  not viable to audit by hand in a spreadsheet.
- **Log:** full detail of the 8 transformations in `bitacora-limpieza.md`. Reproducible script:
  `notebooks/procesar.py` (runs end to end from the raw file).
- **Key transformations:**
  1. Fixed the header bug (`DiscountDLC count` → `Discount` + `DLC count`).
  2. Excluded 2 games with a future release date.
  3. Dropped 15 columns as out of scope (high nulls or unstructured text).
  4. 0 duplicates by `AppID` (reconfirmed).
  5. Excluded 8,423 games with no genre assigned (not classifiable).
  6. Enrichment with BLS CPI-U: `anio_lanzamiento`, `antiguedad_anios`, `precio_ajustado_usd`
     (2026 base year, with a declared limitation: the 2026 CPI is a partial average of only 4
     months).
  7. Calculated `pct_resenas_positivas` (null, not 0%, for the 34,589 games with zero reviews).
  8. Derived dataset `steam_juegos_por_genero.csv`, exploded by genre (decision confirmed with
     the user: a game with N genres produces N rows).
- **Count reconciliation:** 125,855 initial − 2 (future date) − 0 (duplicates) − 8,423 (no
  genre) = **117,430 final**. Verified with an `assert` in the script. The genre-exploded
  dataset has 338,575 game-genre rows.
- **Outliers investigated:** `DLC count` maxes at 3,703 (Fantasy Grounds VTT, verified as real,
  not removed). `Metacritic score` uses `0` as a "no data" sentinel (documented, not confused
  with a real score).
- **Note for Phase 4:** Steam's `Genres` taxonomy mixes real genres (`Action`, `RPG`) with
  content descriptors/business model tags (`Violent`, `Gore`, `Free To Play`, `Early Access`).
  33 unique values in total — Phase 4 will need to decide how to handle them.
- **Exit gate:** ✅ complete
  - [x] Tool chosen and justified.
  - [x] Every type of dirty data explicitly reviewed.
  - [x] Full log with what, why, how and rows affected per transformation.
  - [x] Count reconciliation checks out (verified with `assert`).
  - [x] Outliers investigated and the decision justified.
  - [x] Process reproducible from the raw file (`notebooks/procesar.py`).
  - [x] The clean dataset is still sufficient: 117,430 games with genre and price; 10,479 pass
        the ≥500-review filter; 99,085 are paid — enough volume for price quartiles.

## 4. Analyse

**Status:** ✅ closed (approved by the user on 2026-07-28)

- **Tool:** Python (pandas). Reproducible scripts: `notebooks/analizar.py` (descriptive
  statistics, quartiles, genre × band table) and `notebooks/verificar.py` (the 7 checks below).
  Tables exported to `salidas/tablas/genero_x_franja_precio.csv` and
  `salidas/tablas/resumen_por_genero.csv`.

- **Scope decision (confirmed with the user before tabulating):** the `Genres` column mixes real
  game genres with content descriptors (`Violent`, `Gore`, `Nudity`, `Sexual Content`), non-game
  software tags (`Utilities`, `Education`, `Accounting`, `Movie`, etc. — 17 values) and business
  model/status (`Free To Play`, `Early Access`). These were excluded from the genre × price
  analysis (29,101 of 338,575 game-genre rows), leaving **10 real game genres**: Action,
  Adventure, Casual, Indie, Massively Multiplayer, RPG, Racing, Simulation, Sports, Strategy.

- **Descriptive statistics (base `steam_juegos_limpios`, 117,430 games):**
  - `precio_ajustado_usd`: mean $5.89, median $3.13, P75 $6.84 (right-skewed, max $1,284.88 —
    tails from bundles/premium software).
  - `pct_resenas_positivas` (82,841 games with ≥1 review): mean 75.83%, median 81.82%, P25 65%.
  - `antiguedad_anios`: median 4 years, P75 7 years.
  - 99,085 paid games, 18,345 F2P (Price = 0). 10,479 games pass the ≥500-review filter.

- **Analysis base and quartiles:** paid filter (`Price > 0`) + ≥500 reviews → 9,048 games (23,822
  game-genre rows after exploding by real genre). Quartiles of `precio_ajustado_usd` calculated
  on that base: **Q1 ≤ $3.25 · Q2 $3.25-$6.46 · Q3 $6.46-$12.36 · Q4 > $12.36**.

- **Findings:**
  1. **The cheapest band (Q1) is systematically the worst-reception band across all 10 genres.**
     Median % positive reviews in Q1 ranges from 76.0% (Massively Multiplayer) to 86.3% (Casual),
     always the lowest or tied-lowest of the 4 bands in its genre
     (`salidas/tablas/genero_x_franja_precio.csv`).
  2. **The best reception clusters at Q3 ($6.46-$12.36) or Q4 (>$12.36), not the highest price
     overall.** In Action, Indie, Simulation, Casual and Strategy the peak is Q3; in Adventure,
     Racing, Sports and RPG it's Q4. No genre has its best reception in Q1 or Q2.
  3. **Moderate and consistent effect size:** the gap between Q1 and the best band ranges from
     2.50 p.p. (RPG) to 5.04 p.p. (Adventure). It's a real but not dramatic difference — it
     doesn't support a "price alone doubles reception" claim, only a directional pattern.
  4. **Three candidates with the best combination of effect + volume + absolute reception:**
     Adventure (4,030 games, +5.04 p.p., peak median 87.5%), Indie (5,561 games, +3.94 p.p., peak
     median 88.2%) and Casual (2,230 games, +3.31 p.p., the highest median of the 10 genres in
     its best band: 89.6%). These feed into the Phase 6 recommendations, not a closed decision
     here.
  5. **Massively Multiplayer is a case apart:** a non-monotonic pattern (Q2 is its best band, not
     Q3/Q4), the lowest median of the 10 genres across all 4 bands (74-79%), and the smallest n
     (176 games) — weak evidence, documented as such, neither dismissed nor recommended.

- **Checks applied** (`notebooks/verificar.py`):
  1. **Sanity:** adjusted quartiles (3.25/6.46/12.36) vs. raw unadjusted list price
     (2.49/4.99/9.99) — same order of magnitude, the inflation correction doesn't distort the
     scale. Plausible for Steam's indie/AA catalogue.
  2. **Recalculation via an alternate path:** the genre × band table was recalculated with
     `pivot_table` instead of `groupby.agg`; matches point for point (spot-check Action × Q3:
     86.64% both ways).
  3. **Age as a confounder:** correlation of `antiguedad_anios` vs `pct_resenas_positivas` =
     -0.087 (practically null) — age doesn't explain the price pattern. Documented that
     correlation doesn't imply causation.
  4. **Age control:** the table was repeated splitting recent games (≤ median age) from older
     ones, for Action/Adventure/Indie/Casual. The "Q1 is worst" pattern holds in both bands — not
     an artefact of cheap games simply being older.
  5. **Effect size quantified:** see finding 3 (2.50-5.04 p.p.), not just direction.
  6. **Manual recalculation of `pct_resenas_positivas`** on 5 random games
     (`Positive/(Positive+Negative)×100`) — matches the precomputed column exactly in all 5
     cases.
  7. **Sample-size robustness by genre:** n in the analysis base ranges from 176 (Massively
     Multiplayer) to 5,561 (Indie). Genres with n < 350 (Massively Multiplayer, Sports, Racing)
     are reported but flagged with a small-sample warning.

- **What the data doesn't answer:**
  - No dated individual reviews — the game-age proxy (already anticipated in Phase 1) doesn't
    capture whether a game's reception changed over time, only cumulative reception as a function
    of how old the game is.
  - Doesn't establish causality: the "mid-to-high price → better reception" pattern is a
    descriptive correlation; it may reflect selection (studios that charge more also invest more
    in quality) rather than raising price improving reception.
  - Doesn't cover the long tail (<500 reviews, 34.1% of the catalogue with 0 reviews) — excluded
    by a Phase 1 decision, documented as an additional deliverable in Phase 6.
  - Massively Multiplayer has insufficient evidence (n=176) for a firm recommendation on its own.

- **Exit gate:** ✅ complete
  - [x] Full, reviewed descriptive statistics.
  - [x] Every Phase 1 question has an answer backed by a concrete calculation.
  - [x] Every calculation documented and reproducible (`notebooks/analizar.py`,
        `notebooks/verificar.py`).
  - [x] Every finding passed a sanity check and an alternate-path recalculation.
  - [x] Effects quantified, not just directional (2.50-5.04 p.p.).
  - [x] Alternative interpretations considered and ruled out with evidence (age as a confounder,
        ruled out with ≈0 correlation and age-band control).
  - [x] What the data cannot answer is written down as a limitation.
  - [x] No causal claim rests on correlation alone.

## 5. Share

**Status:** ✅ closed (approved by the user on 2026-07-28)

- **Audience(s) and deliverables** (confirmed with the user before building):
  1. **Investment committee** (executive): `entregables/resumen_ejecutivo.docx` — no jargon,
     conclusion first, 4 figures with interpretation, limitations visible.
  2. **Investment committee** (~30 min, live presentation): `entregables/presentacion_fase5.pptx`
     — 13 slides: title with the conclusion, context, method, 4 findings (one per slide),
     candidates (stat callouts), limitations, next step (Phase 6), methodology/checks appendix,
     prepared Q&A appendix, close. Speaker notes included.
  3. **Senior analyst / portfolio repo** (technical): `notebooks/caso_steam_precio_recepcion.ipynb`
     — end-to-end narrated notebook (context → sources → cleaning → analysis → checks →
     visualisation), every code cell runs without errors, with interpretation after each result.

- **Visualisations** (spotlighting: 4 of the 5 Phase 4 findings carry the argument; the fifth —
  Massively Multiplayer, weak evidence — is documented in text, not charted separately). Files in
  `salidas/graficos/`, generated with `notebooks/graficos.py`:
  1. `01_q1_vs_mejor_franja.png` — *"The cheapest price band has the worst reception in every
     Steam genre"* (grouped bars, Q1 vs. best band, sorted by effect).
  2. `02_heatmap_genero_franja.png` — *"The best reception clusters at mid-to-high prices (Q3/Q4),
     never the cheapest"* (heatmap, genre × band).
  3. `03_ranking_efecto_candidatos.png` — *"Adventure, Indie and Casual combine the best effect,
     volume and absolute reception"* (effect ranking, candidates highlighted).
  4. `04_control_antiguedad.png` — *"The pattern holds for both recent and older games: it is not
     an age effect"* (grouped bars by age band, 4 genres).
  - Design checklist applied to all 4: bar axis starts at zero, one lead colour (blue) with grey
    for context, sorted by value, source note in the footer, alt text written for every figure
    (see notebook), no 3D elements.

- **Prepared Q&A** (presentation appendix, the 5 toughest questions with a written answer):
  1. Isn't this just that expensive games come from bigger studios with better marketing?
  2. Why exclude the 34% of games with no reviews? Aren't opportunities lost there?
  3. How sensitive is the result to how the price bands were defined?
  4. Why trust a third-party dataset instead of direct data from Valve?
  5. What's the exact number behind "Adventure is the best candidate"?

- **Exit gate:** ✅ complete
  - [x] Audience defined and format matched to it (executive, live presentation, technical).
  - [x] Every chart has a headline that states the finding.
  - [x] Every chart passes the three-part filter (practical question / data / visual element).
  - [x] Chart type justified by the goal (bars for comparison, heatmap for intensity across two
        dimensions).
  - [x] Axes, order, colours and annotations reviewed (visual check of the 4 figures and the 13
        slides before publishing).
  - [x] Accessibility verified (alt text per figure, information not encoded by colour alone,
        underlying data table available in `salidas/tablas/`).
  - [x] Limitations and assumptions visible, not hidden in an appendix (own section in both the
        executive summary and the presentation).
  - [x] Q&A prepared for the five hardest questions.

## 6. Act

**Status:** ⬜ 8 of 9 — content and publication done; presentation rehearsal open (see exit gate)

- **Finding → insight → recommendation chain:** the 5 Phase 4 findings were elevated to insight
  and recommendation in the opening table of `entregables/recomendaciones.md`.

- **Recommendations** (full cards in `entregables/recomendaciones.md`), prioritised by impact
  against effort:

| # | Action | Evidence | Impact | Effort | Priority |
|---|---|---|---|---|---|
| R1 | Concentrate next cycle's due diligence on Adventure, Indie and Casual | The 3 highest reception medians (86.2 / 86.7 / 88.2%) + band effect of 3.31-5.04 p.p. + volume (4,030 / 5,561 / 2,230 games) | High — reallocates effort across 49.6% of the analysed base; **not** a financial impact | Low | 1 |
| R2 | Add the catalogue's price-quartile position to screening; flag >50% in Q1 | Q1 is the worst median band across all 10 genres (76.0-86.3%); survives the age control | Medium — effect of 2.50-5.04 p.p., which is why it's a warning signal, not a disqualifying criterion | Low | 2 |
| R3 | Deprioritise Massively Multiplayer this cycle; Sports and Racing as "insufficient evidence" | MMO: 76.4% median, non-monotonic pattern, n=176. Sports n=329, Racing n=338, below the n<350 threshold from check 7 | Medium — frees up 3.5% of the base | Low | 3 |

  Each card also includes a success metric with a deadline and the critical risk/assumption. The
  most uncomfortable risk is stated in R3: Steam reviews poorly measure a recurring-revenue model
  like MMOs, so deprioritising on weak evidence could be exactly how an opportunity is missed.

- **Limitations** (7 full ones in `entregables/recomendaciones.md`): no causality (the
  alternative selection reading — those who charge more also invest more in production — cannot
  be ruled out with this data); no revenue or sales data; survivorship bias; the long tail (34.1%
  of the catalogue with 0 reviews) is excluded by the ≥500 filter; aggregated, undated reviews;
  partial CPI base year (Jan-Apr 2026); third-party source (fails the "Original" component of
  ROCCC).

- **Desirable additional data:** real revenue or units sold; dated individual reviews; production
  budget or studio size (would let us directly test the alternative selection reading); price and
  discount history; retention and spend per user (to evaluate MMOs with a metric suited to their
  model); console and mobile data.

- **Next steps:** (1) lower the threshold to 50 and 100 reviews to analyse the long tail —
  unlocks whether the fund should open an investment lane for small studios; (2) cross-reference
  the 3 prioritised genres with a revenue source — turns hour-prioritisation into
  capital-prioritisation; (3) sensitivity analysis on the bands (quintiles and fixed bands).

- **Published at:** ✅ https://github.com/BobbyTarantino099/steam-price-reception — public
  repository. Full narrative lives on the portfolio site:
  https://juanesportfolio.com/cases/steam-price-reception/. `README.md` is a short abstract
  linking to both. Raw data linked to Kaggle instead of uploaded.

- **What this case demonstrates versus the others:** turning an investment question into a
  pricing + sentiment analysis on a dataset with a real structural flaw (a broken header that
  misaligns columns, not trivial nulls), enriched with a second source (CPI-U) to compare 29
  years in real dollars — and, above all, ruling out the alternative explanation (age) with code
  before publishing the finding, plus reporting the genre that didn't fit the conclusion as
  insufficient rather than omitting it. Portfolio coverage matrix and gaps in
  `entregables/portafolio-indice.md`.

- **Exit gate:** ⬜ 8 of 9 — one item left, and it can't be closed by a script
  - [x] Every finding was elevated to insight and recommendation.
  - [x] Every recommendation has action, evidence, impact, metric, risk and effort.
  - [x] Recommendations prioritised by impact against effort.
  - [x] Limitations and additional data documented.
  - [x] Public `README.md` complete, linking to the site and the case's full evidence.
  - [x] No sensitive data or licence violations: no PII, raw file not uploaded, CC BY 4.0
        attribution present.
  - [x] **Analysis reproducible from the raw file by a third party** — verified in practice, not
        just on paper: `datos/limpios/` was deleted and `procesar.py` + `analizar.py` were rerun
        from the raw file on a machine other than the one the scripts were authored on. The
        regenerated tables matched the committed ones byte for byte, and the count reconciliation
        held (125,855 − 2 − 0 − 8,423 = 117,430). This is the strongest local proxy available for
        a true third-party run; nobody outside this project has cloned the repo and reproduced it
        yet.
  - [x] Written what skill this case demonstrates relative to the rest of the portfolio.
  - [ ] **Presentation versions rehearsed out loud: 30 minutes and 3 minutes** — both are
        *written* (the 30-min deck at `entregables/presentacion_fase5.pptx`, the 3-min script at
        `entregables/guion-presentacion.md`), but neither has been rehearsed. This is the one exit
        criterion nothing but doing it can satisfy — it stays open until the user has said both
        out loud, ideally to someone outside the field.

## 7. Portfolio

**Status:** ⬜ open — repository and site published; presentation rehearsal is the one item left
before this case can be called fully closed (see Phase 6 exit gate)

- **Coverage matrix and gaps:** see `entregables/portafolio-indice.md`. As the first case, it
  covers "find patterns" as the problem type, Python as the tool, and video games as the domain.
  The gaps it leaves for the next case — SQL as the lead tool, longitudinal data, a different
  problem type, a domain outside video games — are documented there.
- **Case repository:** public, at
  https://github.com/BobbyTarantino099/steam-price-reception. Contains the full evidence layer:
  this file, the cleaning log, source records, data dictionary, reproducible scripts, notebook,
  and deliverables.
- **Site page:** https://juanesportfolio.com/cases/steam-price-reception/ — the case's L1 card
  (home page) and L2 narrative (case page), built from this repository's front-matter-driven
  content contract.

## Decision log
| Date | Decision | Reason | Alternative discarded |
|---|---|---|---|
| 2026-07-28 | Sector: digital platforms / pricing + sentiment on Steam | User interest + fits an investor client | Studios/publishers, esports, community |
| 2026-07-28 | Fictional client: investment fund | Forces a concrete decision (where to invest) | A studio deciding what to launch; a platform optimising its catalogue |
| 2026-07-28 | Dataset: Steam Games Dataset (fronkongames), CC BY 4.0 | Has price + genres + positive/negative in a single file, adequate volume and recency, medium saturation | Game Recommendations on Steam (antonkozyriev) — discarded for high saturation; Steam games complete dataset (trolukovich, 2019) — discarded for age and free-text-only reviews |
| 2026-07-28 | Time window: the full available history | User prefers full coverage, with time to spare | Limiting to the last 5 or 3 years |
| 2026-07-28 | Minimum review threshold: ≥500 | Prioritises statistical reliability over long-tail coverage | Threshold of 50 or 100 reviews |
| 2026-07-28 | Price bands by quartiles calculated on the real data | Avoids arbitrary bands imposed upfront | Predefined fixed bands |
| 2026-07-28 | F2P excluded from the price-band analysis | They have no real price band; documented separately | Including F2P as a "Free" band; excluding them from the whole case |
| 2026-07-28 | Correct the age/inflation bias with an external CPI + year control, instead of declaring it a limitation | User prefers methodological rigour over simplicity, with time to spare | Leaving it as a declared limitation; limiting the window to 5 years |
| 2026-07-28 | Approve BLS CPI-U as the second data source | Passes ROCCC with no failures: first-party, public domain, covers 1997-2026 | Looking for a third-party inflation index or one from another region |
| 2026-07-28 | Don't upload the raw CSV (~400 MB) to the public repo; link to Kaggle instead | The file exceeds what's reasonable for a portfolio repo | Uploading a reduced sample of the raw file for end-to-end reproducibility |
| 2026-07-28 | Explode by genre (one row per game-genre) instead of keeping only the primary genre or mono-genre games | The user preferred every genre to get its own evidence, accepting that a game counts in several groups | Primary genre only; or discarding multi-genre games |
| 2026-07-28 | Exclude 8,423 games with no genre assigned | They can't be placed in any genre × price combination, which is the core of the question | Imputing an "Unclassified" category |
| 2026-07-28 | Use the partial 2026 CPI average (Jan-Apr) as the base year | It's the only data available as of the download date; declared as a limitation instead of waiting for the full year | Using 2025 as the base year (most recent complete year) |
| 2026-07-28 | Recommendations limited to prioritising due diligence by genre, without a pricing thesis for portfolio companies | The dataset has no revenue or sales data; recommending "raise the price" would exceed what the evidence supports | Adding an operational pricing thesis; adding a recommendation to expand the analysis as R4 |
| 2026-07-28 | Three recommendations, no more | The framework calls for prioritising by impact against effort and sending the rest to future exploration; the long tail and band sensitivity go to "next steps" | Stating 5-6 recommendations including future-analysis ones |
| 2026-07-28 | Report Massively Multiplayer as deprioritised for insufficient evidence, with the counter-argument written in its own card | Omitting the genre that didn't fit would have been the easiest mistake; declaring it with its risk is more credible | Omitting it from the deliverable; or recommending/dismissing it with the evidence at hand |
| 2026-07-28 | Don't upload the raw file to the repo; link to Kaggle in the reproduction instructions | Consistent with the Phase 2 decision; 400 MB doesn't reasonably fit in a portfolio repo | Uploading a reduced sample for end-to-end reproducibility |
| 2026-07-28 | Exclude from "genre" the content descriptors (Violent, Gore, Nudity, Sexual Content), non-game software tags (17 values), and Free To Play/Early Access | These are Steam taxonomy tags that don't represent a real video game genre; mixing them in would distort the genre × price table | Keeping all 33 tags as-is; or excluding only the non-game-software subset |
| 2026-08-10 | Translate the full case repository (CASO.md, log, source records, deliverables) to English | The site is English-only; a visitor reaching the repo from the site would otherwise hit a language switch mid-evidence-chain | Keeping the repo in Spanish and only translating the site's L2 page |
| 2026-08-10 | Regenerate the 4 charts with English text before publishing | A Spanish chart on an English page is the most visible inconsistency the site could ship with | Publishing the English page with the original Spanish charts and a note |
| 2026-08-10 | Rewrite README.md as a short abstract linking to the site, instead of duplicating the full narrative | The full story now lives on the site (L2); a second full copy in the repo would drift out of sync with it over time | Keeping the long-form README as the primary narrative surface |
