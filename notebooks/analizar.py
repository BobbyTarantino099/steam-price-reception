import pandas as pd
import numpy as np
from pathlib import Path

RUTA_BASE = Path(__file__).resolve().parents[1]
(RUTA_BASE / 'salidas' / 'tablas').mkdir(parents=True, exist_ok=True)
pd.set_option('display.width', 160)
pd.set_option('display.max_columns', 20)

df_g = pd.read_csv(f'{RUTA_BASE}/datos/limpios/steam_juegos_por_genero.csv', low_memory=False)
df_1 = pd.read_csv(f'{RUTA_BASE}/datos/limpios/steam_juegos_limpios.csv', low_memory=False)

def log(t):
    print('\n' + '='*70)
    print(t)
    print('='*70)

# ---------------------------------------------------------------
# Decision confirmada con el usuario: excluir no-generos
# ---------------------------------------------------------------
NO_GENERO_CONTENIDO = ['Violent', 'Gore', 'Nudity', 'Sexual Content']
NO_GENERO_SOFTWARE = ['Utilities', 'Design & Illustration', 'Animation & Modeling', 'Education',
                      'Video Production', 'Game Development', 'Audio Production',
                      'Software Training', 'Photo Editing', 'Web Publishing', 'Accounting',
                      'Movie', 'Documentary', 'Episodic', 'Short', 'Tutorial', '360 Video']
NO_GENERO_MODELO = ['Free To Play', 'Early Access']
EXCLUIR = set(NO_GENERO_CONTENIDO + NO_GENERO_SOFTWARE + NO_GENERO_MODELO)

n_antes = len(df_g)
n_juegos_excluidos_appid = df_g.loc[df_g['Genres'].isin(EXCLUIR), 'AppID'].nunique()
df_gen_real = df_g[~df_g['Genres'].isin(EXCLUIR)].copy()
log('Filtro de taxonomia de genero (decision confirmada por el usuario)')
print(f'Filas antes (juego-genero): {n_antes}')
print(f'Filas eliminadas por no-genero: {n_antes - len(df_gen_real)}')
print(f'Filas despues: {len(df_gen_real)}')
print(f'Generos reales resultantes: {df_gen_real["Genres"].nunique()}')
print(sorted(df_gen_real['Genres'].unique()))

# =================================================================
# PASO 1 - Estadistica descriptiva base (sobre 1 fila = 1 juego)
# =================================================================
log('PASO 1 - Descriptivos generales (steam_juegos_limpios, N=1 fila/juego)')
print('N juegos total:', len(df_1))
print('\nprecio_ajustado_usd (todos, incluye F2P en 0):')
print(df_1['precio_ajustado_usd'].describe())
print('\npct_resenas_positivas (solo juegos con >=1 resena):')
print(df_1['pct_resenas_positivas'].describe())
print('\nantiguedad_anios:')
print(df_1['antiguedad_anios'].describe())

n_pago = (df_1['Price'] > 0).sum()
n_f2p = (df_1['Price'] == 0).sum()
print(f'\nJuegos de pago (Price>0): {n_pago} | F2P (Price==0): {n_f2p}')

total_resenas = df_1['Positive'] + df_1['Negative']
n_pasa_filtro = (total_resenas >= 500).sum()
print(f'Juegos con >=500 resenas (Positive+Negative): {n_pasa_filtro}')

# =================================================================
# PASO 2 - Filtro de analisis + cuartiles de precio ajustado
# =================================================================
log('PASO 2 - Filtro de analisis (pago + >=500 resenas) y cuartiles')

df_1['total_resenas'] = df_1['Positive'] + df_1['Negative']
base_precio = df_1[(df_1['Price'] > 0) & (df_1['total_resenas'] >= 500)].copy()
print(f'Juegos que entran a la base de cuartiles (pago y >=500 resenas): {len(base_precio)}')

# Cuartiles calculados sobre precio AJUSTADO, base = juegos de pago con >=500 resenas
cuartiles = base_precio['precio_ajustado_usd'].quantile([0.25, 0.5, 0.75]).round(2)
print('Cuartiles de precio_ajustado_usd (base de calculo):')
print(cuartiles)

q1, q2, q3 = cuartiles[0.25], cuartiles[0.5], cuartiles[0.75]
bordes = [-np.inf, q1, q2, q3, np.inf]
etiquetas = [f'Q1 (<= {q1})', f'Q2 ({q1}-{q2}]', f'Q3 ({q2}-{q3}]', f'Q4 (> {q3})']

# Aplicar la MISMA franja (bordes fijos) a la base de juego-genero, filtrada igual
df_gen_real['total_resenas'] = df_gen_real['Positive'] + df_gen_real['Negative']
base_analisis = df_gen_real[(df_gen_real['Price'] > 0) & (df_gen_real['total_resenas'] >= 500)].copy()
base_analisis['franja_precio'] = pd.cut(base_analisis['precio_ajustado_usd'], bins=bordes, labels=etiquetas)

print(f'\nFilas juego-genero en base de analisis (genero real, pago, >=500 resenas): {len(base_analisis)}')
print('Juegos unicos en esta base:', base_analisis['AppID'].nunique())
print('\nDistribucion de franja de precio (conteo de filas juego-genero):')
print(base_analisis['franja_precio'].value_counts().sort_index())

# =================================================================
# PASO 3 - Tabla genero x franja de precio
# =================================================================
log('PASO 3 - Tabla genero x franja de precio (pct_resenas_positivas)')

tabla = (base_analisis
         .groupby(['Genres', 'franja_precio'], observed=True)
         .agg(n_juegos=('AppID', 'count'),
              media_pct_positivas=('pct_resenas_positivas', 'mean'),
              mediana_pct_positivas=('pct_resenas_positivas', 'median'),
              media_antiguedad=('antiguedad_anios', 'mean'))
         .round(2)
         .reset_index())

# Solo celdas con volumen minimamente robusto (n>=20) para reportar
tabla_robusta = tabla[tabla['n_juegos'] >= 20].sort_values(['Genres', 'franja_precio'])
pd.set_option('display.max_rows', 200)
print(tabla_robusta.to_string(index=False))

tabla.to_csv(f'{RUTA_BASE}/salidas/tablas/genero_x_franja_precio.csv', index=False)

# Resumen por genero (todas las franjas juntas) para ranking inicial
resumen_genero = (base_analisis
                  .groupby('Genres', observed=True)
                  .agg(n_juegos=('AppID', 'count'),
                       media_pct_positivas=('pct_resenas_positivas', 'mean'),
                       mediana_pct_positivas=('pct_resenas_positivas', 'median'),
                       media_antiguedad=('antiguedad_anios', 'mean'),
                       media_precio_ajustado=('precio_ajustado_usd', 'mean'))
                  .round(2)
                  .sort_values('mediana_pct_positivas', ascending=False))
log('Resumen por genero (todas las franjas, ordenado por mediana de % positivas)')
print(resumen_genero.to_string())
resumen_genero.to_csv(f'{RUTA_BASE}/salidas/tablas/resumen_por_genero.csv')
