"""
Extract the video's poster frame: the still the case page shows until the reader presses play.

    python video/portada.py

Reads the final render (video/composicion/renders/, not versioned) and writes video/portada.jpg,
which IS versioned: the site copies it with scripts/cases/sync_figures.py, and without the render
it could not be made again.

The frame is the end of scene 1: the full count, the question and the five orange needles. It is
the hook, so it invites pressing play, and it does not repeat the hero figure, which the page
shows right under the video.

Needs FFmpeg on PATH.
"""

from pathlib import Path
import subprocess

DIR = Path(__file__).resolve().parent
RENDER = DIR / "composicion" / "renders" / "steam-price-reception.mp4"
DESTINO = DIR / "portada.jpg"

SEGUNDO = 8.45   # s on the root timeline: scene 1 settled, scene 2 not yet in
ANCHO = 1280     # the page column is ~56rem; 1280 covers it at 1.5x


def main() -> None:
    subprocess.run(
        ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", f"{SEGUNDO}",
         "-i", str(RENDER), "-frames:v", "1", "-vf", f"scale={ANCHO}:-2", "-q:v", "3",
         str(DESTINO)],
        check=True,
    )
    print(f"{RENDER.name} @ {SEGUNDO} s -> {DESTINO.name} ({DESTINO.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
