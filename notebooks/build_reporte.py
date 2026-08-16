"""Builds entregables/reporte-tecnico.html and .pdf — the case's technical report.

Condenses what CASO.md records across 480 lines: the phases, the decisions that could have
gone another way, and where it ended. The executive summary answers "what should we do";
this answers "how do I know you did it properly".

Content is written here rather than parsed from the Markdown, same as build_docx.py.

Run: python notebooks/build_reporte.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import reporte  # noqa: E402

BASE = Path(__file__).resolve().parents[1]
G = BASE / 'salidas' / 'graficos'

doc = reporte.Reporte(
    titulo='Price and reception on Steam: where should due diligence go?',
    acento='#1f5fa8',
    contra='#c2410c',
)

# --- Portada ---------------------------------------------------------------
doc.portada(
    eyebrow='Technical report · Portfolio case study',
    hallazgo='In all ten genres, the cheapest price band has the worst reception — and the best '
             'sits at mid-to-high prices, not at the top. The effect is real but moderate, which '
             'is why it supports a screening rule and not a pricing thesis.',
    meta=[
        ('Domain', 'Video games'),
        ('Tools', 'Python · pandas · matplotlib'),
        ('Scale', '125,855 games · 2 sources'),
        ('Sources', 'Steam catalogue (CC BY 4.0) · BLS CPI-U'),
        ('Window', 'Full history, 1997–2026'),
        ('Published', '28 July 2026'),
    ],
    figura=G / '01_q1_vs_mejor_franja.png',
    pie_figura='Each genre\'s cheapest band against its best band. The best is ahead in all ten, '
               'by 2.5 to 5.0 percentage points.',
)

# --- Las fases -------------------------------------------------------------
doc.seccion(
    'The phases, and what each one settled',
    'Every phase closes on an exit gate checked point by point. The one that mattered most here '
    'was phase 3: the raw file had a structural defect, not a cosmetic one.',
    salto=True,
)
doc.fases([
    ('0 · Choose',
     'An investor client, so the analysis ends in a decision',
     'A fund choosing where to spend due-diligence time. Without a client there is no decision to '
     'enable, and phase 6 would end at findings.'),
    ('1 · Ask',
     'Which genre and price band combination sustains the best reception',
     'Framed to be answerable: inflation-adjusted price quartiles, paid games with at least 500 '
     'reviews, controlling for game age.'),
    ('2 · Prepare',
     'A second source added rather than a limitation declared',
     'Comparing prices across 29 years needs real dollars, so BLS CPI-U joins the Steam catalogue. '
     'It passes ROCCC with no failures.'),
    ('3 · Process',
     'A broken header that misaligned every column',
     'The raw header declares 39 columns but each row carries 40. Eight transformations logged, '
     'with counts reconciled at every step.'),
    ('4 · Analyse',
     'Seven verification blocks, including the obvious rival explanation',
     'Older games are cheaper and better reviewed, so age was tested as a confounder before the '
     'finding was published — not after.'),
    ('5 · Share',
     'Four figures, one message each',
     'Dumbbell, matrix table, effect ranking and an age control panel; each headline states the '
     'finding and carries its number.'),
    ('6 · Act',
     'Three recommendations, and one genre deliberately deprioritised',
     'Massively Multiplayer did not fit the pattern and is reported as such, with its '
     'counter-argument written out.'),
    ('7 · Portfolio',
     'Published against a contract enforced by code',
     'Later revisited to translate the whole evidence chain to English, so a visitor arriving from '
     'the site never hits a language switch.'),
])
doc.cerrar()

# --- Decisiones ------------------------------------------------------------
doc.seccion(
    'The decisions that defined the case',
    'Eight of the twenty-two recorded in <strong>CASO.md</strong>. The discarded alternative is '
    'the line that matters: it shows the choice was reasoned rather than reflexive.',
    salto=True,
)
doc.decisiones([
    ('Fictional client: an investment fund',
     'It forces a concrete decision — where to spend due-diligence time — instead of an open-ended '
     'exploration.',
     'A studio deciding what to launch, or a platform optimising its catalogue.'),
    ('Correct the inflation bias with an external index instead of declaring it a limitation',
     'Comparing a 1998 price against a 2026 one in nominal dollars is not a comparison. CPI-U '
     'turns the whole history into real dollars.',
     'Leaving it as a declared limitation, or cutting the window to five years — both cheaper, '
     'and both would have weakened the finding.'),
    ('Price bands as quartiles computed from the data',
     'Bands imposed upfront would have decided the answer before measuring it.',
     'Predefined fixed price bands.'),
    ('Minimum threshold of 500 reviews',
     'Statistical reliability over long-tail coverage: a game with nine reviews has a percentage, '
     'not a reception.',
     'A threshold of 50 or 100 reviews.'),
    ('Explode by genre, one row per game-genre pair',
     'Every genre gets its own evidence, accepting that a multi-genre game counts in several '
     'groups.',
     'Keeping only the primary genre, or discarding multi-genre games — both would have thrown '
     'away most of the catalogue.'),
    ('Exclude content descriptors and non-game software from "genre"',
     'Violent, Gore, Free To Play and seventeen software tags are Steam taxonomy, not video game '
     'genres. Mixing them in would distort the genre × price table.',
     'Keeping all 33 tags as they come.'),
    ('Report Massively Multiplayer as deprioritised, with its counter-argument',
     'It is the one genre that does not fit the pattern. Omitting it would have been the easiest '
     'mistake in the whole case.',
     'Leaving it out of the deliverable, or recommending it on the evidence available.'),
    ('Recommendations limited to screening by genre, with no pricing thesis',
     'The dataset has no revenue or sales data. Recommending "raise the price" would exceed what '
     'the evidence supports.',
     'Adding an operational pricing thesis for portfolio companies.'),
])
doc.cerrar()

# --- El momento crítico ----------------------------------------------------
doc.seccion('The moment the case nearly went the other way', salto=True)
doc.critico('A broken header, and the rival explanation that had to be ruled out', [
    'The raw file\'s header declares 39 columns while every row carries 40: the name '
    '<code>DiscountDLC count</code> merges two separate fields. Read naively, every column after '
    'that point is shifted by one — and the file still loads without error.',
    'The second risk was analytical rather than structural. Older games are both cheaper and '
    'better reviewed, so the entire finding could have been an <strong>age effect</strong> wearing '
    'a price label. It was tested before publication, not after: splitting recent from older games '
    'and re-running the pattern within each group.',
    'The pattern holds in both. That is the check that turns "cheap games are worse reviewed" from '
    'a correlation into something worth acting on.',
])
doc.figura(G / '04_control_antiguedad.png',
           'The same pattern within recent and older games: the cheapest band trails in both.')
doc.cerrar()

# --- Hallazgos -------------------------------------------------------------
doc.seccion(
    'What the data says',
    'Each finding was written as a sentence carrying a number before any chart was drawn.',
    salto=True,
)
doc.html_libre('<h3>1 · The peak sits at mid-to-high prices, never the cheapest</h3>')
doc.figura(G / '02_heatmap_genero_franja.png',
           'Median positive-review share by genre and price band.')
doc.html_libre(
    '<p>Five genres peak at <strong>Q3 ($6.46–$12.36)</strong> and four at Q4. <strong>No genre '
    'has its best reception in Q1 or Q2</strong> — which also rules out the simplistic "more '
    'expensive is always better" reading: in half the genres the most expensive band already '
    'trails Q3.</p>'
    '<h3>2 · The effect is real but moderate: 2.50 to 5.04 percentage points</h3>'
)
doc.figura(G / '03_ranking_efecto_candidatos.png',
           'The price effect by genre, with the three strongest combined candidates highlighted.')
doc.html_libre(
    '<p>Quantifying the gap is what keeps the recommendation honest: it supports a directional '
    'screening argument, not a claim that price alone transforms a product\'s reception.</p>'
)
doc.tabla(
    ['Genre', 'Games', 'Median reception'],
    [['Adventure', '4,030', '86.2%'], ['Indie', '5,561', '86.7%'], ['Casual', '2,230', '88.2%']],
    numericas=(1, 2),
)
doc.cerrar()

# --- Verificación ----------------------------------------------------------
doc.seccion('What each check ruled out', salto=True)
doc.tabla(
    ['Check', 'What it ruled out'],
    [
        ['V1 · Sanity', 'That the inflation adjustment distorted the bands — compared against raw list price'],
        ['V2 · Recomputation', 'An aggregation error, by rebuilding the genre × band table a second way'],
        ['V3 · Confounder', 'That age drives reception, by measuring the correlation directly'],
        ['V4 · Age control', 'That the pattern is an age effect — it holds in recent and older games alike'],
        ['V5 · Effect size', 'A difference too small to act on: 2.50 to 5.04 p.p.'],
        ['V6 · Source semantics', 'A misread metric, by recomputing the positive share by hand for random games'],
        ['V7 · Sample robustness', 'Genres too thin to carry a conclusion'],
    ],
)
doc.cerrar()

# --- Cierre ----------------------------------------------------------------
doc.seccion('Conclusions, limits and what this case demonstrates', salto=True)
doc.html_libre(
    '<h3>Recommendations</h3>'
    '<ul>'
    '<li><strong>Concentrate due diligence on Adventure, Indie and Casual</strong> — the three '
    'genres combining the strongest effect, enough volume and the best absolute reception.</li>'
    '<li><strong>Use the cheapest band as a screening signal</strong>, not as a verdict: a 2.5–5.0 '
    'point gap justifies a second look, not a rejection.</li>'
    '<li><strong>Deprioritise Massively Multiplayer</strong> for insufficient evidence, with the '
    'counter-argument on record rather than hidden.</li>'
    '</ul>'
    '<h3>What these data cannot answer</h3>'
    '<ul>'
    '<li><strong>No revenue or sales data</strong>, so nothing here supports a pricing thesis — '
    'only a screening rule.</li>'
    '<li><strong>Reception is not quality.</strong> Review share measures how buyers reacted, not '
    'how good a game is.</li>'
    '<li><strong>The 2026 CPI base is partial</strong> (January to April), declared rather than '
    'waited out.</li>'
    '<li><strong>Nothing here is causal.</strong> Price and reception move together; the case does '
    'not claim one produces the other.</li>'
    '</ul>'
    '<h3>What this case demonstrates</h3>'
    '<p>Ruling out the obvious rival explanation <em>before</em> publishing the finding — the step '
    'most portfolio cases skip. Alongside it: a dataset with a real structural defect rather than '
    'tidy nulls, and a second source brought in to make 29 years of prices comparable instead of '
    'writing the problem off as a limitation.</p>'
)
doc.pie(
    'Full phase log, cleaning log with every discarded alternative, ROCCC source records and the '
    'seven verification blocks: <strong>CASO.md</strong> in the case repository — '
    'github.com/BobbyTarantino099/steam-price-reception'
)
doc.cerrar()

doc.escribir(BASE / 'entregables' / 'reporte-tecnico.html')
