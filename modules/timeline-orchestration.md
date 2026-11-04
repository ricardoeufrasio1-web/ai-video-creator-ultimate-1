# Timeline orchestration

## Purpose
Convert a storyboard into a deterministic, frame-based timeline. This module is renderer-neutral; the HyperFrames adapter maps the plan to timed HTML clips and a paused GSAP timeline.

## Timebase
- Choose one project frame rate (FPS) and keep it for the whole composition.
- Store editorial decisions in seconds for readability, but derive integer frame positions: `frame = round(seconds * fps)`.
- Derive render duration from frames, not repeated floating-point additions.
- Snap scene boundaries to frames. Record any intentional sub-frame source timing separately.
- Never silently change FPS after timing narration, music, or transitions.

## Scene model
Each scene should define a stable ID, start frame/time, duration, track/layer, visual description, audio cues, transition in/out, and continuity notes. Optional asset references must resolve through the asset manifest. Reject negative durations, duplicate IDs, invalid references, and accidental gaps/overlaps when the brief requires a continuous sequence.

## Transitions and overlap
- A cut has no overlap.
- A dissolve or motion transition needs explicit overlap duration and both source ranges.
- Total composition duration is the maximum end frame across all tracks.
- Do not shorten narration or source footage implicitly to make a transition fit.
- For short-form content, prioritize readable action and intelligible speech over decorative transitions.

## Continuity
Track subject appearance, wardrobe, props, set, lighting, camera axis, screen direction, object state, and audio ambience. Every scene prompt should state what carries over from the previous scene and the exact state at its start. Flag continuity breaks for review rather than inventing missing details.

## Narration synchronization
Build a phrase-level cue sheet with in/out times. Align visible actions to the spoken phrase; leave enough time for the action to complete. Preserve user-supplied narration verbatim when requested. Do not auto-generate captions if the user explicitly requests no on-screen text.

## Validation
1. Convert all scene boundaries to frames.
2. Check IDs, duration, track, asset references, overlaps, and composition end.
3. Check voice/music/SFX ranges against the composition.
4. Generate a timing report with warnings and blocking errors.
5. Preview representative frames around every cut and transition.

## Deliverables
Provide the timeline data, timing report, continuity notes, and any renderer-specific project. A plan or generated HTML is not a rendered MP4; report rendering status truthfully.
