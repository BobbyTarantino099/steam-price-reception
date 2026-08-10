import pandas as pd
import numpy as np
from pathlib import Path

# Raiz del caso, resuelta desde la ubicacion de este archivo: el script corre igual
# en cualquier maquina y desde cualquier directorio de trabajo.
RUTA_BASE = Path(__file__).resolve().parents[1]
RUTA_CRUDO = f'{RUTA_BASE}/datos/crudos/steam_fronkongames_catalogo-historico_2026-07-28.csv'
RUTA_CPI = f'{RUTA_BASE}/datos/crudos/bls_cpi-u_anual_1997-2026_2026-07-28.csv'
FECHA_DESCARGA = pd.Timestamp('2026-07-28')

log = []
def registrar(titulo, **kv):
    log.append((titulo, kv))
    print(f'--- {titulo} ---')
    for k, v in kv.items():
        print(f'{k}: {v}')
    print()

# =========================================================
# T1 — Corregir bug de cabecera
# =========================================================
header_original = pd.read_csv(RUTA_CRUDO, nrows=0).columns.tolist()
idx = header_original.index('DiscountDLC count')
cols_fixed = header_original[:idx] + ['Discount', 'DLC count'] + header_original[idx+1:]
df = pd.read_csv(RUTA_CRUDO, header=None, names=cols_fixed, skiprows=1, low_memory=False)
n_inicial = len(df)
registrar('T1 - Bug de cabecera corregido',
          filas=n_inicial, columnas=df.shape[1],
          detalle="'DiscountDLC count' (pos. 7 de la cabecera cruda) fusionaba 'Discount' y 'DLC count'")

# =========================================================
# T2 — Tipos: Release date a datetime; excluir lanzamientos futuros
# =========================================================
df['Release date'] = pd.to_datetime(df['Release date'], errors='coerce')
no_parseables = df['Release date'].isna().sum()
futuros = (df['Release date'] > FECHA_DESCARGA).sum()
df = df[df['Release date'] <= FECHA_DESCARGA].copy()
registrar('T2 - Tipado de fecha y exclusion de lanzamientos futuros',
          fechas_no_parseables=int(no_parseables),
          juegos_excluidos_fecha_futura=int(futuros),
          filas_restantes=len(df))

# =========================================================
# T3 — Descartar columnas fuera de alcance para este caso
# =========================================================
cols_descartadas = ['Movies', 'Score rank', 'Metacritic url', 'Reviews', 'Notes',
                     'Website', 'Support url', 'Support email', 'About the game',
                     'Supported languages', 'Full audio languages', 'Screenshots',
                     'Header image', 'Categories', 'Tags']
df = df.drop(columns=cols_descartadas)
registrar('T3 - Columnas fuera de alcance descartadas',
          columnas_descartadas=len(cols_descartadas),
          motivo='No aportan a precio/genero/reseñas; nulos muy altos o no estructuradas',
          columnas_restantes=df.shape[1])

# =========================================================
# T4 — Duplicados por AppID (reconfirmacion)
# =========================================================
n_dup = df.duplicated(subset=['AppID']).sum()
df = df.drop_duplicates(subset=['AppID'])
registrar('T4 - Duplicados por AppID', duplicados_encontrados=int(n_dup))

# =========================================================
# T5 — Nulos en Genres: excluir juegos sin genero (no clasificables)
# =========================================================
n_sin_genero = df['Genres'].isna().sum()
df = df[df['Genres'].notna()].copy()
registrar('T5 - Exclusion de juegos sin genero asignado',
          juegos_sin_genero_excluidos=int(n_sin_genero),
          filas_restantes=len(df))

# =========================================================
# T6 — Enriquecer con CPI-U: año, antigüedad, precio ajustado
# =========================================================
df_cpi = pd.read_csv(RUTA_CPI)
ANIO_BASE = int(df_cpi['anio'].max())
cpi_base = df_cpi.loc[df_cpi['anio'] == ANIO_BASE, 'cpi_anual_promedio'].iloc[0]

df['anio_lanzamiento'] = df['Release date'].dt.year
n_antes_merge = len(df)
df = df.merge(df_cpi[['anio', 'cpi_anual_promedio']], left_on='anio_lanzamiento', right_on='anio', how='left')
assert len(df) == n_antes_merge, 'el merge con CPI duplico filas: anio no es unico en la tabla CPI'
sin_cpi = df['cpi_anual_promedio'].isna().sum()

df['antiguedad_anios'] = ANIO_BASE - df['anio_lanzamiento']
df['precio_ajustado_usd'] = (df['Price'] * (cpi_base / df['cpi_anual_promedio'])).round(2)
df = df.drop(columns=['anio'])

registrar('T6 - Enriquecimiento con CPI-U (BLS)',
          anio_base=ANIO_BASE, cpi_base=cpi_base,
          juegos_sin_cpi_coincidente=int(sin_cpi),
          nota='CPI de 2026 es un promedio parcial (ene-abr), declarado en la ficha de fuente')

# =========================================================
# T7 — % reseñas positivas (metrica de fase 1)
# =========================================================
total_resenas = df['Positive'] + df['Negative']
df['pct_resenas_positivas'] = np.where(total_resenas > 0, (df['Positive'] / total_resenas * 100).round(2), np.nan)
sin_resenas = (total_resenas == 0).sum()
registrar('T7 - Calculo de % de reseñas positivas',
          formula='Positive / (Positive+Negative) * 100',
          juegos_sin_ninguna_resena=int(sin_resenas))

# =========================================================
# Verificaciones de rango (reejecucion de pruebas de integridad)
# =========================================================
assert (df['Price'] >= 0).all(), 'precio negativo encontrado'
assert (df['Positive'] >= 0).all() and (df['Negative'] >= 0).all(), 'reseñas negativas encontradas'
assert df['AppID'].is_unique, 'AppID dejo de ser unico'
registrar('Verificacion de rangos', resultado='OK - sin precios ni reseñas negativas, AppID unico')

# =========================================================
# Reconciliacion de conteos
# =========================================================
n_final = len(df)
reconciliacion = n_inicial - int(futuros) - int(n_dup) - int(n_sin_genero)
assert reconciliacion == n_final, f'la reconciliacion no cuadra: {reconciliacion} != {n_final}'
registrar('Reconciliacion de conteos',
          inicial=n_inicial, menos_fecha_futura=int(futuros), menos_duplicados=int(n_dup),
          menos_sin_genero=int(n_sin_genero), final=n_final)

# =========================================================
# Exportar: dataset limpio (un juego = una fila)
# =========================================================
(RUTA_BASE / 'datos' / 'limpios').mkdir(parents=True, exist_ok=True)
ruta_limpio = f'{RUTA_BASE}/datos/limpios/steam_juegos_limpios.csv'
df.to_csv(ruta_limpio, index=False)

# =========================================================
# T8 — Explotar por genero (una fila por juego-genero)
# =========================================================
df_genero = df.copy()
df_genero['Genres'] = df_genero['Genres'].str.split(',')
n_antes_explode = len(df_genero)
df_genero = df_genero.explode('Genres')
df_genero['Genres'] = df_genero['Genres'].str.strip()
registrar('T8 - Explosion por genero (dataset derivado para el analisis de fase 4)',
          filas_antes=n_antes_explode, filas_despues=len(df_genero),
          nota='Un juego con N generos genera N filas; un mismo juego puede aparecer en varios generos')

ruta_genero = f'{RUTA_BASE}/datos/limpios/steam_juegos_por_genero.csv'
df_genero.to_csv(ruta_genero, index=False)

print('\n=== RESUMEN FINAL ===')
print('Dataset limpio (1 fila = 1 juego):', df.shape, '->', ruta_limpio)
print('Dataset por genero (1 fila = 1 juego x genero):', df_genero.shape, '->', ruta_genero)
