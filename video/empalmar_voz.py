"""
Splice the re-recorded scenes into the voice take.

    python video/empalmar_voz.py      # then: python video/limpiar_voz.py

Why: two sentences of the first take overstated what the case's own data says (see guion.md,
"Notes on the claims"), and were re-recorded on 11/10/2026:

- scene 3, video/voz_fragmento_s3.wav: "...the cheapest band was never the best" (the take said
  "had the worst reception", which holds in 9 of 10 genres, not 10);
- scene 4, video/voz_fragmento_s4.wav: "Among older games ... Among recent ones, the gap mostly
  closes" (the take said "Recent or old, the cheapest band still comes last").

All recordings are sources and are never edited. This writes a new file,
video/voz_empalmada.wav, which is what limpiar_voz.py cleans.

Every cut sits in the middle of a natural pause of the take, so no word is touched:

- scene 3 replaces 31.30-42.00 s: from the pause after "...isn't ten dollars today." to right
  after the original "All ten." The take keeps 0.9 s of its own room tone before the fragment,
  which starts speaking at ~0 s.
- scene 4 replaces 42.60-53.05 s: from the pause after "All ten." to the pause before "Which
  genres...". Its recording ends right on the "s" of "genres", so it gets a short fade-out and
  the pause after it is the take's own.

The fragments are 5-7 dB louder than the take, so each gain is measured, not guessed: it is set
to match the loudness of the stretch it replaces. Each join is a 30 ms crossfade, short enough to
be inaudible and long enough to avoid a click.

Needs FFmpeg on PATH.
"""

from pathlib import Path
import re
import subprocess

DIR = Path(__file__).resolve().parent
TOMA = DIR / "voz.wav"
DESTINO = DIR / "voz_empalmada.wav"

# (fragment, cut into the take at, back to the take at, fade-out at the fragment's end) in seconds
FRAGMENTOS = [
    (DIR / "voz_fragmento_s3.wav", 31.30, 42.00, 0.0),
    (DIR / "voz_fragmento_s4.wav", 42.60, 53.05, 0.04),
]
FUNDIDO = 0.03      # s, crossfade at each join


def lufs(archivo: Path, desde: float | None = None, hasta: float | None = None) -> float:
    """Integrated loudness, in mono, of a file or a stretch of it."""
    rango = []
    if desde is not None:
        rango = ["-ss", f"{desde}", "-t", f"{hasta - desde}"]
    salida = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", *rango, "-i", str(archivo),
         "-af", "aformat=channel_layouts=mono,ebur128", "-f", "null", "-"],
        check=True, capture_output=True, text=True,
    ).stderr
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", salida)[-1])


def duracion(archivo: Path) -> float:
    return float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(archivo)],
        check=True, capture_output=True, text=True,
    ).stdout)


def main() -> None:
    entradas = ["-i", str(TOMA)]
    partes, grafo, resumen = [], [], []
    desde = 0.0
    for k, (fragmento, entra, sale, fundido) in enumerate(FRAGMENTOS, start=1):
        assert entra >= desde, "fragments must be in order and must not overlap"
        entradas += ["-i", str(fragmento)]
        ganancia = lufs(TOMA, entra, sale) - lufs(fragmento)
        cola = ""
        if fundido:
            cola = f",afade=t=out:st={duracion(fragmento) - fundido:.3f}:d={fundido}"
        grafo.append(f"[0:a]atrim={desde}:{entra},asetpts=PTS-STARTPTS[toma{k}]")
        grafo.append(f"[{k}:a]volume={ganancia:.2f}dB{cola},asetpts=PTS-STARTPTS[frag{k}]")
        partes += [f"toma{k}", f"frag{k}"]
        resumen.append(f"{fragmento.name} {entra}-{sale} s ({ganancia:+.1f} dB)")
        desde = sale
    grafo.append(f"[0:a]atrim=start={desde},asetpts=PTS-STARTPTS[resto]")
    partes.append("resto")

    # Chain the parts with crossfades: [a][b] -> x1, [x1][c] -> x2, ...
    actual = partes[0]
    for i, siguiente in enumerate(partes[1:], start=1):
        salida = "salida" if i == len(partes) - 1 else f"x{i}"
        grafo.append(f"[{actual}][{siguiente}]acrossfade=d={FUNDIDO}[{salida}]")
        actual = salida

    subprocess.run(
        ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *entradas,
         "-filter_complex", ";".join(grafo), "-map", "[salida]", str(DESTINO)],
        check=True,
    )
    print(f"{TOMA.name} -> {DESTINO.name}: " + " · ".join(resumen))


if __name__ == "__main__":
    main()
