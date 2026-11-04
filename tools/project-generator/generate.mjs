#!/usr/bin/env node
import { readFile, mkdir, writeFile, copyFile } from "node:fs/promises";
import path from "node:path";
import { pathToFileURL } from "node:url";

function fail(message) {
  console.error(`Error: ${message}`);
  process.exitCode = 1;
}

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, (char) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
  })[char]);
}

function safeId(value) {
  return String(value).toLowerCase().replace(/[^a-z0-9_-]+/g, "-").replace(/^-+|-+$/g, "") || "video-project";
}

function validate(project) {
  const errors = [];
  if (!project || typeof project !== "object" || Array.isArray(project)) return ["Root JSON value must be an object."];
  if (typeof project.title !== "string" || !project.title.trim()) errors.push("'title' must be a non-empty string.");
  for (const key of ["width", "height"]) {
    if (project[key] !== undefined && (!Number.isInteger(project[key]) || project[key] < 1 || project[key] > 8192)) errors.push(`'${key}' must be an integer from 1 to 8192.`);
  }
  if (project.fps !== undefined && (typeof project.fps !== "number" || !Number.isFinite(project.fps) || project.fps < 1 || project.fps > 120)) errors.push("'fps' must be a number from 1 to 120.");
  if (project.background !== undefined && (typeof project.background !== "string" || !/^(#[0-9a-fA-F]{3,8}|[a-zA-Z]+)$/.test(project.background))) errors.push("'background' must be a simple CSS color (hex or named color).");
  if (!Array.isArray(project.scenes) || project.scenes.length === 0) errors.push("'scenes' must be a non-empty array.");
  const ids = new Set();
  for (const [index, scene] of (Array.isArray(project.scenes) ? project.scenes : []).entries()) {
    if (!scene || typeof scene !== "object" || Array.isArray(scene)) { errors.push(`scenes[${index}] must be an object.`); continue; }
    if (typeof scene.id !== "string" || !scene.id.trim()) errors.push(`scenes[${index}].id is required.`);
    else if (ids.has(scene.id)) errors.push(`Duplicate scene id: ${scene.id}`);
    else ids.add(scene.id);
    if (typeof scene.title !== "string" || !scene.title.trim()) errors.push(`scenes[${index}].title must be a non-empty string.`);
    if (typeof scene.duration !== "number" || !Number.isFinite(scene.duration) || scene.duration <= 0 || scene.duration > 3600) errors.push(`scenes[${index}].duration must be greater than 0 and at most 3600 seconds.`);
    for (const field of ["eyebrow", "subtitle"]) if (scene[field] !== undefined && typeof scene[field] !== "string") errors.push(`scenes[${index}].${field} must be a string.`);
  }
  return errors;
}

function buildHtml(project) {
  const width = project.width ?? 1920;
  const height = project.height ?? 1080;
  const fps = project.fps ?? 30;
  const compositionId = safeId(project.compositionId ?? project.title);
  let cursorFrames = 0;
  const scenes = project.scenes.map((scene, index) => {
    const startFrame = cursorFrames;
    const durationFrames = Math.max(1, Math.round(scene.duration * fps));
    cursorFrames += durationFrames;
    const start = (startFrame / fps).toFixed(6);
    const duration = (durationFrames / fps).toFixed(6);
    const id = safeId(scene.id);
    const eyebrow = scene.eyebrow ? `<div class="eyebrow">${escapeHtml(scene.eyebrow)}</div>` : "";
    const subtitle = scene.subtitle ? `<p class="subtitle">${escapeHtml(scene.subtitle)}</p>` : "";
    return `    <section class="scene clip" id="scene-${id}" data-start="${start}" data-duration="${duration}" data-track-index="0">
      ${eyebrow}
      <h1 class="headline">${escapeHtml(scene.title)}</h1>
      ${subtitle}
    </section>`;
  }).join("\n");
  const total = (cursorFrames / fps).toFixed(3);
  return `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${escapeHtml(project.title)}</title>
<style>
*{box-sizing:border-box}html,body{margin:0;width:100%;height:100%;overflow:hidden}
body{background:${project.background ?? "#101722"};color:#fff;font-family:Inter,Arial,sans-serif}
#root{position:relative;width:${width}px;height:${height}px;overflow:hidden;background:${project.background ?? "#101722"}}
.scene{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:8%;opacity:0}
.eyebrow{color:#9ed9ff;font-size:${Math.round(width*0.022)}px;letter-spacing:.22em;font-weight:700;margin-bottom:2.5%}
.headline{font-size:${Math.round(width*0.065)}px;line-height:1.08;letter-spacing:-.035em;font-weight:800;margin:0;max-width:90%}
.subtitle{font-size:${Math.round(width*0.026)}px;line-height:1.4;color:#c6d0dc;max-width:78%;margin:3% auto 0}
</style>
</head>
<body>
<div id="root" data-composition-id="${compositionId}" data-start="0" data-width="${width}" data-height="${height}" data-fps="${fps}" data-duration="${total}">
${scenes}
</div>
<!-- Demo dependency: vendor and pin GSAP locally for deterministic/offline production. -->
<script src="https://cdn.jsdelivr.net/npm/gsap@3/dist/gsap.min.js"></script>
<script>
(() => {
  const timeline = gsap.timeline({ paused: true });
  document.querySelectorAll(".scene").forEach((scene) => {
    const start = Number(scene.dataset.start);
    const duration = Number(scene.dataset.duration);
    timeline.set(scene, { opacity: 1 }, start);
    timeline.to(scene, { opacity: 0, duration: 0.001 }, start + duration);
  });
  window.__timelines = window.__timelines || {};
  window.__timelines["${compositionId}"] = timeline;
})();
</script>
</body>
</html>
`;
}

async function main() {
  const [inputArg, outputArg] = process.argv.slice(2);
  if (!inputArg || !outputArg || inputArg === "--help" || inputArg === "-h") {
    console.log("Usage: node generate.mjs <project.json> <new-output-directory>");
    return;
  }
  const input = path.resolve(inputArg);
  const output = path.resolve(outputArg);
  const raw = await readFile(input, "utf8");
  const project = JSON.parse(raw);
  const errors = validate(project);
  if (errors.length) throw new Error(errors.join("\n"));
  if (output === path.dirname(output) || output === input || output.startsWith(input + path.sep)) throw new Error("Choose a separate output directory.");
  await mkdir(path.dirname(output), { recursive: true });
  await mkdir(output, { recursive: false });
  await writeFile(path.join(output, "index.html"), buildHtml(project), "utf8");
  await copyFile(input, path.join(output, "project.json"));
  console.log(`Generated ${path.join(output, "index.html")}`);
  console.log(`Composition: ${safeId(project.compositionId ?? project.title)} | scenes: ${project.scenes.length} | duration: ${project.scenes.reduce((sum, scene) => sum + Math.round(scene.duration * (project.fps ?? 30)), 0) / (project.fps ?? 30)}s`);
}

main().catch((error) => fail(error.message));
