# FFmpeg renderer (experimental)

This command-line renderer assembles ordered local image/video scenes into MP4 and optionally mixes voiceover/music. It is a first real rendering path, not an AI media generator.

## Requirements
- Python 3.9+
- FFmpeg on PATH with libx264 and AAC support

## Project format
See examples/render/ffmpeg-render-fixture.json. Asset paths are relative to the JSON file and may not escape its directory. Each scene has an id, type (image or video), src, and duration in seconds. Optional voiceover and music paths start at time zero. When both are supplied, music is mixed at reduced volume under voice.

## Run
    python3 tools/ffmpeg-render/create_fixture.py
    python3 tools/ffmpeg-render/render.py examples/render/ffmpeg-render-fixture.json --output /tmp/demo.mp4
    ffprobe -v error -show_streams -show_format -of json /tmp/demo.mp4

## Validation tests

Run the renderer input-validation tests with:

    python3 tools/ffmpeg-render/test_validation.py

These tests cover empty scene lists, path traversal attempts, missing assets, and unsupported scene types. The CI workflow runs them before rendering its MP4 fixture.

## Current limitations
- Hard cuts only; no transitions, animated text, captions, or motion graphics.
- Audio starts at time zero; no per-scene cue placement, ducking automation, or loudness normalization.
- Video scenes loop if shorter than the declared duration.
- Local files only; no provider API calls, downloads, cloud jobs, or social publishing.
- Output is checked for existence and non-zero size; use FFprobe and human visual/audio review for delivery QA.
- Does not yet convert the full portable timeline schema or HyperFrames compositions.
