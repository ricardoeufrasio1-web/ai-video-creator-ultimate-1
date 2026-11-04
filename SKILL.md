---
name: ai-video-creator-ultimate
description: Universal AI video production workflow for research, scripting, storyboarding, asset planning, editing, quality assurance, rendering, and publishing across niches and formats. Uses HyperFrames as the primary editing/rendering workflow when available.
---

# AI Video Creator Ultimate

A modular, tool-aware workflow for producing complete videos from an idea, brief, article, script, product, or source assets across educational, documentary, marketing, recipe, entertainment, news, storytelling, tutorial, and other niches.

## Principles

- Identify audience, purpose, platform, format, duration, language, tone, and desired outcome.
- Preserve user-provided facts, wording, scripts, brand constraints, and source material unless asked to revise them.
- Research factual/current topics; distinguish verified facts, uncertainty, opinion, and creative reconstruction.
- Design for clarity, pacing, accessibility, and audience value; never promise virality or guaranteed performance.
- Maintain continuity across subjects, wardrobe, props, locations, lighting, screen direction, and timeline.
- Respect copyright, licenses, privacy, consent, platform rules, and disclosure requirements.
- Be transparent about assets, tools, checks performed, and whether a video was actually rendered.
- Prefer free/open-source tools when practical; never describe a service as unlimited/free unless current terms support it.

## End-to-end workflow

1. **Intake:** clarify essential brief details; safely default the rest.
2. **Research:** verify factual claims and retain source notes.
3. **Creative strategy:** define audience insight, format, hook, narrative arc, and CTA where appropriate.
4. **Script:** write narration/dialogue and estimate realistic duration. Preserve exact user wording when requested.
5. **Storyboard:** specify timestamps, action, framing, camera movement, audio, transitions, and continuity.
6. **Asset plan:** list footage, generated media, voice, music, effects, graphics, references, rights, and provenance.
7. **Timeline:** select FPS, derive frame boundaries, coordinate tracks, transitions, and audio cues.
8. **Production/edit:** assemble media, motion, typography, captions, transitions, and mix with available tools.
9. **Quality assurance:** inspect facts, timing, continuity, spelling, audio, artifacts, safe areas, aspect ratio, and export settings.
10. **Delivery:** provide MP4 only if an actual render succeeded; otherwise provide editable source and exact render instructions. Include a publishing pack when useful.

Use [docs/production-checklist.md](docs/production-checklist.md) as the handoff gate.

## Editing and rendering priority

Use **HyperFrames** as the primary composition and deterministic rendering workflow when supported. Consult current upstream docs before installation or relying on CLI syntax. Use FFmpeg for media inspection, conversion, trimming, audio processing, and encoding when available. Remotion and other systems are optional adapters, not mandatory dependencies.

## Project generation and validation

- For text-only title-card sequences, use `tools/project-generator/generate.mjs` and `docs/project-schema.md`. It creates HTML and copies JSON; it does not generate media or render MP4.
- Use `tools/asset-preflight/check.mjs` for local asset paths and rights-metadata warnings.
- Use `tools/timeline-validator/validate.mjs` for scene timing, frame alignment, asset IDs, and audio cue ranges.
- After a real render, export metadata using FFprobe and use `tools/render-preflight/check-render.mjs` to check streams, dimensions, FPS, and duration.
- These checkers are structural diagnostics only. They do not prove rights, visual quality, audio quality, or synchronization.

## Runtime and render status

Check Node.js, FFmpeg, browser/runtime, and renderer dependencies before promising an export. If no compatible runtime is available (including phone-only workflows), prepare a portable project and setup instructions rather than claiming a render. Distinguish **generated**, **structurally checked**, **visually reviewed**, **audio reviewed**, and **approved**. Metadata-only checks are not visual/audio QA.

## Specialist modules

Load only what the task needs:

- Research and fact-checking: `modules/research.md`
- Scripts, hooks, pacing, CTA: `modules/scriptwriting.md`
- Storyboard, camera, lighting, continuity: `modules/creative-direction.md`
- Asset planning and production: `modules/asset-production.md`
- Timeline, FPS, tracks: `modules/timeline-orchestration.md`
- Motion and transitions: `modules/transitions-motion.md`
- Asset provenance and rights: `modules/media-management.md`
- Voice and TTS production: `modules/voice-production.md`
- Audio, mixing, and cue synchronization: `modules/audio.md`, `modules/audio-synchronization.md`
- Captions and accessibility: `modules/captions-accessibility.md`
- Automation and project generation: `modules/automation.md`
- HyperFrames editing: `modules/editing-hyperframes.md`
- QA and render validation: `modules/quality-assurance.md`, `modules/render-validation.md`
- Publishing and handoff: `modules/publishing.md`

## Universal formats and deliverables

Adapt to vertical 9:16, square 1:1, landscape 16:9, or other requested formats; short- or long-form duration; voiceover, presenter, dialogue, ASMR, or text-led formats. Depending on the task and available tools, deliver a brief, research notes, script, timed storyboard, generation prompts, asset manifest, continuity guide, editable project, verified MP4, captions, thumbnail concept, title, description, social copy, tags, and credits.

## Automation and troubleshooting

GitHub Actions validates JSON syntax, JavaScript syntax, the sample timeline, starter project generation, and sample render metadata. See [docs/testing.md](docs/testing.md). For common setup and production issues, see [docs/troubleshooting.md](docs/troubleshooting.md).

## Licensing and references

Treat external repositories and tools as technical references, not automatically reusable code. Before copying or redistributing code, verify exact version, license, dependency licenses, attribution, and commercial-use restrictions. The license for this skill covers only original files in this repository.
