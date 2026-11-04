# Timeline validator

Validate a renderer-neutral timeline JSON before creating an edit. Requires Node.js 22+ and uses built-in modules only.

## Run

```bash
node tools/timeline-validator/validate.mjs examples/timelines/short-form.json
```

The validator checks project FPS/dimensions, unique scene and cue IDs, positive durations, frame alignment, scene bounds, cue ranges, and references to declared asset IDs. Audio cues that extend past the visual composition, reference a non-audio asset, or use an out-of-range gain are blocking errors. Sub-frame cue timing is reported as a warning. It prints warnings and errors separately; blocking errors return a non-zero exit code.

Run focused regression tests with:

```bash
node tools/timeline-validator/test.mjs
```

This is structural validation only. It does not inspect media codecs, listen to audio, prove synchronization, or render a video.

## Schema
See [the sample timeline](../../examples/timelines/short-form.json) and [timeline orchestration](../../modules/timeline-orchestration.md).
