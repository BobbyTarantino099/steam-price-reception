const pptxgen = require('pptxgenjs');
const path = require('path');

// Raiz del caso, resuelta desde la ubicacion de este script: corre en cualquier maquina.
const RUTA_BASE = path.resolve(__dirname, '..');

const NAVY = '1E2761';
const ICEBLUE = 'CADCFC';
const WHITE = 'FFFFFF';
const ACCENT = '1F5FA8';
const GRAY = '6E7B91';
const DARKTEXT = '1A1A2E';
const LIGHTBG = 'F7F9FC';

const GRAFICOS = path.join(RUTA_BASE, 'salidas', 'graficos') + path.sep;

let pres = new pptxgen();
pres.layout = 'LAYOUT_WIDE'; // 13.3 x 7.5
const W = 13.33, H = 7.5;

function addFooter(slide, texto) {
  slide.addText(texto, {
    x: 0.5, y: H - 0.42, w: W - 1.0, h: 0.3,
    fontSize: 9, color: GRAY, fontFace: 'Calibri', align: 'left',
  });
}

// =====================================================================
// 1. TITLE
// =====================================================================
{
  const s = pres.addSlide();
  s.background = { color: NAVY };
  s.addText('Price and reception on Steam', {
    x: 0.8, y: 1.7, w: W - 1.6, h: 1.0,
    fontSize: 24, color: ICEBLUE, fontFace: 'Calibri', bold: false, align: 'left',
  });
  s.addText('Which genres should an investment fund prioritise for due diligence?', {
    x: 0.8, y: 2.5, w: W - 1.6, h: 2.0,
    fontSize: 38, color: WHITE, fontFace: 'Cambria', bold: true, align: 'left',
  });
  s.addText('Portfolio case study — Data Analyst  ·  July 28, 2026', {
    x: 0.8, y: H - 1.3, w: W - 1.6, h: 0.5,
    fontSize: 14, color: ICEBLUE, fontFace: 'Calibri', align: 'left',
  });
  s.addNotes('Welcome. Framing: a portfolio case that simulates the work of a data analyst for an investment fund evaluating the video game sector. Expected total duration: ~30 minutes.');
}

// =====================================================================
// 2. CONTEXT
// =====================================================================
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  s.addText('Context', {
    x: 0.6, y: 0.5, w: 6.0, h: 0.6, fontSize: 28, bold: true, color: NAVY, fontFace: 'Cambria',
  });
  s.addText([
    { text: 'The business problem\n', options: { bold: true, color: DARKTEXT, fontSize: 16, breakLine: true } },
    { text: 'An investment fund is evaluating entry into the video game sector and has no data-driven basis for deciding which genre to prioritise for its investment thesis in the PC/Steam market.\n\n', options: { color: DARKTEXT, fontSize: 14, breakLine: true } },
    { text: 'The question we answer\n', options: { bold: true, color: DARKTEXT, fontSize: 16, breakLine: true } },
    { text: 'Which genre and price-band combinations show the most consistent pattern of high reception (% positive reviews), controlling for game age?\n\n', options: { color: DARKTEXT, fontSize: 14, breakLine: true } },
    { text: 'The decision this enables\n', options: { bold: true, color: DARKTEXT, fontSize: 16, breakLine: true } },
    { text: 'Recommend 2-3 genres where the committee should prioritise investment due diligence.', options: { color: DARKTEXT, fontSize: 14 } },
  ], { x: 0.6, y: 1.35, w: 7.1, h: 5.5, valign: 'top', margin: 0 });

  // Stat callout card
  s.addShape('roundRect', { x: 8.15, y: 1.35, w: 4.55, h: 5.3, fill: { color: LIGHTBG }, line: { type: 'none' }, rectRadius: 0.12 });
  s.addText('117,430', { x: 8.45, y: 1.7, w: 3.95, h: 0.9, fontSize: 44, bold: true, color: ACCENT, fontFace: 'Cambria', align: 'center' });
  s.addText('games published on Steam analysed', { x: 8.45, y: 2.5, w: 3.95, h: 0.6, fontSize: 13, color: DARKTEXT, align: 'center' });
  s.addText('10', { x: 8.45, y: 3.35, w: 3.95, h: 0.9, fontSize: 44, bold: true, color: ACCENT, fontFace: 'Cambria', align: 'center' });
  s.addText('real video game genres evaluated', { x: 8.45, y: 4.15, w: 3.95, h: 0.6, fontSize: 13, color: DARKTEXT, align: 'center' });
  s.addText('8,998', { x: 8.45, y: 5.0, w: 3.95, h: 0.9, fontSize: 44, bold: true, color: ACCENT, fontFace: 'Cambria', align: 'center' });
  s.addText('paid games with ≥500 reviews (analysis base)', { x: 8.45, y: 5.8, w: 3.95, h: 0.7, fontSize: 13, color: DARKTEXT, align: 'center' });

  addFooter(s, 'Out of scope: PC/Steam only; does not establish causality; does not allocate investment budget.');
  s.addNotes('Fictional client: investment fund. Steam as a proxy for the PC/digital market. The question was defined and approved in Phase 1 (Ask) of the case.');
}

// =====================================================================
// 3. METHOD
// =====================================================================
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  s.addText('Method', {
    x: 0.6, y: 0.5, w: 6.0, h: 0.6, fontSize: 28, bold: true, color: NAVY, fontFace: 'Cambria',
  });

  const filas = [
    ['1', 'Sources', 'Steam Games Dataset (fronkongames, Kaggle, CC BY 4.0) + CPI-U inflation index (BLS, US) to adjust prices across years.'],
    ['2', 'Cleaning', 'Fixed a header bug in the raw CSV, excluded duplicates and 8,423 games with no genre assigned. Count reconciliation verified with an assert.'],
    ['3', 'Analysis filter', 'Paid games (Price > 0) with ≥500 reviews — the minimum volume for the % positive reviews to be statistically reliable.'],
    ['4', 'Price bands', 'Inflation-adjusted price quartiles, calculated on the data itself (not arbitrary bands).'],
  ];
  let y = 1.5;
  filas.forEach(([n, titulo, desc]) => {
    s.addShape('ellipse', { x: 0.6, y: y, w: 0.55, h: 0.55, fill: { color: ACCENT }, line: { type: 'none' } });
    s.addText(n, { x: 0.6, y: y, w: 0.55, h: 0.55, fontSize: 18, bold: true, color: WHITE, align: 'center', valign: 'middle' });
    s.addText(titulo, { x: 1.35, y: y - 0.05, w: 3.0, h: 0.6, fontSize: 15, bold: true, color: NAVY, valign: 'top' });
    s.addText(desc, { x: 4.5, y: y - 0.05, w: 8.2, h: 0.9, fontSize: 12.5, color: DARKTEXT, valign: 'top' });
    y += 1.35;
  });

  addFooter(s, 'Full, reproducible detail in notebooks/caso_steam_precio_recepcion.ipynb');
  s.addNotes('This is a summary; the full technical detail (ROCCC, biases, cleaning log) is in the notebook and in CASO.md. For this audience (investment committee) only the essentials are shown.');
}

// =====================================================================
// 4-7. FINDINGS (one per slide, image + interpretation)
// =====================================================================
const hallazgos = [
  {
    num: '1',
    titulo: 'The cheapest band has the worst reception, across all 10 genres without exception',
    img: GRAFICOS + '01_q1_vs_mejor_franja.png',
    interpretacion: 'In each of the 10 real game genres, the cheapest price band (≤$3.25 adjusted) gets the lowest median % of positive reviews. The improvement moving to the best band ranges from +2.5 to +5.0 percentage points.',
    notas: 'Three-part filter: the practical question is which price band suits each genre; the data shows Q1 is systematically lowest; the chart confirms it visually, bar by bar.',
  },
  {
    num: '2',
    titulo: 'The best reception clusters at mid-to-high prices, not at the expensive extreme',
    img: GRAFICOS + '02_heatmap_genero_franja.png',
    interpretacion: 'The heatmap shows the reception peak is at Q3 ($6.46-$12.36) or Q4, depending on genre — never Q1 or Q2. There is no simple linear "more expensive is always better" relationship.',
    notas: 'Recalculated via an alternate path (pivot_table) and matches groupby.agg. This rules out a calculation error behind the pattern.',
  },
  {
    num: '3',
    titulo: 'Adventure, Indie and Casual: the candidates with the best combined evidence',
    img: GRAFICOS + '03_ranking_efecto_candidatos.png',
    interpretacion: 'Ranking genres by effect size (the difference between Q1 and its best band), Adventure leads with +5.04 p.p. Together with Indie (+3.94 p.p., largest volume: 5,561 games) and Casual (+3.31 p.p., highest absolute reception: 89.6%), they combine the strongest evidence.',
    notas: 'Massively Multiplayer is left out: worst reception across all 4 bands and only 176 games of evidence.',
  },
  {
    num: '4',
    titulo: "The pattern is not an artefact of the game's age",
    img: GRAFICOS + '04_control_antiguedad.png',
    interpretacion: 'We split recent games from older ones: across the four reference genres, Q1 remains the weakest band in both groups. The correlation between age and % positive reviews is just -0.087.',
    notas: 'This is the key check against the most obvious alternative interpretation: that cheap games have simply been on the market longer and accumulated more negative reviews because of that.',
  },
];

hallazgos.forEach((h) => {
  const s = pres.addSlide();
  s.background = { color: WHITE };
  s.addText(`Finding ${h.num}`, {
    x: 0.6, y: 0.35, w: 4.0, h: 0.4, fontSize: 13, bold: true, color: ACCENT, fontFace: 'Calibri',
  });
  s.addText(h.titulo, {
    x: 0.6, y: 0.7, w: W - 1.2, h: 0.9, fontSize: 22, bold: true, color: NAVY, fontFace: 'Cambria', valign: 'top',
  });
  s.addImage({ path: h.img, x: 0.9, y: 1.75, w: 8.6, h: 4.85, sizing: { type: 'contain', w: 8.6, h: 4.85 } });
  s.addShape('roundRect', { x: 9.75, y: 1.75, w: 2.95, h: 4.85, fill: { color: LIGHTBG }, line: { type: 'none' }, rectRadius: 0.1 });
  s.addText(h.interpretacion, {
    x: 9.95, y: 1.95, w: 2.55, h: 4.5, fontSize: 12.5, color: DARKTEXT, valign: 'top', margin: 0,
  });
  addFooter(s, 'Source: Steam Games Dataset (fronkongames, CC BY 4.0) + BLS CPI-U.');
  s.addNotes(h.notas);
});

// =====================================================================
// 8. CANDIDATES - stat callouts
// =====================================================================
{
  const s = pres.addSlide();
  s.background = { color: NAVY };
  s.addText('Candidates with the best evidence for due diligence', {
    x: 0.6, y: 0.55, w: W - 1.2, h: 0.8, fontSize: 26, bold: true, color: WHITE, fontFace: 'Cambria',
  });
  const cards = [
    { genero: 'Adventure', stat: '+5.04 p.p.', desc: 'largest price effect on reception', n: '4,030 games of evidence' },
    { genero: 'Indie', stat: '5,561', desc: 'games — the largest volume of evidence', n: '+3.94 p.p. effect' },
    { genero: 'Casual', stat: '89.6%', desc: 'the highest absolute reception of the 10 genres', n: '+3.31 p.p. effect' },
  ];
  let x = 0.7;
  cards.forEach((c) => {
    s.addShape('roundRect', { x, y: 1.8, w: 3.85, h: 4.6, fill: { color: '283A7A' }, line: { type: 'none' }, rectRadius: 0.12 });
    s.addText(c.genero, { x: x + 0.25, y: 2.05, w: 3.35, h: 0.55, fontSize: 20, bold: true, color: ICEBLUE, fontFace: 'Cambria' });
    s.addText(c.stat, { x: x + 0.25, y: 2.7, w: 3.35, h: 1.0, fontSize: 40, bold: true, color: WHITE, fontFace: 'Cambria' });
    s.addText(c.desc, { x: x + 0.25, y: 3.75, w: 3.35, h: 1.1, fontSize: 13.5, color: ICEBLUE, valign: 'top' });
    s.addText(c.n, { x: x + 0.25, y: 5.6, w: 3.35, h: 0.6, fontSize: 12, color: 'A9BCE8', italic: true });
    x += 4.15;
  });
  addFooter(s, 'Massively Multiplayer is left off this list: insufficient evidence (176 games) and worst reception across all 4 bands.');
  s.addNotes('These three feed into the formal recommendations of Phase 6 (Act), not yet closed — this presents the evidence, not the final investment decision.');
}

// =====================================================================
// 9. LIMITATIONS
// =====================================================================
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  s.addText("What this analysis doesn't answer", {
    x: 0.6, y: 0.5, w: W - 1.2, h: 0.6, fontSize: 28, bold: true, color: NAVY, fontFace: 'Cambria',
  });
  const items = [
    ['Causality', 'The pattern is a descriptive correlation. It may reflect selection (studios who charge more also invest more in quality), not that raising the price improves reception.'],
    ['Long tail', "34.1% of the catalogue has no reviews and is excluded from the analysis for statistical reliability — not because the opportunity was dismissed."],
    ['Evolution over time', "There are no dated individual reviews; game age is used as a proxy, not the real evolution of reception."],
    ['Scope of the recommendation', "Prioritises genres, doesn't allocate budget or replace studio-or-publisher-specific due diligence."],
  ];
  let y = 1.55;
  items.forEach(([t, d]) => {
    s.addShape('roundRect', { x: 0.6, y, w: W - 1.2, h: 1.15, fill: { color: LIGHTBG }, line: { type: 'none' }, rectRadius: 0.08 });
    s.addText(t, { x: 0.9, y: y + 0.12, w: 3.0, h: 0.9, fontSize: 15, bold: true, color: ACCENT, valign: 'top' });
    s.addText(d, { x: 4.0, y: y + 0.12, w: W - 4.7, h: 0.9, fontSize: 12.5, color: DARKTEXT, valign: 'top' });
    y += 1.35;
  });
  s.addNotes("These limitations are stated explicitly, not hidden in an appendix, following Phase 5's exit gate.");
}

// =====================================================================
// 10. NEXT STEPS
// =====================================================================
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  s.addText('Next step: Phase 6 — Act', {
    x: 0.6, y: 0.5, w: W - 1.2, h: 0.6, fontSize: 28, bold: true, color: NAVY, fontFace: 'Cambria',
  });
  s.addText([
    { text: "This presentation closes the analysis and visualisation phases (Phases 4-5 of the case). Phase 6 will translate this evidence into:\n\n", options: { fontSize: 15, color: DARKTEXT, breakLine: true } },
    { text: '•  ', options: { color: ACCENT, bold: true, breakLine: false } },
    { text: 'A formal prioritisation recommendation between Adventure, Indie and Casual\n', options: { fontSize: 14, color: DARKTEXT, breakLine: true } },
    { text: '•  ', options: { color: ACCENT, bold: true, breakLine: false } },
    { text: 'The consolidated limitations for the investment committee\n', options: { fontSize: 14, color: DARKTEXT, breakLine: true } },
    { text: '•  ', options: { color: ACCENT, bold: true, breakLine: false } },
    { text: 'Desirable additional data before committing capital (e.g. studio size, marketing budget, the <500-review long tail)\n', options: { fontSize: 14, color: DARKTEXT, breakLine: true } },
  ], { x: 0.6, y: 1.5, w: W - 1.2, h: 3.5, valign: 'top', margin: 0 });
  s.addNotes('Make clear to the audience that the formal investment decision is not being made in this meeting — this is the evidence that will support it.');
}

// =====================================================================
// 11. APPENDIX - DETAILED METHODOLOGY
// =====================================================================
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  s.addText('Appendix — Methodology and checks', {
    x: 0.6, y: 0.5, w: W - 1.2, h: 0.6, fontSize: 24, bold: true, color: NAVY, fontFace: 'Cambria',
  });
  s.addText([
    { text: 'Adjusted price quartiles (base: 8,998 paid games with ≥500 reviews)\n', options: { bold: true, fontSize: 14, color: DARKTEXT, breakLine: true } },
    { text: 'Q1 ≤ $3.25  ·  Q2 $3.25-$6.46  ·  Q3 $6.46-$12.36  ·  Q4 > $12.36\n\n', options: { fontSize: 13, color: GRAY, breakLine: true } },
    { text: 'Checks applied before accepting the result\n', options: { bold: true, fontSize: 14, color: DARKTEXT, breakLine: true } },
    { text: '1. Sanity check: adjusted quartiles vs. raw unadjusted list price, same order of magnitude.\n', options: { fontSize: 12.5, color: DARKTEXT, breakLine: true } },
    { text: '2. Recalculation via an alternate path (pivot_table vs. groupby.agg) — matches point for point.\n', options: { fontSize: 12.5, color: DARKTEXT, breakLine: true } },
    { text: '3. Age ruled out as a confounder: correlation ≈ -0.087.\n', options: { fontSize: 12.5, color: DARKTEXT, breakLine: true } },
    { text: '4. Control by age band (recent vs. older): the pattern holds.\n', options: { fontSize: 12.5, color: DARKTEXT, breakLine: true } },
    { text: '5. Effect size quantified (2.50-5.04 p.p.), not just direction.\n', options: { fontSize: 12.5, color: DARKTEXT, breakLine: true } },
    { text: '6. Manual recalculation of % positive reviews on a random sample — matches exactly.\n', options: { fontSize: 12.5, color: DARKTEXT, breakLine: true } },
    { text: '7. Sample robustness reviewed by genre (n = 176 to 5,561); genres with n<350 flagged.', options: { fontSize: 12.5, color: DARKTEXT } },
  ], { x: 0.6, y: 1.4, w: W - 1.2, h: 5.6, valign: 'top', margin: 0 });
  addFooter(s, 'Full technical notebook: notebooks/caso_steam_precio_recepcion.ipynb');
  s.addNotes('Appendix for the senior analyst / technical audience who wants to audit the method.');
}

// =====================================================================
// 12. APPENDIX - PREPARED Q&A
// =====================================================================
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  s.addText('Appendix — Prepared questions and answers', {
    x: 0.6, y: 0.4, w: W - 1.2, h: 0.55, fontSize: 22, bold: true, color: NAVY, fontFace: 'Cambria',
  });
  const qa = [
    ["Isn't this just that expensive games come from bigger studios with better marketing?", "We don't rule it out: it's the case's most important causality limitation. The dataset has no studio size or marketing budget — recommended as additional data for Phase 6."],
    ["Why exclude the 34% of games with no reviews? Aren't opportunities lost there?", 'They are excluded for statistical reliability (with <500 reviews the % is noise), not because the opportunity is dismissed. Documented as pending additional analysis.'],
    ['How sensitive is the result to how the price bands were defined?', 'The quartiles were recalculated via an alternate path and compared against raw unadjusted price — same order of magnitude. A sensitivity test with fixed bands is a reasonable next step.'],
    ['Why trust a third-party dataset instead of direct data from Valve?', 'This is a declared failure in the ROCCC assessment (partial failure on "Original"). It\'s used as the best public source that combines price, genre and reviews; `estimated_owners` is not used as the main metric for this reason.'],
    ['What\'s the exact number behind "Adventure is the best candidate"?', 'Adventure: 4,030 games, +5.04 p.p. effect, peak median 87.48% in Q4. All calculations are reproducible in the technical notebook.'],
  ];
  let y = 1.15;
  qa.forEach(([q, a]) => {
    s.addText('Q: ' + q, { x: 0.6, y, w: W - 1.2, h: 0.5, fontSize: 12.5, bold: true, color: ACCENT, valign: 'top' });
    s.addText('A: ' + a, { x: 0.6, y: y + 0.42, w: W - 1.2, h: 0.7, fontSize: 11.5, color: DARKTEXT, valign: 'top' });
    y += 1.18;
  });
  s.addNotes("The five toughest questions, prepared in writing, following Phase 5's exit gate.");
}

// =====================================================================
// 13. CLOSE
// =====================================================================
{
  const s = pres.addSlide();
  s.background = { color: NAVY };
  s.addText('Thank you', {
    x: 0.8, y: 2.6, w: W - 1.6, h: 1.2, fontSize: 40, bold: true, color: WHITE, fontFace: 'Cambria',
  });
  s.addText('Source: Steam Games Dataset (fronkongames, Kaggle, CC BY 4.0) + BLS CPI-U (public domain).', {
    x: 0.8, y: 3.9, w: W - 1.6, h: 0.5, fontSize: 14, color: ICEBLUE,
  });
  s.addText('Portfolio case study — Data Analyst  ·  contact: juanesa2002@gmail.com', {
    x: 0.8, y: H - 1.2, w: W - 1.6, h: 0.5, fontSize: 12, color: 'A9BCE8',
  });
  s.addNotes('Close. Open the floor for questions using the prepared Q&A appendix.');
}

pres.writeFile({ fileName: path.join(RUTA_BASE, 'entregables', 'presentacion_fase5.pptx') }).then(() => {
  console.log('PPTX generado');
});
