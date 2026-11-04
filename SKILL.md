---
name: ai-video-creator-ultimate
description: Universal, tool-aware AI video production skill. Use when a user wants to plan, create, edit, render, review, or publish videos from an idea, brief, article, product, script, or source assets across niches, languages, and platforms.
license: MIT
compatibility: Requires an Agent Skills-compatible host. Procedural video production requires code execution, filesystem access, and a verified renderer. Remote image/video generation providers are optional and are not part of the default workflow.
metadata:
  author: ricardoeufrasio1-web
  version: "1.2.0"
---

# AI Video Creator Ultimate

## Product direction: autonomous, provider-free production by default

The default path must create original visual material with the project's own procedural graphics, animation, typography, diagrams, compositing and editing code. Do not require or silently call external AI image/video generation services. External providers are optional only when the user explicitly requests them. The goal is a single conversational creative director and production engine, not a prompt pack that hands the work to other generators.

The engine should support a broad, extensible range of visual languages: live-action looks as references, documentary, UGC, commercial, food, travel, sports, news, education, storytelling, 2D/3D-inspired graphics, vector, hand-drawn, collage, stop-motion-inspired, infographic, kinetic typography, data visualization, abstract and hybrid styles. It must allow custom styles and combinations. See docs/style-catalog.md.

For attention-focused editing, use modules/viral-editing-language.md: hooks, pattern interrupts, pacing, punch-ins, match cuts, speed ramps, dynamic transitions, kinetic typography, sound accents, visual resets, payoff and loop endings. Virality is never guaranteed; clarity, truth and accessibility take priority.

The no-provider engine can generate procedural graphics, original vector scenes, 2D/2.5D animation, motion design and complete edits from supplied assets. It cannot create arbitrary photorealistic footage or natural human performances without source footage or a generative model. Never imply otherwise. Rendering also requires a host that can execute code and write files; a text-only chat cannot render an MP4.


A portable, modular workflow for producing videos across educational, documentary, marketing, recipe, entertainment, news, storytelling, tutorial, product, and other niches. This skill is designed for any agent that supports the open Agent Skills format. It is not tied to one chat provider.

## Operating contract: discover capabilities first

Before starting production, inspect the tools actually available in the current chat/agent environment. Do not assume that another agent's tools, APIs, subscriptions, files, browser, terminal, or integrations are available here.

Classify the environment:

- **Level 1 — Chat only:** can reason and write. Deliver research (if browsing exists), brief, script, storyboard, prompts, asset plan, and exact handoff instructions. Do not claim to create files, render, or publish.
- **Level 2 — Chat + files/workspace:** can read/write project files and package an editable project. Render only if a renderer is installed and executable.
- **Level 3 — Execution + media runtime:** can run scripts, access a filesystem, and use FFmpeg plus a supported renderer. Can assemble and render after preflight passes.
- **Level 4 — Optional connected generation providers:** may use authorized external image/video/voice/music services only when explicitly requested. These are not required by the default procedural path.
- **Level 5 — Publishing integrations:** also has authorized platform connectors/API access. Can publish only after the user explicitly approves the target account, content, and action.

A skill cannot grant missing tools, subscriptions, compute, API keys, storage, network access, or publishing permissions. Never imply otherwise. Explain the highest level available and proceed as far as possible without blocking useful work.

## User experience

The user should be able to describe the desired video in ordinary language. Ask only for essential missing details; use sensible defaults for the rest. Do not make the user manually copy prompts between stages when the environment can execute the steps. Keep the user informed of decisions, blockers, costs, and approval points.

## End-to-end workflow

1. **Intake:** identify subject, audience, purpose, platform, aspect ratio, duration, language, tone, CTA, brand constraints, deadline, budget, and available source assets. Ask only for missing essentials.
2. **Research:** browse current/factual topics when browsing is available. Track sources and distinguish facts, uncertainty, opinion, and creative reconstruction.
3. **Creative strategy:** define audience insight, concept, hook, narrative arc, format, pacing, and CTA where appropriate.
4. **Script:** write narration/dialogue and estimate realistic spoken duration. Preserve supplied wording exactly when requested.
5. **Storyboard:** specify scene IDs, timestamps, duration, action, framing, camera movement, lighting, location, props, continuity, narration, music, SFX, and transitions.
6. **Asset plan:** identify footage, generated images/video, voice, music, effects, graphics, references, rights, consent, provenance, and fallback options.
7. **Asset production:** default to original procedural graphics, vector illustrations, diagrams, typography, 2D/2.5D animation and user-supplied assets. Do not call external image/video generators unless explicitly requested. Keep optional provider operations behind adapters. Never fabricate an asset URL or claim generation succeeded without a returned file.
8. **Timeline:** define FPS, dimensions, frame boundaries, tracks, transitions, audio cues, captions, and asset references. Validate before rendering.
9. **Edit and render:** prefer HyperFrames when installed and verified; use FFmpeg for media inspection, conversion, trimming, mixing, and encoding. Remotion or another renderer may be used through an adapter. Verify the actual output file.
10. **Quality assurance:** check facts, spelling, timing, continuity, visual artifacts, safe areas, aspect ratio, audio clipping/loudness, captions, stream metadata, and export settings. Distinguish automated checks from human review.
11. **Delivery:** provide the verified MP4 only when it exists and passed the relevant checks. Also provide editable project/source, captions, thumbnail concept, title, description, social copy, tags, credits, and a concise QA report when useful.
12. **Publishing:** prepare a publishing pack by default. Publish only through an available authorized integration and after explicit user confirmation. Never request or expose passwords or tokens in chat.

## Editing and rendering priority

Use HyperFrames as the preferred composition/rendering workflow when the environment supports it. Consult the current upstream documentation and installed CLI help before relying on commands. Use FFmpeg for media operations. Remotion and other renderers are optional adapters. If no renderer/runtime exists, deliver a portable editable project and clear instructions rather than claiming an MP4 was rendered.

## Project generation and validation

- Provider-free procedural scene generator: `tools/procedural-scene-engine/generate.mjs` (Node.js 22+), creates self-contained SVG/HTML compositions from JSON without remote assets.\n- Procedural MP4 renderer: `tools/procedural-scene-engine/render.py` uses local FFmpeg for text, rectangles, lines, progress bars, camera moves, transitions and local audio mixing; see its README for limitations.\n- Optional offline narration: `tools/procedural-scene-engine/tts.py` uses a locally installed eSpeak NG executable; it does not use a remote AI service and its voice quality is synthetic/robotic.\n- Text-only starter composition: `tools/project-generator/generate.mjs` (Node.js 22+). It creates HTML and copies project JSON; it does not generate media or render MP4.
- Asset preflight: `tools/asset-preflight/check.mjs` checks manifest structure, local paths, and missing rights-metadata warnings; it cannot prove ownership or licensing.
- Timeline validation: `tools/timeline-validator/validate.mjs` checks scene timing, frame alignment, asset IDs, and audio cue ranges; it does not render or prove synchronization.
- Render preflight: `tools/render-preflight/check-render.mjs` checks FFprobe metadata after an actual render; it does not inspect every frame or listen to audio.
- Skill packaging: `tools/package-skill/package.py` creates a portable Agent Skill folder and ZIP containing the existing modules, docs, tools, examples, and templates.

Run only scripts that are present in the loaded skill package. Check prerequisites first and report errors honestly.

## Specialist modules

Read only the modules needed for the current task:

- Research and fact-checking: `modules/research.md`
- Scripts, hooks, pacing, CTA: `modules/scriptwriting.md`
- Storyboard, camera, lighting, continuity: `modules/creative-direction.md`
- Asset planning and production: `modules/asset-production.md`
- Timeline and FPS: `modules/timeline-orchestration.md`
- Motion and transitions: `modules/transitions-motion.md`
- Asset provenance and rights: `modules/media-management.md`
- Voice and TTS: `modules/voice-production.md`
- Audio and cue synchronization: `modules/audio.md`, `modules/audio-synchronization.md`
- Captions and accessibility: `modules/captions-accessibility.md`
- Automation and project generation: `modules/automation.md`
- HyperFrames editing: `modules/editing-hyperframes.md`
- QA and render validation: `modules/quality-assurance.md`, `modules/render-validation.md`
- Publishing and handoff: `modules/publishing.md`

## Universal formats

Support vertical 9:16, square 1:1, landscape 16:9, or other requested formats; short- or long-form duration; voiceover, presenter, dialogue, ASMR, screen-led, or text-led styles. Adapt the workflow to the requested niche rather than assuming a recipe, marketing, or social-video use case.

## Safety, rights, and reliability

- Respect copyright, licensing, privacy, consent, likeness/voice rights, and platform policies.
- Do not clone a real person's voice or likeness without appropriate authorization.
- Do not present synthetic footage as documentary evidence.
- Track asset source, license, consent status, and commercial-use restrictions.
- Prefer free/open-source tools where practical, but never promise unlimited free generation.
- Never commit API keys, passwords, or access tokens. Use the host's secret manager/environment variables.
- Do not publish, spend money, or use paid credits without user approval.
- Never claim that research, generation, editing, rendering, review, or publishing happened unless the corresponding tool/action succeeded.
- See `docs/production-checklist.md`, `docs/agent-compatibility.md`, and `docs/troubleshooting.md`.

## Reporting status

For every production, clearly report:
- what was created;
- what was only planned;
- which tools/providers were actually used;
- which automated checks passed or failed;
- whether the MP4 file exists and was verified;
- whether visual/audio review was performed;
- any remaining manual steps, costs, or permissions.


## Cross-agent compatibility and capability discovery

This skill uses the open Agent Skills convention and is not tied to one AI provider. Before production, inspect the tools actually available in the current chat. Do not assume another product's browser, terminal, filesystem, image/video generation, voice, renderer, storage, or publishing integrations are available here.

Classify the session:
- **Chat only:** deliver research (if browsing exists), brief, script, storyboard, prompts, asset plan, and handoff instructions.
- **Files/workspace:** also create editable project files and packages.
- **Media runtime:** render only after verifying the renderer, FFmpeg, dependencies, assets, and output.
- **Generation providers:** generate media only through connected, authorized providers; disclose quotas and costs.
- **Publishing integrations:** publish only through an authorized connection and after explicit user approval.

A Skill cannot grant missing tools, subscriptions, compute, API keys, storage, network access, or publishing permissions. Continue as far as the host allows and clearly state what is and is not possible. Never claim an asset, render, review, or publication succeeded unless the corresponding tool returned success and the output was verified.

For platform-neutral installation, capability levels, provider adapter expectations, rendering checks, and publishing approval, read `docs/agent-compatibility.md`.


## Integration contracts and render roadmap

- Provider-neutral adapter requirements: `docs/provider-adapter-contract.md`
- Full timeline-to-render implementation plan and acceptance criteria: `docs/full-render-integration-plan.md`
- Example adapter capability descriptor: `examples/providers/adapter.example.json`

Do not describe a provider adapter as implemented merely because its contract or example exists. The current repository still needs concrete provider integrations and broader end-to-end media review.


## Local MP4 rendering adapter (experimental)

When Python and FFmpeg are available, the agent may use `tools/ffmpeg-render/render.py` to assemble a local timeline of image/video assets and optional voiceover/music into MP4. Read `tools/ffmpeg-render/README.md` for its deliberately limited schema and constraints. Do not describe this as AI generation, full HyperFrames timeline support, or automatic publishing. CI performs a deterministic FFmpeg render smoke test; final projects still require visual/audio review.


## Default provider-free production contract

When the user asks to create a video without external AI services:
1. Select a realizable visual style from the catalog or define a custom style bible.
2. Write a complete script and frame/time-based storyboard.
3. Generate visuals using code-authored SVG, HTML/CSS/Canvas, vector characters, diagrams, charts, procedural backgrounds and motion graphics.
4. Animate using deterministic keyframes, easing, camera transforms, parallax, masks and transitions.
5. Edit to a beat map with intentional cuts, pacing changes, overlays, captions and sound design.
6. Use user-provided audio or a verified local TTS/audio engine if installed; otherwise do not invent a voice track.
7. Render with the bundled engine only after it is implemented and verified, or with a verified host renderer.
8. Validate the actual MP4 and report the visual style, duration, dimensions, audio tracks and remaining limitations.

Do not describe the procedural engine as complete until source code, tests, package inclusion, and an end-to-end MP4 render test all pass. See docs/autonomous-engine-roadmap.md.
