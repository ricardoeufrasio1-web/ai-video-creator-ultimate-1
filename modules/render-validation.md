# Render Validation

A successful render command is not the same as a verified deliverable. Validate the actual output file after rendering.

## 1. Minimum technical checks

Use a media inspector such as FFprobe when available. Confirm:
- output file exists and is non-empty;
- at least one video stream exists;
- width, height, aspect ratio, and frame rate match the delivery brief;
- duration is within the expected tolerance;
- audio stream exists when required;
- codecs and container are accepted by the destination workflow.

Example inspection command (requires FFmpeg/FFprobe installed):

```bash
ffprobe -v error -show_format -show_streams -of json output.mp4 > output.ffprobe.json
```

Pass the resulting JSON to the render-preflight checker documented in `tools/render-preflight/README.md`.

## 2. Visual inspection

Watch the complete file at normal speed. Inspect the opening, ending, every scene boundary, transitions, text, and any critical action. Look for:
- black frames or gaps;
- frozen frames, unintended duplicates, or dropped-looking motion;
- wrong crop, aspect ratio, or safe-area placement;
- image drift, morphing, continuity breaks, and incorrect props;
- unreadable or misspelled graphics;
- watermark or placeholder assets that were not approved.

Automated black-frame detection may help, but it can produce false positives and cannot replace viewing.

## 3. Audio inspection

Listen on headphones and a phone speaker. Check:
- missing, muted, or truncated dialogue;
- synchronization drift;
- clipping, distortion, clicks, abrupt edits, and excessive noise;
- music masking speech;
- unintended silence or audio continuing after picture;
- correct language, pronunciation, and approved script.

Use waveform/peak and silence analysis as diagnostics, not as proof of quality.

## 4. Delivery package

Include the final media, project/timeline source, asset manifest, and a short delivery note. State dimensions, FPS, duration, audio status, and any known limitations. Keep source assets and licensed materials organized.

## 5. Honest status reporting

Distinguish clearly between:
- **Generated:** a render process produced a file.
- **Structurally checked:** metadata and project files passed automated checks.
- **Visually reviewed:** the complete video was watched.
- **Audio reviewed:** the complete soundtrack was listened to.
- **Approved:** the responsible reviewer accepted the deliverable.

Never claim visual or audio QA based only on metadata. Never claim a render exists unless the file has actually been produced and verified.
