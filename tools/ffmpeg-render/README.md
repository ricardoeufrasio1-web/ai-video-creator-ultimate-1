# FFmpeg renderer (experimental)

This command-line renderer assembles ordered local image/video scenes into MP4 and optionally mixes voiceover/music. It is a first real rendering path, not an AI media generator.

## Requirements
- Python 3.9+
- FFmpeg on PATH with libx264 and AAC support

## Project format
See examples/render/ffmpeg-render-fixture.json. Asset paths are relative to the JSON file and may not escape its directory. Each scene has an id, type (image or video), src, and duration in seconds. An optional project-level `transition` object supports `type: crossfade`, `duration: 0.5`, and optional `effect` (default `fade`) to transition every adjacent scene; supported effects are `fade`, `dissolve`, `wipeleft`, `wiperight`, `slideleft`, `slideright`, `circleopen`, and `circleclose`. Overlaps are subtracted from the final timeline duration. Omit it for hard cuts. Optional per-scene `motion` supports `none` (default), `zoom_in`, and `zoom_out` for a subtle animated camera zoom. Optional per-scene `fade_in` and `fade_out` values (seconds) fade that clip from/to black; both default to 0 and must not exceed the scene duration. Optional voiceover/music paths can use `voiceover_offset` and `music_offset` (seconds, default 0). When both are supplied, music is mixed at reduced volume under voice. Optional `captions` points to an SRT file; it is muxed as a selectable MP4 subtitle track (not burned into the picture). Optional `audio_normalization` can be `true` (use defaults) or an object with `integrated_lufs` (-36 to -5, default -16), `true_peak_db` (-9 to 0, default -1.5), and `loudness_range` (1 to 20, default 11); it applies FFmpeg loudnorm after mixing. Optional `audio_cues` is an array of timeline-positioned clips with unique `id`, local `src`, `role` (`narration`, `dialogue`, `music`, `sfx`, or `ambience`), `start`, `duration`, `gain` (linear 0–4), `fade_in`, and `fade_out` in seconds. Each cue is trimmed, positioned, and mixed into the output. Cue ranges must fit within the total scene duration.

## Run
    python3 tools/ffmpeg-render/create_fixture.py
    python3 tools/ffmpeg-render/render.py examples/render/ffmpeg-render-fixture.json --output /tmp/demo.mp4
    ffprobe -v error -show_streams -show_format -of json /tmp/demo.mp4

## Validation tests

Run the renderer input-validation tests with:

    python3 tools/ffmpeg-render/test_validation.py

These tests cover empty scene lists, path traversal attempts, missing assets, and unsupported scene types. The CI workflow runs them before rendering a two-scene MP4 fixture with a real crossfade and checks the resulting 2.5-second duration, positioned audio, subtitle stream, and enabled loudness normalization.

## Current limitations
- Selectable crossfade-style transitions are supported between every adjacent scene when enabled globally; per-boundary transition selection, directional camera pans, animated text, and motion graphics are not implemented. SRT captions are selectable subtitle tracks, not burned-in captions.
- Audio cues can be positioned and faded on the timeline; automatic dialogue ducking is not implemented. Optional post-mix loudness normalization is available, but final listening checks are still required.
- Video scenes loop if shorter than the declared duration.
- Local files only; no provider API calls, downloads, cloud jobs, or social publishing.
- Output is checked for existence and non-zero size; use FFprobe and human visual/audio review for delivery QA.
- Does not yet convert the full portable timeline schema or HyperFrames compositions.
