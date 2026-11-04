---
name: ai-video-creator-ultimate
description: Universal, tool-aware AI video production skill. Use when a user wants to plan, create, edit, render, review, or publish videos from an idea, brief, article, product, script, or source assets across niches, languages, and platforms.
license: MIT
compatibility: Requires an agent that can read skill resources. Full automation additionally requires execution tools, filesystem or workspace access, media tools, and configured generation providers.
metadata:
  author: ricardoeufrasio1-web
  version: "1.1.0"
---

# AI Video Creator Ultimate

A portable, modular workflow for producing videos across educational, documentary, marketing, recipe, entertainment, news, storytelling, tutorial, product, and other niches. This skill is designed for any agent that supports the open Agent Skills format. It is not tied to one chat provider.

## Operating contract: discover capabilities first

Before starting production, inspect the tools actually available in the current chat/agent environment. Do not assume that another agent's tools, APIs, subscriptions, files, browser, terminal, or integrations are available here.

Classify the environment:

- **Level 1 — Chat only:** can reason and write. Deliver research (if browsing exists), brief, script, storyboard, prompts, asset plan, and exact handoff instructions. Do not claim to create files, render, or publish.
- **Level 2 — Chat + files/workspace:** can read/write project files and package an editable project. Render only if a renderer is installed and executable.
- **Level 3 — Execution + media runtime:** can run scripts, access a filesystem, and use FFmpeg plus a supported renderer. Can assemble and render after preflight passes.
- **Level 4 — Connected generation providers:** also has authorized image/video/voice/music generation services. Can generate assets subject to provider quotas, terms, and cost.
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
7. **Asset production:** use available authorized providers or user assets. Keep provider-specific operations behind adapters. Never fabricate an asset URL or claim generation succeeded without a returned file.
8. **Timeline:** define FPS, dimensions, frame boundaries, tracks, transitions, audio cues, captions, and asset references. Validate before rendering.
9. **Edit and render:** prefer HyperFrames when installed and verified; use FFmpeg for media inspection, conversion, trimming, mixing, and encoding. Remotion or another renderer may be used through an adapter. Verify the actual output file.
10. **Quality assurance:** check facts, spelling, timing, continuity, visual artifacts, safe areas, aspect ratio, audio clipping/loudness, captions, stream metadata, and export settings. Distinguish automated checks from human review.
11. **Delivery:** provide the verified MP4 only when it exists and passed the relevant checks. Also provide editable project/source, captions, thumbnail concept, title, description, social copy, tags, credits, and a concise QA report when useful.
12. **Publishing:** prepare a publishing pack by default. Publish only through an available authorized integration and after explicit user confirmation. Never request or expose passwords or tokens in chat.

## Editing and rendering priority

Use HyperFrames as the preferred composition/rendering workflow when the environment supports it. Consult the current upstream documentation and installed CLI help before relying on commands. Use FFmpeg for media operations. Remotion and other renderers are optional adapters. If no renderer/runtime exists, deliver a portable editable project and clear instructions rather than claiming an MP4 was rendered.

## Project generation and validation

- Text-only starter composition: `tools/project-generator/generate.mjs` (Node.js 22+). It creates HTML and copies project JSON; it does not generate media or render MP4.
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
