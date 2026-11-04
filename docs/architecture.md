# Architecture

## Design goal

A universal production system with a small core and optional specialist modules. The system should adapt to the user's niche, platform, skill level, device, budget, and available tools rather than forcing one fixed production style.

## Layers

1. **Core orchestrator** — interprets the request, selects modules, tracks constraints, and coordinates delivery.
2. **Research and strategy** — factual research, audience, objective, format, creative brief, and source tracking.
3. **Narrative design** — hooks, scripts, pacing, story arcs, CTAs, and duration estimates.
4. **Visual direction** — storyboard, shot list, camera, lighting, visual style, and continuity.
5. **Asset production** — footage, generated images/video, narration, music, sound effects, graphics, and typography.
6. **Editing and rendering** — HyperFrames-first composition, FFmpeg media operations, optional renderer adapters.
7. **Quality assurance** — factual, visual, audio, timing, accessibility, and export checks.
8. **Publishing** — platform metadata, captions, thumbnail concepts, credits, and performance hypotheses.

## Core contracts

Each module should accept a concise brief and return structured, reusable artifacts. Avoid hard dependencies on a single AI provider. Track asset provenance, source URLs, license/consent status, aspect ratio, duration, and continuity identifiers.

## Renderer strategy

- Primary: HyperFrames when supported by the execution environment.
- Media utility: FFmpeg when installed.
- Optional: Remotion or other renderers only when suitable and license-compliant.
- Fallback: provide editable source/project and exact instructions when local rendering is unavailable.

## Device-aware operation

Before choosing tools, identify whether the user has a desktop, cloud runtime, or phone-only workflow. Never imply that a phone can run a desktop rendering pipeline without a suitable remote environment. Keep generated assets portable and explain where files must be placed.

## Reliability

Use deterministic timelines, explicit durations, stable asset paths, seeded randomness when needed, and preflight checks. Network assets should be downloaded and validated before final rendering.
