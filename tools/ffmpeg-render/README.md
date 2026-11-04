# FFmpeg renderer (experimental)

This command-line renderer assembles ordered local image/video scenes into MP4 and optionally mixes voiceover/music. It is a first real rendering path, not an AI media generator.

## Requirements
- Python 3.9+
- FFmpeg on PATH with libx264 and AAC support

## Project format
See examples/render/ffmpeg-render-fixture.json. Asset paths are relative to the JSON file and may not escape its directory. Each scene has an id, type (image or video), src, and duration in seconds. An optional project-level `transition` object supports `type: crossfade` and `duration: 0.5` to dissolve every adjacent scene; overlaps are subtracted from the final timeline duration. Omit it for hard cuts. Optional per-scene `fade_in` and `fade_out` values (seconds) fade that clip from/to black; both default to 0 and must not exceed the scene duration. Optional voiceover/music paths can use `voiceover_offset` and `music_offset` (seconds, default 0). When both are supplied, music is mixed at reduced volume under voice. Optional `captions` points to an SRT file; it is muxed as a selectable MP4 subtitle track (not burned into the picture). Optional `audio_cues` is an array of timeline-positioned clips with unique `id`, local `src`, `role` (`narration`, `dialogue`, `music`, `sfx`, or `ambience`), `start`, `duration`, `gain` (linear 0–4), `fade_in`, and `fade_out` in seconds. Each cue is trimmed, positioned, and mixed into the output. Cue ranges must fit within the total scene duration.

## Run
    python3 tools/ffmpeg-render/create_fixture.py
    python3 tools/ffmpeg-render/render.py examples/render/ffmpeg-render-fixture.json --output /tmp/demo.mp4
    ffprobe -v error -show_streams -show_format -of json /tmp/demo.mp4

## Validation tests

Run the renderer input-validation tests with:

    python3 tools/ffmpeg-render/test_validation.py

These tests cover empty scene lists, path traversal attempts, missing assets, and unsupported scene types. The CI workflow runs them before rendering a two-scene MP4 fixture with a real crossfade and checks the resulting 2.5-second duration.

## Current limitations
- Crossfade transitions are supported between every adjacent scene when enabled globally; per-boundary transition selection, animated text, and motion graphics are not implemented. SRT captions are selectable subtitle tracks, not burned-in captions.
- Audio cues can be positioned and faded on the timeline; automatic dialogue ducking and loudness normalization are not implemented.
- Video scenes loop if shorter than the declared duration.
- Local files only; no provider API calls, downloads, cloud jobs, or social publishing.
- Output is checked for existence and non-zero size; use FFprobe and human visual/audio review for delivery QA.
- Does not yet convert the full portable timeline schema or HyperFrames compositions.
