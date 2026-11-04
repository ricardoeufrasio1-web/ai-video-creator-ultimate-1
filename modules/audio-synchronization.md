# Audio synchronization

## Goal
Coordinate narration, dialogue, music, and sound effects with the visual timeline while preserving intelligibility and intentional pacing.

## Cue-sheet model
Every audio cue should have a stable ID, asset ID/path, track role, start time, source in/out (when trimming), timeline duration, gain target, fade in/out, and sync note. Use seconds for editorial readability and convert all timeline boundaries to integer frames using the project FPS.

## Narration
- Use phrase-level cues rather than one undifferentiated block when action must match speech.
- Preserve supplied narration verbatim when requested.
- Estimate duration from the actual recording, not only word count.
- Leave natural pauses; do not accelerate speech beyond intelligibility to force a fit.
- Align the visual action to the phrase that describes it, not merely to scene boundaries.

## Music and effects
- Keep music subordinate to speech and important sound effects.
- Use fades at intentional boundaries; avoid abrupt cuts unless stylistically deliberate.
- Duck music under dialogue when needed, and document the automation curve.
- Check peaks, clipping, phase issues, channel layout, and loudness against the target platform's current guidance.
- Confirm music and sound-effect licenses, including synchronization and commercial-use rights.

## Validation
Check missing files, negative starts, invalid source ranges, zero/negative durations, cues beyond composition end, duplicate IDs, and unexpected overlaps on exclusive tracks. Intentional overlaps must be explicit. Listen to the rendered mix; metadata validation cannot judge sound quality.

## Deliverables
Provide a cue sheet, mix notes, and separate stems when requested. Do not claim that audio is synchronized until the final rendered output has been reviewed.
