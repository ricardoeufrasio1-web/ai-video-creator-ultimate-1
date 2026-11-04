# AI Video Creator Ultimate

A universal, modular skill for planning and producing videos across niches, platforms, languages, and formats — from research and scripting to storyboarding, asset planning, editing, quality assurance, and publishing.

## What it does

- Turns an idea, brief, article, product, script, or source assets into a production plan.
- Supports educational, documentary, marketing, recipes, entertainment, news, storytelling, tutorial, and other formats.
- Creates timed scripts, storyboards, shot lists, scene prompts, continuity notes, and asset manifests.
- Uses **HyperFrames as the preferred editing/rendering workflow** when the environment supports it.
- Includes a Node.js starter generator for text-based HyperFrames compositions.
- Includes an asset preflight checker for local media paths and rights metadata.
- Uses FFmpeg for media operations when available; treats Remotion and other systems as optional adapters.
- Produces a publishing pack: titles, descriptions, captions, thumbnails concepts, credits, and source notes.

## Quick start

1. Read [SKILL.md](SKILL.md).
2. Define the audience, goal, platform, format, duration, language, tone, and any required CTA.
3. Follow the production workflow in [docs/workflow.md](docs/workflow.md).
4. Use the brief and storyboard templates in [templates/](templates/).
5. To generate a starter composition, use [tools/project-generator](tools/project-generator/README.md) with [the example project JSON](examples/hyperframes-basic/project.json).
6. If rendering with HyperFrames, follow [docs/hyperframes-workflow.md](docs/hyperframes-workflow.md) and check upstream documentation for current installation details.

## Preferred editing engine: HyperFrames

HyperFrames is the primary composition/rendering reference for this project. It supports HTML/CSS/JavaScript-based video compositions and a deterministic frame-oriented rendering pipeline. It is **not bundled** in this repository. Install it separately according to its official documentation and review its current license, dependencies, and runtime requirements.

Typical environment requirements may include Node.js 22+, FFmpeg, and a compatible browser/runtime. Exact requirements can change by version and operating system. Do not assume that a phone-only environment can run the full renderer.

## Project generator

The starter generator uses Node.js built-ins and accepts a small text-only JSON schema. It creates an `index.html` composition and preserves the source JSON. It does not generate images, video, voice, or music, and it does not render MP4. See [project schema](docs/project-schema.md) and [generator guide](tools/project-generator/README.md). Use [asset preflight](tools/asset-preflight/README.md) to check media paths and rights metadata before editing.

## Requirements and limitations

- This repository contains a skill and production tooling, not a hosted video-generation service.
- Image, video, voice, music, and model providers may charge fees, impose quotas, or restrict commercial use.
- Free/open-source tools are preferred where practical, but unlimited free generation is never guaranteed.
- A rendered MP4 must only be claimed when an actual render has completed and passed basic checks.
- When rendering is unavailable, deliver an editable project, assets, and clear setup/render instructions.

## Repository map

- `SKILL.md` — main skill instructions.
- `docs/architecture.md` — modular system architecture.
- `docs/workflow.md` — end-to-end production workflow.
- `docs/hyperframes-workflow.md` — HyperFrames-first editing and rendering.
- `docs/render-pipeline.md` — production pipeline from brief to validated export.
- `docs/project-schema.md` — starter JSON project format.
- `tools/project-generator/` — Node.js project generator.
- `tools/asset-preflight/` — local media manifest checker.
- `examples/assets/` — example asset manifest.
- `examples/hyperframes-basic/` — HTML composition and JSON example.
- `templates/asset-manifest.csv` — reusable asset tracking sheet.
- `docs/providers.md` — provider-neutral asset strategy.
- `docs/licensing.md` — licensing and rights checklist.
- `templates/` — reusable creative brief and storyboard templates.
- `modules/research.md` — research and fact-checking.
- `modules/scriptwriting.md` — scripts, hooks, pacing, and CTA.
- `modules/creative-direction.md` — storyboard, camera, lighting, and continuity.
- `modules/asset-production.md` — asset planning and production.
- `modules/timeline-orchestration.md` — frame-accurate timeline planning.
- `modules/media-management.md` — asset organization, provenance, and rights preflight.
- `modules/automation.md` — repeatable generation and validation.
- `modules/editing-hyperframes.md` — HyperFrames-first editing.
- `modules/audio.md` — narration, music, and sound design.
- `modules/captions-accessibility.md` — caption timing and accessibility.
- `modules/quality-assurance.md` — pre-delivery inspection.
- `modules/publishing.md` — publishing metadata and delivery.
- `THIRD_PARTY_NOTICES.md` — reference projects and attribution/licensing review notes.

## License

The repository's original documentation and skill files are licensed under MIT; see [LICENSE](LICENSE). This license applies only to original files in this repository. It does not change the licenses or terms of HyperFrames, FFmpeg, Remotion, other third-party software, models, APIs, fonts, music, footage, or generated assets.
