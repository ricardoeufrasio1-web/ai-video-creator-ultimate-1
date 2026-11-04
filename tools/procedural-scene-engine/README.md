# Procedural Scene Engine — first executable prototype

This dependency-free Node.js tool creates a self-contained HTML/SVG composition from JSON. It generates original vector shapes, typography, simple diagrams and basic entrance animation without calling remote image or video generation services.

## Run

```bash
node tools/procedural-scene-engine/generate.mjs examples/procedural-scenes/vertical-explainer.json ./output/vertical-explainer
```

Open the generated index.html in a modern browser to preview it. The output contains inline SVG, CSS and JavaScript; it makes no network requests.\n\nTo render the supported procedural shapes and text to MP4 using local FFmpeg:\n\n```bash\npython3 tools/procedural-scene-engine/render.py examples/procedural-scenes/render-fixture.json --output ./output/procedural.mp4\n```\n\nThe MP4 renderer supports text, rectangles, lines and progress bars on generated color backgrounds. It requires FFmpeg with libx264 and drawtext support.

## Supported elements

- text
- rect
- circle
- line
- bar

Scenes support duration, background, accent, accessible description, rise/slide/pop entrances, push/pull/pan/drift/shake camera presets, and fade/wipe/circle/zoom reveal transitions. Dimensions, FPS, colors, IDs, durations and element values are validated.

## Current limits

This is an initial procedural graphics/composition prototype, not the complete engine. The MP4 renderer currently renders text, rectangles, lines and progress bars on color backgrounds; it does not yet reproduce the HTML preview camera moves/transitions, render circles, synthesize speech, generate realistic footage, import external fonts, or provide a full keyframe/timeline editor. It produces silent MP4 files. Automated FFmpeg/FFprobe smoke tests verify the supported MP4 path, but every production still needs visual review.
