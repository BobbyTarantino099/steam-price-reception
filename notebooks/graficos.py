import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from pathlib import Path

RUTA_BASE = Path(__file__).resolve().parents[1]
(RUTA_BASE / 'salidas' / 'graficos').mkdir(parents=True, exist_ok=True)
sns.set_style('white')
plt.rcParams['font.size'] = 11

GRIS = '#b0b0b0'
AZUL = '#1f5fa8'
NARANJA = '#d9822b'

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
etiquetas = ['Q1 (<=3,25)', 'Q2 (3,25-6,46)', 'Q3 (6,46-12,36)', 'Q4 (>12,36)']
base['franja_precio'] = pd.cut(base['precio_ajustado_usd'], bins=bordes, labels=etiquetas)

tabla = (base.groupby(['Genres', 'franja_precio'], observed=True)
         .agg(n=('AppID', 'count'), mediana_pct=('pct_resenas_positivas', 'median'))
         .reset_index())
tabla_robusta = tabla[tabla['n'] >= 20].copy()

FUENTE = ('Fuente: Steam Games Dataset (fronkongames, Kaggle, CC BY 4.0) + BLS CPI-U. '
          'Base: 8.998 juegos de pago con >=500 resenas, 10 generos reales (excluye descriptores '
          'de contenido, etiquetas de software y Free To Play/Early Access). Precio ajustado por '
          'inflacion, base 2026 (promedio parcial ene-abr).')

def nota_fuente(fig, texto=FUENTE):
    fig.text(0.01, -0.02, texto, ha='left', va='top', fontsize=7.5, color='#555555', wrap=True)

# =================================================================
# FIGURA 1 - Q1 vs mejor franja por genero (barras agrupadas)
# =================================================================
filas = []
for genero, sub in tabla_robusta.groupby('Genres'):
    q1_val = sub.loc[sub['franja_precio'] == etiquetas[0], 'mediana_pct']
    if q1_val.empty:
        continue
    q1_val = q1_val.iloc[0]
    mejor = sub.loc[sub['mediana_pct'].idxmax()]
    filas.append({'Genres': genero, 'Q1': q1_val, 'mejor': mejor['mediana_pct'],
                  'franja_mejor': mejor['franja_precio'], 'dif': mejor['mediana_pct'] - q1_val})
f1 = pd.DataFrame(filas).sort_values('dif', ascending=True)

fig, ax = plt.subplots(figsize=(9, 6.3))
y = np.arange(len(f1))
ax.barh(y - 0.2, f1['Q1'], height=0.4, color=GRIS, label='Franja más barata (Q1)')
ax.barh(y + 0.2, f1['mejor'], height=0.4, color=AZUL, label='Mejor franja del género')
ax.set_yticks(y)
ax.set_yticklabels(f1['Genres'])
ax.set_xlim(0, 108)
ax.set_xlabel('Mediana de % de reseñas positivas')
fig.suptitle('La franja más barata es la de peor recepción en los 10 géneros de Steam',
             fontsize=14, weight='bold', x=0.01, ha='left', y=1.03)
ax.set_title('Diferencia entre Q1 (≤3,25 USD) y la mejor franja de precio de cada género, en p.p.',
             fontsize=10, color='#444444', loc='left', pad=12)
for i, row in enumerate(f1.itertuples()):
    ax.text(row.mejor + 1.5, i + 0.2, f'+{row.dif:.1f} p.p.', va='center', fontsize=9, color=AZUL)
    ax.text(row.Q1 + 1.5, i - 0.2, f'{row.Q1:.1f}%', va='center', fontsize=8.5, color='#555555')
fig.legend(loc='upper right', bbox_to_anchor=(0.98, 0.97), ncol=2, frameon=False, fontsize=9)
sns.despine(left=True, bottom=False)
ax.grid(axis='x', color='#eeeeee')
nota_fuente(fig)
fig.savefig(f'{RUTA_BASE}/salidas/graficos/01_q1_vs_mejor_franja.png', dpi=150, bbox_inches='tight')
plt.close(fig)

# =================================================================
# FIGURA 2 - Mapa de calor genero x franja (mediana % positivas)
# =================================================================
pivot = tabla_robusta.pivot(index='Genres', columns='franja_precio', values='mediana_pct')
orden_genero = pivot.mean(axis=1).sort_values(ascending=False).index
pivot = pivot.loc[orden_genero]

fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(pivot, annot=True, fmt='.1f', cmap='Blues', cbar_kws={'label': '% mediana de reseñas positivas'},
            linewidths=0.5, linecolor='white', ax=ax, vmin=70, vmax=92)
fig.suptitle('La mejor recepción se concentra en precios medios-altos (Q3/Q4), nunca en el más barato',
             fontsize=13, weight='bold', x=0.01, ha='left', y=1.04)
ax.set_title('Mediana de % de reseñas positivas por género y franja de precio ajustado',
             fontsize=10, color='#444444', loc='left', pad=10)
ax.set_xlabel('')
ax.set_ylabel('')
nota_fuente(fig)
fig.savefig(f'{RUTA_BASE}/salidas/graficos/02_heatmap_genero_franja.png', dpi=150, bbox_inches='tight')
plt.close(fig)

# =================================================================
# FIGURA 3 - Ranking de efecto, candidatos destacados
# =================================================================
f3 = f1.sort_values('dif', ascending=True).copy()
CANDIDATOS = {'Adventure', 'Indie', 'Casual'}
colores = [AZUL if g in CANDIDATOS else GRIS for g in f3['Genres']]

fig, ax = plt.subplots(figsize=(8.5, 6.2))
y = np.arange(len(f3))
ax.barh(y, f3['dif'], color=colores)
ax.set_yticks(y)
ax.set_yticklabels(f3['Genres'])
ax.set_xlabel('Diferencia en puntos porcentuales (mejor franja − Q1)')
fig.suptitle('Adventure, Indie y Casual combinan mejor efecto, volumen y recepción absoluta',
             fontsize=13, weight='bold', x=0.01, ha='left', y=1.03)
ax.set_title('Efecto de precio sobre recepción por género (p.p.); azul = candidatos con mejor evidencia combinada',
             fontsize=9.5, color='#444444', loc='left', pad=12)
for i, row in enumerate(f3.itertuples()):
    ax.text(row.dif + 0.05, i, f'{row.dif:.2f}', va='center', fontsize=9,
            color=AZUL if row.Genres in CANDIDATOS else '#555555', weight='bold' if row.Genres in CANDIDATOS else 'normal')
ax.set_xlim(0, f3['dif'].max() + 1)
sns.despine(left=True)
ax.grid(axis='x', color='#eeeeee')
nota_fuente(fig)
fig.savefig(f'{RUTA_BASE}/salidas/graficos/03_ranking_efecto_candidatos.png', dpi=150, bbox_inches='tight')
plt.close(fig)

# =================================================================
# FIGURA 4 - Control por antiguedad (recientes vs viejos) para los 3 candidatos + Action de referencia
# =================================================================
mediana_antig = base['antiguedad_anios'].median()
base['banda'] = np.where(base['antiguedad_anios'] <= mediana_antig, 'Recientes', 'Viejos')
generos_fig4 = ['Adventure', 'Indie', 'Casual', 'Action']
sub4 = base[base['Genres'].isin(generos_fig4)]
tabla4 = (sub4.groupby(['Genres', 'banda', 'franja_precio'], observed=True)
          .agg(n=('AppID', 'count'), mediana_pct=('pct_resenas_positivas', 'median'))
          .reset_index())
tabla4 = tabla4[tabla4['n'] >= 20]

fig, axes = plt.subplots(1, 4, figsize=(15, 5.3), sharey=True)
fig.subplots_adjust(top=0.72, bottom=0.12)
for ax, genero in zip(axes, generos_fig4):
    d = tabla4[tabla4['Genres'] == genero]
    for banda, color, offset in [('Recientes', AZUL, -0.18), ('Viejos', GRIS, 0.18)]:
        dd = d[d['banda'] == banda].set_index('franja_precio').reindex(etiquetas)
        x = np.arange(len(etiquetas)) + offset
        ax.bar(x, dd['mediana_pct'], width=0.36, color=color, label=banda)
    ax.set_xticks(np.arange(len(etiquetas)))
    ax.set_xticklabels(['Q1', 'Q2', 'Q3', 'Q4'])
    ax.set_title(genero, fontsize=11, weight='bold', pad=8)
    ax.set_ylim(0, 100)
    sns.despine(ax=ax, left=True)
    ax.grid(axis='y', color='#eeeeee')
axes[0].set_ylabel('Mediana % reseñas positivas')
axes[0].legend(loc='lower right', frameon=False, fontsize=8)
fig.suptitle('El patrón se sostiene en juegos recientes y viejos: no es un efecto de antigüedad',
             fontsize=14, weight='bold', x=0.01, ha='left', y=0.99)
fig.text(0.01, 0.885, 'Mediana de % reseñas positivas por franja de precio, separando juegos recientes (≤ mediana de antigüedad) de viejos',
         fontsize=10, color='#444444')
nota_fuente(fig)
fig.savefig(f'{RUTA_BASE}/salidas/graficos/04_control_antiguedad.png', dpi=150, bbox_inches='tight')
plt.close(fig)

print('Figuras generadas:')
import os
for f in sorted(os.listdir(f'{RUTA_BASE}/salidas/graficos')):
    print(' -', f)
