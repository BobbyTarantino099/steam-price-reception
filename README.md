# En Steam, la franja de precio más barata es la de peor recepción en los 10 géneros

> Los juegos de menos de 3,25 USD reales tienen sistemáticamente la peor recepción de su género.
> La mejor está en 6,46–12,36 USD — nunca en el precio más bajo, y tampoco siempre en el más alto.
> Sobre esa base, recomiendo concentrar la due diligence en Adventure, Indie y Casual.

![La franja más barata es la de peor recepción en los 10 géneros de Steam](salidas/graficos/01_q1_vs_mejor_franja.png)

`Python` `pandas` `matplotlib` `125.855 juegos` `2 fuentes combinadas`

---

## Contexto

Un fondo de inversión enfocado en videojuegos no tiene un criterio basado en datos para decidir en
qué género priorizar su tesis en el mercado de PC/Steam. Le sobran candidatos y le faltan filtros:
la pregunta operativa no es "¿qué juego es bueno?" sino "¿en qué parte del catálogo conviene
gastar las horas de due diligence?".

La pregunta analítica que planteé: **¿qué combinaciones de género y franja de precio (cuartiles de
precio ajustado por inflación, sobre juegos de pago con ≥500 reseñas) en el catálogo histórico de
Steam muestran el patrón más consistente de alto porcentaje de reseñas positivas, controlando por
antigüedad del juego?** La decisión que habilita es concreta: recomendar 2-3 géneros donde el
comité debe priorizar due diligence, con la evidencia de qué franja de precio sostiene mejor
recepción en cada uno.

## Datos

| Fuente | Periodo | Volumen | Licencia |
|---|---|---|---|
| [Steam Games Dataset](https://www.kaggle.com/datasets/fronkongames/steam-games-dataset) (fronkongames) | 1997-06-30 → 2026-05 | 125.855 juegos × 40 columnas | CC BY 4.0 |
| [CPI-U, serie `CUUR0000SA0`](https://www.bls.gov/cpi/) (Bureau of Labor Statistics, EE. UU.) | 1997–2026 | Índice anual | Dominio público |

El CSV crudo pesa ~400 MB y **no está en este repositorio**: descárgalo del enlace de Kaggle (ver
[Reproducir](#reproducir)). Atribución requerida por CC BY 4.0: dataset de *fronkongames*, Kaggle.
Sin PII en ninguna de las dos fuentes.

**Limitaciones principales** (las siete completas están en
[`entregables/recomendaciones.md`](entregables/recomendaciones.md#limitaciones)):

- **No hay causalidad.** El patrón es correlación descriptiva. La lectura alternativa más fuerte
  —los estudios que cobran más también invierten más en producción— no puede descartarse con estos
  datos. Lo que sí descarté con evidencia es que sea un artefacto de antigüedad.
- **No hay ingresos ni ventas.** `estimated_owners` viene en rangos estimados por SteamSpy, no
  confirmados por Valve, y no se usó como métrica. El caso habla de recepción, no de rentabilidad.
- **La cola larga queda fuera.** El filtro de ≥500 reseñas excluye deliberadamente al 34,1% del
  catálogo, que tiene 0 reseñas. La muestra está sesgada hacia juegos visibles.
- **Sesgo de supervivencia.** Solo juegos publicados en Steam. Ni cancelados, ni retirados, ni
  consolas, ni móvil.

## Proceso

**Herramientas:** Python con pandas. El archivo tiene 400 MB y un bug estructural de cabecera —
auditarlo a mano en una hoja de cálculo era inviable, y el caso exigía que la limpieza fuera
reproducible de punta a punta.

**Decisiones de limpieza clave:**

1. **Bug de cabecera corregido.** La cabecera cruda declara 39 columnas pero cada fila trae 40: el
   nombre `DiscountDLC count` fusiona dos columnas reales, `Discount` y `DLC count`. Todo lo
   posterior a esa posición estaba desalineado. Se corrige insertando el nombre faltante antes de
   cargar.
2. **Ajuste por inflación en vez de limitación declarada.** Combiné el catálogo con el CPI-U del
   BLS para comparar en dólares reales de 2026 precios de juegos publicados con 29 años de
   diferencia. Un juego de 9,99 USD de 1999 no es el mismo producto que uno de 9,99 USD de 2025.
3. **Explosión por género.** Un juego con N géneros genera N filas, para que cada género reciba su
   propia evidencia. 117.430 juegos → 338.575 filas juego-género.
4. **Limpieza de la taxonomía de géneros.** La columna `Genres` de Steam mezcla géneros reales con
   descriptores de contenido (`Violent`, `Gore`), etiquetas de software no-juego (`Accounting`,
   `Utilities`) y modelo de negocio (`Free To Play`, `Early Access`). Excluí las 23 etiquetas que
   no son un género de videojuego y me quedé con 10 reales.

Reconciliación de conteos: 125.855 − 2 (lanzamiento futuro) − 0 (duplicados) − 8.423 (sin género) =
**117.430**, verificado con `assert` en el script. Base final de análisis: 9.048 juegos de pago con
≥500 reseñas.
Detalle completo en [`bitacora-limpieza.md`](bitacora-limpieza.md) y
[`documentacion/`](documentacion/).

## Hallazgos

### 1. La franja más barata es la de peor recepción en los 10 géneros, sin excepción

![Comparación entre la franja Q1 y la mejor franja de cada género](salidas/graficos/01_q1_vs_mejor_franja.png)

La mediana de reseñas positivas en Q1 (≤3,25 USD reales) va de 76,0% en Massively Multiplayer a
86,3% en Casual, y en los diez géneros es la más baja o está empatada en el último lugar de su
género. No hay un solo género donde lo barato reciba mejor recepción.

### 2. El pico está en precios medios-altos, no en el precio más alto

![Mapa de calor de recepción por género y franja de precio](salidas/graficos/02_heatmap_genero_franja.png)

En Action, Indie, Simulation, Casual y Strategy la mejor franja es Q3 (6,46–12,36 USD); en
Adventure, Racing, Sports y RPG es Q4 (>12,36 USD). Ningún género tiene su mejor recepción en Q1 ni
en Q2. Esto descarta la lectura simplista de "más caro, mejor": en la mitad de los géneros la
franja más cara ya empeora respecto a Q3.

### 3. El efecto es real pero moderado: de 2,50 a 5,05 puntos porcentuales

![Ranking de efecto por género con los tres candidatos resaltados](salidas/graficos/03_ranking_efecto_candidatos.png)

La diferencia entre Q1 y la mejor franja de cada género va de 2,51 p.p. (RPG) a 5,05 p.p.
(Adventure). Cuantificarlo importa: sostiene un argumento direccional de cribado, no uno de que el
precio por sí solo transforme la recepción de un producto. Adventure, Indie y Casual son los tres
que combinan mejor efecto, volumen (4.030, 5.561 y 2.230 juegos) y recepción absoluta (medianas de
86,2%, 86,7% y 88,2%).

### 4. No es un efecto de antigüedad: el patrón se sostiene en juegos nuevos y viejos

![El patrón se sostiene al separar juegos recientes de juegos viejos](salidas/graficos/04_control_antiguedad.png)

La objeción evidente es que los juegos baratos son simplemente los viejos. No se sostiene: la
correlación entre antigüedad y recepción es −0,087 (prácticamente nula), y al repetir la tabla
separando juegos recientes de juegos viejos, "Q1 es la peor franja" aparece en ambas bandas.

### 5. Massively Multiplayer es la excepción, y se reporta como tal

No tiene gráfico propio, a propósito. Es el único género con patrón no monótono (su mejor franja es
Q2), tiene la mediana más baja de los diez en las cuatro franjas (74,8%–79,0%) y el n más pequeño
de la base (176 juegos). La evidencia es débil, así que no se recomienda ni se descarta: se
documenta como insuficiente.

## Recomendaciones

Las tres fichas completas —con acción, evidencia, impacto, métrica de éxito, riesgo y esfuerzo—
están en [`entregables/recomendaciones.md`](entregables/recomendaciones.md).

| # | Recomendación | Evidencia | Impacto | Esfuerzo |
|---|---|---|---|---|
| **R1** | Concentrar la due diligence del próximo ciclo en **Adventure, Indie y Casual** | Las tres medianas de recepción más altas (86,2 / 86,7 / 88,2%) + efecto de franja de 3,31–5,05 p.p. + volumen de objetivos suficiente | Alto | Bajo |
| **R2** | Añadir al cribado la **posición del catálogo en los cuartiles de precio**; marcar para revisión los estudios con >50% en Q1 | Q1 es la peor franja en los 10 géneros; el patrón sobrevive al control por antigüedad | Medio | Bajo |
| **R3** | **Despriorizar Massively Multiplayer** este ciclo; Sports y Racing como "evidencia insuficiente" | MMO: mediana 76,4%, patrón no monótono, n=176. Sports (329) y Racing (338) bajo el umbral de n<350 | Medio | Bajo |

Las tres son de esfuerzo bajo porque las tres son reglas sobre un proceso que el fondo ya ejecuta.
Ese es deliberadamente el techo de lo que este análisis puede sostener: con reseñas agregadas y sin
datos de ingresos, la recomendación honesta es **dónde mirar primero**, no dónde poner el dinero.

**Próximo paso principal:** bajar el umbral de reseñas a 50 y 100 para ver si el patrón se sostiene
en la cola larga indie/nicho. Eso desbloquea la decisión de si el fondo debe abrir un carril de
inversión en estudios pequeños.

## Reproducir

```bash
# 1. Clonar
git clone <URL-DEL-REPOSITORIO>
cd Videojuegos

# 2. Dependencias
pip install pandas matplotlib seaborn jupyter

# 3. Descargar el crudo (no está en el repo, ~400 MB)
#    https://www.kaggle.com/datasets/fronkongames/steam-games-dataset
#    Guardarlo como:
#    datos/crudos/steam_fronkongames_catalogo-historico_2026-07-28.csv
#    El CPI-U ya está en datos/crudos/bls_cpi-u_anual_1997-2026_2026-07-28.csv

# 4. Ejecutar en orden
python notebooks/procesar.py    # limpieza -> datos/limpios/
python notebooks/analizar.py    # cuartiles y tabla genero x franja -> salidas/tablas/
python notebooks/verificar.py   # las 7 verificaciones del analisis
python notebooks/graficos.py    # las 4 figuras -> salidas/graficos/
```

El notebook narrado de punta a punta está en
[`notebooks/caso_steam_precio_recepcion.ipynb`](notebooks/caso_steam_precio_recepcion.ipynb).

## Estructura del repositorio

```
├── README.md                    # este archivo
├── CASO.md                      # bitácora viva de las 6 fases y sus decisiones
├── bitacora-limpieza.md         # las 8 transformaciones, con su porqué
├── datos/
│   ├── crudos/                  # CPI-U; el crudo de Steam se descarga aparte
│   └── limpios/                 # datasets derivados
├── documentacion/
│   ├── diccionario-de-datos.md
│   └── fichas-de-fuente.md      # ROCCC por fuente
├── notebooks/                   # procesar · analizar · verificar · graficos · notebook narrado
├── salidas/
│   ├── graficos/                # las 4 figuras
│   └── tablas/                  # género × franja y resumen por género
└── entregables/
    ├── recomendaciones.md       # las 3 fichas completas + limitaciones
    ├── resumen_ejecutivo.docx   # para el comité
    └── presentacion_fase5.pptx  # 13 diapositivas, con notas de orador
```

## Qué demuestra este caso

Traducir una pregunta de inversión en un análisis de pricing y sentimiento, sobre un dataset con
una imperfección estructural real —no nulos triviales, sino una cabecera rota que desalinea las
columnas— y combinándolo con una segunda fuente (CPI-U) para poder comparar precios a lo largo de
29 años en dólares reales.

Lo que más me interesa mostrar aquí es la parte que suele faltar: **descartar la explicación
alternativa antes de publicar el hallazgo**. La objeción obvia a "los juegos baratos tienen peor
recepción" es que los juegos baratos son los viejos. La verifiqué, no se sostiene, y esa
verificación está en el repositorio con su código. Y el género que no encajó en la conclusión
—Massively Multiplayer— se reporta como evidencia insuficiente en vez de omitirse.

---

*Cliente ficticio, análisis real. Datos de Steam Games Dataset (fronkongames), CC BY 4.0, e índice
CPI-U del Bureau of Labor Statistics (EE. UU.).*
