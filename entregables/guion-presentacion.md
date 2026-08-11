# Presentation script — Steam: price and reception

Two versions live here, and per the framework's own rule they are built separately, not one
sped up from the other: the 30-minute version is the deck (`presentacion_fase5.pptx`, 13 slides
with speaker notes); the 3-minute version below is the one actually used most — interviews,
networking, "tell me about a project."

**Neither version is rehearsed yet.** Writing the script is not the same as practising it out
loud, in front of someone outside the field, until it stops sounding read. That step is next,
and it's the user's to do, not something a document can verify.

---

## 3-minute version

**Target duration:** 3 minutes
**Audience:** interviews, networking — the version used most often
**Delivery note:** say this, don't read it. Practise until the transitions feel like thinking,
not recitation.

| Beat | What to say | Time |
|---|---|---|
| Hook | "I analysed 125,855 games on Steam to answer a question an investment fund would actually ask: which genre is worth prioritising for due diligence." | 20s |
| Context | "They had more candidates than filters — too many studios, no data-driven way to narrow the list." | 20s |
| Question | "So I asked: which genre and price-band combinations get the most consistent good reception, once you control for how old the game is?" | 20s |
| Main finding | "The answer surprised me a little: the cheapest games are the worst-received ones, in every single genre. Not a few — all ten. And the best reception isn't at the top price either, it's in the middle-upper range." | 40s |
| The check that matters | "The obvious objection is that cheap games are just old games. I checked — the correlation between age and reception is basically zero. The pattern holds whether the game is new or old." | 30s |
| Recommendation | "So I recommended the fund concentrate due diligence on three genres — Adventure, Indie, Casual — that combine the strongest effect, the most evidence, and the best absolute reception." | 25s |
| Limitation | "One thing I was careful to say plainly: this is correlation, not proof that raising a price improves reviews. Without revenue data, the honest claim is 'here's where to look first,' not 'here's where to invest.'" | 25s |
| Close | "The part I'm proudest of isn't the finding — it's that I reported the genre that *didn't* fit the story, Massively Multiplayer, as insufficient evidence instead of leaving it out." | 20s |

**Total: ~3 minutes.** Trim the check or the close first if running long — never the limitation.

---

## Prepared Q&A

The five toughest questions, with the answer already written. Having them ready in writing is
what separates an analysis that gets approved from one that gets sent back.

| Hard question | Answer | Backing |
|---|---|---|
| Isn't this just that expensive games come from bigger studios with better marketing? | We don't rule it out — it's the case's biggest causality limitation. The dataset has no studio size or marketing budget, so this reading can't be tested directly with what we have. It's listed as desirable additional data. | `entregables/recomendaciones.md`, Limitations §1 and §"Additional data" |
| Why exclude the 34% of games with zero reviews? Aren't opportunities lost there? | Excluded for statistical reliability, not because the opportunity is dismissed — under 500 reviews, the % positive is mostly noise. It's flagged as the first next step: rerun at thresholds of 50 and 100 to see if the pattern holds in the long tail. | `entregables/recomendaciones.md`, Next steps §1 |
| How sensitive is this to how you defined the price bands? | The quartiles were sanity-checked against the raw unadjusted list price (same order of magnitude) and recalculated with `pivot_table` as a second method — both matched. A sensitivity test with fixed bands and quintiles is a listed next step, not yet run. | `notebooks/verificar.py`, checks 1-2; Next steps §3 |
| Why trust a third-party dataset instead of data straight from Valve? | It's a declared ROCCC failure, not a hidden one — the source fails "Original" because it's an aggregator. It was chosen because it's the best public source combining price, genre and reviews in one file; `estimated_owners` specifically isn't used as a metric because of this. | `documentacion/fichas-de-fuente.md`, ROCCC table |
| What's the exact number behind "Adventure is the best candidate"? | 4,030 games of evidence, +5.04 percentage points of effect between its cheapest and best price band, peak median reception of 87.5%. Every number is reproducible from `notebooks/analizar.py`. | `salidas/tablas/genero_x_franja_precio.csv` |

---

## 30-minute version

Full deck: `entregables/presentacion_fase5.pptx` — 13 slides with speaker notes covering title,
context, method, the 4 findings (one per slide), candidate summary, limitations, next steps, a
methodology/checks appendix, and this same prepared Q&A as a closing appendix.
