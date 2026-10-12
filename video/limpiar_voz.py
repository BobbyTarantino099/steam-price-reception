"""
Clean the voice recording for the video.

It reads the spliced take (video/voz_empalmada.wav, built by empalmar_voz.py from the two
recordings, which are sources and never edited) and writes a new file,
video/composicion/voz_limpia.wav, which is what the composition plays. Re-run both after
re-recording:

    python video/empalmar_voz.py
    python video/limpiar_voz.py

Needs FFmpeg on PATH. The filter chain, in order:

1. Down-mix to mono: the voice is a single source, and stereo only doubles the size.
2. High-pass at 80 Hz: removes rumble and hum below the voice.
3. FFT denoise (20 dB) with the noise floor at -70 dB. The floor has to sit BELOW the
   real noise (-63 dB RMS in the pauses): at -60 dB the filter barely acted, which was
   only caught by measuring the pauses before and after, not by ear.
4. A soft noise gate (ratio 4, not a hard cut) to lower what is left in the pauses.
5. Loudness to -19 LUFS, the usual target for MONO speech (-16 is the stereo one), in
   two passes: measure the cleaned voice, then apply exactly the gain that is missing,
   with a limiter at -1.5 dBFS as a ceiling for the loudest syllables. `loudnorm` was
   tried first and dropped: it switches mode on its own when the peaks don't fit, and
   landed anywhere between -18.8 and -22 LUFS.

Chosen by ear on 11/10/2026 out of three samples: none, this one, and a stronger
non-local-means filter (`anlmdn`). This one was the most balanced: it lowers the pauses
from 32 to ~41 dB below the voice without touching the voice or the
pronunciation. `anlmdn` also cut the end of the audio in FFmpeg 9.0.
"""

from pathlib import Path
import re
import subprocess

DIR = Path(__file__).resolve().parent
ORIGEN = DIR / "voz_empalmada.wav"
DESTINO = DIR / "composicion" / "voz_limpia.wav"

LIMPIEZA = ",".join([
    # Mono FIRST, inside the chain. With `-ac 1` the down-mix happens after the filters,
    # so the loudness was measured on stereo (+3 dB) and the gain came out 3 dB short.
    "aformat=channel_layouts=mono",
    "highpass=f=80",
    "afftdn=nr=20:nf=-70",
    "agate=threshold=0.003:ratio=4:attack=5:release=150",
])

OBJETIVO_LUFS = -19.0
TECHO_DB = -1.5


def medir() -> float:
    """First pass: integrated loudness (LUFS) of the cleaned voice."""
    salida = subprocess.run(
        [
            "ffmpeg", "-hide_banner", "-nostats", "-i", str(ORIGEN),
            "-af", f"{LIMPIEZA},ebur128", "-f", "null", "-",
        ],
        check=True, capture_output=True, text=True,
    ).stderr
    # The summary at the end carries the last "I:" line.
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", salida)[-1])


def main() -> None:
    ganancia = OBJETIVO_LUFS - medir()
    techo = 10 ** (TECHO_DB / 20)
    subprocess.run(
        [
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
            "-i", str(ORIGEN),
            "-af", f"{LIMPIEZA},volume={ganancia:.2f}dB,alimiter=limit={techo:.4f}:level=disabled",
            "-ar", "48000",
            str(DESTINO),
        ],
        check=True,
    )
    print(f"{ORIGEN.name} -> {DESTINO.relative_to(DIR)}  (gain {ganancia:+.1f} dB)")


if __name__ == "__main__":
    main()
