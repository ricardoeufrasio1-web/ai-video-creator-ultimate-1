# Procedural Scene Engine — first executable prototype

This dependency-free Node.js tool creates a self-contained HTML/SVG composition from JSON. It generates original vector shapes, typography, simple diagrams and basic entrance animation without calling remote image or video generation services.

## Run

Create a narrated MP4 from one JSON project in a single command (Node.js is not required for this render path; Python, FFmpeg, FFprobe and eSpeak NG must be installed):

```bash
python3 tools/procedural-scene-engine/run_pipeline.py examples/procedural-scenes/one-command-video.json --output ./output/final.mp4 --report ./output/qa-report.json
```

The pipeline optionally synthesizes narration locally, renders the video, probes the actual MP4 streams and writes a QA metadata report. `provider_calls: 0` means no remote media provider was called. It does not claim that automated metadata checks replace watching/listening to the final video.



```bash
node tools/procedural-scene-engine/generate.mjs examples/procedural-scenes/vertical-explainer.json ./output/vertical-explainer
```

Open the generated index.html in a modern browser to preview it. The output contains inline SVG, CSS and JavaScript; it makes no network requests.

To render the supported procedural shapes and text to MP4 using local FFmpeg:

```bash
python3 tools/procedural-scene-engine/render.py examples/procedural-scenes/render-fixture.json --output ./output/procedural.mp4
```

The MP4 renderer supports text, timed captions, rectangles, lines, circles, triangles, diamonds, stars and progress bars on generated color backgrounds. It also supports project-level crossfades (fade, dissolve, wipe, slide and circle variants), zoom/pan camera moves, staggered element reveals, and optional local audio files as project-level voiceover/music objects, with gain and start offset. For offline synthetic narration, the optional tts.py helper uses locally installed eSpeak NG (no network/API); for example: `python3 tools/procedural-scene-engine/tts.py "Olá, vamos começar!" --output ./output/voice.wav --voice pt-br`. The voice is synthetic and comparatively robotic, not a photorealistic AI voice. It requires FFmpeg with libx264 and drawtext support. No audio is synthesized; audio files must be supplied by the user.

## Supported elements

- text
- rect
- circle
- line
- bar

The SVG/HTML generator supports text, rectangles, circles, lines, progress bars, triangles, diamonds and stars. Set `theme.gradient` to `{ "from": "#101827", "to": "#68d5ff", "angle": 25 }` for a project-wide linear gradient, or set `gradient` on an individual scene to override it. Scenes also support duration, background, accent, accessible description, rise/slide/pop entrances, push/pull/pan/drift/shake camera presets, and fade/wipe/circle/zoom reveal transitions. Dimensions, FPS, gradient colors/angles, IDs, durations and element values are validated.

## Current limits

This is an initial procedural graphics/composition prototype, not the complete engine. The MP4 renderer currently renders text, rectangles, lines and progress bars on color backgrounds, with selectable cross-scene transitions, local audio mixing, staggered element reveals, and simple zoom/pan camera moves. It does not yet render arbitrary SVG paths, rigged characters, synthesize speech, generate realistic footage, import external fonts, or provide a full keyframe/timeline editor. More elaborate camera paths remain preview-only. It produces silent MP4 files unless local voiceover or music files are supplied. Speech synthesis is a separate optional local eSpeak NG step. Automated FFmpeg/FFprobe smoke tests verify the supported MP4 path, but every production still needs visual review.
