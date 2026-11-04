# AI Video Creator Ultimate

A universal, portable Agent Skill and modular toolkit for planning and producing videos across niches, platforms, languages, and formats — from research and scripting to assets, editing, quality assurance, rendering, and publishing handoff.

## One skill, compatible agents

This project follows the open Agent Skills folder format: a directory with a `SKILL.md` file plus optional scripts, references, examples, and assets. It is designed to be imported into any AI chat/agent that implements Agent Skills. The format does not guarantee that every chat can execute scripts, generate media, render video, or publish; those capabilities depend on the host agent and its connected tools.

## Install / import

- **GitHub import:** use the host agent's Skills/Extensions import feature and provide this public repository URL: https://github.com/ricardoeufrasio1-web/ai-video-creator-ultimate-1
- **ZIP import:** download or generate the portable ZIP described below, then import the ZIP if the host supports it.
- **Manual:** provide the `SKILL.md` and supporting folder to an agent that supports local skill folders.

The exact import UI differs by product. Some chat products do not support installing skills; in those, attach the skill files or paste the instructions for that conversation. A chat that cannot execute code can still use the planning, scriptwriting, storyboard, prompt, and publishing-pack workflows.

## Build a portable ZIP

Requires Python 3.9+ on a computer or cloud workspace with this repository checked out:

```bash
python3 tools/package-skill/package.py
```

Output:
- `dist/ai-video-creator-ultimate/` — portable skill folder.
- `dist/ai-video-creator-ultimate.zip` — importable archive for hosts that accept skill ZIPs.

The package includes the complete existing `SKILL.md`, docs, modules, tools, examples, and templates. It excludes Git metadata, CI config, caches, and generated outputs.

## Capabilities

- Turns an idea, brief, article, product, script, or source assets into a production plan.
- Supports educational, documentary, marketing, recipe, entertainment, news, storytelling, tutorial, product, and other niches.
- Creates timed scripts, storyboards, shot lists, scene prompts, continuity notes, and asset manifests.
- Uses HyperFrames as the preferred editing/rendering workflow when the environment supports it.
- Includes project generation plus asset, timeline, and rendered-output metadata preflight tools.
- Uses FFmpeg for media operations when available; treats Remotion and other renderers as optional adapters.
- Produces publishing metadata, captions, thumbnail concepts, credits, and source notes.

## Execution levels

1. **Chat only:** plan, research (if browsing exists), script, storyboard, prompts, and handoff.
2. **Files/workspace:** create editable project files and package outputs.
3. **Media runtime:** run renderer/FFmpeg and verify actual MP4 output.
4. **Generation providers:** generate images, video, voice, and audio where connected and authorized.
5. **Publishing integrations:** publish only when connected and explicitly approved.

A Skill does not install missing tools or bypass subscriptions, quotas, API keys, compute limits, storage, or platform permissions. Image, video, voice, and music providers may charge fees or restrict commercial use.

## Existing toolkit and honest limitations

- **Project generator:** creates a text-based HTML starter composition and copies source JSON. It does not generate AI media or render MP4.
- **Asset preflight:** checks manifest structure, local paths, and missing rights metadata. It cannot prove ownership or licensing.
- **Timeline validator:** checks scene timing, frame alignment, asset IDs, and audio cue ranges. It does not render or prove synchronization.
- **Render preflight:** checks FFprobe metadata such as streams, dimensions, FPS, and duration. It does not decode every frame or listen to audio.

GitHub Actions validates JSON, JavaScript syntax, sample timeline validation, starter generation, and sample render metadata. CI passing does not replace actual rendering or visual/audio review.

## Preferred renderer

HyperFrames is the primary composition/rendering reference. It is not bundled. Install it separately and review its current license, dependencies, and runtime requirements. Node.js 22+, FFmpeg, and a compatible browser/runtime may be required depending on version. Verify the installed CLI's current help before use.

## Repository map

- `SKILL.md` — main universal skill instructions.
- `docs/` — architecture, compatibility, workflow, providers, schema, licensing, render pipeline, testing, checklist, and troubleshooting.
- `modules/` — research, scripting, creative direction, asset production, editing, timeline, motion, voice, audio, captions, QA, and publishing specialists.
- `tools/` — project generator, asset preflight, timeline validator, render preflight, and portable package builder.
- `examples/` — starter composition, asset manifest, timeline, and FFprobe metadata examples.
- `templates/` — creative brief, storyboard, and asset tracking templates.
- `.github/workflows/quality.yml` — automated repository checks.
- `THIRD_PARTY_NOTICES.md` — reference projects and attribution/licensing review notes.

## License

Original documentation and skill files are licensed under MIT; see [LICENSE](LICENSE). This does not change licenses or terms for HyperFrames, FFmpeg, Remotion, third-party software, models, APIs, fonts, music, footage, or generated assets.


## Cross-agent portability

This project follows the open Agent Skills folder convention. Import it into any AI chat/agent that explicitly supports Agent Skills. The format makes the instructions portable; it does not guarantee that every host can execute scripts, generate media, render MP4, or publish. Those actions require tools, workspace access, runtime dependencies, provider connections, and permissions supplied by the host.

For compatibility guidance and the current execution limits, see [docs/agent-compatibility.md](docs/agent-compatibility.md).

## Build a portable installation ZIP

If you have Python 3.9+ and a local/cloud workspace with this repository checked out, run:

```bash
python3 tools/package-skill/package.py
```

This creates `dist/ai-video-creator-ultimate.zip` and the matching folder. The archive includes the existing modules, docs, tools, examples, and templates so the skill's relative references remain available. Import the ZIP only in agents that explicitly support skill archive imports.

A chat that does not support Agent Skills can still use the instructions by attaching the files, but that is not a persistent installation. See [the compatibility guide](docs/agent-compatibility.md).

**Important:** the portable package carries the workflow and utilities already in this repository; it does not magically add image/video/voice providers, a hosted rendering server, paid credits, or social account permissions. Current gaps are listed in the compatibility guide.


## First real MP4 renderer

An experimental local FFmpeg renderer is available at `tools/ffmpeg-render/`. It assembles ordered local image/video scenes and optional voiceover/music into MP4. Run `python3 tools/ffmpeg-render/create_fixture.py` and then follow `tools/ffmpeg-render/README.md`. GitHub Actions now renders a deterministic two-second MP4 fixture and validates its video/audio streams with FFprobe. This proves the local renderer path, not AI asset generation or social publishing.
