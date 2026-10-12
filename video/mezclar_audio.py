"""
Mix the cleaned voice with a music bed for the whole video.

    python video/mezclar_audio.py              # uses the chosen track (MUSICA below)
    python video/mezclar_audio.py musica_2.mp3  # try another one

Reads video/composicion/voz_limpia.wav (limpiar_voz.py) and a track in video/, and writes
video/composicion/mezcla.wav, which is what the composition plays. Run it after limpiar_voz.py.

The music tracks are NOT in the repository: their licences allow using them inside a video but
not redistributing the files on their own, the same reason the raw Steam CSV is not versioned.
Where each one comes from is written down in video/README.md.

How the bed is set, measured rather than guessed:

1. The music is cut to the video's length (68.0 s) and brought to a base of -28 LUFS over that
   stretch, 9 dB under the voice (-19 LUFS). That is what is heard in the pauses and under the
   closing card. The tracks arrive mastered at -10 to -12 LUFS, so this is a big cut.
2. The voice ducks it: a sidechain compressor keyed on the voice lowers the music while the voice
   speaks and lets it come back in the pauses. That keeps the voice clear without leaving the
   music flat and quiet from start to end.
3. A short fade-in at the start, and a fade-out that ends exactly with the video, so the track
   does not stop mid-phrase (all the tracks are longer than the video).
4. A limiter at -1 dBFS on the sum, so voice plus music never clips. The mono voice at -19 LUFS
   becomes -16 LUFS once it plays on both channels, the usual stereo target for web video.

Needs FFmpeg on PATH.
"""

from pathlib import Path
import re
import subprocess
import sys

DIR = Path(__file__).resolve().parent
VOZ = DIR / "composicion" / "voz_limpia.wav"
DESTINO = DIR / "composicion" / "mezcla.wav"

MUSICA = "musica_1.mp3"   # the chosen track; see video/README.md for its source and licence

DURACION = 68.0       # s, the composition's length (index.html, root data-duration)
BASE_LUFS = -28.0     # music level when the voice is silent
FUNDIDO_ENTRADA = 0.8
FUNDIDO_SALIDA = 3.5  # ends exactly at DURACION

# Ducking: how hard and how fast the voice pushes the music down.
DUCKING = "threshold=0.02:ratio=4:attack=25:release=500:knee=4"


def lufs(archivo: Path, hasta: float | None = None) -> float:
    rango = ["-t", f"{hasta}"] if hasta else []
    salida = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", *rango, "-i", str(archivo),
         "-af", "ebur128", "-f", "null", "-"],
        check=True, capture_output=True, text=True,
    ).stderr
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", salida)[-1])


def mezclar(musica: Path, destino: Path) -> float:
    ganancia = BASE_LUFS - lufs(musica, DURACION)
    grafo = ";".join([
        f"[1:a]atrim=0:{DURACION},asetpts=PTS-STARTPTS,aresample=48000,"
        f"aformat=channel_layouts=stereo,volume={ganancia:.2f}dB,"
        f"afade=t=in:st=0:d={FUNDIDO_ENTRADA},"
        f"afade=t=out:st={DURACION - FUNDIDO_SALIDA}:d={FUNDIDO_SALIDA}[musica]",
        # The voice is mono: copy it to both channels at full level (plain up-mixing lowers each
        # channel 3 dB), and pad it with silence to the video's length, because the sidechain
        # compressor stops when its key stops and would take the closing card's music with it.
        f"[0:a]aresample=48000,pan=stereo|c0=c0|c1=c0,apad=whole_dur={DURACION},asplit=2[clave][voz]",
        f"[musica][clave]sidechaincompress={DUCKING}[cama]",
        "[voz][cama]amix=inputs=2:normalize=0:duration=longest,"
        f"atrim=0:{DURACION},alimiter=limit=0.891:level=disabled[salida]",
    ])
    subprocess.run(
        ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
         "-i", str(VOZ), "-i", str(musica),
         "-filter_complex", grafo, "-map", "[salida]", str(destino)],
        check=True,
    )
    return ganancia


def main() -> None:
    musica = DIR / (sys.argv[1] if len(sys.argv) > 1 else MUSICA)
    destino = Path(sys.argv[2]) if len(sys.argv) > 2 else DESTINO
    ganancia = mezclar(musica, destino)
    print(f"{VOZ.name} + {musica.name} ({ganancia:+.1f} dB) -> {destino}")


if __name__ == "__main__":
    main()
