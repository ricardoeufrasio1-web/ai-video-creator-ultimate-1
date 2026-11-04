# Render Preflight

Checks metadata exported by FFprobe. This is a lightweight structural check; it does not render video, decode every frame, listen to audio, or prove visual/audio quality.

## Requirements

- Node.js 22+
- An FFprobe JSON file generated from the actual rendered output

## Generate metadata

```bash
ffprobe -v error -show_format -show_streams -of json output.mp4 > output.ffprobe.json
```

## Run

```bash
node tools/render-preflight/check-render.mjs output.ffprobe.json --expect-width 1080 --expect-height 1920 --expect-fps 30 --require-audio
```

Optional flags:
- `--expect-duration 30` checks duration in seconds (tolerance: 0.5 seconds).
- `--require-audio` requires at least one audio stream.
- `--expect-width N`, `--expect-height N`, and `--expect-fps N` compare expected video properties.

The checker reports errors and warnings and exits non-zero when errors are found. Missing expectations are not guessed. Inspect the full render manually after preflight.
