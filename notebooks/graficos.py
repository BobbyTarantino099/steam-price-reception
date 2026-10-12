import pandas as pd
import numpy as np
from pathlib import Path

import estilo

RUTA_BASE = Path(__file__).resolve().parents[1]
(RUTA_BASE / 'salidas' / 'graficos').mkdir(parents=True, exist_ok=True)

estilo.aplicar()

FUENTE = ('Steam Games Dataset (fronkongames, Kaggle, CC BY 4.0) + BLS CPI-U')
NOTA = ('Base: 8,998 paid games with >=500 reviews, 10 real genres. '
        'Price adjusted for inflation, 2026 base year (partial average, Jan-Apr)')
PERIODO = 'Steam catalogue, 1997-2026'

df_g = pd.read_csv(f'{RUTA_BASE}/datos/limpios/steam_juegos_por_genero.csv', low_memory=False)

NO_GENERO = set(['Violent', 'Gore', 'Nudity', 'Sexual Content',
                  'Utilities', 'Design & Illustration', 'Animation & Modeling', 'Education',
                  'Video Production', 'Game Development', 'Audio Production',
                  'Software Training', 'Photo Editing', 'Web Publishing', 'Accounting',
                  'Movie', 'Documentary', 'Episodic', 'Short', 'Tutorial', '360 Video',
                  'Free To Play', 'Early Access'])
df_gen_real = df_g[~df_g['Genres'].isin(NO_GENERO)].copy()
df_gen_real['total_resenas'] = df_gen_real['Positive'] + df_gen_real['Negative']

base = df_gen_real[(df_gen_real['Price'] > 0) & (df_gen_real['total_resenas'] >= 500)].copy()
q1, q2, q3 = 3.25, 6.46, 12.36
bordes = [-np.inf, q1, q2, q3, np.inf]
etiquetas = ['Q1 (<=3.25)', 'Q2 (3.25-6.46)', 'Q3 (6.46-12.36)', 'Q4 (>12.36)']
base['franja_precio'] = pd.cut(base['precio_ajustado_usd'], bins=bordes, labels=etiquetas)

tabla = (base.groupby(['Genres', 'franja_precio'], observed=True)
         .agg(n=('AppID', 'count'), mediana_pct=('pct_resenas_positivas', 'median'))
         .reset_index())
tabla_robusta = tabla[tabla['n'] >= 20].copy()

CANDIDATOS = ['Adventure', 'Indie', 'Casual']

# Q1 y mejor franja por genero
filas = []
for genero, sub in tabla_robusta.groupby('Genres'):
    q1_val = sub.loc[sub['franja_precio'] == etiquetas[0], 'mediana_pct']
    if q1_val.empty:
        continue
    q1_val = q1_val.iloc[0]
    mejor = sub.loc[sub['mediana_pct'].idxmax()]
    filas.append({'Genres': genero, 'Q1': q1_val, 'mejor': mejor['mediana_pct'],
                  'franja_mejor': mejor['franja_precio'], 'dif': mejor['mediana_pct'] - q1_val})
f1 = pd.DataFrame(filas).sort_values('dif', ascending=False)

# =================================================================
# FIGURA 1 - Dumbbell: Q1 contra la mejor franja, por genero
#
# Antes eran barras agrupadas, que obligan a comparar dos longitudes
# desde ejes distintos. El dumbbell muestra la diferencia como una
# distancia, que es exactamente lo que dice el hallazgo.
# =================================================================
fig, ax = estilo.figura(
    titular='The cheapest price band is never the best-received in any Steam genre',
    subtitulo="Median share of positive reviews: cheapest band vs. the genre's best band",
    periodo=PERIODO, fuente=FUENTE, nota=NOTA, figsize=(9.2, 6.8),
    izquierda=0.175,
)
estilo.dumbbell(
    ax, list(f1['Genres']), list(f1['Q1']), list(f1['mejor']),
    etiqueta_desde='Cheapest band (Q1)', etiqueta_hasta="Genre's best band",
)
for i, row in enumerate(f1.itertuples()):
    ax.text(row.mejor + 0.6, i, f'+{row.dif:.1f}', va='center', ha='left',
            color=estilo.ACENTO, **estilo._prop('medio', 9.5))
ax.set_xlim(70, 95)
ax.set_xlabel('Median % positive reviews')
estilo.leyenda(ax)
estilo.guardar(fig, f'{RUTA_BASE}/salidas/graficos/01_q1_vs_mejor_franja.png')

# =================================================================
# FIGURA 2 - Tabla-matriz: genero x franja
#
# Antes era un mapa de calor, que obliga a leer el color y adivinar el
# numero. Aqui manda el numero y el color acompana.
# =================================================================
pivot = tabla_robusta.pivot(index='Genres', columns='franja_precio', values='mediana_pct')
orden = pivot.mean(axis=1).sort_values(ascending=False).index
pivot = pivot.loc[orden]
n_por_genero = (base.groupby('Genres', observed=True)['AppID'].count()
                .reindex(orden).astype(int))

fig, ax = estilo.figura(
    titular='The best reception clusters at mid-to-high prices, never the cheapest',
    subtitulo='Median share of positive reviews, by genre and inflation-adjusted price band',
    periodo=PERIODO, fuente=FUENTE, nota=NOTA, figsize=(9.2, 7.0),
    izquierda=0.235, abajo=0.16,
)
estilo.tabla_matriz(
    ax,
    filas=list(pivot.index),
    columnas=['Q1  <=$3.25', 'Q2  $3.25-6.46', 'Q3  $6.46-12.36', 'Q4  >$12.36'],
    valores=[[None if pd.isna(v) else float(v) for v in fila] for fila in pivot.values],
    etiqueta_filas=[f'{n:,} games' for n in n_por_genero],
)
estilo.guardar(fig, f'{RUTA_BASE}/salidas/graficos/02_heatmap_genero_franja.png')

# =================================================================
# FIGURA 3 - Ranking del efecto, candidatos destacados
# =================================================================
f3 = f1.sort_values('dif', ascending=False)
colores = estilo.destacar(list(f3['Genres']), CANDIDATOS)

fig, ax = estilo.figura(
    titular='Adventure, Indie and Casual combine the best effect, volume and reception',
    subtitulo='Gap in percentage points between the cheapest band and each genre\'s best band',
    periodo=PERIODO, fuente=FUENTE, nota=NOTA, figsize=(9.2, 6.6),
    izquierda=0.175,
)
y = np.arange(len(f3))
# Lollipop en vez de barra: la masa de la barra no aporta, el extremo si.
for i, (v, c) in enumerate(zip(f3['dif'], colores)):
    ax.plot([0, v], [i, i], color=c, linewidth=2.4, solid_capstyle='round', zorder=1)
ax.scatter(f3['dif'], y, s=95, color=colores, zorder=2, edgecolor=estilo.PAPEL, linewidth=1.6)
for i, row in enumerate(f3.itertuples()):
    destacado = row.Genres in CANDIDATOS
    ax.text(row.dif + 0.14, i, f'{row.dif:.2f}', va='center', ha='left',
            color=estilo.ACENTO if destacado else estilo.TINTA_SUAVE,
            **estilo._prop('medio' if destacado else 'regular', 9.5))
ax.set_yticks(y)
ax.set_yticklabels(f3['Genres'])
ax.invert_yaxis()
ax.set_xlim(0, f3['dif'].max() + 1.0)
ax.set_xlabel('Percentage points')
ax.grid(axis='x')
ax.set_axisbelow(True)
# Sin flecha: colocada justo debajo de la fila que comenta, en la banda vacia
# entre dos filas. Una flecha hasta el punto cruzaria las etiquetas vecinas.
ax.text(0.12, 0.52, 'Highest effect, and 4,030 games of evidence',
        va='center', ha='left', color=estilo.TINTA_SUAVE, **estilo._prop('regular', 9))
estilo.guardar(fig, f'{RUTA_BASE}/salidas/graficos/03_ranking_efecto_candidatos.png')

# =================================================================
# FIGURA 4 - Control por antiguedad: tiras de puntos, viejos vs recientes
# =================================================================
# Antes eran barras agrupadas desde cero, en cuatro generos: con diferencias
# de 1 a 4 puntos sobre un eje de 0 a 100 todas las barras median lo mismo, y
# el ojo comparaba reciente contra viejo, no Q1 contra las otras franjas, que
# es lo que dice el hallazgo. Ahora cada fila es una tira de puntos en una
# escala corta: Q1 en gris, las otras tres en azul, y la fila se sombrea donde
# Q1 queda ultima. Los diez generos, como en la escena 4 del video.
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

mediana_antig = base['antiguedad_anios'].median()
base['banda'] = np.where(base['antiguedad_anios'] <= mediana_antig, 'Recent', 'Older')
tabla4 = (base.groupby(['Genres', 'banda', 'franja_precio'], observed=True)
          .agg(n=('AppID', 'count'), mediana_pct=('pct_resenas_positivas', 'median'))
          .reset_index())
tabla4 = tabla4[tabla4['n'] >= 20]

def tira(genero, banda):
    """Medianas de las cuatro franjas, o None si alguna tiene menos de 20 juegos."""
    m = (tabla4[(tabla4['Genres'] == genero) & (tabla4['banda'] == banda)]
         .set_index('franja_precio')['mediana_pct'])
    return m if len(m) == 4 else None

def q1_ultima(m):
    return m is not None and m.iloc[0] == m.min()

# Arriba los generos donde el patron resiste en ambos grupos; luego el resto;
# al final los que no tienen datos suficientes.
generos4 = sorted(base['Genres'].unique())
resisten = [g for g in generos4 if q1_ultima(tira(g, 'Recent'))]
sin_datos = [g for g in generos4 if tira(g, 'Recent') is None or tira(g, 'Older') is None]
generos4 = resisten + [g for g in generos4 if g not in resisten + sin_datos] + sin_datos
assert resisten == ['Adventure', 'Casual', 'Indie'], 'cambio el resultado: revisar titular y hallazgo 4'

fig, ax_madre = estilo.figura(
    titular='Among recent games, the cheapest band still trails only in Adventure, Indie and Casual',
    subtitulo=f'Median share of positive reviews by price band, splitting games at the median age '
              f'({mediana_antig:.0f} years)',
    periodo=PERIODO, fuente=FUENTE, nota=NOTA, figsize=(10.4, 7.4),
    izquierda=0.175, abajo=0.2,
)
caja = ax_madre.get_position()
ax_madre.remove()
ejes = fig.subplots(1, 2, sharey=True, gridspec_kw=dict(
    # El techo baja lo que ocupan el titulo de cada panel y su recuento: sin eso
    # se montaban sobre la linea de periodo de la cabecera.
    left=caja.x0, right=caja.x1, bottom=caja.y0, top=caja.y1 - 0.075, wspace=0.08))

V0, V1 = 77, 93
for ax, banda, nombre in [(ejes[0], 'Older', f'Older games (over {mediana_antig:.0f} years)'),
                          (ejes[1], 'Recent', f'Recent games ({mediana_antig:.0f} years or less)')]:
    ultimas = 0
    con_datos = 0
    for i, genero in enumerate(generos4):
        m = tira(genero, banda)
        if m is None:
            ax.text(V0 + 0.3, i, 'too few games in some bands', va='center', ha='left',
                    color=estilo.TINTA_TENUE, style='italic', **estilo._prop('regular', 8.5))
            continue
        con_datos += 1
        if q1_ultima(m):
            ultimas += 1
            ax.axhspan(i - 0.42, i + 0.42, color=estilo.RAMPA[0], zorder=0, lw=0)
        ax.plot([V0 + 0.3, V1 - 0.3], [i, i], color=estilo.REGLA, lw=1.2, zorder=1)
        ax.scatter(m.iloc[1:], [i] * 3, s=34, color=estilo.ACENTO, zorder=2,
                   edgecolor=estilo.PAPEL, linewidth=0.8)
        ax.scatter([m.iloc[0]], [i], s=90, color=estilo.CONTEXTO, zorder=3,
                   edgecolor=estilo.PAPEL, linewidth=1.2)
    ax.set_title(nombre, color=estilo.TINTA, pad=22, loc='left', **estilo._prop('medio', 11))
    ax.text(0, 1.012, f'Cheapest band last in {ultimas} of {con_datos} genres', transform=ax.transAxes,
            va='bottom', ha='left', color=estilo.TINTA_SUAVE, **estilo._prop('regular', 9.5))
    ax.set_xlim(V0, V1)
    ax.set_xticks([80, 85, 90])
    ax.set_xticklabels(['80%', '85%', '90%'])
    ax.grid(axis='x', zorder=0)
    ax.set_axisbelow(True)
    ax.tick_params(axis='y', length=0)
    for lado in ('left', 'top', 'right'):
        ax.spines[lado].set_visible(False)

ejes[0].set_yticks(range(len(generos4)))
ejes[0].set_yticklabels(generos4)
ejes[0].set_ylim(len(generos4) - 0.5, -0.5)

marcas = [
    Line2D([], [], ls='', marker='o', ms=9, color=estilo.CONTEXTO, label='Cheapest band (Q1)'),
    Line2D([], [], ls='', marker='o', ms=6, color=estilo.ACENTO, label='The other three bands'),
    Patch(color=estilo.RAMPA[0], label='Cheapest band comes last'),
]
leg = ejes[0].legend(handles=marcas, loc='upper left', bbox_to_anchor=(0, -0.07), ncol=3,
                     frameon=False, handletextpad=0.5, columnspacing=1.8)
for t in leg.get_texts():
    t.set_color(estilo.TINTA_SUAVE)
estilo.guardar(fig, f'{RUTA_BASE}/salidas/graficos/04_control_antiguedad.png')

print('Figuras generadas:')
import os
for f in sorted(os.listdir(f'{RUTA_BASE}/salidas/graficos')):
    print(' -', f)
