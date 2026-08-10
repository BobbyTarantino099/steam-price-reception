# Recomendaciones — Precio y recepción en Steam

**Caso:** ¿Qué combinaciones de género y franja de precio en Steam sostienen mejor recepción?
**Cliente:** Comité de inversión de un fondo enfocado en videojuegos (cliente ficticio).
**Fecha:** 2026-07-28
**Base de evidencia:** 9.048 juegos de pago con ≥500 reseñas (23.822 filas juego-género),
catálogo histórico de Steam. Tablas: `salidas/tablas/genero_x_franja_precio.csv` y
`salidas/tablas/resumen_por_genero.csv`.

---

## De hallazgo a insight a recomendación

| Hallazgo (fase 4) | Insight (qué significa para el fondo) | Recomendación |
|---|---|---|
| La franja más barata (Q1, ≤3,25 USD reales) es la de peor recepción en los 10 géneros | Precio bajo no compra recepción; en Steam funciona más como señal de producto de bajo presupuesto que como palanca de adopción | R2 — usar la posición de precio del catálogo como filtro de cribado |
| La mejor recepción se concentra en Q3 (6,46–12,36 USD) o Q4 (>12,36 USD), nunca en Q1 ni Q2 | Existe una "zona de precio" defendible; los estudios que ya operan en ella tienen validado su encaje precio-producto | R1 y R2 |
| Adventure, Indie y Casual combinan mejor efecto de franja, volumen y recepción absoluta | Son los géneros donde la tesis "precio medio-alto + buena recepción" tiene más sustento y más objetivos disponibles para invertir | R1 — concentrar la due diligence ahí |
| Massively Multiplayer tiene la peor recepción de los 10 géneros (mediana 76,4%), patrón no monótono y n=176 | No es un "no", es un "no lo sabemos con estos datos"; comprometer horas de due diligence ahí es caro y mal informado | R3 — despriorizar este ciclo |

---

## R1 — Concentrar la due diligence del próximo ciclo en Adventure, Indie y Casual

- **Acción:** el equipo de originación reduce la lista larga de estudios y publishers candidatos a
  los tres géneros Adventure, Indie y Casual para el ciclo de due diligence del próximo semestre.
  Responsable: analista senior de originación. Plazo: definir la lista larga en 4 semanas.
- **Evidencia:** de los 10 géneros de juego reales analizados, estos tres son los únicos que
  combinan (a) recepción absoluta alta —mediana de reseñas positivas de 88,2% (Casual), 86,7%
  (Indie) y 86,2% (Adventure), las tres más altas del conjunto— con (b) un efecto de franja de
  precio claro —+3,31 p.p. (Casual), +3,94 p.p. (Indie) y +5,05 p.p. (Adventure) entre la franja
  más barata y la mejor de su género— y (c) volumen suficiente de objetivos: 2.230, 5.561 y 4.030
  juegos respectivamente, contra 176 del género más pequeño.
  Fuente: `salidas/tablas/resumen_por_genero.csv` y `genero_x_franja_precio.csv`.
  *Nota de precisión:* en Adventure la mejor franja es Q4 (87,48%) por 0,01 p.p. sobre Q3 (87,47%).
  Es un empate técnico, no una preferencia por Q4; se reporta así para no sobreinterpretar el dato.
- **Impacto esperado:** concentra el esfuerzo en el 49,6% de la base analizada (11.821 de 23.822
  filas juego-género) que reúne los tres géneros con mejor recepción, en vez de repartirlo entre
  10. **Supuesto explícito:** el impacto es de *asignación de esfuerzo*, no de retorno financiero —
  el dataset no contiene ventas ni ingresos reales, así que no se estima ni se promete un efecto
  sobre TIR o múltiplo.
- **Métrica de éxito:** % de las operaciones que entran a due diligence profunda que pertenecen a
  los tres géneros priorizados (objetivo: ≥70%), y mediana de % de reseñas positivas del catálogo
  de los estudios que pasan el primer filtro (objetivo: ≥86%). Evaluación a 6 meses.
- **Riesgo / supuesto crítico:** el patrón es correlacional y se apoya en la recepción del público,
  no en desempeño comercial. Tendría que ser cierto que la recepción es un proxy razonable del
  valor del estudio. Si no lo es —por ejemplo, si un género con peor recepción tiene mucha mejor
  monetización—, la priorización estaría optimizando la variable equivocada. **Mitigación:** el
  comité debe cruzar esta priorización con datos de ingresos antes de comprometer capital (ver
  Próximos pasos).
- **Esfuerzo:** bajo. Es una regla de filtrado sobre un proceso que el equipo ya ejecuta.

## R2 — Incorporar la posición de precio del catálogo al cribado de due diligence

- **Acción:** añadir al formulario de cribado un campo obligatorio: qué porcentaje del catálogo del
  estudio candidato se sitúa en cada cuartil de precio ajustado (Q1 ≤3,25 · Q2 3,25–6,46 ·
  Q3 6,46–12,36 · Q4 >12,36 USD reales de 2026). Un estudio con más de la mitad del catálogo en Q1
  se marca para revisión explícita antes de avanzar. Responsable: analista de originación.
  Plazo: incorporarlo al formulario antes de abrir la próxima lista larga.
- **Evidencia:** Q1 es la franja de peor recepción mediana en los 10 géneros sin excepción, con
  medianas que van de 76,0% (Massively Multiplayer) a 86,3% (Casual), siempre la más baja o
  empatada-más-baja de su género. El patrón se sostiene al separar juegos recientes de viejos
  (verificación 4, `notebooks/verificar.py`), y la antigüedad no lo explica (correlación
  antigüedad × recepción = −0,087).
- **Impacto esperado:** el efecto de franja es de 2,51 a 5,05 p.p. de reseñas positivas. Es una
  diferencia real pero moderada. **Supuesto explícito:** por eso este campo se usa como señal de
  alerta que obliga a una revisión, no como criterio de descarte automático — el tamaño del efecto
  no justifica descartar un estudio solo por su franja de precio.
- **Métrica de éxito:** % de fichas de cribado con el campo completo (objetivo: 100% a 3 meses) y
  número de casos marcados que, tras revisión, resultaron efectivamente en un problema de
  posicionamiento de producto. Evaluación a 6 meses.
- **Riesgo / supuesto crítico:** los cuartiles se calcularon sobre el catálogo histórico completo
  de Steam y en dólares ajustados con CPI-U de EE. UU. Tendría que ser cierto que esas bandas
  siguen siendo representativas del mercado actual y de la región del estudio evaluado. Si el
  fondo mira mercados con paridad de precio distinta (LATAM, Asia), las bandas necesitan
  recalcularse. **Además:** existe una lectura alternativa no descartada —que los estudios que
  cobran más también invierten más en calidad—, en cuyo caso el precio es síntoma y no causa. Eso
  no invalida su uso como *señal de cribado*, pero sí impide usarlo como consejo de "sube el
  precio".
- **Esfuerzo:** bajo. Un campo nuevo en un formulario existente; el cálculo se hace con datos
  públicos de Steam.

## R3 — Despriorizar Massively Multiplayer y tratar Sports y Racing como sin evidencia suficiente

- **Acción:** excluir Massively Multiplayer de la lista larga de este ciclo y etiquetar Sports y
  Racing como "requieren evidencia adicional" —no se descartan, pero no consumen horas de due
  diligence hasta tener una base de datos más amplia. Responsable: comité de inversión, en la
  reunión de definición de alcance del ciclo.
- **Evidencia:** Massively Multiplayer tiene la mediana de reseñas positivas más baja de los 10
  géneros en las 4 franjas de precio (74,8%–79,0%; mediana global 76,4%), es el único género con
  patrón no monótono —su mejor franja es Q2, no Q3/Q4— y tiene el n más pequeño de la base (176
  juegos). Sports (329 juegos) y Racing (338) también quedan por debajo del umbral de n<350 que se
  fijó en la verificación 7 de fase 4 para reportar con advertencia de muestra chica.
- **Impacto esperado:** libera las horas de originación de tres géneros que suman el 3,5% de la
  base analizada (843 de 23.822 filas juego-género) y las redirige a R1. **Supuesto explícito:** el
  impacto es de asignación de tiempo del equipo, no financiero.
- **Métrica de éxito:** cero operaciones de Massively Multiplayer entrando a due diligence profunda
  sin una fuente de datos adicional que la sustente, revisado al cierre del ciclo (6 meses).
- **Riesgo / supuesto crítico:** este es el riesgo más incómodo de las tres recomendaciones. Un n
  de 176 juegos es evidencia débil, y despriorizar por evidencia débil puede ser exactamente cómo
  se pierde una oportunidad: los MMO son un modelo de negocio de ingresos recurrentes que la
  métrica de reseñas de Steam captura mal —un jugador insatisfecho con la monetización deja reseña
  negativa aunque el juego sea rentable. Si el fondo tiene tesis de ingresos recurrentes, esta
  recomendación debería revisarse con datos de retención y gasto por usuario, no con reseñas.
- **Esfuerzo:** bajo. Es una decisión de alcance, no un proceso nuevo.

---

## Priorización (impacto contra esfuerzo)

| # | Recomendación | Impacto | Esfuerzo | Prioridad |
|---|---|---|---|---|
| R1 | Concentrar due diligence en Adventure, Indie y Casual | Alto | Bajo | **1 — hacer ya** |
| R2 | Añadir posición de precio al cribado | Medio | Bajo | **2 — hacer ya** |
| R3 | Despriorizar MMO; Sports y Racing sin evidencia suficiente | Medio | Bajo | **3 — decidir en la reunión de alcance** |

Las tres son de esfuerzo bajo porque las tres son reglas sobre un proceso que el fondo ya tiene.
Ninguna requiere contratar, comprar datos ni construir herramientas. Ese es deliberadamente el
techo de lo que este análisis puede sostener: con reseñas agregadas y sin datos de ingresos, la
recomendación honesta es *dónde mirar primero*, no *dónde poner el dinero*.

---

## Limitaciones

1. **No hay causalidad.** El patrón "precio medio-alto → mejor recepción" es correlación
   descriptiva. La lectura alternativa más fuerte —selección: los estudios que cobran más también
   invierten más en producción— no puede descartarse con estos datos. Lo que sí se descartó, con
   evidencia, es que el patrón sea un artefacto de antigüedad (correlación −0,087 y control por
   banda de antigüedad).
2. **No hay datos de ingresos ni de ventas.** `estimated_owners` viene en rangos estimados por
   SteamSpy, no confirmados por Valve, y no se usó como métrica del análisis. Por tanto el caso no
   dice nada sobre rentabilidad, solo sobre recepción del público.
3. **Sesgo de supervivencia.** El dataset solo contiene juegos publicados en Steam: no hay juegos
   cancelados, rechazados ni retirados, ni nada fuera de PC/Steam (consolas, móvil).
4. **La cola larga está fuera.** El filtro de ≥500 reseñas —decidido en fase 1 por confiabilidad
   estadística— excluye deliberadamente al 34,1% del catálogo que tiene 0 reseñas. La muestra está
   sesgada hacia juegos visibles y exitosos. Si el fondo busca precisamente estudios pequeños y
   emergentes, este análisis no los cubre.
5. **Reseñas agregadas, no fechadas.** No existe la evolución temporal de la recepción de un juego;
   la antigüedad del juego se usó como proxy, y ese proxy no captura si un juego mejoró o empeoró
   su recepción tras el lanzamiento.
6. **Ajuste por inflación con año base parcial.** El CPI-U de 2026 es el promedio de solo cuatro
   meses (ene–abr), el único dato disponible a la fecha de descarga.
7. **Fuente de tercera parte.** El dataset es de un agregador (fronkongames), no de Valve
   directamente. Falla el componente "Original" de ROCCC; se declara y no se oculta.

## Datos adicionales que fortalecerían las conclusiones

| Dato | Qué desbloquearía |
|---|---|
| Ingresos o unidades vendidas reales (Valve, o datos de la propia empresa objetivo en la due diligence) | Pasar de "mejor recepción" a "mejor retorno" — es lo que de verdad decide una inversión |
| Reseñas individuales con fecha | Ver si la recepción se sostiene, mejora o se degrada tras el lanzamiento, y separar el efecto del lanzamiento del efecto del precio |
| Presupuesto de producción o tamaño del estudio | Probar directamente la lectura alternativa de selección: si al controlar por presupuesto el efecto del precio desaparece, R2 pierde sustento |
| Histórico de cambios de precio y descuentos por juego | Distinguir precio de lista de precio efectivamente pagado; el análisis actual usa precio de lista |
| Datos de retención y gasto por usuario | Evaluar Massively Multiplayer con la métrica adecuada a su modelo de negocio, en vez de con reseñas (ver riesgo de R3) |
| Datos de consolas y móvil | Saber si el patrón de precio es de Steam o de la industria; hoy no se puede distinguir |

## Próximos pasos

1. **Analizar la cola larga (<500 reseñas).** Repetir la tabla género × franja bajando el umbral a
   50 y 100 reseñas para ver si el patrón se sostiene en el segmento indie/nicho. *Decisión que
   desbloquea:* si el fondo debe o no abrir un carril de inversión en estudios pequeños.
   (Entregable adicional ya previsto desde fase 1.)
2. **Cruzar los tres géneros priorizados con una fuente de ingresos.** *Decisión que desbloquea:*
   convertir la priorización de horas (R1) en una priorización de capital.
3. **Análisis de sensibilidad de las franjas.** Recalcular con quintiles y con bandas fijas para
   confirmar que la conclusión no depende de haber elegido cuartiles. *Decisión que desbloquea:*
   cuánta confianza poner en el campo de cribado de R2.
