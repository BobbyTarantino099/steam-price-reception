# Video: a 68-second trailer of the case

A narrated, animated walk through the case in five scenes: the question, the broken data, the
finding, the objection, and an invitation to read the case. It is built from the case's own
files: the real rows of the raw CSV, the analysis tables and the cleaned dataset. No number in
it is typed by hand.

**Watch it:** [on YouTube](https://youtu.be/zHiZ3W4nJxE) (unlisted: reachable from this link and
the case page, not from search).
**Script:** [`guion.md`](guion.md). Read its *Notes on the claims* before changing a sentence.

The video is rendered with [HyperFrames](https://github.com/heygen-com/hyperframes) (HeyGen,
Apache 2.0): each scene is an HTML page animated with GSAP, captured frame by frame in headless
Chrome and encoded with FFmpeg.

## What is here, and what is not

```
video/
├── guion.md              # the script: narration, visuals, and why each claim holds
├── empalmar_voz.py       # 1. splices re-recorded sentences into the voice take
├── limpiar_voz.py        # 2. denoises the voice and sets its loudness
├── datos_video.py        # 3. pulls every number on screen from the case's files
├── mezclar_audio.py      # 4. lays the music bed under the voice
└── composicion/          # the HyperFrames project
    ├── index.html        # mounts the five scenes on one timeline, plays the mix
    ├── compositions/     # s1.html … s5.html, one per scene, each with its own clock
    ├── assets/datos.js   # written by datos_video.py — never edit by hand
    ├── assets/fonts/     # Inter, the same type as the figures (OFL, see LICENCIA.md)
    └── package.json      # pins the HyperFrames version: renders repeat over time
```

**Not versioned** (see `.gitignore`):

- **The voice recordings** (`voz*.wav`) and everything derived from them: the cleaned voice, the
  mix and the transcript. They are personal; the published video is the public form of them.
  Without them the video cannot be regenerated from this repository. That is the cost of
  keeping them private, and it was chosen on purpose.
- **The music** (`musica_*.mp3`). Its licence allows using it inside a video, not
  redistributing the file on its own. This is the same reason the raw Steam CSV is not stored
  here.
- **Renders** (`composicion/renders/`) are outputs.
- **`composicion/CLAUDE.md` and `AGENTS.md`**, the generic agent instructions that
  `hyperframes init` writes into every project. Run the same command in an empty folder to get
  them again.

## Rebuild

Requirements: Python 3.10+ with pandas, Node 22+, FFmpeg on `PATH`. The HyperFrames CLI runs
through `npx` at the version pinned in `composicion/package.json`. Transcription uses its local
Parakeet model (`npx hyperframes models install parakeet`, ~640 MB once).

From the case root, in this order. Each step reads the previous one's output:

```bash
python video/empalmar_voz.py     # voz.wav + fragments          -> voz_empalmada.wav
python video/limpiar_voz.py      # -> composicion/voz_limpia.wav (-19 LUFS, mono)
python video/datos_video.py      # raw CSV + tables + cleaned data -> composicion/assets/datos.js
python video/mezclar_audio.py    # voice + music                 -> composicion/mezcla.wav (-16 LUFS)

cd video/composicion
npx hyperframes transcribe voz_limpia.wav --engine parakeet --language en   # word timings
npm run check                    # lint, layout, motion and contrast: must pass
npm run render                   # -> renders/
```

`datos_video.py` needs the raw CSV in `datos/crudos/` (see the main README) and `datos/limpios/`,
which `notebooks/procesar.py` regenerates. It stops with an assert if the analysis base it
mirrors ever changes (8,998 games, median age 6 years).

Turn telemetry off once with `npx hyperframes telemetry disable`. Do not use `npm run publish`:
it uploads the project to HeyGen.

## Making the video of another case

The process is meant to be repeated. What carries over unchanged, and what each case rewrites:

| Piece | Reuse | Per case |
|---|---|---|
| `limpiar_voz.py` | as is | only if the recording room changes (noise floor) |
| `mezclar_audio.py` | as is | `MUSICA` and `DURACION` |
| `empalmar_voz.py` | the mechanism | the list of fragments and their cut points, or nothing if the take is clean |
| `datos_video.py` | the rule: every number from the case's files | everything else |
| `composicion/index.html` | the skeleton, the palette tokens, the signature | the scene list and its cuts |
| `compositions/s*.html` | the patterns: word-by-word text, counters, data-driven rows | the scenes |
| `guion.md` | the format | the content |

The order that worked, and why:

1. **Write the script and check every claim against the data before recording.** In this case,
   two sentences of the first take overstated what the analysis shows (see `guion.md`). Both were
   found only when the data behind each scene was recomputed. Each one cost a re-recording and a
   splice. Checking first is cheaper.
2. **Record the whole take**, with the same microphone, room and distance throughout, and a
   second of silence at both ends. Synthetic voices (`hyperframes tts`, Kokoro) were tried and
   dropped: too robotic, and they skip the pauses the script relies on.
3. **Transcribe** to get word timings. The transcript's *text* is unreliable (it misheard "fund"
   as "fan", "old" as "all"). Only its *times* are used, and captions must come from the script.
4. **Build one scene at a time** and review it before the next one. Scene times are the
   transcript time minus the scene's start on the root.
5. **Music last**, once the cut is final. The ducking follows the voice, so the bed adapts to
   whatever was recorded.

## Music

The track comes from [Pixabay Music](https://pixabay.com/music/), filtered for no-copyright
tracks and downloaded without an account, so its page link was not kept. Pixabay's licence allows
use inside a video without attribution, but some of its tracks are registered with YouTube
Content ID. If the upload gets a claim, the way out is the track's licence on its Pixabay page.
For the next case, **save the track's page link when you download it**.

## Pilot evaluation (2026-10-11)

The video started as an exploratory pilot, with four questions to decide whether to make one per
case:

- **Does it invite reading the case?** The two people who watched it said it does. Two is a
  small sample, but it points the right way.
- **Does the motion explain or just decorate?** Scenes 2 to 4 animate what the narration
  argues: the misaligned columns, the inflation adjustment, the cheap band never winning, the
  age split. That is more than the static figures can do.
- **Can it be regenerated with commands?** Yes, with the chain above. It needs the private voice
  recordings and the music, as stated.
- **What did it cost?** Two working sessions, including two re-recordings and the setup that
  only happens once: the transcription model, the voice cleaning and the mixing scripts.
