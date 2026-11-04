#!/usr/bin/env node
import { readFile } from "node:fs/promises";
import path from "node:path";

const errors = [];
const warnings = [];
const add = (list, message) => list.push(message);
const validNumber = (v) => typeof v === "number" && Number.isFinite(v);

async function main() {
  const inputArg = process.argv[2];
  if (!inputArg || inputArg === "--help" || inputArg === "-h") {
    console.log("Usage: node validate.mjs <timeline.json>");
    return;
  }
  const inputPath = path.resolve(inputArg);
  const data = JSON.parse(await readFile(inputPath, "utf8"));
  if (!data || typeof data !== "object" || Array.isArray(data)) throw new Error("Timeline root must be an object.");

  const fps = data.fps ?? 30;
  if (!validNumber(fps) || fps < 1 || fps > 120) add(errors, "fps must be a number between 1 and 120.");
  for (const dim of ["width", "height"]) {
    const v = data[dim] ?? (dim === "width" ? 1920 : 1080);
    if (!Number.isInteger(v) || v < 1 || v > 8192) add(errors, `${dim} must be an integer from 1 to 8192.`);
  }
  if (!Array.isArray(data.scenes) || data.scenes.length === 0) add(errors, "scenes must be a non-empty array.");

  const assetIds = new Set();
  for (const [i, asset] of (Array.isArray(data.assets) ? data.assets : []).entries()) {
    if (!asset || typeof asset.id !== "string" || !asset.id.trim()) add(errors, `assets[${i}] needs an id.`);
    else if (assetIds.has(asset.id)) add(errors, `Duplicate asset id: ${asset.id}`);
    else assetIds.add(asset.id);
  }

  const sceneIds = new Set();
  let maxEnd = 0;
  for (const [i, scene] of (Array.isArray(data.scenes) ? data.scenes : []).entries()) {
    if (!scene || typeof scene !== "object") { add(errors, `scenes[${i}] must be an object.`); continue; }
    if (typeof scene.id !== "string" || !scene.id.trim()) add(errors, `scenes[${i}] needs an id.`);
    else if (sceneIds.has(scene.id)) add(errors, `Duplicate scene id: ${scene.id}`);
    else sceneIds.add(scene.id);
    if (!validNumber(scene.start) || scene.start < 0) add(errors, `scenes[${i}].start must be >= 0.`);
    if (!validNumber(scene.duration) || scene.duration <= 0) add(errors, `scenes[${i}].duration must be > 0.`);
    if (validNumber(scene.start) && validNumber(scene.duration) && scene.duration > 0) {
      const end = scene.start + scene.duration;
      maxEnd = Math.max(maxEnd, end);
      if (validNumber(fps) && Math.abs(scene.start * fps - Math.round(scene.start * fps)) > 0.001) add(warnings, `Scene ${scene.id}: start is not aligned to an integer frame at ${fps} fps.`);
      if (validNumber(fps) && Math.abs(scene.duration * fps - Math.round(scene.duration * fps)) > 0.001) add(warnings, `Scene ${scene.id}: duration is not aligned to an integer frame at ${fps} fps.`);
    }
    if (scene.assetId && !assetIds.has(scene.assetId)) add(errors, `Scene ${scene.id}: unknown assetId '${scene.assetId}'.`);
  }

  const cueIds = new Set();
  for (const [i, cue] of (Array.isArray(data.audioCues) ? data.audioCues : []).entries()) {
    if (!cue || typeof cue !== "object") { add(errors, `audioCues[${i}] must be an object.`); continue; }
    if (typeof cue.id !== "string" || !cue.id.trim()) add(errors, `audioCues[${i}] needs an id.`);
    else if (cueIds.has(cue.id)) add(errors, `Duplicate audio cue id: ${cue.id}`);
    else cueIds.add(cue.id);
    if (!validNumber(cue.start) || cue.start < 0) add(errors, `audioCues[${i}].start must be >= 0.`);
    if (!validNumber(cue.duration) || cue.duration <= 0) add(errors, `audioCues[${i}].duration must be > 0.`);
    if (cue.assetId && !assetIds.has(cue.assetId)) add(errors, `Audio cue ${cue.id}: unknown assetId '${cue.assetId}'.`);
    if (cue.assetId) {
      const asset = (Array.isArray(data.assets) ? data.assets : []).find((item) => item?.id === cue.assetId);
      if (asset && asset.type && asset.type !== "audio") add(errors, `Audio cue ${cue.id}: asset '${cue.assetId}' must have type audio.`);
    }
    if (validNumber(cue.start) && validNumber(cue.duration) && cue.start + cue.duration > maxEnd + 0.001) add(errors, `Audio cue ${cue.id}: extends beyond visual composition end (${maxEnd.toFixed(3)}s).`);
    if (validNumber(fps) && validNumber(cue.start) && Math.abs(cue.start * fps - Math.round(cue.start * fps)) > 0.001) add(warnings, `Audio cue ${cue.id}: start is not aligned to an integer frame at ${fps} fps.`);
    if (validNumber(fps) && validNumber(cue.duration) && Math.abs(cue.duration * fps - Math.round(cue.duration * fps)) > 0.001) add(warnings, `Audio cue ${cue.id}: duration is not aligned to an integer frame at ${fps} fps.`);
    if (cue.gain !== undefined && (!validNumber(cue.gain) || cue.gain < 0 || cue.gain > 4)) add(errors, `Audio cue ${cue.id}: gain must be between 0 and 4.`);
    if (cue.role && !["narration", "dialogue", "music", "sfx", "ambience"].includes(cue.role)) add(warnings, `Audio cue ${cue.id}: unrecognized role '${cue.role}'.`);
  }

  console.log(`Timeline: ${data.title ?? path.basename(inputPath)}`);
  console.log(`FPS: ${fps} | Scenes: ${Array.isArray(data.scenes) ? data.scenes.length : 0} | Assets: ${assetIds.size} | Audio cues: ${Array.isArray(data.audioCues) ? data.audioCues.length : 0} | Visual duration: ${maxEnd.toFixed(3)}s`);
  warnings.forEach((m) => console.warn(`WARNING: ${m}`));
  errors.forEach((m) => console.error(`ERROR: ${m}`));
  console.log(`Warnings: ${warnings.length} | Errors: ${errors.length}`);
  if (errors.length) process.exitCode = 1;
}
main().catch((error) => { console.error(`Validation failed: ${error.message}`); process.exitCode = 1; });
