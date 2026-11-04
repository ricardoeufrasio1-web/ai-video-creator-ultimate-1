# Provider adapter contract

## Goal

Keep the creative workflow independent from image, video, speech, music, storage, and publishing vendors. The skill should request a capability through a stable contract; a host-specific adapter performs the vendor call.

This document defines an integration boundary, not a claim that a provider is already connected.

## Adapter categories

- `image.generate`
- `video.generate`
- `speech.synthesize`
- `audio.generate` (music or sound effects; rights must be checked)
- `media.inspect`
- `media.render`
- `storage.put` / `storage.get`
- `publish.create`

## Common request envelope

Every operation should accept a structured request with:
- `job_id`: stable production job identifier;
- `operation_id`: unique idempotency key for retries;
- `input`: operation-specific data;
- `constraints`: duration, dimensions, aspect ratio, locale, quality, file format;
- `rights`: consent, license, commercial-use and disclosure requirements;
- `budget`: user-approved spend ceiling or `0` for no paid calls;
- `callback`: optional host-supported status mechanism.

## Common response envelope

Return:
- `status`: `succeeded`, `queued`, `failed`, or `needs_approval`;
- `provider` and `model`;
- `operation_id`;
- `assets`: array of verified output descriptors (ID, local path or host file reference, MIME type, byte size, dimensions/duration when known);
- `usage`: cost/credits/tokens if reported by provider;
- `warnings`: terms, watermark, quality or rights limitations;
- `error`: stable code and safe diagnostic text on failure.

Never return a success state without a real provider result and a verified output reference. Do not expose credentials in logs or response bodies.

## Required adapter behavior

1. Validate input and reject unsupported dimensions, durations, languages, or formats before spending credits.
2. Check user authorization, rights, and approved budget.
3. Use secure host secrets; never embed keys in source files, prompts, manifests, or Git.
4. Apply bounded retries only for transient failures. Reuse the same idempotency key where the provider supports it.
5. Respect rate limits and provider concurrency constraints.
6. Record provider/model/version, parameters, timestamp, output provenance, license/terms URL, and reported usage.
7. Verify downloads are complete, non-empty, and match expected MIME/format.
8. Support cancellation or clearly report when cancellation is unavailable.
9. Return actionable errors without leaking private data.
10. Offer a provider-neutral fallback when practical.

## Image generation input

Required: prompt, aspect ratio or width/height, output format. Optional: style, reference asset IDs with authorization, negative constraints, seed, quality. Return actual image file references and dimensions.

## Video generation input

Required: prompt, target duration, aspect ratio. Optional: start/end frame references, camera motion, frame rate, quality. Return actual video file references, duration, dimensions, and any provider watermark/limit information.

## Speech synthesis input

Required: exact text, language/locale, voice ID or approved voice description. Optional: pace, emotion, pronunciation dictionary, output format. Return audio reference, duration, sample rate, voice/model provenance, and usage. Do not clone a real person's voice without clear authorization.

## Render adapter input

Required: project/timeline reference, assets, output format, dimensions, FPS, output location. Return a verified output reference and render logs. Renderer must be installed and version-pinned in reproducible environments.

## Publishing adapter input

Required: platform, connected account reference, media reference, title/description and platform-required metadata. Publishing must be gated by a final explicit approval from the user. Return the platform post ID and canonical URL when available.

## Cost and free-mode behavior

If the user budget is zero, do not call a paid generation API or paid rendering service. Use user-provided assets, genuinely free/local tools, or deliver a production-ready plan and editable project. Never assume free trial credits are available.

## Host integration

The agent host is responsible for exposing adapter operations as tools or MCP actions and for managing secrets. A Markdown skill cannot call arbitrary providers by itself. Each integration must be tested in the target host before being advertised as available.
