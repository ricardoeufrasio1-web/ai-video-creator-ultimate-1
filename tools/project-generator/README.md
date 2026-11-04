# HyperFrames starter project generator

A small Node.js 22+ generator that turns a text-only `project.json` into an HTML composition and copies the source JSON into the output folder. It uses Node built-ins only; it does not install dependencies, generate AI assets, or render MP4.

## Run

From the repository root:

```bash
node tools/project-generator/generate.mjs examples/hyperframes-basic/project.json ./output/my-video
```

Then follow the current [HyperFrames workflow](../../docs/hyperframes-workflow.md). Install HyperFrames separately and check the installed CLI's `--help` before using commands.

## Input
See [project schema](../../docs/project-schema.md) and [example project](../../examples/hyperframes-basic/project.json).

## Output
- `index.html` — fixed-size HTML/CSS composition with timed clips and a paused GSAP timeline.
- `project.json` — copy of the validated input for reproducibility.

The generator refuses to overwrite an existing output directory. Choose a new path or move the old output yourself.

## Limitations
This is a starter for text title cards and sequential cuts. It does not fetch images, synthesize narration, create captions, add music, or export MP4. GSAP is referenced from a CDN in this demonstration; for offline/reproducible rendering, vendor and pin a reviewed local GSAP version in the generated project and verify the renderer setup.
