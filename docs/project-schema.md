# Project JSON schema (starter)

The starter generator accepts a deliberately small, text-only project format. It creates a HyperFrames-oriented HTML composition; it does not generate media assets or render a video.

## Minimal example

```json
{
  "title": "A short introduction",
  "compositionId": "intro-demo",
  "width": 1080,
  "height": 1920,
  "fps": 30,
  "background": "#101722",
  "scenes": [
    {
      "id": "opening",
      "duration": 3,
      "eyebrow": "A QUICK GUIDE",
      "title": "Start with one clear idea",
      "subtitle": "A simple, focused opening."
    },
    {
      "id": "closing",
      "duration": 2,
      "title": "Make it memorable",
      "subtitle": "End with one useful takeaway."
    }
  ]
}
```

## Fields

| Field | Type | Rules |
|---|---|---|
| title | string | Required, non-empty |
| compositionId | string | Optional; normalized to a safe identifier if omitted |
| width, height | integer | Optional; defaults 1920x1080; 1–8192 |
| fps | number | Optional; defaults 30; 1–120 |
| background | string | Optional CSS color value; defaults to a dark neutral |
| scenes | array | Required; at least one scene |
| scenes[].id | string | Required, unique |
| scenes[].duration | number | Required, positive seconds |
| scenes[].eyebrow | string | Optional |
| scenes[].title | string | Required, non-empty |
| scenes[].subtitle | string | Optional |

Scenes are laid out sequentially. Each scene is a single title-card clip with a cut between scenes. The generator derives start times from cumulative durations and rounds boundaries to the selected frame rate. The current starter does not support external image/audio assets, custom transitions, multiple tracks, or voice synchronization.

## Validation and security
The generator validates types, ranges, IDs, and text before writing. Text is HTML-escaped. The output directory is resolved before writing. Do not place secrets or executable code in project JSON.

For a more complete production timeline, use the timeline orchestration and asset-manifest modules; this starter schema is intentionally narrower than the full workflow.
