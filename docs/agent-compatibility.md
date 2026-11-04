# Agent compatibility and execution guide

## Purpose

The AI Video Creator Ultimate is packaged using the open Agent Skills convention: a skill directory with a required `SKILL.md` and optional scripts, references, examples, and assets. The same package can be reused by different agents that implement this convention.

The format standardizes packaging and instructions. It does **not** standardize each host's import UI, tool names, code execution, filesystem, browser, media generation, renderer, storage, or social publishing integrations.

## Portable import

1. Open the target agent's skill/extension import area.
2. Import the public GitHub repository or the generated ZIP if supported.
3. Confirm the skill appears in that agent's installed skills list.
4. Start a new chat and ask it to create a short test project.
5. Check that the agent can read the referenced modules and scripts. Some hosts import only a single Markdown file; if so, attach the full package or ask the host to read the supporting files from the repository.
6. Ask the agent to report its available tools before requesting a real render.

If the host does not support installing skills, attach `SKILL.md` and the supporting files to a conversation or paste the main instructions. This is a per-chat fallback, not a persistent installation.

## Capability negotiation

The agent must inspect its own available tools and classify the session:

| Level | Available capabilities | Reliable deliverable |
|---|---|---|
| 1 | Chat only | Brief, research, script, storyboard, prompts, handoff |
| 2 | File/workspace access | Editable project and package |
| 3 | Execution, renderer, FFmpeg | Rendered MP4 after file verification |
| 4 | Authorized generation providers | Generated image/video/voice/audio assets |
| 5 | Authorized publishing integration | Approved publication and post URL/status |

Do not infer a capability from the model name or product brand. Verify tools in the current session.

## Provider adapters

Provider-specific services should be isolated behind adapters rather than hard-coded into the core skill. An adapter should document:

- provider and API version;
- required credentials and secure secret storage;
- supported operations and input/output schema;
- model/quality/duration/format constraints;
- cost, quota, rate limits, and retry policy;
- rights, privacy, retention, and commercial-use terms;
- failure modes and a provider-independent fallback.

Do not hard-code API keys or ask users to paste secrets into ordinary chat. Use the host's approved connection flow or secret manager.

## Rendering contract

Before rendering, verify that the runtime, renderer, FFmpeg, fonts, assets, and required browser dependencies are available. Use the current installed CLI help and the project's render guide. After rendering, verify that the output file exists, has non-zero size, and passes FFprobe metadata checks. A successful metadata check does not prove visual or audio quality; review representative frames and listen to the output when tools allow.

## Publishing contract

Prepare a publishing pack without publishing by default. Publishing requires an authorized integration, the correct account, platform-specific metadata, and explicit user approval immediately before the action. Report the returned post URL or platform confirmation; never claim success without it.

## Platform-specific notes

Maintain platform-specific installation instructions separately from the core skill. Avoid promising universal one-click installation: each host chooses whether it supports Agent Skills, which archive/repository sources it accepts, and which tools it exposes to the agent.

## Current project status

The repository contains modular production guidance, starter project generation, asset/timeline/render-metadata validators, examples, and CI structural checks. It does not yet include live image/video/voice provider adapters, a hosted job runner, a verified end-to-end MP4 render, or universal social publishing connectors. These require implementation and, in some cases, provider accounts or paid usage.
