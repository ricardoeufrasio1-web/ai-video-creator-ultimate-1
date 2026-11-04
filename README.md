# AI Video Creator Ultimate

A universal, modular skill for planning and producing videos across niches, platforms, languages, and formats — from research and scripting to storyboarding, asset planning, editing, quality assurance, and publishing.

## What it does

- Turns an idea, brief, article, product, script, or source assets into a production plan.
- Supports educational, documentary, marketing, recipes, entertainment, news, storytelling, tutorial, and other formats.
- Creates timed scripts, storyboards, shot lists, scene prompts, continuity notes, and asset manifests.
- Uses **HyperFrames as the preferred editing/rendering workflow** when the environment supports it.
- Uses FFmpeg for media operations when available; treats Remotion and other systems as optional adapters.
- Produces a publishing pack: titles, descriptions, captions, thumbnails concepts, credits, and source notes.

## Quick start

1. Read [SKILL.md](SKILL.md).
2. Define the audience, goal, platform, format, duration, language, tone, and any required CTA.
3. Follow the production workflow in [docs/workflow.md](docs/workflow.md).
4. Use the brief and storyboard templates in [templates/](templates/).
5. If rendering with HyperFrames, follow [docs/hyperframes-workflow.md](docs/hyperframes-workflow.md) and check upstream documentation for current installation details.

## Preferred editing engine: HyperFrames

HyperFrames is the primary composition/rendering reference for this project. It supports HTML/CSS/JavaScript-based video compositions and a deterministic frame-oriented rendering pipeline. It is **not bundled** in this repository. Install it separately according to its official documentation and review its current license, dependencies, and runtime requirements.

Typical environment requirements may include Node.js 22+, FFmpeg, and a compatible browser/runtime. Exact requirements can change by version and operating system. Do not assume that a phone-only environment can run the full renderer.

## Requirements and limitations

- This repository contains a skill and production documentation, not a hosted video-generation service.
- Image, video, voice, music, and model providers may charge fees, impose quotas, or restrict commercial use.
- Free/open-source tools are preferred where practical, but unlimited free generation is never guaranteed.
- A rendered MP4 must only be claimed when an actual render has completed and passed basic checks.
- When rendering is unavailable, deliver an editable project, assets, and clear setup/render instructions.

## Repository map

- `SKILL.md` — main skill instructions.
- `docs/architecture.md` — modular system architecture.
- `docs/workflow.md` — end-to-end production workflow.
- `docs/hyperframes-workflow.md` — HyperFrames-first editing and rendering.
- `docs/providers.md` — provider-neutral asset strategy.
- `docs/licensing.md` — licensing and rights checklist.
- `templates/` — reusable creative brief and storyboard templates.
- `modules/quality-assurance.md` — pre-delivery QA checklist.
- `THIRD_PARTY_NOTICES.md` — reference projects and attribution/licensing review notes.

## License

The repository's original documentation and skill files are licensed under MIT; see [LICENSE](LICENSE). This license applies only to original files in this repository. It does not change the licenses or terms of HyperFrames, FFmpeg, Remotion, other third-party software, models, APIs, fonts, music, footage, or generated assets.
