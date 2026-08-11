% Price and reception on Steam: where should investment due diligence be prioritised?
% Executive summary — Portfolio case study
% July 28, 2026

## Context

An investment fund is evaluating entry into the video game sector and needs a data-driven basis
for deciding which **genre** to prioritise for its investment analysis (due diligence). This
report uses Steam's historical catalogue — the largest PC game market — as a reference sample of
the market.

**Question we answer:** which genre and price combinations achieve the best reception from
players (measured as % positive reviews), and which genres are therefore better investment
candidates?

## What we did

We analysed 117,430 games published on Steam. To isolate a reliable signal, we focused on the
8,998 paid games with at least 500 reviews — the minimum volume for the % positive reviews to be
statistically reliable — and grouped them into 10 real video game genres and 4 price bands (from
cheapest to most expensive, calculated from the data itself). Prices were adjusted for inflation
so games from different years could be compared on equal footing.

## Main finding

**The cheapest price band gets, across all 10 genres without exception, the worst reception.**
The best reception isn't at the highest possible price, but in a mid-to-high range
(approximately $6-$12 adjusted, depending on genre).

![The cheapest band has the worst reception across all 10 Steam genres](../salidas/graficos/01_q1_vs_mejor_franja.png)

The difference is real but moderate: between 2.5 and 5 percentage points of improvement moving
from the cheapest band to each genre's best band. Not a dramatic effect, but a consistent one
across all 10 categories.

![The best reception clusters at mid-to-high prices, never the cheapest](../salidas/graficos/02_heatmap_genero_franja.png)

## Candidates with the best evidence for due diligence

Of the 10 genres, three combine the best price effect, the largest volume of evidence, and the
highest absolute reception: **Adventure, Indie and Casual.**

![Adventure, Indie and Casual combine the best effect, volume and absolute reception](../salidas/graficos/03_ranking_efecto_candidatos.png)

- **Adventure** shows the largest reception jump between the cheapest band and its best band
  (+5 percentage points), with 4,030 games of evidence.
- **Indie** is the genre with the most evidence volume (5,561 games) and a solid improvement
  (+3.9 points).
- **Casual** has the highest absolute reception of the 10 genres in its best price band (89.6%
  positive reviews), though with lower volume (2,230 games).

**Massively Multiplayer** is left off this list: it's the genre with the worst reception across
all price bands and very little evidence (176 games) — not enough data to confidently recommend
or rule it out.

## Is this just an effect of cheap games being older?

No. We repeated the analysis splitting recent games from older ones, and the pattern holds the
same in both groups: the cheapest band remains the worst-reception one, regardless of the game's
age.

![The pattern holds for recent and older games: it is not an age effect](../salidas/graficos/04_control_antiguedad.png)

## What this analysis doesn't answer

- **It doesn't prove causality.** The pattern shows an association between price and reception,
  not that raising a game's price automatically improves its reviews. It may reflect that studios
  who charge more also invest more in production quality.
- **It doesn't cover the "long tail."** We deliberately excluded games with fewer than 500 reviews
  (34% of the catalogue has no reviews at all) to keep statistical reliability. That tail remains
  as pending additional analysis.
- **It doesn't measure reviews over time,** only each game's historical cumulative total as of the
  data collection date.
- This analysis prioritises genres; **it doesn't allocate investment budget** or replace
  studio-or-publisher-specific due diligence.

## Next step

The formal recommendations phase (Phase 6 of the case) will translate this evidence into a
concrete prioritisation proposal, with its limitations and the additional data recommended before
committing capital.

---

*Source: Steam Games Dataset (fronkongames, Kaggle, CC BY 4.0 licence) and the CPI-U consumer
price index (US Bureau of Labor Statistics). Portfolio case study built with Python/pandas; full
methodology and checks available in the technical notebook
`notebooks/caso_steam_precio_recepcion.ipynb`.*
