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
// 1. TITULO
// =====================================================================
{
  const s = pres.addSlide();
  s.background = { color: NAVY };
  s.addText('Precio y recepción en Steam', {
    x: 0.8, y: 1.7, w: W - 1.6, h: 1.0,
    fontSize: 24, color: ICEBLUE, fontFace: 'Calibri', bold: false, align: 'left',
  });
  s.addText('¿En qué géneros debería un fondo de inversión priorizar su due diligence?', {
    x: 0.8, y: 2.5, w: W - 1.6, h: 2.0,
    fontSize: 38, color: WHITE, fontFace: 'Cambria', bold: true, align: 'left',
  });
  s.addText('Caso de estudio de portafolio — Analista de Datos  ·  28 de julio de 2026', {
    x: 0.8, y: H - 1.3, w: W - 1.6, h: 0.5,
    fontSize: 14, color: ICEBLUE, fontFace: 'Calibri', align: 'left',
  });
  s.addNotes('Bienvenida. Marco: caso de portafolio que simula el trabajo de un analista de datos para un fondo de inversión evaluando el sector de videojuegos. Duración total prevista: ~30 minutos.');
}

// =====================================================================
// 2. CONTEXTO
// =====================================================================
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  s.addText('Contexto', {
    x: 0.6, y: 0.5, w: 6.0, h: 0.6, fontSize: 28, bold: true, color: NAVY, fontFace: 'Cambria',
  });
  s.addText([
    { text: 'El problema de negocio\n', options: { bold: true, color: DARKTEXT, fontSize: 16, breakLine: true } },
    { text: 'Un fondo de inversión evalúa entrar al sector de videojuegos y no tiene un criterio basado en datos para decidir en qué género priorizar su tesis de inversión en el mercado de PC/Steam.\n\n', options: { color: DARKTEXT, fontSize: 14, breakLine: true } },
    { text: 'La pregunta que respondemos\n', options: { bold: true, color: DARKTEXT, fontSize: 16, breakLine: true } },
    { text: '¿Qué combinaciones de género y franja de precio muestran el patrón más consistente de alta recepción (% de reseñas positivas), controlando por antigüedad del juego?\n\n', options: { color: DARKTEXT, fontSize: 14, breakLine: true } },
    { text: 'La decisión que habilita\n', options: { bold: true, color: DARKTEXT, fontSize: 16, breakLine: true } },
    { text: 'Recomendar 2-3 géneros donde el comité debería priorizar due diligence de inversión.', options: { color: DARKTEXT, fontSize: 14 } },
  ], { x: 0.6, y: 1.35, w: 7.1, h: 5.5, valign: 'top', margin: 0 });

  // Stat callout card
  s.addShape('roundRect', { x: 8.15, y: 1.35, w: 4.55, h: 5.3, fill: { color: LIGHTBG }, line: { type: 'none' }, rectRadius: 0.12 });
  s.addText('117.430', { x: 8.45, y: 1.7, w: 3.95, h: 0.9, fontSize: 44, bold: true, color: ACCENT, fontFace: 'Cambria', align: 'center' });
  s.addText('juegos publicados en Steam analizados', { x: 8.45, y: 2.5, w: 3.95, h: 0.6, fontSize: 13, color: DARKTEXT, align: 'center' });
  s.addText('10', { x: 8.45, y: 3.35, w: 3.95, h: 0.9, fontSize: 44, bold: true, color: ACCENT, fontFace: 'Cambria', align: 'center' });
  s.addText('géneros de videojuego reales evaluados', { x: 8.45, y: 4.15, w: 3.95, h: 0.6, fontSize: 13, color: DARKTEXT, align: 'center' });
  s.addText('8.998', { x: 8.45, y: 5.0, w: 3.95, h: 0.9, fontSize: 44, bold: true, color: ACCENT, fontFace: 'Cambria', align: 'center' });
  s.addText('juegos de pago con ≥500 reseñas (base de análisis)', { x: 8.45, y: 5.8, w: 3.95, h: 0.7, fontSize: 13, color: DARKTEXT, align: 'center' });

  addFooter(s, 'Fuera de alcance: solo PC/Steam; no establece causalidad; no asigna presupuesto de inversión.');
  s.addNotes('Cliente ficticio: fondo de inversión. Steam como proxy del mercado de PC/digital. La pregunta fue definida y aprobada en la fase 1 (Preguntar) del caso.');
}

// =====================================================================
// 3. METODO
// =====================================================================
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  s.addText('Método', {
    x: 0.6, y: 0.5, w: 6.0, h: 0.6, fontSize: 28, bold: true, color: NAVY, fontFace: 'Cambria',
  });

  const filas = [
    ['1', 'Fuentes', 'Steam Games Dataset (fronkongames, Kaggle, CC BY 4.0) + índice de inflación CPI-U (BLS, EE. UU.) para ajustar precios entre años.'],
    ['2', 'Limpieza', 'Corrección de un bug de cabecera del CSV crudo, exclusión de duplicados y de 8.423 juegos sin género asignado. Reconciliación de conteos verificada con assert.'],
    ['3', 'Filtro de análisis', 'Juegos de pago (Price > 0) con ≥500 reseñas — el volumen mínimo para que el % de reseñas positivas sea estadísticamente confiable.'],
    ['4', 'Franjas de precio', 'Cuartiles de precio ajustado por inflación, calculados sobre los datos mismos (no bandas arbitrarias).'],
  ];
  let y = 1.5;
  filas.forEach(([n, titulo, desc]) => {
    s.addShape('ellipse', { x: 0.6, y: y, w: 0.55, h: 0.55, fill: { color: ACCENT }, line: { type: 'none' } });
    s.addText(n, { x: 0.6, y: y, w: 0.55, h: 0.55, fontSize: 18, bold: true, color: WHITE, align: 'center', valign: 'middle' });
    s.addText(titulo, { x: 1.35, y: y - 0.05, w: 3.0, h: 0.6, fontSize: 15, bold: true, color: NAVY, valign: 'top' });
    s.addText(desc, { x: 4.5, y: y - 0.05, w: 8.2, h: 0.9, fontSize: 12.5, color: DARKTEXT, valign: 'top' });
    y += 1.35;
  });

  addFooter(s, 'Detalle completo y reproducible en notebooks/caso_steam_precio_recepcion.ipynb');
  s.addNotes('Este es un resumen; el detalle técnico completo (ROCCC, sesgos, bitácora de limpieza) está en el notebook y en CASO.md. Para esta audiencia (comité de inversión) se muestra solo lo esencial.');
}

// =====================================================================
// 4-7. HALLAZGOS (uno por diapositiva, imagen + interpretacion)
// =====================================================================
const hallazgos = [
  {
    num: '1',
    titulo: 'La franja más barata es la de peor recepción, en los 10 géneros sin excepción',
    img: GRAFICOS + '01_q1_vs_mejor_franja.png',
    interpretacion: 'En cada uno de los 10 géneros de juego reales, la franja de precio más económica (≤3,25 USD ajustados) obtiene la mediana de % de reseñas positivas más baja. La mejora al pasar a la mejor franja va de +2,5 a +5,0 puntos porcentuales.',
    notas: 'Filtro de tres partes: la pregunta practica es que franja de precio conviene por genero; los datos muestran Q1 sistematicamente mas bajo; el grafico lo confirma visualmente barra por barra.',
  },
  {
    num: '2',
    titulo: 'La mejor recepción se concentra en precios medios-altos, no en el extremo caro',
    img: GRAFICOS + '02_heatmap_genero_franja.png',
    interpretacion: 'El mapa de calor muestra que el pico de recepción está en Q3 (6,46–12,36 USD) o Q4, según el género — nunca en Q1 o Q2. No hay una relación lineal simple de "más caro siempre mejor".',
    notas: 'Recalculado por via alterna (pivot_table) y coincide con groupby.agg. Esto descarta un error de calculo detras del patron.',
  },
  {
    num: '3',
    titulo: 'Adventure, Indie y Casual: los candidatos con mejor evidencia combinada',
    img: GRAFICOS + '03_ranking_efecto_candidatos.png',
    interpretacion: 'Al ordenar los géneros por el tamaño del efecto (diferencia entre Q1 y su mejor franja), Adventure lidera con +5,04 p.p. Junto con Indie (+3,94 p.p., mayor volumen: 5.561 juegos) y Casual (+3,31 p.p., mayor recepción absoluta: 89,6%), combinan la evidencia más sólida.',
    notas: 'Massively Multiplayer queda fuera: peor recepcion en las 4 franjas y solo 176 juegos de evidencia.',
  },
  {
    num: '4',
    titulo: 'El patrón no es un artefacto de la antigüedad del juego',
    img: GRAFICOS + '04_control_antiguedad.png',
    interpretacion: 'Separamos juegos recientes de juegos más antiguos: en los cuatro géneros de referencia, Q1 sigue siendo la franja más débil en ambos grupos. La correlación entre antigüedad y % de reseñas positivas es de apenas −0,087.',
    notas: 'Esta es la verificacion clave contra la interpretacion alternativa mas obvia: que los juegos baratos simplemente llevan mas tiempo en el mercado y acumularon mas resenas negativas por eso.',
  },
];

hallazgos.forEach((h) => {
  const s = pres.addSlide();
  s.background = { color: WHITE };
  s.addText(`Hallazgo ${h.num}`, {
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
  addFooter(s, 'Fuente: Steam Games Dataset (fronkongames, CC BY 4.0) + BLS CPI-U.');
  s.addNotes(h.notas);
});

// =====================================================================
// 8. CANDIDATOS - stat callouts
// =====================================================================
{
  const s = pres.addSlide();
  s.background = { color: NAVY };
  s.addText('Candidatos con mejor evidencia para due diligence', {
    x: 0.6, y: 0.55, w: W - 1.2, h: 0.8, fontSize: 26, bold: true, color: WHITE, fontFace: 'Cambria',
  });
  const cards = [
    { genero: 'Adventure', stat: '+5,04 p.p.', desc: 'mayor efecto de precio sobre recepción', n: '4.030 juegos de evidencia' },
    { genero: 'Indie', stat: '5.561', desc: 'juegos — el mayor volumen de evidencia', n: '+3,94 p.p. de efecto' },
    { genero: 'Casual', stat: '89,6%', desc: 'la recepción absoluta más alta de los 10 géneros', n: '+3,31 p.p. de efecto' },
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
  addFooter(s, 'Massively Multiplayer queda fuera de esta lista: evidencia insuficiente (176 juegos) y peor recepción en las 4 franjas.');
  s.addNotes('Estos tres son insumo para las recomendaciones formales de la fase 6 (Actuar), aun no cerradas — aqui se presenta la evidencia, no la decision final de inversion.');
}

// =====================================================================
// 9. LIMITACIONES
// =====================================================================
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  s.addText('Qué no responde este análisis', {
    x: 0.6, y: 0.5, w: W - 1.2, h: 0.6, fontSize: 28, bold: true, color: NAVY, fontFace: 'Cambria',
  });
  const items = [
    ['Causalidad', 'El patrón es una correlación descriptiva. Puede reflejar selección (estudios que cobran más también invierten más en calidad), no que subir el precio mejore la recepción.'],
    ['Cola larga', '34,1% del catálogo no tiene ninguna reseña y queda fuera del análisis por confiabilidad estadística — no porque se haya descartado como oportunidad.'],
    ['Evolución en el tiempo', 'No hay reseñas fechadas individuales; se usa la antigüedad del juego como proxy, no la evolución real de la recepción.'],
    ['Alcance de la recomendación', 'Prioriza géneros, no asigna presupuesto ni reemplaza el due diligence específico de cada estudio o publisher.'],
  ];
  let y = 1.55;
  items.forEach(([t, d]) => {
    s.addShape('roundRect', { x: 0.6, y, w: W - 1.2, h: 1.15, fill: { color: LIGHTBG }, line: { type: 'none' }, rectRadius: 0.08 });
    s.addText(t, { x: 0.9, y: y + 0.12, w: 3.0, h: 0.9, fontSize: 15, bold: true, color: ACCENT, valign: 'top' });
    s.addText(d, { x: 4.0, y: y + 0.12, w: W - 4.7, h: 0.9, fontSize: 12.5, color: DARKTEXT, valign: 'top' });
    y += 1.35;
  });
  s.addNotes('Estas limitaciones estan escritas explicitamente, no escondidas en un anexo, siguiendo la puerta de salida de la fase 5.');
}

// =====================================================================
// 10. PROXIMOS PASOS
// =====================================================================
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  s.addText('Próximo paso: fase 6 — Actuar', {
    x: 0.6, y: 0.5, w: W - 1.2, h: 0.6, fontSize: 28, bold: true, color: NAVY, fontFace: 'Cambria',
  });
  s.addText([
    { text: 'Esta presentación cierra la fase de análisis y visualización (fases 4-5 del caso). La fase 6 traducirá esta evidencia en:\n\n', options: { fontSize: 15, color: DARKTEXT, breakLine: true } },
    { text: '•  ', options: { color: ACCENT, bold: true, breakLine: false } },
    { text: 'Una recomendación formal de priorización entre Adventure, Indie y Casual\n', options: { fontSize: 14, color: DARKTEXT, breakLine: true } },
    { text: '•  ', options: { color: ACCENT, bold: true, breakLine: false } },
    { text: 'Las limitaciones consolidadas para el comité de inversión\n', options: { fontSize: 14, color: DARKTEXT, breakLine: true } },
    { text: '•  ', options: { color: ACCENT, bold: true, breakLine: false } },
    { text: 'Los datos adicionales deseables antes de comprometer capital (p. ej. tamaño de estudio, presupuesto de marketing, cola larga <500 reseñas)\n', options: { fontSize: 14, color: DARKTEXT, breakLine: true } },
  ], { x: 0.6, y: 1.5, w: W - 1.2, h: 3.5, valign: 'top', margin: 0 });
  s.addNotes('Dejar claro a la audiencia que la decision de inversion formal no se toma en esta reunion, sino que esta es la evidencia que la sustentara.');
}

// =====================================================================
// 11. ANEXO - METODOLOGIA DETALLADA
// =====================================================================
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  s.addText('Anexo — Metodología y verificaciones', {
    x: 0.6, y: 0.5, w: W - 1.2, h: 0.6, fontSize: 24, bold: true, color: NAVY, fontFace: 'Cambria',
  });
  s.addText([
    { text: 'Cuartiles de precio ajustado (base: 8.998 juegos de pago con ≥500 reseñas)\n', options: { bold: true, fontSize: 14, color: DARKTEXT, breakLine: true } },
    { text: 'Q1 ≤ 3,25 USD  ·  Q2 3,25–6,46  ·  Q3 6,46–12,36  ·  Q4 > 12,36 USD\n\n', options: { fontSize: 13, color: GRAY, breakLine: true } },
    { text: 'Verificaciones aplicadas antes de aceptar el resultado\n', options: { bold: true, fontSize: 14, color: DARKTEXT, breakLine: true } },
    { text: '1. Prueba de sensatez: cuartiles ajustados vs. precio de lista bruto, mismo orden de magnitud.\n', options: { fontSize: 12.5, color: DARKTEXT, breakLine: true } },
    { text: '2. Recálculo por vía alterna (pivot_table vs. groupby.agg) — coincide punto por punto.\n', options: { fontSize: 12.5, color: DARKTEXT, breakLine: true } },
    { text: '3. Antigüedad como confusor descartada: correlación ≈ −0,087.\n', options: { fontSize: 12.5, color: DARKTEXT, breakLine: true } },
    { text: '4. Control por banda de antigüedad (recientes vs. viejos): el patrón se sostiene.\n', options: { fontSize: 12.5, color: DARKTEXT, breakLine: true } },
    { text: '5. Efecto de tamaño cuantificado (2,50–5,04 p.p.), no solo dirección.\n', options: { fontSize: 12.5, color: DARKTEXT, breakLine: true } },
    { text: '6. Recálculo manual de % de reseñas positivas sobre muestra al azar — coincide exacto.\n', options: { fontSize: 12.5, color: DARKTEXT, breakLine: true } },
    { text: '7. Robustez de muestra revisada por género (n = 176 a 5.561); géneros con n<350 marcados.', options: { fontSize: 12.5, color: DARKTEXT } },
  ], { x: 0.6, y: 1.4, w: W - 1.2, h: 5.6, valign: 'top', margin: 0 });
  addFooter(s, 'Notebook técnico completo: notebooks/caso_steam_precio_recepcion.ipynb');
  s.addNotes('Anexo para el analista senior / audiencia tecnica que quiera auditar el metodo.');
}

// =====================================================================
// 12. ANEXO - Q&A PREPARADO
// =====================================================================
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  s.addText('Anexo — Preguntas y respuestas preparadas', {
    x: 0.6, y: 0.4, w: W - 1.2, h: 0.55, fontSize: 22, bold: true, color: NAVY, fontFace: 'Cambria',
  });
  const qa = [
    ['¿No es esto solo que los juegos caros vienen de estudios más grandes con mejor marketing?', 'No lo descartamos: es la limitación de causalidad más importante del caso. El dataset no tiene tamaño de estudio ni presupuesto de marketing — se recomienda como dato adicional para la fase 6.'],
    ['¿Por qué excluir el 34% de juegos sin reseñas? ¿No se pierden oportunidades ahí?', 'Se excluyen por confiabilidad estadística (con <500 reseñas el % es ruido), no porque se descarte la oportunidad. Queda documentado como análisis adicional pendiente.'],
    ['¿Qué tan sensible es el resultado a cómo definieron las franjas de precio?', 'Los cuartiles se recalcularon por vía alterna y se compararon contra el precio bruto sin ajustar — mismo orden de magnitud. Una prueba de sensibilidad con bandas fijas es un siguiente paso razonable.'],
    ['¿Por qué confiar en un dataset de terceros y no en datos directos de Valve?', 'Es una falla declarada en la evaluación ROCCC (falla parcial en "Original"). Se usa por ser la mejor fuente pública que junta precio, género y reseñas; `estimated_owners` no se usa como métrica principal por esta razón.'],
    ['¿Cuál es el número exacto detrás de "Adventure es el mejor candidato"?', 'Adventure: 4.030 juegos, +5,04 p.p. de efecto, mediana máxima 87,48% en Q4. Todos los cálculos son reproducibles en el notebook técnico.'],
  ];
  let y = 1.15;
  qa.forEach(([q, a]) => {
    s.addText('P: ' + q, { x: 0.6, y, w: W - 1.2, h: 0.5, fontSize: 12.5, bold: true, color: ACCENT, valign: 'top' });
    s.addText('R: ' + a, { x: 0.6, y: y + 0.42, w: W - 1.2, h: 0.7, fontSize: 11.5, color: DARKTEXT, valign: 'top' });
    y += 1.18;
  });
  s.addNotes('Las cinco preguntas mas incomodas, preparadas por escrito, siguiendo la puerta de salida de la fase 5.');
}

// =====================================================================
// 13. CIERRE
// =====================================================================
{
  const s = pres.addSlide();
  s.background = { color: NAVY };
  s.addText('Gracias', {
    x: 0.8, y: 2.6, w: W - 1.6, h: 1.2, fontSize: 40, bold: true, color: WHITE, fontFace: 'Cambria',
  });
  s.addText('Fuente: Steam Games Dataset (fronkongames, Kaggle, CC BY 4.0) + BLS CPI-U (dominio público).', {
    x: 0.8, y: 3.9, w: W - 1.6, h: 0.5, fontSize: 14, color: ICEBLUE,
  });
  s.addText('Caso de estudio de portafolio — Analista de Datos  ·  contacto: juanesa2002@gmail.com', {
    x: 0.8, y: H - 1.2, w: W - 1.6, h: 0.5, fontSize: 12, color: 'A9BCE8',
  });
  s.addNotes('Cierre. Abrir espacio de preguntas usando el anexo de Q&A preparado.');
}

pres.writeFile({ fileName: path.join(RUTA_BASE, 'entregables', 'presentacion_fase5.pptx') }).then(() => {
  console.log('PPTX generado');
});
