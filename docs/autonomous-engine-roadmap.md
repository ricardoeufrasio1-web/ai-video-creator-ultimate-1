# Autonomous engine: implementation and acceptance roadmap

## Product definition
The default production path must not require a remote image/video generation provider, API key, paid credit, external editing website or social account. It should create original visual material procedurally and assemble it locally when the host runtime permits.

"Standalone" means no remote media-generation service. It does not mean no execution environment: a compatible agent host or local runtime is still required to run code and export files.

## Current implementation snapshot (2026-11-04)

Implemented prototypes: an extensible style/editing catalog; a self-contained SVG/HTML scene generator; an FFmpeg renderer for text, rectangles, lines and progress bars; optional local voiceover/music mixing; basic zoom/pan camera moves; cross-scene transitions; and CI smoke tests for generated MP4 metadata. The procedural renderer is still deliberately limited and does not yet implement the full visual element library, all preview effects, speech synthesis, captions, rich motion-graphics components, or end-to-end long-form editing. Treat these as prototypes until the latest CI run passes and the output receives human visual/audio review.

## Milestones
1. **Creative system** — universal style taxonomy, style bible, genre adaptation, storyboard and beat map.
2. **Procedural graphics** — reusable SVG/Canvas/HTML scene components, title systems, diagrams, charts, backgrounds, icons and original vector characters.
3. **Animation engine** — frame-based keyframes, easing, camera transforms, particles, parallax, masks and transitions.
4. **Timeline integration** — convert the portable timeline to a renderable composition with visuals, narration, music, SFX and captions.
5. **Audio path** — support user voice recordings and optional local TTS only when a licensed executable/model is installed; normalize, mix and synchronize.
6. **Renderer integration** — reproducible MP4 render from a clean checkout using documented, pinned dependencies.
7. **Viral editing presets** — hook/beat templates, dynamic pacing, punch-ins, match cuts, kinetic text, sound accents and loop endings.
8. **QA and packaging** — render fixtures, frame extraction, metadata checks, audio checks, sample MP4 artifact and portable Skill ZIP.
9. **Publishing handoff** — create titles, descriptions, thumbnails, captions and platform exports. Actual posting remains optional and requires platform authorization.

## Acceptance criteria
A milestone is complete only when:
- implementation files exist and are included in the Skill package;
- tests cover valid and invalid cases;
- CI or a reproducible host run passes;
- documentation matches actual behavior;
- generated outputs are inspected;
- no remote media generation provider is silently required.

## Style and format coverage
Support an extensible library rather than a finite "all styles" promise. Include live-action looks as creative references, 2D/3D animation, illustration, collage, motion graphics, infographic, documentary, UGC, product ads, recipes, education, storytelling, sports, news, tutorials, music visualizers and platform-native edits. If the procedural renderer cannot realize a requested photoreal style, state the gap and offer a faithful procedural interpretation or a user-footage route.

## Non-goals
- Bypassing host execution restrictions or subscription/compute limits.
- Claiming photorealistic generative footage without a model or source footage.
- Publishing without explicit user approval and authorized platform access.
- Bundling third-party code, models, fonts or music without license review.
