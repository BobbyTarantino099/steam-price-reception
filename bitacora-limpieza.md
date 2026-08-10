# Bitácora de limpieza — Caso Steam (precio y recepción)

**Dataset de entrada:** `datos/crudos/steam_fronkongames_catalogo-historico_2026-07-28.csv` — 125.855 filas
**Datasets de salida:**
- `datos/limpios/steam_juegos_limpios.csv` — 117.430 filas (1 fila = 1 juego)
- `datos/limpios/steam_juegos_por_genero.csv` — 338.575 filas (1 fila = 1 juego × género)

**Herramienta:** Python (pandas), justificado en fase 0: reproducibilidad sobre un archivo de 400 MB
con una imperfección estructural (bug de cabecera) que exige un script, no revisión manual.

**Segunda fuente incorporada:** BLS CPI-U anual (`datos/crudos/bls_cpi-u_anual_1997-2026_2026-07-28.csv`),
aprobada en fase 2, usada para el ajuste por inflación.

Script completo: `notebooks/procesar.py`.

## Transformaciones

### T1 — Corrección del bug de cabecera
- **Qué:** la cabecera cruda declara 39 nombres de columna; cada fila trae 40 valores. El nombre
  `DiscountDLC count` (posición 7) fusiona dos columnas reales: `Discount` y `DLC count`.
- **Por qué:** sin corregir esto, todas las columnas desde `About the game` en adelante quedan
  desalineadas con su dato real (confirmado en fase 2: `About the game` mostraba `'0'` en vez de
  texto descriptivo).
- **Cómo:** se insertó el nombre faltante en la lista de columnas antes de cargar el CSV
  (`header=None, names=cols_fixed, skiprows=1`), en vez de dejar que pandas infiera la cabecera.
- **Filas afectadas:** las 125.855, todas estaban desalineadas.
- **Alternativa descartada:** recortar la columna `About the game` (texto largo) para "reacomodar" —
  descartada porque no ataca la causa raíz y rompe con cualquier fila que tenga comas sin escapar.

### T2 — Tipado de fecha y exclusión de lanzamientos futuros
- **Qué:** `Release date` de texto a `datetime`; exclusión de juegos con fecha de lanzamiento
  posterior a la fecha de descarga (2026-07-28).
- **Por qué:** 2 juegos tienen fecha de lanzamiento futura (planeada) y 0 reseñas — no representan
  aún un caso real de "recepción" y no deben contarse como población observada.
- **Cómo:** `pd.to_datetime(errors='coerce')` + filtro `Release date <= fecha_descarga`.
- **Filas afectadas:** 2 eliminadas (0 fechas no parseables).
- **Alternativa descartada:** conservarlos con reseñas en 0 — descartada porque distorsionaría
  cualquier promedio de % de reseñas positivas hacia abajo sin motivo real.

### T3 — Columnas fuera de alcance descartadas
- **Qué:** se descartaron 15 columnas: `Movies`, `Score rank`, `Metacritic url`, `Reviews`, `Notes`,
  `Website`, `Support url`, `Support email`, `About the game`, `Supported languages`,
  `Full audio languages`, `Screenshots`, `Header image`, `Categories`, `Tags`.
- **Por qué:** o no aportan a la pregunta (precio, género, reseñas), o tienen nulos entre 34% y 100%
  (`Movies` 100%, `Score rank` 99,97%), o son texto libre no estructurado que este caso no analiza.
- **Cómo:** `df.drop(columns=[...])`.
- **Filas afectadas:** ninguna (es eliminación de columnas, no de filas).
- **Alternativa descartada:** conservar `Tags` para un análisis de texto — descartada por alcance
  (fuera de la pregunta de fase 1); queda como "dato adicional deseable" para fase 6.

### T4 — Duplicados por `AppID`
- **Qué:** verificación de duplicados usando `AppID` como clave.
- **Por qué:** `AppID` es el identificador único declarado por Steam; ya se había verificado 0
  duplicados en fase 2, se reconfirma después de las transformaciones anteriores.
- **Cómo:** `duplicated(subset=['AppID'])`.
- **Filas afectadas:** 0.
- **Alternativa descartada:** N/A, no hubo duplicados que resolver.

### T5 — Exclusión de juegos sin género
- **Qué:** 8.423 juegos (6,69% del catálogo tras T2) no tienen ningún género asignado en Steam.
- **Por qué:** la pregunta analítica exige clasificar por género; un juego sin género no se puede
  ubicar en ninguna combinación género × franja de precio.
- **Cómo:** `df[df['Genres'].notna()]`.
- **Filas afectadas:** 8.423 eliminadas.
- **Alternativa descartada:** imputar un género genérico ("Sin clasificar") — descartada porque
  inventaría una categoría que Steam no asignó y distorsionaría el conteo de esa categoría.

### T6 — Enriquecimiento con CPI-U (BLS) y precio ajustado por inflación
- **Qué:** se une el catálogo con el índice CPI-U anual de BLS por año de lanzamiento, y se calcula
  `precio_ajustado_usd = Price × (CPI_2026 / CPI_año_lanzamiento)`, con año base = 2026 (el más
  reciente del dataset, según la métrica definida en fase 1).
- **Por qué:** sin este ajuste, comparar precios de un juego de 1997 con uno de 2026 subestima el
  valor real pagado por los juegos más antiguos.
- **Cómo:** `merge` por año + fórmula vectorizada; verificado con `assert` de que el merge no
  duplicó filas (confirmado: 0 juegos quedaron sin CPI coincidente).
- **Filas afectadas:** las 117.430 restantes, todas recibieron un precio ajustado.
- **Limitación declarada:** el CPI de 2026 (año base) es un **promedio parcial** de solo 4 meses
  (enero-abril), el único dato disponible a la fecha de descarga. El de 2025 usa 11 meses (octubre
  no publicado por un cierre de gobierno de EE. UU.). Esto introduce un margen de imprecisión menor
  en los precios ajustados de los juegos más recientes; se declara en el README del caso.
- **Alternativa descartada:** esperar a que BLS publique el año 2026 completo — descartada por
  calendario del proyecto; se prefiere declarar la limitación.

### T7 — Cálculo de % de reseñas positivas
- **Qué:** `pct_resenas_positivas = Positive / (Positive + Negative) × 100`, tal como se definió en
  fase 1.
- **Por qué:** es la métrica central de "recepción" del caso.
- **Cómo:** cálculo vectorizado; los 34.589 juegos con 0 reseñas totales quedan como `NaN` en vez de
  0%, para no confundir "sin datos" con "recepción neutra".
- **Filas afectadas:** las 117.430, de las cuales 34.589 quedan sin valor (correctamente, como nulo).
- **Alternativa descartada:** asignar 0% a los juegos sin reseñas — descartada porque 0% implicaría
  "recepción negativa", cuando en realidad es "sin evidencia".

### T8 — Explosión por género (dataset derivado)
- **Qué:** se generó `steam_juegos_por_genero.csv`, donde cada juego con N géneros produce N filas
  (una por género), a partir de `steam_juegos_limpios.csv`.
- **Por qué:** decisión confirmada con el usuario para responder la pregunta de "combinaciones de
  género y franja de precio" — un juego con varios géneros aporta evidencia a cada uno.
- **Cómo:** `Genres.str.split(',')` + `explode()`.
- **Filas afectadas:** de 117.430 juegos se generan 338.575 filas juego-género (un mismo juego
  puede aparecer en varios géneros — no son mutuamente excluyentes, y esto se declara explícitamente
  para que fase 4 no interprete los conteos por género como población de juegos únicos).
- **Alternativa descartada:** quedarse solo con el género primario o solo con juegos mono-género —
  ambas evaluadas y descartadas por el usuario en fase 2.

## Observación para fase 4 (no bloquea el cierre de esta fase)

La columna `Genres` de Steam mezcla, bajo la misma etiqueta, géneros propiamente dichos (`Action`,
`RPG`, `Strategy`) con descriptores de contenido/modelo de negocio (`Violent`, `Gore`,
`Free To Play`, `Early Access`, `Nudity`). Hay 33 valores únicos en total. Esto no es un error de
datos — es la taxonomía real de Steam — pero fase 4 deberá decidir si excluye o trata aparte las
etiquetas que no son géneros de juego en sentido estricto, para no comparar peras con manzanas al
recomendar "en qué género invertir".

## Reconciliación
| Concepto | Filas |
|---|---|
| Iniciales (tras corregir cabecera) | 125.855 |
| Eliminadas por fecha de lanzamiento futura | 2 |
| Eliminadas por duplicados de `AppID` | 0 |
| Eliminadas por no tener género asignado | 8.423 |
| **Finales (`steam_juegos_limpios.csv`)** | **117.430** |
| Filas tras explotar por género (`steam_juegos_por_genero.csv`) | 338.575 |

Verificado con `assert` en el script: `125.855 − 2 − 0 − 8.423 == 117.430`. ✅

## Verificación posterior
- [x] Conteos cuadran (`assert` en `procesar.py`).
- [x] Categorías estandarizadas (géneros) son las 33 esperadas de la taxonomía de Steam.
- [x] Rangos numéricos plausibles: sin precios ni reseñas negativas; `AppID` sigue siendo única.
- [x] Proceso reproducible desde el crudo (`procesar.py` corre de punta a punta sin edición manual).
- [x] El dataset limpio sigue respondiendo la pregunta: quedan 117.430 juegos con género, precio y
      reseñas; 10.479 pasan el filtro de ≥500 reseñas que se aplicará en fase 4, y 99.085 son de
      pago (`Price > 0`) — suficiente volumen para la franja de precio por cuartiles.
