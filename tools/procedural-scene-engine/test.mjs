import { mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { execFileSync } from "node:child_process";
import assert from "node:assert/strict";

const root=path.resolve(import.meta.dirname,"../..");
const temp=await mkdtemp(path.join(os.tmpdir(),"procedural-engine-"));
try {
  const out=path.join(temp,"video");
  execFileSync(process.execPath,[path.join(root,"tools/procedural-scene-engine/generate.mjs"),path.join(root,"examples/procedural-scenes/vertical-explainer.json"),out],{stdio:"pipe"});
  const html=await readFile(path.join(out,"index.html"),"utf8");
  const project=JSON.parse(await readFile(path.join(out,"project.json"),"utf8"));
  assert.equal(project.scenes.length,2);
  assert.match(html,/YOUR BODY/);
  assert.match(html,/NEEDS WATER/);
  assert.match(html,/animation-delay:3s/);
  assert.match(html,/<svg/);
  assert.match(html,/camera-push-in/);
  assert.match(html,/#68d5ff/);
  assert.match(html,/transition-wipe-left/);
  assert.match(html,/<polygon points=/);
  assert.match(html,/<linearGradient id="bg-gradient-0"/);
  assert.match(html,/stop-color="#101827"/);
  assert.match(html,/stop-color="#68d5ff"/);
  assert.match(html,/star/);
  assert.doesNotMatch(html,/<script[^>]+src=/i);
  const invalid=path.join(temp,"invalid-gradient.json");
  const bad=structuredClone(project);
  bad.theme.gradient={from:"not a color!",to:"#ffffff",angle:20};
  await writeFile(invalid,JSON.stringify(bad),"utf8");
  assert.throws(()=>execFileSync(process.execPath,[path.join(root,"tools/procedural-scene-engine/generate.mjs"),invalid,path.join(temp,"invalid-output")],{stdio:"pipe"}),/status|failed/i);
  console.log("Procedural scene engine smoke test passed.");
} finally { await rm(temp,{recursive:true,force:true}); }
