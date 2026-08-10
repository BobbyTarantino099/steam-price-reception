# Caso: Precio y recepción en Steam (caso de inversión en videojuegos)

**Estado:** fase 6 — Actuar (en curso; entregables escritos, publicación y ensayo pendientes)
**Última actualización:** 2026-07-28

## 0. Elegir (ficha de decisión)

**Fecha:** 2026-07-28

### El caso
- **Sector / cliente ficticio:** Fondo de inversión evaluando entrada en el sector de videojuegos,
  usando el mercado de Steam como proxy del mercado de PC/digital.
- **Problema de negocio en una frase:** ¿Qué combinaciones de género y franja de precio en Steam
  logran mejor recepción (reseñas) sin sacrificar precio, y qué géneros son por tanto mejores
  candidatos de inversión?
- **Decisión concreta que habilita:** Recomendar en qué género(s) conviene que el fondo priorice
  su tesis de inversión (p. ej. estudios o publishers de ese género).
- **Audiencia de la presentación:** Portafolio / reclutadores (caso de demostración de habilidad).

### Los datos
- **Fuente candidata:** Steam Games Dataset (fronkongames), Kaggle / Hugging Face.
- **Licencia:** CC BY 4.0 — requiere atribución en el README público.
- **Periodo y volumen:** 125.855 juegos publicados en Steam, catálogo histórico completo hasta la
  fecha de recolección (dataset con actualizaciones periódicas).
- **Prueba de integridad inicial:** ⚠️ verificada solo a nivel de metadatos (columnas, licencia,
  volumen, procedencia vía API oficial + SteamSpy). Nulos, duplicados y unicidad de clave reales
  quedan pendientes de la prueba completa en fase 2, con el archivo ya cargado. Dos advertencias
  conocidas de antemano:
  1. El CSV crudo tiene un bug de cabecera que desalinea las columnas posteriores a
     `Discount`/`DLC count`.
  2. `estimated_owners` viene en rangos, no en cifra exacta.
- **¿Contiene los campos que la pregunta exige?** Sí — `price`, `genres`, `positive`/`negative`
  (reseñas). Falta: reseñas individuales fechadas (solo agregado por juego), así que "sostener
  precio en el tiempo" se analizará por antigüedad del juego, no por evolución real de reseñas.

### Calibración
- **Estimación de esfuerzo:** ~1 semana de trabajo enfocado.
- **¿Da para 30 minutos de presentación?** Sí.
- **¿Hay limpieza real que documentar?** Sí — bug de cabecera, precios en 0 para F2P a tratar
  aparte, posibles nulos en tags/géneros, duplicados potenciales por reediciones.

### Encaje en el portafolio
- **Qué demuestra que mis otros casos no:** Es el primer caso, así que fija la base: traducir una
  pregunta de inversión a un análisis de pricing + sentimiento, con Python/pandas, sobre un dataset
  con una imperfección estructural real (no solo nulos triviales).
- **Herramienta principal:** Python (pandas).
- **Nivel de saturación del dataset:** Medio.

### Decisión
- [x] Adelante
- [ ] Descartado — motivo:

**Puerta de salida fase 0:** ✅ completa (aprobada por el usuario el 2026-07-28).

---

## 1. Preguntar

**Estado:** ✅ cerrada (aprobada por el usuario el 2026-07-28)

- **Problema de negocio:** Un fondo de inversión enfocado en videojuegos no tiene un criterio
  basado en datos para decidir en qué género priorizar su tesis de inversión en el mercado de
  PC/Steam.
- **Pregunta analítica (SMART):** ¿Qué combinaciones de género y franja de precio (cuartiles de
  precio ajustado por inflación, calculados sobre juegos de pago con ≥500 reseñas) en el catálogo
  histórico de Steam muestran el patrón más consistente de alto % de reseñas positivas,
  controlando por antigüedad del juego?
- **Decisión que habilita:** Recomendar 2-3 géneros donde el comité debería priorizar due
  diligence de inversión, con la evidencia de qué franja de precio sostiene mejor recepción en
  cada uno.
- **Tipo de problema:** Encontrar patrones.

- **Partes interesadas:**

| Quién | Qué decide / necesita | Formato |
|---|---|---|
| Comité de inversión (primaria) | Decide dónde priorizar due diligence; necesita recomendación clara con evidencia y riesgos | Presentación ~30 min + resumen ejecutivo |
| Analista senior (secundaria) | Valida método, limpieza y supuestos | Bitácora + documentación técnica (notebook) |

- **Métricas:**

| Métrica | Fórmula | Unidad | Granularidad | Ventana |
|---|---|---|---|---|
| % reseñas positivas | `positive / (positive + negative) × 100` | Porcentaje | Por juego | Acumulado histórico a la fecha de recolección del dataset |
| Categoría Steam (solo para presentar) | Recalculada con umbrales públicos de Steam sobre volumen y % positivo | Categórica (Overwhelmingly Positive…Negative) | Por juego | Igual que arriba |
| Filtro de inclusión | `positive + negative ≥ 500` | Conteo | Por juego | — |
| Precio ajustado por inflación | `price × (CPI_base / CPI_release_year)`, base = año más reciente del dataset | USD reales | Por juego | Requiere índice CPI (fuente externa, EE.UU.) — pendiente de validar en fase 2 |
| Antigüedad del juego | `año_base − release_year` | Años | Por juego | Variable de control, no filtro |
| Franja de precio | Cuartiles de precio **ajustado** sobre juegos de pago (price > 0) que pasen el filtro de reseñas | Rango USD reales | Por juego | Estática (catálogo completo) |

⚠️ Pendiente (no bloquea esta fase, se resuelve en Procesar): cómo desagregar juegos con
múltiples géneros.

⚠️ Condicional: la corrección por inflación depende de que la fuente CPI externa pase la prueba
de integridad de la fase 2. Si no la pasa, este punto se degrada a "limitación declarada" y se
documenta el porqué en vez de aplicarse silenciosamente.

- **Fuera de alcance:**
  - Solo PC/Steam — no consolas ni móvil.
  - Juegos F2P quedan fuera del análisis de franja de precio (se documentan como contexto aparte).
  - No establece causalidad, solo patrón/correlación descriptiva.
  - No asigna presupuesto de inversión, solo prioriza géneros para due diligence.
  - Excluye la cola larga con <500 reseñas (indie/nicho) — se deja como "entregable adicional
    para explorar" en fase 6.

**Puerta de salida fase 1:** ✅ completa
- [x] Problema de negocio en 1-2 frases, sin jerga.
- [x] Pregunta analítica SMART y justa.
- [x] Decisión concreta escrita.
- [x] Tipo de problema identificado.
- [x] Partes interesadas mapeadas con lo que cada una necesita.
- [x] Métricas con definición operativa.
- [x] Alcance con qué queda explícitamente fuera.

## 2. Preparar

**Estado:** ✅ cerrada (aprobada por el usuario el 2026-07-28)

- **Fuentes:** ver fichas completas en `documentacion/fichas-de-fuente.md`.
  1. **Steam Games Dataset** (Kaggle, fronkongames) — descargado 2026-07-28. 125.855 filas × 40
     columnas reales (la cabecera cruda solo declara 39, ver bug abajo). CC BY 4.0.
  2. **CPI-U** (Bureau of Labor Statistics, EE. UU., serie `CUUR0000SA0`) — aprobada el 2026-07-28
     como segunda fuente para el ajuste por inflación de la fase 1. Dominio público. Se descargará
     en fase 3 al aplicar el ajuste.

- **Evaluación ROCCC:** detalle completo en `documentacion/fichas-de-fuente.md`.
  - Steam Games Dataset: falla parcialmente en **O**riginal (es agregador de tercera parte, no
    Valve directo) y en el componente de confiabilidad de `estimated_owners` (estimación de
    SteamSpy, no ventas reales). El resto de las letras es alto. No se descarta; se declara como
    limitación.
  - CPI-U: no falla ninguna letra — primera parte, actual, comprensivo para el uso previsto,
    documentado.

- **Sesgos identificados:**
  - **Sesgo de supervivencia:** el dataset solo contiene juegos que llegaron a publicarse en
    Steam; no capta juegos rechazados, retirados, ni la industria fuera de PC/Steam.
  - **Sesgo de muestreo (cola larga):** 42.899 juegos (34,1%) tienen 0 reseñas (positivas +
    negativas). El filtro de ≥500 reseñas ya decidido en fase 1 excluye deliberadamente esta cola;
    la muestra final queda sesgada hacia juegos exitosos/visibles. Es una decisión de alcance
    documentada, no un sesgo oculto.
  - **Sesgo de medición en `estimated_owners`:** viene en rangos categóricos estimados por
    SteamSpy, no en cifra confirmada por Valve. No se usará como métrica principal del análisis,
    solo como contexto.
  - **Multi-género sin resolver:** 6,69% de los juegos no tiene género asignado; el resto tiene
    entre 1 y 19 géneros (mediana ~3). Cómo desagregar géneros múltiples queda pendiente para
    fase 3 (ya señalado en fase 1).

- **Licencia / privacidad / seguridad / accesibilidad:**
  - Steam Games Dataset: CC BY 4.0, requiere atribución en el README público. Sin PII. Archivo
    estático local, sin credenciales involucradas.
  - CPI-U: dominio público, sin restricciones, sin PII.
  - **Decisión de accesibilidad:** el crudo (~400 MB) no se sube al repo público del portafolio;
    el README enlazará directamente a la fuente en Kaggle. Confirmado con el usuario.

- **Prueba de integridad inicial:**
  - Filas × columnas: 125.855 × 40 (la cabecera cruda declara 39 columnas; cada fila trae 40
    campos). **Bug de cabecera confirmado y diagnosticado:** el nombre `DiscountDLC count`
    (posición 7) fusiona dos columnas reales, `Discount` y `DLC count`. Se corrigió insertando el
    nombre faltante antes de cargar el archivo — el procedimiento se documenta en
    `documentacion/fichas-de-fuente.md` y deberá repetirse igual al inicio de la fase 3.
  - Rango de fechas real: 1997-06-30 a 2026-12-01. Solo 2 filas con fecha de lanzamiento futura
    (aún no publicados, 0 reseñas) — se excluirán en fase 3.
  - Nulos por columna: altos y esperables en columnas no usadas por la pregunta (`Movies` 100%,
    `Score rank` 99,97%, `Metacritic url` 96,6%, `Reviews` 90,3%). Las columnas que sí usa la
    pregunta tienen nulos bajos: `Genres` 6,69%, `Price` 0%, `Positive`/`Negative` 0%.
  - Unicidad de clave: `AppID` 125.855 valores únicos sobre 125.855 filas → 0 duplicados exactos.
    0 filas completamente duplicadas.
  - Rangos numéricos: sin negativos en `Price`, `Positive`, `Negative`. `DLC count` llega a 3.703
    en un caso (Fantasy Grounds VTT, verificado como real — tiene miles de DLC de mesa). `Price`
    máximo 999,98 USD, sin valores imposibles. `Metacritic score` usa `0` como centinela de "sin
    dato" (solo 3,38% de los juegos tiene puntaje real) — documentado en el diccionario para que
    fase 3/4 no lo confunda con una puntuación real.
  - Detalle columna por columna en `documentacion/diccionario-de-datos.md`.

- **Confirmación:** estos datos sí responden la pregunta de fase 1. `price`, `genres`, `positive`
  y `negative` están presentes y con nulos manejables. La única brecha (reseñas fechadas
  individuales) ya estaba prevista y resuelta con el proxy de antigüedad del juego.

- **Puerta de salida:** ✅ completa
  - [x] Cada fuente tiene su ficha completa.
  - [x] ROCCC evaluado por fuente, con las fallas declaradas.
  - [x] Sesgos potenciales identificados por escrito.
  - [x] Licencia, privacidad, seguridad y accesibilidad resueltas.
  - [x] Diccionario de datos escrito.
  - [x] Copia inmutable del crudo guardada, con convención de nombres
        (`datos/crudos/steam_fronkongames_catalogo-historico_2026-07-28.csv`).
  - [x] Prueba de integridad inicial ejecutada, con sus resultados anotados.
  - [x] Confirmado que estos datos sí pueden responder la pregunta de la fase 1.

## 3. Procesar

**Estado:** ✅ cerrada (aprobada por el usuario el 2026-07-28)

- **Herramienta y justificación:** Python (pandas) — decidido en fase 0. Se confirma en esta fase:
  el proceso exige reproducibilidad sobre un archivo de 400 MB con un bug estructural de cabecera,
  algo inviable de auditar a mano en una hoja de cálculo.
- **Bitácora:** detalle completo de las 8 transformaciones en `bitacora-limpieza.md`.
  Script reproducible: `notebooks/procesar.py` (corre de punta a punta desde el crudo).
- **Transformaciones clave:**
  1. Corrección del bug de cabecera (`DiscountDLC count` → `Discount` + `DLC count`).
  2. Exclusión de 2 juegos con fecha de lanzamiento futura.
  3. 15 columnas descartadas por estar fuera de alcance (nulos altos o texto no estructurado).
  4. 0 duplicados por `AppID` (reconfirmado).
  5. Exclusión de 8.423 juegos sin género asignado (no clasificables).
  6. Enriquecimiento con CPI-U de BLS: `anio_lanzamiento`, `antiguedad_anios`,
     `precio_ajustado_usd` (año base 2026, con limitación declarada: el CPI de 2026 es un promedio
     parcial de solo 4 meses).
  7. Cálculo de `pct_resenas_positivas` (nulo, no 0%, para los 34.589 juegos sin ninguna reseña).
  8. Dataset derivado `steam_juegos_por_genero.csv`, explotado por género (decisión confirmada con
     el usuario: un juego con N géneros genera N filas).
- **Reconciliación de conteos:** 125.855 inicial − 2 (fecha futura) − 0 (duplicados) − 8.423
  (sin género) = **117.430 final**. Verificado con `assert` en el script. El dataset explotado por
  género tiene 338.575 filas juego-género.
- **Valores atípicos investigados:** `DLC count` máximo de 3.703 (Fantasy Grounds VTT, verificado
  como real, no se elimina). `Metacritic score` usa `0` como centinela de "sin dato" (documentado,
  no se confunde con puntuación real).
- **Observación para fase 4:** la taxonomía `Genres` de Steam mezcla géneros reales (`Action`,
  `RPG`) con descriptores de contenido/modelo de negocio (`Violent`, `Gore`, `Free To Play`,
  `Early Access`). 33 valores únicos en total — fase 4 deberá decidir cómo tratarlos.
- **Puerta de salida:** ✅ completa
  - [x] Herramienta elegida y justificada.
  - [x] Cada tipo de dato sucio revisado explícitamente.
  - [x] Bitácora completa con qué, por qué, cómo y cuántas filas por transformación.
  - [x] Reconciliación de conteos que cuadra (verificada con `assert`).
  - [x] Valores atípicos investigados y la decisión justificada.
  - [x] Proceso reproducible desde el crudo (`notebooks/procesar.py`).
  - [x] El dataset limpio sigue siendo suficiente: 117.430 juegos con género y precio; 10.479 pasan
        el filtro de ≥500 reseñas; 99.085 son de pago — volumen suficiente para cuartiles de precio.

## 4. Analizar

**Estado:** ✅ cerrada (aprobada por el usuario el 2026-07-28)

- **Herramienta:** Python (pandas). Scripts reproducibles: `notebooks/analizar.py` (estadística
  descriptiva, cuartiles, tabla género × franja) y `notebooks/verificar.py` (las 7 verificaciones
  de abajo). Tablas exportadas en `salidas/tablas/genero_x_franja_precio.csv` y
  `salidas/tablas/resumen_por_genero.csv`.

- **Decisión de alcance (confirmada con el usuario antes de tabular):** la columna `Genres` mezcla
  géneros de juego reales con descriptores de contenido (`Violent`, `Gore`, `Nudity`,
  `Sexual Content`), etiquetas de software no-juego (`Utilities`, `Education`, `Accounting`,
  `Movie`, etc. — 17 valores) y modelo de negocio/estado (`Free To Play`, `Early Access`). Se
  excluyeron del análisis género × precio (29.101 de 338.575 filas juego-género), dejando
  **10 géneros de juego reales**: Action, Adventure, Casual, Indie, Massively Multiplayer, RPG,
  Racing, Simulation, Sports, Strategy.

- **Estadística descriptiva (base `steam_juegos_limpios`, 117.430 juegos):**
  - `precio_ajustado_usd`: media 5,89 USD, mediana 3,13 USD, P75 6,84 USD (asimetría a la derecha,
    máx. 1.284,88 USD — colas de bundles/software premium).
  - `pct_resenas_positivas` (82.841 juegos con ≥1 reseña): media 75,83%, mediana 81,82%, P25 65%.
  - `antiguedad_anios`: mediana 4 años, P75 7 años.
  - 99.085 juegos de pago, 18.345 F2P (Price = 0). 10.479 juegos pasan el filtro ≥500 reseñas.

- **Base de análisis y cuartiles:** filtro pago (`Price > 0`) + ≥500 reseñas → 9.048 juegos
  (23.822 filas juego-género tras explotar por género real). Cuartiles de `precio_ajustado_usd`
  calculados sobre esa base: **Q1 ≤ 3,25 · Q2 3,25–6,46 · Q3 6,46–12,36 · Q4 > 12,36 USD**.

- **Hallazgos:**
  1. **La franja más barata (Q1) es sistemáticamente la de peor recepción en los 10 géneros.**
     Mediana de % reseñas positivas en Q1 va de 76,0% (Massively Multiplayer) a 86,3% (Casual),
     siempre la más baja o empatada-más-baja de las 4 franjas de su género
     (`salidas/tablas/genero_x_franja_precio.csv`).
  2. **La mejor recepción se concentra en Q3 (6,46–12,36 USD) o Q4 (>12,36 USD), no en el precio
     más alto absoluto.** En Action, Indie, Simulation, Casual y Strategy el pico es Q3; en
     Adventure, Racing, Sports y RPG es Q4. Ningún género tiene su mejor recepción en Q1 o Q2.
  3. **Efecto de tamaño moderado y consistente:** la diferencia entre Q1 y la mejor franja va de
     2,50 p.p. (RPG) a 5,04 p.p. (Adventure). Es una diferencia real pero no dramática — no
     sostiene un argumento de "el precio por sí solo duplica la recepción", solo un patrón
     direccional.
  4. **Tres candidatos con mejor combinación de efecto + volumen + recepción absoluta:**
     Adventure (4.030 juegos, +5,04 p.p., mediana máxima 87,5%), Indie (5.561 juegos, +3,94 p.p.,
     mediana máxima 88,2%) y Casual (2.230 juegos, +3,31 p.p., la mediana más alta de los 10
     géneros en su mejor franja: 89,6%). Quedan como insumo para las recomendaciones de fase 6,
     no como decisión cerrada aquí.
  5. **Massively Multiplayer es un caso aparte:** patrón no monótono (Q2 es su mejor franja, no
     Q3/Q4), la mediana más baja de los 10 géneros en las 4 franjas (74–79%), y el n más chico
     (176 juegos) — evidencia débil, se documenta como tal, no se descarta ni se recomienda.

- **Verificaciones aplicadas** (`notebooks/verificar.py`):
  1. **Sensatez:** cuartiles ajustados (3,25/6,46/12,36) vs. precio de lista bruto sin ajustar
     (2,49/4,99/9,99) — mismo orden de magnitud, la corrección por inflación no distorsiona la
     escala. Plausible para catálogo indie/AA de Steam.
  2. **Recálculo por vía alterna:** la tabla género × franja se recalculó con `pivot_table` en vez
     de `groupby.agg`; coincide punto por punto (chequeo puntual Action × Q3: 86,64% en ambas vías).
  3. **Confusor de antigüedad:** correlación `antiguedad_anios` vs `pct_resenas_positivas` = −0,087
     (prácticamente nula) — la antigüedad no explica el patrón de precio. Se documenta que
     correlación no implica causalidad.
  4. **Control por antigüedad:** se repitió la tabla separando juegos recientes (≤ mediana de
     antigüedad) vs. viejos, para Action/Adventure/Indie/Casual. El patrón "Q1 es el peor" se
     sostiene en ambas bandas — no es un artefacto de que los juegos baratos sean simplemente más
     viejos.
  5. **Efecto de tamaño cuantificado:** ver hallazgo 3 (2,50–5,04 p.p.), no solo dirección.
  6. **Recálculo manual de `pct_resenas_positivas`** sobre 5 juegos al azar (`Positive/(Positive+
     Negative)×100`) — coincide exacto con la columna precalculada en los 5 casos.
  7. **Desagregación / robustez de muestra:** n por género en la base de análisis va de 176
     (Massively Multiplayer) a 5.561 (Indie). Los géneros con n < 350 (Massively Multiplayer,
     Sports, Racing) se reportan pero con advertencia de muestra chica.

- **Lo que los datos no responden:**
  - No hay reseñas fechadas individuales — el proxy de antigüedad del juego (ya previsto en fase 1)
    no captura si la recepción de un juego cambió con el tiempo, solo la recepción acumulada según
    cuán viejo es el juego.
  - No establece causalidad: el patrón "precio medio-alto → mejor recepción" es una correlación
    descriptiva; puede reflejar selección (estudios que cobran más también invierten más en calidad)
    y no que subir el precio mejore la recepción.
  - No cubre la cola larga (<500 reseñas, 34,1% del catálogo con 0 reseñas) — excluida por decisión
    de fase 1, documentada como entregable adicional en fase 6.
  - Massively Multiplayer tiene evidencia insuficiente (n=176) para una recomendación firme por sí
    solo.

- **Puerta de salida:** ✅ completa
  - [x] Estadística descriptiva completa y revisada.
  - [x] Cada pregunta de la fase 1 tiene una respuesta basada en un cálculo concreto.
  - [x] Todos los cálculos documentados y reproducibles (`notebooks/analizar.py`,
        `notebooks/verificar.py`).
  - [x] Cada hallazgo pasó prueba de sensatez y recálculo por vía alterna.
  - [x] Efectos cuantificados, no solo direccionales (2,50–5,04 p.p.).
  - [x] Interpretaciones alternativas consideradas y descartadas con evidencia (antigüedad como
        confusor, descartada con correlación ≈0 y control por banda de antigüedad).
  - [x] Lo que los datos no pueden responder está escrito como limitación.
  - [x] Ninguna afirmación causal apoyada solo en correlación.

## 5. Compartir

**Estado:** ✅ cerrada (aprobada por el usuario el 2026-07-28)

- **Audiencia(s) y entregables** (confirmados con el usuario antes de construir):
  1. **Comité de inversión** (ejecutiva): `entregables/resumen_ejecutivo.docx` — sin jerga,
     conclusión primero, 4 figuras con su interpretación, limitaciones visibles.
  2. **Comité de inversión** (~30 min, presentación en vivo): `entregables/presentacion_fase5.pptx`
     — 13 diapositivas: título con la conclusión, contexto, método, 4 hallazgos (uno por
     diapositiva), candidatos (stat callouts), limitaciones, próximo paso (fase 6), anexo de
     metodología/verificaciones, anexo de Q&A preparado, cierre. Notas de orador incluidas.
  3. **Analista senior / repo de portafolio** (técnica): `notebooks/caso_steam_precio_recepcion.ipynb`
     — notebook narrado de punta a punta (contexto → fuentes → limpieza → análisis → verificaciones
     → visualización), cada celda de código ejecutada sin errores, con interpretación después de
     cada resultado.

- **Visualizaciones** (spotlighting: 4 de los 5 hallazgos de fase 4 sostienen el argumento; el
  quinto —Massively Multiplayer con evidencia débil— se documenta en texto, no se grafica aparte).
  Archivos en `salidas/graficos/`, generadas con `notebooks/graficos.py`:
  1. `01_q1_vs_mejor_franja.png` — *"La franja más barata es la de peor recepción en los 10 géneros
     de Steam"* (barras agrupadas Q1 vs. mejor franja, ordenadas por efecto).
  2. `02_heatmap_genero_franja.png` — *"La mejor recepción se concentra en precios medios-altos
     (Q3/Q4), nunca en el más barato"* (mapa de calor género × franja).
  3. `03_ranking_efecto_candidatos.png` — *"Adventure, Indie y Casual combinan mejor efecto,
     volumen y recepción absoluta"* (ranking de efecto, candidatos resaltados).
  4. `04_control_antiguedad.png` — *"El patrón se sostiene en juegos recientes y viejos: no es un
     efecto de antigüedad"* (barras agrupadas por banda de antigüedad, 4 géneros).
  - Checklist de diseño aplicado en las 4: eje de barras desde cero, un color protagonista (azul)
    con gris de contexto, orden por valor, nota de fuente al pie, texto alternativo escrito para
    cada figura (ver notebook), sin elementos 3D.

- **Q&A preparado** (anexo de la presentación, 5 preguntas más incómodas con respuesta escrita):
  1. ¿No es esto solo que los juegos caros vienen de estudios más grandes con mejor marketing?
  2. ¿Por qué excluir el 34% de juegos sin reseñas? ¿No se pierden oportunidades ahí?
  3. ¿Qué tan sensible es el resultado a cómo definieron las franjas de precio?
  4. ¿Por qué confiar en un dataset de terceros y no en datos directos de Valve?
  5. ¿Cuál es el número exacto detrás de "Adventure es el mejor candidato"?

- **Puerta de salida:** ✅ completa
  - [x] Audiencia definida y el formato ajustado a ella (ejecutiva, presentación en vivo, técnica).
  - [x] Cada gráfico tiene un titular que enuncia el hallazgo.
  - [x] Cada gráfico pasa el filtro de tres partes (pregunta práctica / datos / elemento visual).
  - [x] Tipo de gráfico justificado por el objetivo (barras para comparación, mapa de calor para
        intensidad por dos dimensiones).
  - [x] Ejes, orden, colores y anotaciones revisados (verificación visual de las 4 figuras y las 13
        diapositivas antes de publicar).
  - [x] Accesibilidad verificada (texto alternativo por figura, información no codificada solo con
        color, tabla de datos subyacente disponible en `salidas/tablas/`).
  - [x] Limitaciones y supuestos visibles, no escondidos en un anexo (sección propia en el resumen
        ejecutivo y en la presentación).
  - [x] Q&A preparado con las cinco preguntas más difíciles.

## 6. Actuar

**Estado:** ⬜ abierta — entregables escritos, pendientes de publicación y ensayo por el usuario

- **Cadena hallazgo → insight → recomendación:** los 5 hallazgos de fase 4 se elevaron a insight y
  a recomendación en la tabla de apertura de `entregables/recomendaciones.md`.

- **Recomendaciones** (fichas completas en `entregables/recomendaciones.md`), priorizadas por
  impacto contra esfuerzo:

| # | Acción | Evidencia | Impacto | Esfuerzo | Prioridad |
|---|---|---|---|---|---|
| R1 | Concentrar la due diligence del próximo ciclo en Adventure, Indie y Casual | Las 3 medianas de recepción más altas (86,2 / 86,7 / 88,2%) + efecto de franja 3,31–5,05 p.p. + volumen (4.030 / 5.561 / 2.230 juegos) | Alto — reasigna esfuerzo al 49,6% de la base analizada; **no** es impacto financiero | Bajo | 1 |
| R2 | Añadir al cribado la posición del catálogo en los cuartiles de precio; marcar >50% en Q1 | Q1 es la peor franja mediana en los 10 géneros (76,0–86,3%); sobrevive al control por antigüedad | Medio — efecto de 2,50–5,05 p.p., por eso es señal de alerta y no criterio de descarte | Bajo | 2 |
| R3 | Despriorizar Massively Multiplayer este ciclo; Sports y Racing como "evidencia insuficiente" | MMO: mediana 76,4%, patrón no monótono, n=176. Sports n=329, Racing n=338, bajo el umbral n<350 de la verificación 7 | Medio — libera el 3,5% de la base | Bajo | 3 |

  Cada ficha incluye además métrica de éxito con plazo y el riesgo/supuesto crítico. El riesgo más
  incómodo está declarado en R3: las reseñas de Steam miden mal un modelo de ingresos recurrentes
  como el de los MMO, así que despriorizar por evidencia débil podría ser exactamente cómo se
  pierde una oportunidad.

- **Limitaciones** (7 completas en `entregables/recomendaciones.md`): sin causalidad (la lectura
  alternativa de selección —quien cobra más invierte más en producción— no se puede descartar con
  estos datos); sin datos de ingresos ni ventas; sesgo de supervivencia; la cola larga (34,1% del
  catálogo con 0 reseñas) queda fuera por el filtro de ≥500; reseñas agregadas y no fechadas; año
  base del CPI parcial (ene–abr 2026); fuente de tercera parte (falla el componente "Original" de
  ROCCC).

- **Datos adicionales deseables:** ingresos o unidades vendidas reales; reseñas individuales con
  fecha; presupuesto de producción o tamaño del estudio (permitiría probar directamente la lectura
  alternativa de selección); histórico de precios y descuentos; retención y gasto por usuario
  (para evaluar MMO con la métrica adecuada a su modelo); datos de consolas y móvil.

- **Próximos pasos:** (1) bajar el umbral a 50 y 100 reseñas para analizar la cola larga —
  desbloquea si el fondo abre un carril de inversión en estudios pequeños; (2) cruzar los 3 géneros
  priorizados con una fuente de ingresos — convierte la priorización de horas en priorización de
  capital; (3) análisis de sensibilidad de las franjas (quintiles y bandas fijas).

- **Publicado en:** ⬜ pendiente — repositorio público de GitHub. `README.md` escrito y listo en la
  raíz del repo, con las 4 figuras enlazadas por ruta relativa y el crudo enlazado a Kaggle en vez
  de subido. Falta crear el repo y sustituir el marcador `<URL-DEL-REPOSITORIO>` en el bloque de
  reproducibilidad del README y en `entregables/portafolio-indice.md`.

- **Qué demuestra este caso frente a los demás:** traducir una pregunta de inversión a un análisis
  de pricing + sentimiento sobre un dataset con una imperfección estructural real (cabecera rota
  que desalinea columnas, no nulos triviales), enriquecido con una segunda fuente (CPI-U) para
  comparar 29 años en dólares reales — y, sobre todo, descartar la explicación alternativa
  (antigüedad) con código antes de publicar el hallazgo, además de reportar como insuficiente el
  género que no encajó en la conclusión. Matriz de cobertura y huecos del portafolio en
  `entregables/portafolio-indice.md`.

- **Puerta de salida:** ⬜ parcial — 6 de 9
  - [x] Cada hallazgo se elevó a insight y a recomendación.
  - [x] Cada recomendación tiene acción, evidencia, impacto, métrica, riesgo y esfuerzo.
  - [x] Recomendaciones priorizadas por impacto contra esfuerzo.
  - [x] Limitaciones y datos adicionales documentados.
  - [x] `README.md` público completo y con los gráficos visibles (rutas relativas verificadas).
  - [x] Sin datos sensibles ni infracciones de licencia: sin PII, crudo no subido, atribución
        CC BY 4.0 presente en el README.
  - [ ] **Análisis reproducible desde el crudo por un tercero** — los pasos están escritos, pero
        nadie externo los ha corrido en una máquina limpia. Pendiente de prueba real.
  - [x] Escrito qué habilidad demuestra este caso frente a los demás del portafolio.
  - [ ] **Versiones de la presentación ensayadas: 30 minutos y 3 minutos** — no ensayadas. La de
        30 min tiene su mazo (fase 5); la de 3 min no tiene guion escrito todavía.

  ⬜ Pendiente adicional fuera de la puerta: publicar el repositorio y actualizar el enlace.

## Bitácora de decisiones
| Fecha | Decisión | Motivo | Alternativa descartada |
|---|---|---|---|
| 2026-07-28 | Sector: plataformas digitales / pricing + sentimiento en Steam | Interés del usuario + encaja con cliente inversor | Estudios/publishers, esports, comunidad |
| 2026-07-28 | Cliente ficticio: fondo de inversión | Fuerza una decisión concreta (dónde invertir) | Estudio decidiendo qué lanzar; plataforma optimizando catálogo |
| 2026-07-28 | Dataset: Steam Games Dataset (fronkongames), CC BY 4.0 | Tiene price + genres + positive/negative en un solo archivo, volumen y recencia adecuados, saturación media | Game Recommendations on Steam (antonkozyriev) — descartado por saturación alta; Steam games complete dataset (trolukovich, 2019) — descartado por antigüedad y reseñas solo en texto libre |
| 2026-07-28 | Ventana temporal: todo el histórico disponible | El usuario prefiere cobertura completa, con tiempo disponible de sobra | Acotar a últimos 5 o 3 años |
| 2026-07-28 | Umbral mínimo de reseñas: ≥500 | Prioriza confiabilidad estadística sobre cobertura de cola larga | Umbral de 50 o 100 reseñas |
| 2026-07-28 | Franjas de precio por cuartiles calculados sobre los datos reales | Evita bandas arbitrarias impuestas de antemano | Bandas fijas predefinidas |
| 2026-07-28 | F2P excluido del análisis de franja de precio | No tienen franja de precio real; se documentan aparte | Incluir F2P como franja "Gratis"; excluirlos de todo el caso |
| 2026-07-28 | Corregir sesgo de antigüedad/inflación con CPI externo + control por año, en vez de declarar limitación | El usuario prefiere rigor metodológico sobre simplicidad, con tiempo disponible de sobra | Dejarlo como limitación declarada; acotar ventana a 5 años |
| 2026-07-28 | Aprobar CPI-U de BLS como segunda fuente de datos | Pasa ROCCC sin fallas: primera parte, dominio público, cubre 1997-2026 | Buscar un índice de inflación de terceros o de otra región |
| 2026-07-28 | No subir el CSV crudo (~400 MB) al repo público; enlazar a Kaggle en su lugar | El archivo excede lo razonable para un repo de portafolio | Subir una muestra reducida del crudo para reproducibilidad end-to-end |
| 2026-07-28 | Explotar por género (una fila por juego-género) en vez de quedarse con el género primario o solo mono-género | El usuario prefirió que cada género reciba su propia evidencia, aceptando que un juego cuente en varios grupos | Género primario únicamente; o descartar juegos multi-género |
| 2026-07-28 | Excluir 8.423 juegos sin género asignado | No se pueden ubicar en ninguna combinación género × precio, que es el corazón de la pregunta | Imputar una categoría "Sin clasificar" |
| 2026-07-28 | Usar promedio parcial de CPI 2026 (ene-abr) como año base | Es el único dato disponible a la fecha de descarga; se declara como limitación en vez de esperar el año completo | Usar 2025 como año base (año completo más reciente) |
| 2026-07-28 | Recomendaciones limitadas a priorizar due diligence por género, sin tesis de pricing para participadas | El dataset no tiene ingresos ni ventas; recomendar "sube el precio" excedería lo que la evidencia sostiene | Añadir una tesis de pricing operativa; añadir una recomendación de ampliar el análisis como R4 |
| 2026-07-28 | Tres recomendaciones, no más | El marco pide priorizar por impacto contra esfuerzo y mandar el resto a exploración futura; la cola larga y la sensibilidad de franjas van a "próximos pasos" | Enunciar 5-6 recomendaciones incluyendo las de análisis futuro |
| 2026-07-28 | Reportar Massively Multiplayer como despriorizado por evidencia insuficiente, con el contraargumento escrito en su propia ficha | Omitir el género que no encajó habría sido el error más fácil; declararlo con su riesgo es más creíble | Omitirlo del entregable; o recomendarlo/descartarlo con la evidencia que hay |
| 2026-07-28 | No subir el crudo al repo; enlazar a Kaggle en las instrucciones de reproducción | Coherente con la decisión de fase 2; 400 MB no caben razonablemente en un repo de portafolio | Subir una muestra reducida para reproducibilidad end-to-end |
| 2026-07-28 | Excluir de "género" los descriptores de contenido (Violent, Gore, Nudity, Sexual Content), etiquetas de software no-juego (17 valores) y Free To Play/Early Access | Son etiquetas de la taxonomía Steam que no representan un género de videojuego real; mezclarlas distorsionaría la tabla género × precio | Mantener las 33 etiquetas tal cual; o excluir solo el subconjunto de software no-juego |
