---
name: ai-video-creator-ultimate
description: Universal AI video production workflow for research, scripting, storyboarding, asset planning, editing, quality assurance, rendering, and publishing across niches and formats. Uses HyperFrames as the primary editing/rendering workflow when available.
---

# AI Video Creator Ultimate

A modular, tool-aware workflow for producing complete videos from an idea, brief, article, script, product, or source assets. Works across educational, documentary, marketing, recipe, entertainment, news, storytelling, tutorial, and other niches.

## Core principles

- Start by identifying the audience, purpose, platform, format, duration, language, tone, and desired outcome.
- Preserve user-provided facts, wording, scripts, brand constraints, and source material unless asked to revise them.
- Research factual topics and distinguish verified facts, uncertainty, opinion, and creative reconstruction.
- Design for clarity, pacing, retention, accessibility, and audience value; never promise virality or guaranteed performance.
- Maintain continuity across scenes: subjects, wardrobe, props, locations, lighting, screen direction, and timeline.
- Respect copyright, licenses, privacy, consent, platform rules, and disclosure requirements.
- Be transparent about which assets were generated, which tools were used, and whether a video was actually rendered.
- Prefer free and open-source tools when practical, but never describe a service as unlimited or free unless its current terms support that claim.

## Workflow

1. **Intake** — clarify the brief and identify missing essential information. Do not ask for details that can be safely defaulted.
2. **Research** — for factual or current topics, gather reliable sources, verify claims, and retain source notes.
3. **Creative strategy** — define the core promise, audience insight, format, hook, narrative arc, and call to action where appropriate.
4. **Script** — write narration/dialogue and estimate duration at a realistic speaking pace. Keep user-supplied wording unchanged when requested.
5. **Storyboard** — divide the video into scenes/shots with timestamps, visual action, framing, camera movement, audio, transitions, and continuity notes.
6. **Asset plan** — specify required footage, generated images/video, voice, music, sound effects, graphics, and reference assets. Track rights and provenance.
7. **Timeline** — select one FPS, derive frame boundaries, coordinate tracks and transitions, and synchronize narration and visual action.
8. **Production and edit** — assemble media, timing, animation, typography, captions, transitions, and audio mix using available tools.
9. **Quality assurance** — inspect factual accuracy, timing, continuity, spelling, audio clarity, visual artifacts, safe areas, aspect ratio, and export settings.
10. **Delivery** — provide the rendered file only if rendering actually succeeded. Otherwise provide the editable project, assets, and exact render instructions. Include a publishing pack when useful.

## Editing and rendering priority

Use **HyperFrames** as the primary composition and deterministic rendering workflow when the environment supports it. Consult its current upstream documentation before installation or relying on specific CLI commands. HyperFrames generally uses HTML/CSS/JavaScript compositions and a browser/FFmpeg rendering pipeline; check the installed version and requirements rather than assuming commands or dependencies.

Use FFmpeg for media inspection, conversion, trimming, audio processing, and final encoding when available. Remotion may be used as an optional React-based alternative when it fits the project and its license and dependencies have been checked. Other editing systems are adapters, not mandatory dependencies.

## Project generation

For a simple text-only title-card sequence, use `tools/project-generator/generate.mjs` with the schema in `docs/project-schema.md`. The generator creates an HTML composition and copies the source JSON; it does not generate media assets or render MP4. Use `modules/timeline-orchestration.md` for full timeline planning and `modules/automation.md` for repeatable pipelines. Never imply that generated project files have been rendered.

## Runtime checks

- Check Node.js and package-manager availability before running a JavaScript-based renderer.
- Check FFmpeg availability before promising an MP4 export.
- Check browser/runtime and media dependencies required by the chosen renderer.
- Avoid network-dependent assets during deterministic rendering; download and verify assets before render.
- Avoid nondeterministic expressions such as unseeded randomness or wall-clock time in frame-based compositions.
- If no compatible runtime is available (for example, the user is working only on a phone), create a portable project and clear setup instructions instead of claiming to have rendered a video.

## Output options

Depending on the request and available tools, deliver:
- creative brief and research/source notes;
- script and timed storyboard;
- scene-by-scene generation prompts;
- asset manifest and continuity guide;
- editable HTML/HyperFrames or other project files;
- rendered MP4 and export settings, only after successful render;
- SRT/VTT captions when requested or useful;
- thumbnail concept, title, description, social caption, tags, and credits.

## Universal format support

Adapt the plan to vertical 9:16, square 1:1, landscape 16:9, or other requested formats; short-form or long-form duration; voiceover, presenter, dialogue, ASMR, or text-led formats. Do not impose a platform-specific workflow unless the user asks for it.

## Specialist modules

Load only the relevant specialist modules for the task:

- `modules/research.md` — evidence gathering and fact-checking.
- `modules/scriptwriting.md` — hooks, narration, dialogue, pacing, and CTA.
- `modules/creative-direction.md` — storyboard, camera, lighting, and continuity.
- `modules/asset-production.md` — image, video, voice, audio, and graphics assets.
- `modules/timeline-orchestration.md` — FPS, frames, tracks, transitions, and continuity.
- `modules/media-management.md` — asset provenance, folder structure, normalization, and rights checks.
- `modules/audio-synchronization.md` — cue sheets, narration alignment, music, and effects.
- `modules/automation.md` — project generation, validation, repeatability, and errors.
- `modules/editing-hyperframes.md` — composition and rendering with HyperFrames.
- `modules/audio.md` — narration, music, effects, and mixing.
- `modules/captions-accessibility.md` — SRT/VTT and accessible presentation.
- `modules/quality-assurance.md` — pre-delivery inspection.
- `modules/publishing.md` — metadata, captions, credits, and handoff.

Select modules according to the user's request, available tools, and production stage. The core workflow remains usable when a module or external tool is unavailable.

## Project assets and render pipeline

- Use `docs/render-pipeline.md` for the complete preflight-to-delivery process.
- Use `docs/project-schema.md` for the starter JSON structure.
- Use `templates/asset-manifest.csv` to track source, rights, dimensions, duration, and continuity for every asset.
- Use `tools/asset-preflight/check.mjs` with a project JSON manifest to verify local file paths and flag missing rights metadata; see `examples/assets/manifest.example.json`.
- Use `tools/timeline-validator/validate.mjs` to check scene timing, frame alignment, asset IDs, and audio cue ranges; see `examples/timelines/short-form.json`.
- Use `examples/hyperframes-basic/` as an original minimal composition and generator input.
- Use the current HyperFrames CLI diagnostics, lint, check, snapshot, preview, and render commands as documented upstream. Confirm exact flags with the installed CLI.

## Reference projects and licensing

Treat external repositories and tools as technical references, not automatically reusable code. Before copying or redistributing code, verify the exact version, license, dependency licenses, attribution requirements, and commercial-use restrictions. Keep third-party notices where required. The license for this skill covers only original files in this repository and does not relicense external tools, models, media, fonts, or APIs.
