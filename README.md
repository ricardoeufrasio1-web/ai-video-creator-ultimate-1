# AI Video Creator Ultimate

A universal, modular skill for planning and producing videos across niches, platforms, languages, and formats — from research and scripting to storyboarding, asset planning, editing, quality assurance, and publishing.

## Capabilities

- Turns an idea, brief, article, product, script, or source assets into a production plan.
- Supports educational, documentary, marketing, recipes, entertainment, news, storytelling, tutorials, and more.
- Creates timed scripts, storyboards, shot lists, scene prompts, continuity notes, and asset manifests.
- Uses **HyperFrames as the preferred editing/rendering workflow** when the environment supports it.
- Includes Node.js starter generation plus asset, timeline, and rendered-output metadata preflight tools.
- Uses FFmpeg for media operations when available; treats Remotion and other systems as optional adapters.
- Produces publishing metadata, captions, thumbnail concepts, credits, and source notes.

## Quick start

1. Read [SKILL.md](SKILL.md).
2. Define audience, goal, platform, format, duration, language, tone, and CTA.
3. Follow [the end-to-end workflow](docs/workflow.md) and [production checklist](docs/production-checklist.md).
4. Use the brief and storyboard templates in [templates/](templates/).
5. Generate a starter composition with [project-generator](tools/project-generator/README.md) and [the example JSON](examples/hyperframes-basic/project.json).
6. Check local assets with [asset preflight](tools/asset-preflight/README.md) and scene timing with [timeline validation](tools/timeline-validator/README.md).
7. After an actual render, export metadata with FFprobe and run [render preflight](tools/render-preflight/README.md).
8. For HyperFrames, follow [the HyperFrames workflow](docs/hyperframes-workflow.md) and verify current upstream CLI instructions.

## Preferred editing engine: HyperFrames

HyperFrames is the primary composition/rendering reference. It supports HTML/CSS/JavaScript-based video compositions and a frame-oriented rendering pipeline. It is **not bundled** here. Install it separately and review its current license, dependencies, and runtime requirements.

Typical requirements may include Node.js 22+, FFmpeg, and a compatible browser/runtime. Exact requirements can change by version and operating system. Do not assume a phone-only environment can run the full renderer.

## Included tools and limitations

- **Project generator:** creates a text-based HTML starter composition and copies source JSON. It does not generate images, video, voice, music, or MP4.
- **Asset preflight:** checks manifest structure, local paths, and missing rights metadata. It cannot prove ownership or licensing.
- **Timeline validator:** checks scene timing, frame alignment, asset IDs, and audio cue ranges. It does not render or prove synchronization.
- **Render preflight:** checks FFprobe metadata such as streams, dimensions, FPS, and duration. It does not decode every frame or listen to audio.

## Quality automation

GitHub Actions runs JSON parsing, JavaScript syntax checks, sample timeline validation, starter project generation, and render-metadata preflight on pushes to `main`, pull requests, and manual runs. See [testing guide](docs/testing.md). CI passing does not replace manual visual/audio review or licensing checks.

## Requirements and limitations

- This repository is a skill and production toolkit, not a hosted video-generation service.
- Image, video, voice, music, and model providers may charge fees, impose quotas, or restrict commercial use.
- Free/open-source tools are preferred where practical; unlimited free generation is never guaranteed.
- Claim a rendered MP4 only after an actual render has completed and the file has been verified.
- When rendering is unavailable, deliver an editable project, assets, and clear setup/render instructions.

## Repository map

- `SKILL.md` — main skill instructions.
- `docs/` — architecture, workflow, providers, schema, licensing, render pipeline, testing, checklist, and troubleshooting.
- `modules/` — research, scripting, creative direction, asset production, editing, timeline, motion, voice, audio, captions, QA, and publishing specialists.
- `tools/project-generator/` — Node.js project generator.
- `tools/asset-preflight/` — local media manifest checker.
- `tools/timeline-validator/` — scene and audio cue timeline validator.
- `tools/render-preflight/` — FFprobe metadata checker for actual rendered output.
- `examples/` — starter composition, asset manifest, timeline, and FFprobe metadata examples.
- `templates/` — creative brief, storyboard, and asset tracking templates.
- `.github/workflows/quality.yml` — automated repository checks.
- `THIRD_PARTY_NOTICES.md` — reference projects and attribution/licensing review notes.

## License

Original documentation and skill files are licensed under MIT; see [LICENSE](LICENSE). This does not change licenses or terms for HyperFrames, FFmpeg, Remotion, third-party software, models, APIs, fonts, music, footage, or generated assets.
