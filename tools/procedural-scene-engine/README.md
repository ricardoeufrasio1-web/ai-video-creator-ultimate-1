# Procedural Scene Engine — first executable prototype

This dependency-free Node.js tool creates a self-contained HTML/SVG composition from JSON. It generates original vector shapes, typography, simple diagrams and basic entrance animation without calling remote image or video generation services.

## Run

```bash
node tools/procedural-scene-engine/generate.mjs examples/procedural-scenes/vertical-explainer.json ./output/vertical-explainer
```

Open the generated index.html in a modern browser to preview it. The output contains inline SVG, CSS and JavaScript; it makes no network requests.

## Supported elements

- text
- rect
- circle
- line
- bar

Scenes support duration, background, accent, accessible description and simple rise/slide/pop entrance presets. Dimensions, FPS, colors, IDs, durations and element values are validated.

## Current limits

This is an initial procedural graphics/composition prototype, not the complete engine. It does not yet render MP4, synthesize speech, generate realistic footage, import external fonts, or provide a full keyframe/timeline editor. Browser preview animation is not proof of deterministic frame-accurate MP4 rendering. The MP4 renderer integration and automated preview/render QA are subsequent milestones.
