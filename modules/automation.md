# Production automation

## Scope
Automate repeatable project setup, validation, asset organization, and render orchestration without hiding failures or making provider-specific assumptions.

## Principles
- Prefer small scripts with documented inputs and outputs.
- Keep the project manifest as the source of truth.
- Make generation idempotent: rerunning with the same input should produce the same project structure and content.
- Never overwrite user assets silently. Require an explicit overwrite option or write to a new output directory.
- Keep API keys in environment variables or a secret manager; never commit credentials.
- Pin tool versions for reproducible production and record versions in the delivery manifest.

## Suggested stages
1. Parse and validate the creative brief and project JSON.
2. Create the output directory and standard subfolders.
3. Generate the composition and timeline.
4. Resolve asset references and verify files exist.
5. Run renderer diagnostics, lint, and composition checks.
6. Create preview snapshots and inspect them.
7. Render only after blocking checks pass.
8. Validate the output file and package project, assets, metadata, and credits.

## Error handling
- Fail fast on invalid JSON, missing required fields, unsafe paths, duplicate IDs, invalid durations, or missing required assets.
- Print actionable errors with the field or file path and a suggested correction.
- Distinguish warnings from blocking errors.
- Preserve logs and partial outputs for diagnosis; do not label a failed render as successful.
- Return a non-zero process exit code on failure.

## CLI contract
A generator should accept explicit input and output paths, provide `--help`, validate before writing, and print the exact files created. It should not install packages or download assets implicitly. A dry-run mode is recommended for production tooling.

## Security and portability
Treat project JSON, filenames, prompts, and downloaded metadata as untrusted input. Resolve output paths beneath the chosen output directory, escape HTML text, and avoid shell interpolation. Do not execute code embedded in project data. Use local assets for deterministic rendering and disclose external dependencies.

## Current starter generator
See [project-generator](../tools/project-generator/README.md) and [project schema](../docs/project-schema.md). The starter currently creates a title-card composition from text-only scene data; it is not an AI media generator and does not render MP4 by itself.
