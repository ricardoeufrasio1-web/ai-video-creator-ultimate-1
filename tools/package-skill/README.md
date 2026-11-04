# Portable Agent Skill package builder

Builds a distributable folder and ZIP for hosts that support the open Agent Skills format.

## Requirements

- Python 3.9+
- Repository checked out locally or in a cloud workspace

## Run from repository root

```bash
python3 tools/package-skill/package.py
```

## Output

- `dist/ai-video-creator-ultimate/`
- `dist/ai-video-creator-ultimate.zip`

The package carries forward the complete existing modules, docs, tools, examples, and templates. It uses only Python's standard library. It does not install provider credentials, render video, or create AI media.
