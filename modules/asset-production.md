# Asset production module

## Purpose
Plan and create the visual, audio, and graphic assets required by the storyboard.

## Asset types
Footage, generated video, still images, diagrams, charts, screen captures, narration, dialogue, music, sound effects, captions, titles, and brand assets.

## Per-asset record
- Unique asset ID and filename
- Scene(s) and time range
- Type, dimensions, frame rate, and duration
- Source or generation prompt
- Reference inputs and provenance
- License, consent, and disclosure status
- Continuity and edit notes including exact visual state at start/end

## Production rules
1. Use user-provided assets only for the scope the user authorized.
2. Avoid creating reference images that conflict with the intended motion, narration, or chronology. Do not reference a finished food state in a preparation scene unless the user deliberately wants that reveal.
3. Keep recurring characters and products consistent through approved references and fixed descriptions. For the user's latest recipe Flow direction, use the avatar reference as identity anchor only; do not add food reference imagery unless requested.
4. Generate only assets that the edit actually needs.
5. Verify that downloaded or generated assets are complete and compatible before editing.
6. Never imply an asset was generated, downloaded, or licensed if it was not.
7. Match every visual action to the exact narration beat; ensure scene transitions begin from the previous clip's end-state and retain props, ingredient stages, face, wardrobe, framing, and lighting.

## Provider neutrality
Choose providers according to output quality, availability, cost, commercial rights, export format, and device compatibility. Keep prompts and manifests portable so assets can be replaced without rebuilding the entire workflow. For Flow-specific prompt rules, see `modules/google-flow-prompting.md`.
