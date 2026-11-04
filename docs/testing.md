# Testing and quality gates

The repository includes lightweight Node.js tools and a GitHub Actions workflow. The workflow runs on pushes to `main`, pull requests, and manual dispatch.

## Automated checks

The workflow:
1. Parses every tracked-style `.json` file found in the checkout.
2. Runs Node's syntax checker on every `.mjs` file under `tools/`.
3. Runs the timeline validator against the sample timeline.
4. Generates the starter HTML composition into a temporary directory and checks that both expected output files are non-empty.
5. Runs render preflight against the sample FFprobe metadata with explicit expected dimensions, frame rate, duration, and audio.

## Run locally

Requires Node.js 22+.

```bash
# Syntax checks
find tools -name '*.mjs' -print0 | xargs -0 -n1 node --check

# Timeline sample
node tools/timeline-validator/validate.mjs examples/timelines/short-form.json

# Starter composition (choose a new output folder)
node tools/project-generator/generate.mjs examples/hyperframes-basic/project.json ./build/example

# Metadata sample
node tools/render-preflight/check-render.mjs examples/render/ffprobe-output.example.json --expect-width 1080 --expect-height 1920 --expect-fps 30 --expect-duration 30 --require-audio
```

The asset manifest example is a template and references placeholder media paths. The asset preflight tool will correctly report missing files until real assets are placed at those paths or the manifest is updated.

## What CI does not prove

Passing CI does not prove:
- that HyperFrames is installed or compatible with a specific runtime;
- that a real MP4 was rendered;
- that every frame looks correct or every audio track sounds correct;
- that voice, image, video, music, or font licenses are valid;
- that a provider's current terms allow a particular commercial use;
- that generated assets are factually accurate or free of artifacts.

Real production still requires rendering with the selected engine and manual visual/audio review of the exported file.
