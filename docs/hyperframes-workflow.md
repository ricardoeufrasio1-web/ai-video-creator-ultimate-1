# HyperFrames-first workflow

HyperFrames is the preferred composition and rendering workflow for this skill. It is an external dependency and is not bundled in this repository.

## Current documented prerequisites

The current HyperFrames quickstart documents Node.js 22+ and FFmpeg for local MP4 rendering. The CLI's `doctor` command checks the local environment. Confirm the requirements for the exact version installed and operating system before setup.

Official references:
- [Quickstart](https://hyperframes.app/docs/1-startup/2-quickstart)
- [CLI](https://hyperframes.app/docs/5-packages/cli)
- [Rendering](https://hyperframes.app/docs/3-guides/4-rendering)
- [HyperFrames repository](https://github.com/heygen-com/hyperframes)

## Create a project

Use the current CLI. A documented non-interactive starter command is:

```bash
npx hyperframes init my-video --example blank --non-interactive
```

Exact accepted flags can vary by release. Run `npx hyperframes init --help` to confirm.

A typical project contains a root composition such as `index.html`, metadata, a compositions folder, and an assets folder. Treat the generated project as authoritative for its installed version.

## Everyday project loop

```bash
npx hyperframes doctor
npx hyperframes preview
npx hyperframes lint
npx hyperframes check
npx hyperframes snapshot --at 0,2,5
npx hyperframes render --output output.mp4
```

Run commands from the project directory. Check `npx hyperframes <command> --help` for exact flags. Adapt snapshot times to the actual composition duration.

## Composition structure

The documented HTML composition model uses a root element with a composition ID and canvas dimensions. Timed elements use clip metadata such as start time, duration, and track index. Animations must be seekable; GSAP timelines are paused and registered in `window.__timelines` under the matching composition ID.

See `examples/hyperframes-basic/` for an original minimal composition. It loads GSAP from a CDN for demonstration only. For production, pin dependencies locally and avoid network requests during rendering.

## Production principles

- Use explicit timing and a single project frame rate.
- Keep media local and validate all paths before render.
- Use deterministic, seekable animation; avoid wall-clock time and unseeded randomness.
- Run diagnostics, lint, browser/layout checks, preview, and boundary snapshots.
- Inspect the final MP4 with media metadata tools and visual playback.
- Keep source HTML, assets, manifest, and export settings with the project.

## Docker and reproducibility

HyperFrames documents Docker rendering as an option for more reproducible output. Use it only when Docker is available and the current CLI version supports the required flags. Do not make Docker a prerequisite for every user.

## Fallback

If the user is on a phone without access to a compatible remote/desktop runtime, prepare the project and provide exact next steps. Do not claim to have run a local render.
