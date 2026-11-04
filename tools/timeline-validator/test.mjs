#!/usr/bin/env node
import assert from "node:assert/strict";
import { mkdtemp, rm } from "node:fs/promises";
import { writeFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import { spawnSync } from "node:child_process";

const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), "../..");
const validator = path.join(root, "tools/timeline-validator/validate.mjs");
const temp = await mkdtemp(path.join(os.tmpdir(), "timeline-validation-"));
const base = {
  title: "validator test", fps: 30, width: 1080, height: 1920,
  assets: [{ id: "voice", type: "audio", path: "voice.wav" }],
  scenes: [{ id: "scene-1", start: 0, duration: 3 }],
  audioCues: [{ id: "cue-1", assetId: "voice", role: "narration", start: 0, duration: 3 }]
};
function run(data) {
  const file = path.join(temp, "case.json");
  writeFileSync(file, JSON.stringify(data));
  return spawnSync(process.execPath, [validator, file], { encoding: "utf8" });
}
try {
  let result = await run(base);
  assert.equal(result.status, 0, result.stderr || result.stdout);

  result = await run({ ...base, audioCues: [{ ...base.audioCues[0], start: 2.5, duration: 1 }] });
  assert.notEqual(result.status, 0, "cue extending beyond visual end must fail");
  assert.match(result.stderr, /extends beyond visual composition end/);

  result = await run({ ...base, assets: [{ id: "voice", type: "video", path: "clip.mp4" }] });
  assert.notEqual(result.status, 0, "audio cue cannot reference a video asset");
  assert.match(result.stderr, /must have type audio/);

  result = await run({ ...base, audioCues: [{ ...base.audioCues[0], gain: 5 }] });
  assert.notEqual(result.status, 0, "gain above 4 must fail");
  assert.match(result.stderr, /gain must be between 0 and 4/);
  console.log("Timeline validator tests passed (valid cue, cue overflow, asset type, gain range).");
} finally {
  await rm(temp, { recursive: true, force: true });
}
