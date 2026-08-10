# Bloque para la página índice del portafolio

Listo para pegar. Es lo único que muchos van a leer.

---

## Versión larga (índice del portafolio)

> ### En Steam, la franja de precio más barata es la de peor recepción en los 10 géneros
>
> ![](salidas/graficos/01_q1_vs_mejor_franja.png)
>
> Analicé el catálogo histórico de Steam —125.855 juegos— con Python y pandas para responder una
> pregunta de un fondo de inversión: en qué género conviene priorizar la due diligence. Combiné el
> catálogo con el índice CPI-U del BLS para comparar precios de 29 años en dólares reales, y
> encontré que los juegos por debajo de 3,25 USD tienen la peor recepción de su género sin una sola
> excepción, mientras el pico se concentra en 6,46–12,36 USD y nunca en el precio más alto.
> Verifiqué que no fuera un simple efecto de antigüedad —la objeción evidente— y no lo es.
> Recomendé concentrar la due diligence en Adventure, Indie y Casual, y añadir la posición de
> precio del catálogo al cribado, dejando explícito que sin datos de ingresos esto dice dónde
> mirar, no dónde poner el dinero.
>
> `Python` `pandas` `matplotlib` `2 fuentes combinadas` `125.855 juegos`
> · [Ver el caso completo →](URL-DEL-REPOSITORIO)

## Versión corta (LinkedIn, CV)

> **En Steam, la franja de precio más barata es la de peor recepción en los 10 géneros.** Analicé
> 125.855 juegos con Python y pandas, ajustando precios por inflación con el CPI-U del BLS, y
> encontré que el pico de recepción está en 6,46–12,36 USD reales —nunca en lo más barato, tampoco
> siempre en lo más caro. Base de una recomendación de priorizar due diligence en Adventure, Indie
> y Casual para un fondo de inversión.

## Versión de una frase (15 segundos)

> En Steam, lo barato no compra buena recepción: la franja de precio más baja es la peor de su
> género en los diez géneros, y el pico está en 6,46–12,36 dólares reales.

## Línea para el CV

> Analicé 125.855 juegos de Steam combinados con el índice CPI-U para identificar el patrón de
> precio y recepción por género; el resultado —la franja más barata es la de peor recepción en los
> 10 géneros, con un efecto de 2,5 a 5,0 p.p.— fue la base de una recomendación de priorización de
> due diligence para un fondo de inversión.

---

## Matriz de cobertura del portafolio

| Caso | Tipo de problema | Herramienta principal | Dominio | Tipo de dato | Qué demuestra |
|---|---|---|---|---|---|
| **Steam: precio y recepción** | Encontrar patrones | Python (pandas) | Videojuegos / plataformas digitales | Transversal, estructurado, dos fuentes combinadas | Limpieza de una imperfección estructural real (cabecera rota), enriquecimiento con una segunda fuente (CPI-U) para comparabilidad temporal, y descarte explícito de la explicación alternativa antes de publicar |
| Caso 2 | | | | | |
| Caso 3 | | | | | |

**Huecos identificados tras este caso:**

- **Tipos de problema sin cubrir:** predecir, categorizar, detectar lo inusual, identificar temas,
  descubrir conexiones. Este caso cubre solo "encontrar patrones".
- **Herramientas sin demostrar:** SQL y una herramienta de BI (Tableau o Power BI). Este caso es
  íntegramente Python.
- **Tipo de dato sin cubrir:** longitudinal real (series temporales con la misma unidad observada
  en el tiempo). Aquí la antigüedad es un proxy transversal, no una serie.
- **¿Algún caso donde el resultado contradijo la hipótesis inicial?** Parcialmente. La hipótesis
  intuitiva "más caro, mejor recepción" quedó a medias: el pico no está en el precio más alto sino
  en el medio-alto. Falta un caso donde la conclusión se dé de frente contra el supuesto de
  partida.

**El próximo caso debería:** usar **SQL** como herramienta protagonista, sobre datos
**longitudinales**, y preferiblemente un tipo de problema distinto (detectar lo inusual o
categorizar). Un dominio fuera de videojuegos —salud, retail o movilidad— además ampliaría la
cobertura sectorial.
