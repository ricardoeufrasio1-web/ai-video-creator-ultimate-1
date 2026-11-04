# Full timeline and renderer integration plan

## Current starter boundary

The existing project generator creates a simple HTML title-card composition from a deliberately small JSON schema. The timeline validator checks a more general scene/timing structure, but the generator does not yet translate that general timeline into a full media composition. No actual MP4 render is included in the current CI pipeline.

## Target architecture

1. **Creative brief:** normalized user intent, constraints, approvals, budget and output target.
2. **Asset manifest:** stable IDs and verified local/host file references, provenance and rights.
3. **Production timeline:** scene/track model with frame-accurate start/end, media in/out, transitions, narration cues, music/SFX and captions.
4. **Composition adapter:** maps the portable timeline into a renderer-specific project (HyperFrames first, optional Remotion/other adapters).
5. **Render runner:** pinned runtime, installed renderer and FFmpeg, isolated job directory, logs, cancellation and output storage.
6. **Output verifier:** file existence/size, FFprobe streams, duration, dimensions, FPS, plus frame extraction and audio review when supported.
7. **Delivery packager:** MP4, editable source, manifest, captions, thumbnail and publishing metadata.

## Implementation sequence

- Define and version the portable timeline schema.
- Add a deterministic timeline-to-HyperFrames composition generator.
- Add a small fixture with generated-by-code graphics and a licensed/public-domain audio fixture (or silent video) so CI can render without paid providers.
- Pin renderer/runtime versions and test the actual CLI against current upstream documentation.
- Render the fixture in CI and upload the MP4 as a workflow artifact.
- Add provider adapters separately; keep credentials out of repository and test mocks in CI.
- Add a host runner or cloud job service only after the local/CI render is reproducible.

## Acceptance criteria

A render feature is not complete until CI or a reproducible runner:
- builds the composition from the portable timeline;
- executes a real renderer and creates an MP4;
- confirms non-zero file size and expected streams with FFprobe;
- extracts representative frames;
- stores the MP4 and logs as downloadable artifacts;
- records renderer and dependency versions.

A sample FFprobe JSON file is a fixture, not evidence that a real video was rendered.
