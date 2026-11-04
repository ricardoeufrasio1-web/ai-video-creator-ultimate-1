# Asset preflight checker

Checks a JSON asset manifest before editing/rendering. Requires Node.js 22+ and uses built-in modules only.

## Run

```bash
node tools/asset-preflight/check.mjs path/to/assets.json
```

The manifest path is resolved from the current working directory; each asset's `path` is resolved relative to the manifest file. The checker verifies unique IDs, supported asset types, file existence, safe relative paths, and basic rights metadata. It reports warnings separately from blocking errors and exits non-zero when errors exist.

## Manifest format

See [asset manifest example](../../examples/assets/manifest.example.json). Keep original files in the project asset folders and do not put secrets in the manifest.

## Important
A passing check is not legal advice and does not prove ownership, license validity, consent, or platform compliance. A human must review source URLs, license terms, releases, attribution, and commercial-use permissions.
