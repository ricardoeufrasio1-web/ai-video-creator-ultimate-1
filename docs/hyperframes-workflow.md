# HyperFrames-first workflow

HyperFrames is the preferred editing/rendering reference for this skill. It is an external dependency and is not included in this repository.

## Before setup

1. Open the official [HyperFrames repository](https://github.com/heygen-com/hyperframes) and current documentation.
2. Confirm the current supported Node.js version, installation commands, FFmpeg requirements, browser/runtime requirements, and license.
3. Check the operating system and whether the user has a desktop or remote runtime. A mobile-only user may need a cloud/desktop environment.
4. Install only from trusted upstream sources and pin versions for reproducibility.

## Composition principles

- Build scenes as explicit HTML/CSS/JavaScript compositions.
- Use frame-based timing and seekable animation timelines.
- Keep media local and validated before rendering.
- Register animation timelines according to the installed HyperFrames version's documented API.
- Use deterministic values; avoid wall-clock time and unseeded randomness.
- Keep fonts, images, audio, and video paths stable and relative to the project where possible.

## Production sequence

1. Create or initialize a project using the current upstream instructions.
2. Add media and verify codecs, dimensions, frame rates, and durations.
3. Compose scenes and transitions with explicit start/end frames.
4. Run available lint, validation, or browser checks.
5. Preview the complete timeline and inspect scene boundaries.
6. Render using the current documented CLI/API.
7. Inspect the resulting MP4 with a media probe and visual playback.
8. Archive the source project, asset manifest, and export settings.

## Rendering reliability

Check that the render has the expected duration, frame rate, resolution, audio stream, and no missing frames/assets. For deterministic rendering, avoid runtime network fetches and unstable time/random sources.

## Fallback

If HyperFrames cannot run in the available environment, do not fake a render. Deliver the composition source, asset folder structure, and a clear set of steps for a compatible machine or remote runner.
