# Video script: Steam price and reception

**Status:** Pilot — exploratory, not published
**Format:** trailer, 45-60 s, narrated in my own voice (synthetic voices were tried and dropped:
too robotic, and they skipped the pauses the script depends on)
**Length:** 142 words (~55-60 s at a calm pace)

Numbers carry their literal pronunciation in parentheses *(like this)*. The parentheses are a
reading aid for recording, not part of the narration.
**Last updated:** 2026-10-11

The video invites the viewer to read the case; it does not replace it. That is why the narration
leaves out the recommendations (Adventure, Indie, Casual), figures 02 and 03, and the Massively
Multiplayer exception: those stay on the case page. Scene 4 shows three genres holding up without
saying they are the recommendation, so that scene 5's question has an answer to go and find.

## Scene 1 · The hook (0-7 s)

> An investment fund wants to back a video game studio. Steam has over a hundred thousand games.
> Where do you even start looking?

**Visual:** a grid of dots fills up while a counter runs to **125,855**. A deliberately crowded
screen: that is the problem.

## Scene 2 · The data (7-20 s)

> I started with 125,855 *(one hundred twenty-five thousand, eight hundred fifty-five)* games —
> and a file that lied. Its header was one column short, so every value after it sat in the wrong
> place. I fixed that first. Then I adjusted 29 *(twenty-nine)* years of prices for inflation,
> because ten dollars in the early 2000s *(two-thousands)* isn't ten dollars today.

**Visual:** a header row with its columns shifted one position, then snapping into place. Then a
"$10 · early 2000s" price tag growing to its real 2026 value.

## Scene 3 · The finding (20-33 s)

> I split the catalogue into four price bands. In all ten genres, the cheapest band was never the
> best. Not most of them. All ten.

**Visual:** figure 01 (cheapest band vs. each genre's best band), drawing genre by genre. A check mark lights up on each one in orange
`#c2410c`, up to ten. Visual pause on "All ten".

## Scene 4 · The objection (33-45 s)

> The obvious objection: cheap games are just old games. So I checked. Among older games, the
> cheapest band still comes last almost everywhere. Among recent ones, the gap mostly closes —
> except in three genres.

**Visual:** games split at the median age (6 years). Older games first: the cheapest band falls
to last place genre after genre. Then recent games: in most genres it no longer does, and three
stay lit (Adventure, Casual, Indie). They are labelled on screen, as every row is, but the
narration does not name them or call them the recommendation: that is left for scene 5 to ask.

## Scene 5 · The invitation (45-55 s)

> Which genres would I tell the fund to look at first — and what can't this data tell us? That's
> in the case.

**Visual:** the case headline as a closing card, with the URL
`juanesportfolio.com/cases/steam-price-reception/`.

## Notes on the claims

- **Scene 4 corrected (2026-10-11): the age objection is partly right.** The first take said
  "Recent or old, the cheapest band still comes last". Re-running figure 04's own computation
  (`notebooks/graficos.py`: same 8,998-game base, split at the median age of 6 years, bands with
  n ≥ 20) over all genres: among older games the cheapest band is last in 9 of 9 genres with
  enough data; among recent games only in 3 of 9 — Adventure, Casual and Indie, the three the
  case recommends. In RPG and Sports it is even the best band for recent games, and in Action,
  which figure 04 shows, recent Q1 (84.6) edges out Q4 (84.4). Massively Multiplayer lacks data
  in both groups. Scene 4 was re-recorded with the corrected sentence. Finding 4 of the case
  ("not an age effect") and figure 04's title overstate this too; to be corrected after the video.

- **"Never the best", not "the worst" (corrected 2026-10-11).** The first take said "the cheapest
  band had the worst reception" in all ten genres. The case's own table
  (`salidas/tablas/genero_x_franja_precio.csv`) says otherwise: the cheapest band is the worst in
  9 of 10 genres. In Massively Multiplayer it is second best (median 76.03 vs 79.02 / 75.38 /
  74.83). What holds in all ten is that the cheapest band is never the best, which is what
  figure 01 shows. Scene 3 was re-recorded with that sentence and spliced into the take
  (`video/empalmar_voz.py`). The case headline carries the same overstatement; it is to be
  corrected separately, after the video.
- **"125,855 games"** is the starting catalogue, not the analysis base (9,048 paid games with
  ≥500 reviews). The narration says "I started with" for that reason; the number must not be
  reused in scene 3.

## Before recording

Read it aloud against a stopwatch. If it runs past 60 s, scene 2 is the one to trim: the
inflation sentence can go without breaking the story.
