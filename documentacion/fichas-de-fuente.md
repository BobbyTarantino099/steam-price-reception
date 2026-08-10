# Fichas de fuente de datos — Caso Steam

## Fuente 1: Steam Games Dataset (fronkongames)

- **Origen:** tercera parte — agregador (Kaggle), construido a partir de la Steam Web API oficial +
  SteamSpy (estimaciones no oficiales de "owners").
- **URL o ubicación:** kaggle.com/datasets/fronkongames/steam-games-dataset
- **Fecha de descarga:** 2026-07-28
- **Licencia:** CC BY 4.0 — permite uso y redistribución con atribución. Se citará en el README público.
- **Periodo cubierto:** 1997-06-30 a 2026-12-01 (incluye 2 juegos con fecha de lanzamiento futura,
  aún no publicados a la fecha de descarga).
- **Granularidad:** una fila = un juego (`AppID` único) listado en la tienda de Steam.
- **Volumen:** 125.855 filas × 40 columnas reales (la cabecera cruda declara 39 — ver bug abajo).
- **Formato:** CSV, ~400 MB.

### ROCCC
| Letra | Evaluación | Detalle |
|---|---|---|
| **R**eliable | Medio | `price`, `positive`/`negative` vienen de la API oficial de Steam (confiables). `estimated_owners` viene de SteamSpy, que estima por algoritmo, no por ventas reales confirmadas por Valve. |
| **O**riginal | Medio-bajo | Es una fuente de tercera parte (agregador), no un descargable directo de Valve. Es rastreable: el propio dataset documenta que combina Steam Web API + SteamSpy. |
| **C**omprehensive | Alto para esta pregunta | Contiene `price`, `genres`, `positive`, `negative`, que es todo lo que la pregunta de fase 1 exige. Falta reseñas individuales fechadas (solo el acumulado por juego). |
| **C**urrent | Alto | Descargado el mismo día del análisis; el dataset se actualiza periódicamente en origen. |
| **C**ited | Alto | Ficha pública en Kaggle con metodología, autor y licencia declarados. |

**Fallas declaradas:** Originalidad (tercera parte, no Valve directo) y confiabilidad parcial de
`estimated_owners` (rango estimado, no cifra exacta confirmada). Ambas se documentan como
limitación en el informe, no descalifican la fuente.

- **PII presente:** No. Son metadatos de catálogo de juegos, sin datos personales de usuarios.
- **Seguridad:** archivo estático descargado, vive localmente en `datos/crudos/`, sin credenciales ni
  API en vivo involucradas.
- **Accesibilidad / reproducibilidad:** el archivo crudo (~400 MB) no se sube al repo público de
  portafolio. El README público enlazará directamente a la fuente en Kaggle para que cualquier
  persona pueda reproducir la descarga. Decisión confirmada con el usuario.

**Limitaciones conocidas:**
1. **Bug de cabecera confirmado:** la cabecera cruda declara 39 nombres de columna, pero cada fila
   de datos trae 40 campos. El nombre `DiscountDLC count` en la posición 7 en realidad corresponde a
   dos columnas fusionadas (`Discount` y `DLC count`), lo que desalineaba todo lo posterior. Se
   corrigió en esta fase insertando el nombre faltante antes de cargar (detalle en la prueba de
   integridad, abajo). **Esta corrección debe repetirse igual en fase 3 al cargar el crudo — no está
   resuelta en el archivo, solo diagnosticada.**
2. `estimated_owners` viene en rangos categóricos (ej. "0 - 20000"), no en cifra puntual.
3. No incluye reseñas de texto ni fechas individuales de reseña — impide medir evolución temporal
   real del sentimiento; la fase 1 ya adoptó "antigüedad del juego" como proxy.

---

## Fuente 2: CPI-U — Bureau of Labor Statistics (EE. UU.)

- **Origen:** primera parte — agencia de gobierno de EE. UU. (Bureau of Labor Statistics).
- **URL o ubicación:** bls.gov/cpi/data.htm — serie `CUUR0000SA0` (CPI-U, EE. UU., no ajustada
  estacionalmente, base 1982-84=100).
- **Fecha de descarga:** pendiente — se descargará en fase 3 al momento de aplicar el ajuste.
- **Licencia:** dominio público (obra del gobierno de EE. UU.).
- **Periodo cubierto:** 1913 a la fecha (junio 2026 disponible al momento de esta ficha); cubre
  sobradamente el rango 1997-2026 del catálogo de Steam.
- **Granularidad:** índice mensual y promedio anual, EE. UU. urbano agregado.
- **Volumen:** una fila por mes/año publicado.
- **Formato:** tabla HTML / texto plano descargable desde BLS; también accesible por API pública.

### ROCCC
| Letra | Evaluación | Detalle |
|---|---|---|
| **R**eliable | Alto | Metodología oficial, pública y auditada del gobierno de EE. UU. |
| **O**riginal | Alto | Fuente primaria directa, no un agregador. |
| **C**omprehensive | Alto para este uso | Solo se necesita el índice general anual para deflactar precios; el CPI-U lo cubre. |
| **C**urrent | Alto | Se publica mensualmente; el dato más reciente es abril 2026. |
| **C**ited | Alto | Documentación pública de metodología en bls.gov. |

**Aprobada por el usuario el 2026-07-28** como segunda fuente para el ajuste por inflación de la
fase 1 (precio ajustado por inflación). No falla ninguna letra de ROCCC.

- **PII presente:** No.
- **Licencia / privacidad / seguridad / accesibilidad:** sin restricciones — dominio público,
  descargable libremente, cualquiera puede reproducir el acceso.
