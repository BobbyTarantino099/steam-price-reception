# Diccionario de datos — Steam Games Dataset

Cabecera corregida (ver bug de cabecera en `fichas-de-fuente.md`). Nulos calculados sobre las
125.855 filas tras la corrección. Columnas marcadas **★** son las que usa la pregunta analítica de
fase 1; el resto se documenta por completitud pero no entra al análisis.

| Columna | Tipo | Unidad | Valores permitidos | Significado | Nulos |
|---|---|---|---|---|---|
| AppID ★ | entero | id | único, > 0 | Identificador único de la app en Steam | 0.00% |
| Name ★ | texto | — | libre | Nombre del juego | 0.00% (1 fila) |
| Release date ★ | fecha | AAAA-MM-DD | 1997-06-30 a 2026-12-01 | Fecha de lanzamiento en Steam | 0.00% |
| Estimated owners | categórico (rango) | juegos | ej. "0 - 20000" | Estimación de SteamSpy del número de propietarios, en bandas | 0.00% |
| Peak CCU | entero | jugadores | ≥ 0 | Pico de usuarios concurrentes histórico | 0.00% |
| Required age | entero | años | 0–21 | Edad mínima sugerida/requerida | 0.00% |
| Price ★ | decimal | USD | ≥ 0, hasta 999.98 | Precio de lista actual | 0.00% |
| Discount | entero | % | 0–100 | Descuento vigente al momento de la extracción | 0.00% |
| DLC count | entero | conteo | ≥ 0, hasta 3703 | Número de contenidos descargables del juego | 0.00% |
| About the game | texto | — | libre | Descripción del juego en la tienda | 6.72% |
| Supported languages | texto (lista) | — | lista tipo `['English', ...]` | Idiomas de interfaz soportados | 0.00% |
| Full audio languages | texto (lista) | — | lista tipo `['English', ...]` | Idiomas con doblaje/audio completo | 0.00% |
| Reviews | texto | — | libre | Citas de reseñas destacadas (no estructurado) | 90.32% |
| Header image | texto (URL) | — | URL | Imagen de cabecera de la tienda | 0.06% |
| Website | texto (URL) | — | URL | Sitio web oficial del juego | 59.86% |
| Support url | texto (URL) | — | URL | URL de soporte | 56.06% |
| Support email | texto | — | correo | Correo de soporte | 17.98% |
| Windows | booleano | — | True/False | Disponible en Windows | 0.00% |
| Mac | booleano | — | True/False | Disponible en Mac | 0.00% |
| Linux | booleano | — | True/False | Disponible en Linux | 0.00% |
| Metacritic score | entero | puntos | 0–97 (0 = sin dato) | Puntaje de Metacritic si existe | 0.00%* |
| Metacritic url | texto (URL) | — | URL | Enlace a la ficha de Metacritic | 96.62% |
| User score | entero | puntos | siempre 0 en este dataset | Puntaje de usuario (no poblado) | 0.00%* |
| Positive ★ | entero | reseñas | ≥ 0 | Conteo de reseñas positivas | 0.00% |
| Negative ★ | entero | reseñas | ≥ 0 | Conteo de reseñas negativas | 0.00% |
| Score rank | decimal | rank | — | Ranking interno de Steam (casi vacío) | 99.97% |
| Achievements | entero | conteo | ≥ 0 | Número de logros del juego | 0.00% |
| Recommendations | entero | conteo | ≥ 0 | Recomendaciones de Steam | 0.00% |
| Notes | texto | — | libre | Notas/advertencias del desarrollador | 81.48% |
| Average playtime forever | entero | minutos | ≥ 0 | Tiempo de juego promedio histórico | 0.00% |
| Average playtime two weeks | entero | minutos | ≥ 0 | Tiempo de juego promedio últimas 2 semanas | 0.00% |
| Median playtime forever | entero | minutos | ≥ 0 | Mediana de tiempo de juego histórico | 0.00% |
| Median playtime two weeks | entero | minutos | ≥ 0 | Mediana de tiempo de juego últimas 2 semanas | 0.00% |
| Developers | texto | — | libre, separado por coma | Estudio(s) desarrollador(es) | 6.71% |
| Publishers | texto | — | libre, separado por coma | Editora(s) | 7.09% |
| Categories | texto (lista) | — | libre, separado por coma | Categorías de Steam (ej. Single-player) | 7.12% |
| Genres ★ | texto (lista) | — | libre, separado por coma | Género(s) del juego (1 a 19 por juego, mediana ~3) | 6.69% |
| Tags | texto (lista) | — | libre, separado por coma | Tags asignados por la comunidad | 33.77% |
| Screenshots | texto (lista URLs) | — | URLs | Capturas de pantalla | 4.79% |
| Movies | — | — | — | Columna vacía (100% nula) — candidata a descartar en fase 3 | 100.00% |

\* `Metacritic score` y `User score` no tienen nulos técnicos, pero usan `0` como valor centinela
para "sin dato" (solo 4.258 filas, 3.38%, tienen puntaje real de Metacritic > 0). Se documenta aquí
para que la fase 3 no confunda "0 = mala puntuación" con "0 = sin dato".

## Nota sobre el bug de cabecera

La cabecera cruda del CSV tiene 39 nombres mientras que cada fila de datos trae 40 valores. Esto
ocurre porque el nombre `DiscountDLC count` (posición 7) en realidad corresponde a dos columnas que
se fusionaron por error: `Discount` y `DLC count`. Esta tabla ya refleja la cabecera **corregida**.
El detalle de cómo se diagnosticó y el fragmento de código para reproducir la corrección quedan en
`fichas-de-fuente.md` y se repetirán como primer paso de la fase 3 (Procesar).
