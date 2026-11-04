# Media and asset management

## Asset-first workflow
Create an asset manifest before editing. Every media item should have a stable ID, local path, type, source/provenance, rights basis, commercial-use status, and any relevant consent/release status. Keep original files unchanged and create derived versions in a separate folder.

## Folder convention
A practical project layout:

- `assets/originals/` — untouched source files.
- `assets/working/` — normalized, trimmed, resized, or transcoded copies.
- `assets/generated/` — AI-generated material with provider and generation notes.
- `audio/` — narration, music, and sound effects.
- `exports/` — previews and final renders.
- `project/` — timeline, manifest, scripts, and metadata.

## Naming
Use descriptive, stable filenames: `scene-01-opening-source.jpg`, `voiceover-pt-BR-take-02.wav`. Avoid names such as `final-final2-new.mp4`. Do not rename source assets without updating references.

## Normalization
Before editing, inspect dimensions, aspect ratio, frame rate, duration, sample rate, channel layout, and codec. Create working copies to normalize incompatible media. Preserve the original and record conversion settings. Do not upscale or interpolate by default unless the brief requires it.

## Rights and consent
Record where each asset came from and what permissions apply. Verify commercial use, attribution, territory, term, modifications, model/provider terms, music synchronization rights, and releases for identifiable people or voices. Do not assume that publicly accessible media is reusable.

## Preflight
Run `tools/asset-preflight/check.mjs` against the JSON manifest before editing. It checks local file presence and metadata completeness, not legal validity or media integrity. Review all warnings manually.

## Delivery
Package only assets the recipient is allowed to receive. Include attribution and credits where required. Keep private source material and credentials out of public repositories.
