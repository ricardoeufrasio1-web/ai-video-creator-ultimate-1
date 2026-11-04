# Troubleshooting

## The project generator says the output folder already exists
Choose a new, empty output directory. The generator intentionally refuses to overwrite existing work.

## The project generator works but no MP4 appears
The generator only creates a starter HTML composition and copies the JSON input. It does not render video. Install and configure a supported renderer separately, then follow its current official instructions.

## HyperFrames commands differ from the documentation
Check the installed version and run its help/diagnostic commands. CLI options and runtime requirements can change. Do not assume a command copied from an older release still applies.

## Asset preflight reports missing files
The manifest paths are resolved relative to the manifest file. Put the media files in the expected locations or update the manifest paths. The example manifest contains placeholders and is not a ready-to-render asset pack.

## Timeline validation reports frame-alignment warnings
At the selected FPS, a time boundary must map to an integer frame. Adjust start times/durations to frame increments (for example, 1/30 second at 30 FPS) or review whether the warning is acceptable for the target renderer.

## Render preflight fails or warns
Confirm the JSON came from FFprobe inspecting the actual final file. Ensure it includes `streams` and `format` metadata. The checker only reads metadata; it cannot repair a video or detect all image/audio defects.

## Output has the wrong aspect ratio or black bars
Check composition dimensions, source aspect ratios, crop/contain behavior, and final encoder settings. Inspect the actual rendered frames, not only the project JSON.

## Narration and action do not match
Rebuild the cue sheet from the final approved voice track. Adjust visual timing to the spoken action, then re-render and review the complete video. Do not stretch or speed up speech without checking intelligibility.

## Audio sounds clipped or masked
Check source peaks, gain staging, music level, limiter behavior, and export settings. Listen to the final encoded file on headphones and a phone speaker.
