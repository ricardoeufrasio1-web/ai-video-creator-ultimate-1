#!/usr/bin/env node
import { readFile, mkdir, writeFile, copyFile } from "node:fs/promises";
import path from "node:path";

const clamp = (n, min, max) => Math.min(max, Math.max(min, n));
const esc = (v) => String(v).replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const id = (v) => String(v).toLowerCase().replace(/[^a-z0-9_-]+/g,"-").replace(/^-+|-+$/g,"") || "scene";
const color = (v, fallback) => typeof v === "string" && /^(#[0-9a-f]{3,8}|[a-z]{3,20})$/i.test(v) ? v : fallback;

function validate(p) {
  const e=[];
  if (!p || typeof p!=="object" || Array.isArray(p)) return ["Project must be a JSON object."];
  if (typeof p.title!=="string" || !p.title.trim()) e.push("title must be a non-empty string.");
  for (const k of ["width","height"]) if (p[k]!==undefined && (!Number.isInteger(p[k]) || p[k]<64 || p[k]>8192)) e.push(k+" must be an integer from 64 to 8192.");
  if (p.fps!==undefined && (!Number.isFinite(p.fps) || p.fps<1 || p.fps>120)) e.push("fps must be from 1 to 120.");
  if (!Array.isArray(p.scenes) || !p.scenes.length) e.push("scenes must be a non-empty array.");
  const seen=new Set();
  for (const [i,s] of (Array.isArray(p.scenes)?p.scenes:[]).entries()) {
    if (!s || typeof s!=="object" || Array.isArray(s)) { e.push("scenes["+i+"] must be an object."); continue; }
    if (typeof s.id!=="string" || !s.id.trim()) e.push("scenes["+i+"].id is required.");
    else if (seen.has(s.id)) e.push("Duplicate scene id: "+s.id); else seen.add(s.id);
    if (typeof s.duration!=="number" || !Number.isFinite(s.duration) || s.duration<=0 || s.duration>600) e.push("scenes["+i+"].duration must be >0 and <=600 seconds.");
    if (!Array.isArray(s.elements) || !s.elements.length) e.push("scenes["+i+"].elements must contain at least one element.");
    for (const [j,x] of (Array.isArray(s.elements)?s.elements:[]).entries()) {
      if (!x || typeof x!=="object") { e.push("Invalid element at scene "+i+", index "+j); continue; }
      if (!["text","rect","circle","line","bar"].includes(x.type)) e.push("Unsupported element type at scene "+i+", index "+j+".");
      if (x.text!==undefined && typeof x.text!=="string") e.push("Element text must be a string.");
      for (const k of ["x","y","width","height","radius","value"]) if (x[k]!==undefined && (!Number.isFinite(x[k]) || Math.abs(x[k])>100000)) e.push("Invalid numeric "+k+" at scene "+i+", index "+j+".");
    }
  }
  return e;
}
function renderElement(x, w, h, index) {
  const xx=x.x??w/2, yy=x.y??h/2, fill=color(x.fill,"#68d5ff"), opacity=clamp(x.opacity??1,0,1);
  const common='fill="'+fill+'" opacity="'+opacity+'"';
  if (x.type==="text") {
    const size=clamp(x.size??Math.round(w*.06),8,Math.round(w*.3));
    const anchor=x.align==="left"?"start":x.align==="right"?"end":"middle";
    return '<text x="'+xx+'" y="'+yy+'" text-anchor="'+anchor+'" dominant-baseline="middle" font-size="'+size+'" font-weight="'+clamp(x.weight??750,100,900)+'" fill="'+color(x.fill,"#ffffff")+'" class="element enter e'+index+'">'+esc(x.text??"")+'</text>';
  }
  if (x.type==="rect") return '<rect x="'+xx+'" y="'+yy+'" width="'+clamp(x.width??240,1,w*2)+'" height="'+clamp(x.height??120,1,h*2)+'" rx="'+clamp(x.radius??12,0,200)+'" '+common+' class="element enter e'+index+'"/>';
  if (x.type==="circle") return '<circle cx="'+xx+'" cy="'+yy+'" r="'+clamp(x.radius??80,1,Math.max(w,h))+'" '+common+' class="element enter e'+index+'"/>';
  if (x.type==="line") return '<path d="M '+xx+' '+yy+' l '+(x.width??220)+' '+(x.height??0)+'" fill="none" stroke="'+fill+'" stroke-width="'+clamp(x.strokeWidth??8,1,100)+'" stroke-linecap="round" class="element enter e'+index+'"/>';
  const bw=clamp(x.width??w*.6,1,w), bh=clamp(x.height??28,1,h), value=clamp(x.value??.7,0,1);
  return '<g class="element enter e'+index+'"><rect x="'+xx+'" y="'+yy+'" width="'+bw+'" height="'+bh+'" rx="'+(bh/2)+'" fill="'+color(x.track,"#334155")+'"/><rect x="'+xx+'" y="'+yy+'" width="'+(bw*value)+'" height="'+bh+'" rx="'+(bh/2)+'" fill="'+fill+'"/></g>';
}
function build(p) {
  const w=p.width??1080,h=p.height??1920,fps=p.fps??30,bg=color(p.background,"#101827"),accent=color(p.accent,"#68d5ff");
  let cursor=0;
  const scenes=p.scenes.map((s,i)=>{
    const dur=s.duration,start=cursor; cursor+=dur;
    const elements=s.elements.map(renderElement.bind(null)).map((fn)=>fn); // replaced below for explicit scene dimensions
    const body=s.elements.map((el,j)=>renderElement(el,w,h,j)).join("\n");
    const enter=s.animation==="pop"?"pop":s.animation==="slide"?"slide":"rise";
    return '<section class="scene '+enter+'" id="scene-'+id(s.id)+'" style="--scene-bg:'+color(s.background,bg)+';--accent:'+color(s.accent,accent)+';--start:'+start+'s;--duration:'+dur+'s;--index:'+i+'"><svg viewBox="0 0 '+w+' '+h+'" role="img" aria-label="'+esc(s.description??s.title??"Animated scene")+'" xmlns="http://www.w3.org/2000/svg"><rect width="'+w+'" height="'+h+'" fill="var(--scene-bg)"/>'+body+'</svg></section>';
  }).join("\n");
  return '<!doctype html><html lang="'+esc(p.language??"en")+'"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+esc(p.title)+'</title><style>*{box-sizing:border-box}html,body{margin:0;width:100%;height:100%;overflow:hidden;background:#05070b}#stage{position:relative;width:'+w+'px;height:'+h+'px;overflow:hidden;background:'+bg+'}.scene{position:absolute;inset:0;opacity:0;animation:scene-in '+cursor+'s linear both;animation-delay:0s}.scene svg{width:100%;height:100%;display:block}.element{transform-box:fill-box;transform-origin:center}.enter{animation:element-in .7s cubic-bezier(.2,.8,.2,1) both}.rise .e0{animation-delay:.12s}.rise .e1{animation-delay:.28s}.rise .e2{animation-delay:.44s}.rise .e3{animation-delay:.6s}.slide .element{animation-name:slide-in}.pop .element{animation-name:pop-in}@keyframes element-in{from{opacity:0;transform:translateY(38px) scale(.96)}to{opacity:1;transform:translateY(0) scale(1)}}@keyframes slide-in{from{opacity:0;transform:translateX(90px)}to{opacity:1;transform:translateX(0)}}@keyframes pop-in{0%{opacity:0;transform:scale(.65)}75%{opacity:1;transform:scale(1.06)}100%{transform:scale(1)}}@keyframes scene-in{0%{opacity:0}1%,99%{opacity:1}100%{opacity:0}}</style></head><body><main id="stage" data-duration="'+cursor+'" data-fps="'+fps+'">'+scenes+'</main><script>/* Self-contained procedural preview. Scene animation is a visual preview; MP4 export requires a compatible local browser renderer. */</script></body></html>';
}
async function main(){
 const [inputArg,outArg]=process.argv.slice(2);
 if(!inputArg||!outArg||inputArg==="--help"){console.log("Usage: node tools/procedural-scene-engine/generate.mjs <project.json> <new-output-directory>");return;}
 const input=path.resolve(inputArg),out=path.resolve(outArg),p=JSON.parse(await readFile(input,"utf8")),errors=validate(p);
 if(errors.length)throw new Error(errors.join("\n"));
 if(out===input||out.startsWith(input+path.sep))throw new Error("Choose a separate output directory.");
 await mkdir(path.dirname(out),{recursive:true});await mkdir(out,{recursive:false});
 await writeFile(path.join(out,"index.html"),build(p),"utf8");await copyFile(input,path.join(out,"project.json"));
 console.log("Generated self-contained procedural composition: "+path.join(out,"index.html"));
 console.log("Scenes: "+p.scenes.length+" | duration: "+p.scenes.reduce((a,s)=>a+s.duration,0)+"s | "+(p.width??1080)+"x"+(p.height??1920)+" @ "+(p.fps??30)+"fps");
}
main().catch(e=>{console.error("Error: "+e.message);process.exitCode=1;});
