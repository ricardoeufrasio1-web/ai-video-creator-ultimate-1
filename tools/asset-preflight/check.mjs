#!/usr/bin/env node
import { readFile, stat } from "node:fs/promises";
import path from "node:path";

const allowedTypes = new Set(["image", "video", "audio", "font", "graphic", "document", "other"]);
const errors = [];
const warnings = [];

function issue(list, message) { list.push(message); }
function isInside(parent, child) {
  const relative = path.relative(parent, child);
  return relative === "" || (!relative.startsWith("..") && !path.isAbsolute(relative));
}

async function main() {
  const arg = process.argv[2];
  if (!arg || arg === "--help" || arg === "-h") {
    console.log("Usage: node check.mjs <asset-manifest.json>");
    return;
  }
  const manifestPath = path.resolve(arg);
  const raw = await readFile(manifestPath, "utf8");
  const manifest = JSON.parse(raw);
  if (!manifest || typeof manifest !== "object" || !Array.isArray(manifest.assets)) {
    throw new Error("Manifest must be an object containing an 'assets' array.");
  }
  const base = path.dirname(manifestPath);
  const ids = new Set();

  for (const [index, asset] of manifest.assets.entries()) {
    const label = `assets[${index}]`;
    if (!asset || typeof asset !== "object" || Array.isArray(asset)) {
      issue(errors, `${label}: expected an object.`);
      continue;
    }
    if (typeof asset.id !== "string" || !asset.id.trim()) issue(errors, `${label}: missing id.`);
    else if (ids.has(asset.id)) issue(errors, `${label}: duplicate id '${asset.id}'.`);
    else ids.add(asset.id);

    if (!allowedTypes.has(asset.type)) issue(errors, `${label}: type must be one of ${[...allowedTypes].join(", ")}.`);
    if (typeof asset.path !== "string" || !asset.path.trim()) {
      issue(errors, `${label}: missing local path.`);
    } else {
      const resolved = path.resolve(base, asset.path);
      if (!isInside(base, resolved)) issue(errors, `${label}: path escapes the manifest directory: ${asset.path}`);
      else {
        try {
          const info = await stat(resolved);
          if (!info.isFile()) issue(errors, `${label}: path is not a regular file: ${asset.path}`);
        } catch {
          issue(errors, `${label}: file not found: ${asset.path}`);
        }
      }
    }

    if (!asset.source || typeof asset.source !== "string") issue(warnings, `${label}: source/source URL is not documented.`);
    if (!asset.license || typeof asset.license !== "string") issue(warnings, `${label}: license/rights basis is not documented.`);
    if (asset.commercialUse !== true && asset.commercialUse !== false) issue(warnings, `${label}: set commercialUse to true or false after checking the terms.`);
    if (["person", "voice"].includes(asset.subjectType) && asset.consentConfirmed !== true) {
      issue(warnings, `${label}: confirm documented consent/release for person or voice assets.`);
    }
  }

  console.log(`Assets checked: ${manifest.assets.length}`);
  for (const warning of warnings) console.warn(`WARNING: ${warning}`);
  for (const error of errors) console.error(`ERROR: ${error}`);
  console.log(`Warnings: ${warnings.length} | Errors: ${errors.length}`);
  if (errors.length) process.exitCode = 1;
}

main().catch((error) => {
  console.error(`Preflight failed: ${error.message}`);
  process.exitCode = 1;
});
