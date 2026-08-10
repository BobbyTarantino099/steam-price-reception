import pandas as pd
import numpy as np
from pathlib import Path

RUTA_BASE = Path(__file__).resolve().parents[1]
pd.set_option('display.width', 160)
pd.set_option('display.max_columns', 20)
pd.set_option('display.max_rows', 200)

df_g = pd.read_csv(f'{RUTA_BASE}/datos/limpios/steam_juegos_por_genero.csv', low_memory=False)
df_1 = pd.read_csv(f'{RUTA_BASE}/datos/limpios/steam_juegos_limpios.csv', low_memory=False)

NO_GENERO_CONTENIDO = ['Violent', 'Gore', 'Nudity', 'Sexual Content']
NO_GENERO_SOFTWARE = ['Utilities', 'Design & Illustration', 'Animation & Modeling', 'Education',
                      'Video Production', 'Game Development', 'Audio Production',
                      'Software Training', 'Photo Editing', 'Web Publishing', 'Accounting',
                      'Movie', 'Documentary', 'Episodic', 'Short', 'Tutorial', '360 Video']
NO_GENERO_MODELO = ['Free To Play', 'Early Access']
EXCLUIR = set(NO_GENERO_CONTENIDO + NO_GENERO_SOFTWARE + NO_GENERO_MODELO)
df_gen_real = df_g[~df_g['Genres'].isin(EXCLUIR)].copy()
df_gen_real['total_resenas'] = df_gen_real['Positive'] + df_gen_real['Negative']

df_1['total_resenas'] = df_1['Positive'] + df_1['Negative']
base_precio = df_1[(df_1['Price'] > 0) & (df_1['total_resenas'] >= 500)].copy()
cuartiles = base_precio['precio_ajustado_usd'].quantile([0.25, 0.5, 0.75]).round(2)
q1, q2, q3 = cuartiles[0.25], cuartiles[0.5], cuartiles[0.75]
bordes = [-np.inf, q1, q2, q3, np.inf]
etiquetas = [f'Q1 (<= {q1})', f'Q2 ({q1}-{q2}]', f'Q3 ({q2}-{q3}]', f'Q4 (> {q3})']

base_analisis = df_gen_real[(df_gen_real['Price'] > 0) & (df_gen_real['total_resenas'] >= 500)].copy()
base_analisis['franja_precio'] = pd.cut(base_analisis['precio_ajustado_usd'], bins=bordes, labels=etiquetas)

def log(t):
    print('\n' + '='*70); print(t); print('='*70)

# ---------------------------------------------------------------
# V1 - Prueba de sensatez: orden de magnitud de cuartiles vs precio bruto
# ---------------------------------------------------------------
log('V1 - Prueba de sensatez: cuartiles ajustados vs precio de lista (Price) crudo')
cuartiles_bruto = base_precio['Price'].quantile([0.25, 0.5, 0.75]).round(2)
print('Cuartiles precio_ajustado_usd:', cuartiles.to_dict())
print('Cuartiles Price (bruto, sin ajuste inflacion):', cuartiles_bruto.to_dict())
print('Interpretacion: son muy similares porque el ajuste solo mueve precios de anios con CPI',
      'distinto al anio base; el orden de magnitud (unos pocos USD a low-teens) es plausible',
      'para juegos indie/AA en Steam.')

# ---------------------------------------------------------------
# V2 - Recalculo por via alterna: pivot_table en vez de groupby.agg
# ---------------------------------------------------------------
log('V2 - Recalculo via alterna (pivot_table) de mediana % positivas genero x franja')
pivot = base_analisis.pivot_table(index='Genres', columns='franja_precio',
                                   values='pct_resenas_positivas', aggfunc='median',
                                   observed=True).round(2)
print(pivot)
# Cruce puntual contra el groupby original para Action / Q3
manual = base_analisis[(base_analisis['Genres'] == 'Action') &
                        (base_analisis['franja_precio'] == etiquetas[2])]['pct_resenas_positivas'].median()
print(f"\nChequeo puntual Action x {etiquetas[2]}: pivot={pivot.loc['Action', etiquetas[2]]} "
      f"vs filtro manual={round(manual,2)} -> {'OK' if round(manual,2)==pivot.loc['Action', etiquetas[2]] else 'DIFERENCIA'}")

# ---------------------------------------------------------------
# V3 - Correlacion antiguedad vs % positivas (posible confusor)
# ---------------------------------------------------------------
log('V3 - Correlacion entre antiguedad_anios y pct_resenas_positivas (posible confusor)')
corr = base_analisis[['antiguedad_anios', 'pct_resenas_positivas', 'precio_ajustado_usd']].corr()
print(corr.round(3))
print('Nota: correlacion no implica causalidad. Se usa solo para decidir si hace falta controlar')
print('por antiguedad al comparar franjas de precio dentro de cada genero.')

# ---------------------------------------------------------------
# V4 - Control por antiguedad: repetir tabla dentro de bandas de antiguedad
# ---------------------------------------------------------------
log('V4 - Patron precio->recepcion controlando por antiguedad (juegos recientes vs viejos)')
mediana_antig = base_analisis['antiguedad_anios'].median()
print(f'Mediana de antiguedad en la base de analisis: {mediana_antig} anios (punto de corte)')
base_analisis['banda_antiguedad'] = np.where(base_analisis['antiguedad_anios'] <= mediana_antig,
                                              'Reciente (<= mediana)', 'Viejo (> mediana)')
tabla_controlada = (base_analisis
                    .groupby(['banda_antiguedad', 'Genres', 'franja_precio'], observed=True)
                    .agg(n=('AppID', 'count'), mediana_pct=('pct_resenas_positivas', 'median'))
                    .round(2).reset_index())
tabla_controlada = tabla_controlada[tabla_controlada['n'] >= 20]
for genero in ['Action', 'Adventure', 'Indie', 'Casual']:
    print(f'\n--- {genero} ---')
    print(tabla_controlada[tabla_controlada['Genres'] == genero].to_string(index=False))

# ---------------------------------------------------------------
# V5 - Efecto de tamano: diferencia Q1 vs mejor franja por genero
# ---------------------------------------------------------------
log('V5 - Efecto de tamano: diferencia (p.p.) entre Q1 y la mejor franja, por genero')
resumen = (base_analisis.groupby(['Genres', 'franja_precio'], observed=True)
           .agg(n=('AppID', 'count'), mediana_pct=('pct_resenas_positivas', 'median'))
           .reset_index())
resumen = resumen[resumen['n'] >= 20]
filas = []
for genero, sub in resumen.groupby('Genres'):
    if len(sub) < 2:
        continue
    q1_val = sub.loc[sub['franja_precio'] == etiquetas[0], 'mediana_pct']
    if q1_val.empty:
        continue
    q1_val = q1_val.iloc[0]
    mejor = sub.loc[sub['mediana_pct'].idxmax()]
    filas.append({'Genres': genero, 'mediana_Q1': q1_val, 'mejor_franja': mejor['franja_precio'],
                  'mediana_mejor_franja': mejor['mediana_pct'],
                  'diferencia_pp': round(mejor['mediana_pct'] - q1_val, 2)})
tabla_efecto = pd.DataFrame(filas).sort_values('diferencia_pp', ascending=False)
print(tabla_efecto.to_string(index=False))

# ---------------------------------------------------------------
# V6 - Revision de agregacion: el patron se invierte al bajar un nivel?
# ---------------------------------------------------------------
log('V6 - Steam usa Positive/Negative por separado; recalculo pct_resenas_positivas manualmente para 5 juegos al azar')
muestra = base_analisis.sample(5, random_state=42)[['AppID', 'Name', 'Positive', 'Negative', 'pct_resenas_positivas']]
muestra['recalculo_manual'] = (muestra['Positive'] / (muestra['Positive'] + muestra['Negative']) * 100).round(2)
muestra['coincide'] = muestra['pct_resenas_positivas'] == muestra['recalculo_manual']
print(muestra.to_string(index=False))

# ---------------------------------------------------------------
# V7 - Massively Multiplayer: n bajo, marcar como evidencia debil
# ---------------------------------------------------------------
log('V7 - Robustez de muestra por genero (n total en la base de analisis)')
print(base_analisis.groupby('Genres', observed=True)['AppID'].count().sort_values())
