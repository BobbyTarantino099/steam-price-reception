# Recommendations — Price and reception on Steam

**Case:** Which genre and price-band combinations on Steam sustain the best reception?
**Client:** Investment committee of a video-game-focused fund (fictional client).
**Date:** 2026-07-28
**Evidence base:** 9,048 paid games with ≥500 reviews (23,822 game-genre rows), Steam's
historical catalogue. Tables: `salidas/tablas/genero_x_franja_precio.csv` and
`salidas/tablas/resumen_por_genero.csv`.

---

## From finding to insight to recommendation

| Finding (Phase 4) | Insight (what it means for the fund) | Recommendation |
|---|---|---|
| The cheapest band (Q1, ≤$3.25 real) has the worst reception across all 10 genres | Low price doesn't buy reception; on Steam it works more as a signal of a low-budget product than a lever for adoption | R2 — use the catalogue's price position as a screening filter |
| The best reception clusters at Q3 ($6.46-$12.36) or Q4 (>$12.36), never Q1 or Q2 | There's a defensible "price zone"; studios already operating in it have a validated price-product fit | R1 and R2 |
| Adventure, Indie and Casual combine the best band effect, volume and absolute reception | These are the genres where the "mid-to-high price + good reception" thesis has the most support and the most available targets to invest in | R1 — concentrate due diligence there |
| Massively Multiplayer has the worst reception of the 10 genres (76.4% median), a non-monotonic pattern and n=176 | Not a "no", it's an "we don't know with this data"; committing due-diligence hours there is expensive and poorly informed | R3 — deprioritise this cycle |

---

## R1 — Concentrate next cycle's due diligence on Adventure, Indie and Casual

- **Action:** the origination team narrows the long list of candidate studios and publishers to
  the three genres Adventure, Indie and Casual for next semester's due diligence cycle. Owner:
  senior origination analyst. Deadline: define the long list within 4 weeks.
- **Evidence:** of the 10 real game genres analysed, these three are the only ones that combine
  (a) high absolute reception — median positive-review share of 88.2% (Casual), 86.7% (Indie) and
  86.2% (Adventure), the three highest in the set — with (b) a clear price-band effect — +3.31
  p.p. (Casual), +3.94 p.p. (Indie) and +5.05 p.p. (Adventure) between the cheapest band and each
  genre's best — and (c) sufficient target volume: 2,230, 5,561 and 4,030 games respectively,
  against 176 for the smallest genre.
  Source: `salidas/tablas/resumen_por_genero.csv` and `genero_x_franja_precio.csv`.
  *Precision note:* in Adventure the best band is Q4 (87.48%) by 0.01 p.p. over Q3 (87.47%). This
  is a technical tie, not a preference for Q4; reported as such to avoid overinterpreting the
  data.
- **Expected impact:** concentrates effort on the 49.6% of the analysed base (11,821 of 23,822
  game-genre rows) that makes up the three genres with the best reception, instead of spreading
  it across 10. **Explicit assumption:** the impact is *effort allocation*, not financial
  return — the dataset contains no real sales or revenue, so no effect on IRR or multiple is
  estimated or promised.
- **Success metric:** % of deals entering deep due diligence that belong to the three prioritised
  genres (target: ≥70%), and the median % positive reviews of the catalogue of studios that pass
  the first filter (target: ≥86%). Evaluated at 6 months.
- **Risk / critical assumption:** the pattern is correlational and rests on public reception, not
  commercial performance. It would need to be true that reception is a reasonable proxy for a
  studio's value. If it isn't — for example, if a genre with worse reception monetises much
  better — the prioritisation would be optimising the wrong variable. **Mitigation:** the
  committee should cross-reference this prioritisation with revenue data before committing
  capital (see Next steps).
- **Effort:** low. It's a filtering rule on a process the team already runs.

## R2 — Add the catalogue's price position to due diligence screening

- **Action:** add a required field to the screening form: what percentage of a candidate studio's
  catalogue sits in each adjusted-price quartile (Q1 ≤$3.25 · Q2 $3.25-$6.46 · Q3 $6.46-$12.36 ·
  Q4 >$12.36 real 2026 dollars). A studio with more than half its catalogue in Q1 is flagged for
  explicit review before proceeding. Owner: origination analyst. Deadline: incorporate it into the
  form before opening the next long list.
- **Evidence:** Q1 is the worst-median-reception band across all 10 genres without exception, with
  medians ranging from 76.0% (Massively Multiplayer) to 86.3% (Casual), always the lowest or
  tied-lowest in its genre. The pattern holds when splitting recent from older games (check 4,
  `notebooks/verificar.py`), and age doesn't explain it (age × reception correlation = -0.087).
- **Expected impact:** the band effect is 2.51 to 5.05 p.p. of positive reviews. It's a real but
  moderate difference. **Explicit assumption:** that's why this field is used as a warning signal
  that triggers review, not an automatic disqualifying criterion — the effect size doesn't justify
  ruling out a studio based on price band alone.
- **Success metric:** % of screening records with the field completed (target: 100% at 3 months)
  and the number of flagged cases that, after review, turned out to be a real product-positioning
  problem. Evaluated at 6 months.
- **Risk / critical assumption:** the quartiles were calculated on Steam's full historical
  catalogue and in US CPI-U-adjusted dollars. It would need to be true that those bands remain
  representative of the current market and of the region of the studio being evaluated. If the
  fund looks at markets with different price parity (LATAM, Asia), the bands need recalculating.
  **Also:** there's an alternative reading not ruled out — that studios who charge more also
  invest more in quality — in which case price is a symptom, not a cause. That doesn't invalidate
  its use as a *screening signal*, but it does rule out using it as "raise the price" advice.
- **Effort:** low. A new field in an existing form; the calculation uses public Steam data.

## R3 — Deprioritise Massively Multiplayer and treat Sports and Racing as insufficient evidence

- **Action:** exclude Massively Multiplayer from this cycle's long list and label Sports and
  Racing as "needs additional evidence" — not dismissed, but not consuming due-diligence hours
  until a broader data base exists. Owner: investment committee, at the cycle scoping meeting.
- **Evidence:** Massively Multiplayer has the lowest median positive-review share of the 10
  genres across all 4 price bands (74.8%-79.0%; overall median 76.4%), is the only genre with a
  non-monotonic pattern — its best band is Q2, not Q3/Q4 — and has the smallest n in the base
  (176 games). Sports (329 games) and Racing (338) also fall below the n<350 threshold set in
  Phase 4's check 7 for reporting with a small-sample warning.
- **Expected impact:** frees up origination hours from three genres that make up 3.5% of the
  analysed base (843 of 23,822 game-genre rows) and redirects them to R1. **Explicit assumption:**
  the impact is the team's time allocation, not financial.
- **Success metric:** zero Massively Multiplayer deals entering deep due diligence without an
  additional data source to support them, reviewed at cycle close (6 months).
- **Risk / critical assumption:** this is the most uncomfortable risk of the three
  recommendations. An n of 176 games is weak evidence, and deprioritising on weak evidence can be
  exactly how an opportunity is missed: MMOs are a recurring-revenue business model that Steam's
  review metric captures poorly — a player dissatisfied with monetisation leaves a negative
  review even if the game is profitable. If the fund has a recurring-revenue thesis, this
  recommendation should be revisited with retention and spend-per-user data, not reviews.
- **Effort:** low. It's a scoping decision, not a new process.

---

## Prioritisation (impact against effort)

| # | Recommendation | Impact | Effort | Priority |
|---|---|---|---|---|
| R1 | Concentrate due diligence on Adventure, Indie and Casual | High | Low | **1 — do now** |
| R2 | Add price position to screening | Medium | Low | **2 — do now** |
| R3 | Deprioritise MMO; Sports and Racing as insufficient evidence | Medium | Low | **3 — decide at the scoping meeting** |

All three are low-effort because all three are rules on a process the fund already has. None
requires hiring, buying data, or building tools. That's deliberately the ceiling of what this
analysis can support: with aggregated reviews and no revenue data, the honest recommendation is
*where to look first*, not *where to put the money*.

---

## Limitations

1. **No causality.** The "mid-to-high price → better reception" pattern is a descriptive
   correlation. The strongest alternative reading — selection: studios who charge more also
   invest more in production — cannot be ruled out with this data. What was ruled out with
   evidence is that the pattern is an age artefact (correlation -0.087 and age-band control).
2. **No revenue or sales data.** `estimated_owners` comes in SteamSpy-estimated ranges, not
   Valve-confirmed, and was not used as an analysis metric. So the case says nothing about
   profitability, only about public reception.
3. **Survivorship bias.** The dataset only contains games published on Steam: no cancelled,
   rejected, or delisted games, and nothing outside PC/Steam (consoles, mobile).
4. **The long tail is excluded.** The ≥500-review filter — decided in Phase 1 for statistical
   reliability — deliberately excludes the 34.1% of the catalogue with 0 reviews. The sample is
   biased toward visible, successful games. If the fund is specifically looking for small,
   emerging studios, this analysis doesn't cover them.
5. **Aggregated, undated reviews.** There's no time evolution of a game's reception; game age was
   used as a proxy, and that proxy doesn't capture whether a game's reception improved or
   worsened after launch.
6. **Inflation adjustment with a partial base year.** The 2026 CPI-U is the average of only four
   months (Jan-Apr), the only data available as of the download date.
7. **Third-party source.** The dataset comes from an aggregator (fronkongames), not directly from
   Valve. This fails ROCCC's "Original" component; it is declared, not hidden.

## Additional data that would strengthen the conclusions

| Data | What it would unlock |
|---|---|
| Real revenue or units sold (Valve, or the target company's own data during due diligence) | Moving from "best reception" to "best return" — which is what actually decides an investment |
| Dated individual reviews | Seeing whether reception holds, improves, or degrades after launch, and separating the launch effect from the price effect |
| Production budget or studio size | Directly testing the alternative selection reading: if the price effect disappears when controlling for budget, R2 loses support |
| Price and discount history per game | Distinguishing list price from price actually paid; the current analysis uses list price |
| Retention and spend-per-user data | Evaluating Massively Multiplayer with a metric suited to its business model, instead of reviews (see R3's risk) |
| Console and mobile data | Knowing whether the price pattern is a Steam thing or an industry thing; today it can't be distinguished |

## Next steps

1. **Analyse the long tail (<500 reviews).** Repeat the genre × band table lowering the threshold
   to 50 and 100 reviews to see whether the pattern holds in the indie/niche segment. *Decision
   this unlocks:* whether the fund should open an investment lane for small studios. (Additional
   deliverable already anticipated since Phase 1.)
2. **Cross-reference the three prioritised genres with a revenue source.** *Decision this
   unlocks:* turning the hour-prioritisation (R1) into a capital-prioritisation.
3. **Sensitivity analysis on the bands.** Recalculate with quintiles and with fixed bands to
   confirm the conclusion doesn't depend on having chosen quartiles. *Decision this unlocks:* how
   much confidence to place in R2's screening field.
