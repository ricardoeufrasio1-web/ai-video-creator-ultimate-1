# Editing and rendering module — HyperFrames first

## Purpose
Assemble a complete, frame-accurate video using HyperFrames when the environment supports it.

## Preflight
- Confirm operating system and runtime access.
- Check Node.js version against current HyperFrames requirements.
- Check FFmpeg and browser/runtime availability.
- Confirm media codecs, frame rates, dimensions, and asset paths.
- Read current upstream documentation and license before installation.

## Timeline design
Represent each scene with explicit start/end frames, media sources, animation timing, transitions, and audio ranges. Maintain one authoritative project frame rate and calculate frame positions consistently.

## Composition
Use HTML/CSS/JavaScript compositions and the currently documented HyperFrames APIs. Keep reusable components for titles, captions, transitions, charts, lower thirds, and visual effects. Avoid hard-coding platform-specific assumptions into shared components.

## Render discipline
- Keep rendering deterministic.
- Preload local media; avoid runtime network requests.
- Avoid unseeded random values and wall-clock time in animation logic.
- Run available lint/validation and browser checks.
- Preview the full timeline, especially scene boundaries.
- Render with the installed version's documented command.
- Inspect the exported MP4 for duration, resolution, frame rate, audio, and visual errors.

## Alternatives
Use FFmpeg for media conversion and finishing tasks. Use Remotion only as an optional adapter when suitable and license-compliant. Do not require all renderers in one project.

## Honest fallback
If rendering cannot run, deliver the project source and exact instructions. Never claim an MP4 was rendered without verifying the output.
