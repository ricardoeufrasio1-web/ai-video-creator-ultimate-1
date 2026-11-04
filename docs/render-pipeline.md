# Production render pipeline

This document defines the recommended stages for turning a creative brief into a validated deliverable. It is renderer-aware but not tied to a single AI asset provider.

## Stage 1 — Normalize the brief

Create a machine-readable project brief with:
- project ID and title;
- language and locale;
- target platform and aspect ratio;
- frame rate, resolution, and target duration;
- scene list and narration;
- brand, rights, budget, and delivery constraints.

Do not silently change supplied narration or factual claims.

## Stage 2 — Build the asset manifest

Every referenced asset must have a stable ID and path. Track type, scene, duration, dimensions, source/provider, license/consent, and notes. Validate that each required file exists before preview/render.

## Stage 3 — Build the timeline

Convert scene timing into one project timebase. For frame-based work, use a single FPS value and consistent rounding rules. Define explicit start/end frames, media ranges, track order, transitions, and audio fades.

## Stage 4 — Compose

For HyperFrames, generate an HTML composition using the installed version's documented structure. Use timed clip attributes and a seekable animation timeline where required. Keep reusable visual components separate from project-specific content.

## Stage 5 — Preflight

- Check Node.js and FFmpeg availability.
- Run HyperFrames diagnostics.
- Confirm all local asset paths resolve.
- Run the composition linter and browser/layout checks available in the installed CLI.
- Capture review frames at scene boundaries when supported.
- Stop if blocking errors remain.

## Stage 6 — Preview and render

Preview the entire composition. Render to the requested format and output path using the current CLI documentation. Use Docker only when available and useful for reproducibility.

## Stage 7 — Validate the output

Check:
- output file exists and is non-empty;
- duration is within the expected tolerance;
- dimensions and frame rate match the brief;
- audio streams are present when expected;
- first, middle, last, and scene-boundary frames are visually correct;
- no black gaps, frozen frames, missing media, clipping, or abrupt audio cuts.

Use FFprobe/FFmpeg when available. A successful CLI exit alone is not a substitute for inspecting the output.

## Stage 8 — Package delivery

Include the final video, editable source, asset manifest, captions when requested, source/credit notes, and export metadata. Keep temporary files out of the final package.

## Failure behavior

Report the exact failed stage and useful error output. Do not claim a render succeeded if it did not. If the runtime is unavailable, stop at a portable project and setup instructions.


## Experimental local FFmpeg adapter

The repository includes `tools/ffmpeg-render/render.py` as a first executable MP4 path. It supports ordered image/video scenes, hard cuts, normalized dimensions/FPS, and optional voiceover/music starting at time zero. See its README for limitations. The CI job creates synthetic local media, renders a real MP4 with FFmpeg, and checks the resulting streams using FFprobe. This is a renderer smoke test, not a test of AI media generation, full timeline conversion, or human perceptual QA.
