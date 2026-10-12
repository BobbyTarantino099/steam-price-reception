"""
The numbers the video shows, taken from the case's own files instead of typed by hand.

    python video/datos_video.py

Writes video/composicion/assets/datos.js (`window.DATOS = {...}`), loaded by index.html.
A .js and not a .json because a composition must not fetch anything while it renders:
every frame has to come out the same. Two things:

1. Real rows of the raw Steam file, read the way the broken header reads them: the header
   names 39 columns but every row carries 40, because `DiscountDLC count` merges
   `Discount` and `DLC count`. So the discount sits under "DiscountDLC count", the DLC
   count under "About the game", and the description under "Supported languages".
   That is what scene 2 shows before and after the fix.
2. The inflation example of scene 2 ("ten dollars in the early 2000s"), with the same
   CPI-U file and the same 2026 base year as the analysis.
3. Scene 3's chart, which is figure 01 of the case: per genre, the median positive-review
   share of the cheapest band (Q1) and of the genre's best band, from the analysis table
   salidas/tablas/genero_x_franja_precio.csv. Plus the four price bands, read from that
   table's own labels so they cannot drift from the analysis.
4. Scene 4's age control: per genre, the median positive-review share of each price band for
   older and recent games, split at the median age. There is no aggregated table with this
   split, so it is computed here from datos/limpios/ exactly the way notebooks/graficos.py
   builds figure 04 (same base, same bands, same cut, bands with n >= 20), and two asserts
   stop the script if that base ever drifts. Unlike figure 04, it covers all ten genres:
   that is what showed the age objection is partly right (see guion.md).

Needs the raw Steam CSV in datos/crudos/ (see the case README for where to download it) and
datos/limpios/, which notebooks/procesar.py regenerates from it.
"""

from pathlib import Path
import csv
import json
import sys

RAIZ = Path(__file__).resolve().parents[1]
CRUDOS = RAIZ / "datos" / "crudos"
TABLA = RAIZ / "salidas" / "tablas" / "genero_x_franja_precio.csv"
LIMPIOS = RAIZ / "datos" / "limpios" / "steam_juegos_por_genero.csv"
DESTINO = Path(__file__).resolve().parent / "composicion" / "assets" / "datos.js"

FILAS = 4
ANIO_EJEMPLO = 2002   # "early 2000s"
ANIO_BASE = 2026      # base year of the analysis
DOLARES = 10.0


def filas_reales() -> list[dict]:
    """The first rows that make the misalignment visible: paid, discounted, short name."""
    crudo = next(CRUDOS.glob("steam_fronkongames_catalogo-historico_*.csv"))
    csv.field_size_limit(sys.maxsize if sys.maxsize < 2**31 else 2**31 - 1)
    with crudo.open(encoding="utf-8", newline="") as f:
        lector = csv.reader(f)
        cabecera = next(lector)
        assert len(cabecera) == 39, "the header bug is gone: rethink scene 2"
        filas = []
        for r in lector:
            if len(r) != 40:
                continue
            nombre, precio, descuento, dlc, acerca = r[1], r[6], r[7], r[8], r[9]
            if not (nombre.isascii() and len(nombre) <= 26 and acerca.isascii()):
                continue
            if float(precio) <= 0 or int(descuento) <= 0 or len(acerca) < 40:
                continue
            # Content warnings open some descriptions; not what a portfolio should put on screen.
            if acerca.upper().startswith(("WARNING", "CONTENT WARNING", "NOTE")):
                continue
            filas.append({
                "name": nombre,
                "price": f"{float(precio):.2f}",
                "discount": descuento,
                "dlc": dlc,
                "about": acerca[:32].rsplit(" ", 1)[0].rstrip(",.;:'") + "…",
            })
            if len(filas) == FILAS:
                return filas
    raise SystemExit("not enough rows matched")


def inflacion() -> dict:
    with (CRUDOS / "bls_cpi-u_anual_1997-2026_2026-07-28.csv").open(encoding="utf-8") as f:
        cpi = {int(r["anio"]): float(r["cpi_anual_promedio"]) for r in csv.DictReader(f)}
    return {
        "year": ANIO_EJEMPLO,
        "base_year": ANIO_BASE,
        "dollars": DOLARES,
        "real": round(DOLARES * cpi[ANIO_BASE] / cpi[ANIO_EJEMPLO], 2),
    }


def generos() -> dict:
    """Figure 01 as data: cheapest band vs best band, sorted by the gap like the figure."""
    tabla: dict[str, dict[str, float]] = {}
    franjas: dict[str, str] = {}
    with TABLA.open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            q, etiqueta = r["franja_precio"].split(" ", 1)
            franjas[q] = etiqueta.strip("()")
            tabla.setdefault(r["Genres"], {})[q] = float(r["mediana_pct_positivas"])
    filas = []
    for genero, m in tabla.items():
        mejor = max(m, key=m.get)
        assert mejor != "Q1", f"{genero}: the cheapest band is the best one — scene 3 is wrong"
        filas.append({
            "genre": genero,
            "q1": m["Q1"],
            "best": m[mejor],
            "best_band": mejor,
            "gap": f"{m[mejor] - m['Q1']:+.1f}",
        })
    filas.sort(key=lambda r: r["best"] - r["q1"], reverse=True)
    return {"bands": franjas, "genres": filas}


def antiguedad() -> dict:
    """Figure 04's age control, over all ten genres. Mirrors notebooks/graficos.py."""
    import re
    import numpy as np
    import pandas as pd

    fuente = (RAIZ / "notebooks" / "graficos.py").read_text(encoding="utf-8")
    no_genero = eval(re.search(r"NO_GENERO = (set\(\[.*?\]\))", fuente, re.S).group(1))
    g = pd.read_csv(LIMPIOS, low_memory=False)
    g = g[~g["Genres"].isin(no_genero)].copy()
    base = g[(g["Price"] > 0) & (g["Positive"] + g["Negative"] >= 500)].copy()
    assert base["AppID"].nunique() == 8998, "figure 04's base changed: rethink scene 4"
    base["q"] = pd.cut(base["precio_ajustado_usd"], bins=[-np.inf, 3.25, 6.46, 12.36, np.inf],
                       labels=["Q1", "Q2", "Q3", "Q4"])
    corte = float(base["antiguedad_anios"].median())
    assert corte == 6.0, "the median age moved: rethink scene 4"
    base["edad"] = np.where(base["antiguedad_anios"] <= corte, "recent", "older")
    t = (base.groupby(["Genres", "edad", "q"], observed=True)
         .agg(n=("AppID", "count"), m=("pct_resenas_positivas", "median")).reset_index())
    t = t[t["n"] >= 20]

    filas = []
    for genero in sorted(base["Genres"].unique()):
        fila = {"genre": genero}
        for edad in ("older", "recent"):
            m = t[(t["Genres"] == genero) & (t["edad"] == edad)].set_index("q")["m"]
            if len(m) < 4:
                fila[edad] = None          # not enough games in some band
                continue
            fila[edad] = {
                "bands": {q: round(float(v), 2) for q, v in m.items()},
                "q1_last": bool(m["Q1"] == m.min()),
            }
        filas.append(fila)
    return {"cut_years": corte, "genres": filas}


def main() -> None:
    datos = {"rows": filas_reales(), "inflation": inflacion(), **generos(), "age": antiguedad()}
    texto = json.dumps(datos, indent=2, ensure_ascii=False)
    DESTINO.write_text(
        "// Generated by video/datos_video.py. Do not edit by hand.\n"
        f"window.DATOS = {texto};\n",
        encoding="utf-8",
    )
    print(f"-> {DESTINO.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
