#!/usr/bin/env node
import { readFile } from "node:fs/promises";

function argValue(flag) {
  const index = process.argv.indexOf(flag);
  return index >= 0 ? process.argv[index + 1] : undefined;
}
function positiveNumber(value, flag) {
  if (value === undefined) return undefined;
  const number = Number(value);
  if (!Number.isFinite(number) || number <= 0) {
    throw new Error(`Invalid value for ${flag}: expected a positive number.`);
  }
  return number;
}
function rational(value) {
  if (typeof value !== "string") return NaN;
  const [numerator, denominator] = value.split("/").map(Number);
  if (!Number.isFinite(numerator)) return NaN;
  return denominator === undefined ? numerator : denominator === 0 ? NaN : numerator / denominator;
}

const input = process.argv[2];
if (!input || input.startsWith("--")) {
  console.error("Usage: node check-render.mjs <ffprobe.json> [--expect-width N] [--expect-height N] [--expect-fps N] [--expect-duration SEC] [--require-audio]");
  process.exit(2);
}

try {
  const metadata = JSON.parse(await readFile(input, "utf8"));
  const streams = Array.isArray(metadata.streams) ? metadata.streams : [];
  const video = streams.find((stream) => stream.codec_type === "video");
  const audio = streams.filter((stream) => stream.codec_type === "audio");
  const errors = [];
  const warnings = [];
  const expectedWidth = positiveNumber(argValue("--expect-width"), "--expect-width");
  const expectedHeight = positiveNumber(argValue("--expect-height"), "--expect-height");
  const expectedFps = positiveNumber(argValue("--expect-fps"), "--expect-fps");
  const expectedDuration = positiveNumber(argValue("--expect-duration"), "--expect-duration");
  const requireAudio = process.argv.includes("--require-audio");

  if (!video) errors.push("No video stream found.");
  if (video) {
    if (!(Number(video.width) > 0 && Number(video.height) > 0)) errors.push("Video dimensions are missing or invalid.");
    if (expectedWidth && Number(video.width) !== expectedWidth) errors.push(`Width mismatch: expected ${expectedWidth}, got ${video.width}.`);
    if (expectedHeight && Number(video.height) !== expectedHeight) errors.push(`Height mismatch: expected ${expectedHeight}, got ${video.height}.`);
    const fps = rational(video.avg_frame_rate || video.r_frame_rate);
    if (!Number.isFinite(fps) || fps <= 0) warnings.push("Frame rate is missing or could not be parsed.");
    else if (expectedFps && Math.abs(fps - expectedFps) > 0.02) errors.push(`FPS mismatch: expected ${expectedFps}, got ${fps.toFixed(3)}.`);
  }
  if (requireAudio && audio.length === 0) errors.push("Audio was required but no audio stream was found.");
  if (!requireAudio && audio.length === 0) warnings.push("No audio stream found.");
  const duration = Number(metadata.format?.duration ?? video?.duration);
  if (!Number.isFinite(duration) || duration <= 0) warnings.push("Duration is missing or invalid.");
  else if (expectedDuration && Math.abs(duration - expectedDuration) > 0.5) errors.push(`Duration mismatch: expected about ${expectedDuration}s, got ${duration.toFixed(3)}s (tolerance 0.5s).`);

  const report = {
    status: errors.length ? "FAIL" : warnings.length ? "PASS_WITH_WARNINGS" : "PASS",
    file: input,
    video: video ? { codec: video.codec_name ?? null, width: video.width ?? null, height: video.height ?? null, fps: Number.isFinite(rational(video.avg_frame_rate || video.r_frame_rate)) ? rational(video.avg_frame_rate || video.r_frame_rate) : null } : null,
    audioStreams: audio.length,
    durationSeconds: Number.isFinite(duration) ? duration : null,
    errors,
    warnings,
    limitation: "Metadata-only check; does not inspect decoded frames or listen to audio."
  };
  console.log(JSON.stringify(report, null, 2));
  if (errors.length) process.exitCode = 1;
} catch (error) {
  console.error(`Render preflight failed: ${error.message}`);
  process.exitCode = 1;
}
