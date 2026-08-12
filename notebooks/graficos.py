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
    titular='The cheapest price band has the worst reception in every Steam genre',
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
# FIGURA 4 - Control por antiguedad, small multiples
# =================================================================
import matplotlib.pyplot as plt

mediana_antig = base['antiguedad_anios'].median()
base['banda'] = np.where(base['antiguedad_anios'] <= mediana_antig, 'Recent', 'Older')
generos_fig4 = ['Adventure', 'Indie', 'Casual', 'Action']
sub4 = base[base['Genres'].isin(generos_fig4)]
tabla4 = (sub4.groupby(['Genres', 'banda', 'franja_precio'], observed=True)
          .agg(n=('AppID', 'count'), mediana_pct=('pct_resenas_positivas', 'median'))
          .reset_index())
tabla4 = tabla4[tabla4['n'] >= 20]

fig, ax_madre = estilo.figura(
    titular='The pattern holds for recent and older games alike: it is not an age effect',
    subtitulo='Median share of positive reviews by price band, splitting games at the median age',
    periodo=PERIODO, fuente=FUENTE, nota=NOTA, figsize=(10.4, 6.2),
    izquierda=0.07, abajo=0.17,
)
caja = ax_madre.get_position()
ax_madre.remove()
ejes = fig.subplots(1, 4, sharey=True, gridspec_kw=dict(
    left=caja.x0, right=caja.x1, bottom=caja.y0, top=caja.y1, wspace=0.16))

for ax, genero in zip(ejes, generos_fig4):
    d = tabla4[tabla4['Genres'] == genero]
    for banda, color, off in [('Recent', estilo.ACENTO, -0.19), ('Older', estilo.CONTEXTO, 0.19)]:
        dd = d[d['banda'] == banda].set_index('franja_precio').reindex(etiquetas)
        ax.bar(np.arange(len(etiquetas)) + off, dd['mediana_pct'], width=0.36,
               color=color, label=banda, zorder=2)
    ax.set_xticks(np.arange(len(etiquetas)))
    ax.set_xticklabels(['Q1', 'Q2', 'Q3', 'Q4'])
    ax.set_title(genero, color=estilo.TINTA, pad=8, **estilo._prop('medio', 11))
    ax.set_ylim(0, 100)
    ax.grid(axis='y', zorder=0)
    ax.set_axisbelow(True)
    ax.spines['left'].set_visible(False)

ejes[0].set_ylabel('Median % positive reviews')
leg = ejes[0].legend(loc='lower left', handletextpad=0.5, borderaxespad=0.3)
for t in leg.get_texts():
    t.set_color(estilo.TINTA_SUAVE)
    t.set_fontsize(9)
estilo.guardar(fig, f'{RUTA_BASE}/salidas/graficos/04_control_antiguedad.png')

print('Figuras generadas:')
import os
for f in sorted(os.listdir(f'{RUTA_BASE}/salidas/graficos')):
    print(' -', f)
