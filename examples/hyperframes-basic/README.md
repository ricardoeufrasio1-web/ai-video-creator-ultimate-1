# HyperFrames basic composition example

This is a minimal, editable HTML composition for testing the HyperFrames workflow. It is an original example, not copied from the upstream repository.

## Requirements

- Node.js 22 or newer
- npm/npx
- FFmpeg
- A compatible browser/runtime supported by the installed HyperFrames version

## Run

From this repository's root, scaffold a fresh HyperFrames project using the current CLI:

```bash
npx hyperframes init demo-video --example blank --non-interactive
```

Copy `index.html` from this example into the generated `demo-video/` directory, replacing its starter composition. Then:

```bash
cd demo-video
npx hyperframes doctor
npx hyperframes preview
npx hyperframes lint
npx hyperframes check
npx hyperframes render --output output.mp4
```

The example loads GSAP from a CDN. For offline or reproducible production, install/pin the animation dependency locally and update the script reference according to the project's dependency setup.

Check `npx hyperframes <command> --help` because supported flags can change between CLI versions.
