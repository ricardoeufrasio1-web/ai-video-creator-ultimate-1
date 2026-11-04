#!/usr/bin/env python3
"""Render provider-free text/shape scenes to MP4 using FFmpeg's built-in filters."""
import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

COLOR = re.compile(r"^(#[0-9a-fA-F]{6}|[a-zA-Z]{1,20})$")
def safe_color(value, default):
    return value if isinstance(value,str) and COLOR.fullmatch(value) else default

def esc_drawtext(value):
    # FFmpeg filtergraph escaping for drawtext's option parser.
    return str(value).replace("\\","\\\\").replace(":","\\:").replace("'","\\'").replace("%","\\%").replace(",","\\,")

def validate(project):
    errors=[]
    if not isinstance(project,dict): return ["Project root must be an object."]
    if not isinstance(project.get("title"),str) or not project["title"].strip(): errors.append("title must be a non-empty string.")
    w,h,fps=project.get("width",1080),project.get("height",1920),project.get("fps",30)
    if not isinstance(w,int) or not 64<=w<=4096: errors.append("width must be an integer from 64 to 4096.")
    if not isinstance(h,int) or not 64<=h<=4096: errors.append("height must be an integer from 64 to 4096.")
    if not isinstance(fps,(int,float)) or not 1<=fps<=60: errors.append("fps must be from 1 to 60.")
    scenes=project.get("scenes")
    if not isinstance(scenes,list) or not scenes: errors.append("scenes must be a non-empty array."); return errors
    ids=set()
    for i,s in enumerate(scenes):
        if not isinstance(s,dict): errors.append(f"scenes[{i}] must be an object."); continue
        sid=s.get("id")
        if not isinstance(sid,str) or not sid.strip(): errors.append(f"scenes[{i}].id is required.")
        elif sid in ids: errors.append(f"Duplicate scene id: {sid}")
        else: ids.add(sid)
        if not isinstance(s.get("duration"),(int,float)) or not 0<s["duration"]<=300: errors.append(f"scenes[{i}].duration must be >0 and <=300.")
        elements=s.get("elements")
        if not isinstance(elements,list) or not elements: errors.append(f"scenes[{i}].elements must be a non-empty array."); continue
        for j,e in enumerate(elements):
            if not isinstance(e,dict) or e.get("type") not in {"text","rect","line","bar"}: errors.append(f"Unsupported element at scenes[{i}].elements[{j}].")
            elif e.get("type")=="text" and not isinstance(e.get("text"),str): errors.append(f"Text element {i}:{j} requires string text.")
            for k in ("x","y","width","height","size","value"):
                if isinstance(e,dict) and k in e and (not isinstance(e[k],(int,float)) or abs(e[k])>100000): errors.append(f"Invalid {k} at scenes[{i}].elements[{j}].")
    return errors

def build_filter(project):
    w,h,fps=project.get("width",1080),project.get("height",1920),project.get("fps",30)
    inputs=[]; filters=[]; labels=[]
    for i,s in enumerate(project["scenes"]):
        duration=float(s["duration"]); bg=safe_color(s.get("background",project.get("background")),"#101827")
        inputs += ["-f","lavfi","-i",f"color=c={bg}:s={w}x{h}:r={fps}:d={duration:.6f}"]
        chain=f"[{i}:v]"
        for j,e in enumerate(s["elements"]):
            typ=e["type"]; fill=safe_color(e.get("fill"),"#ffffff")
            if typ=="text":
                size=max(8,min(int(e.get("size",int(w*.06))),int(w*.3)))
                x=float(e.get("x",w/2))-size*.5*len(e["text"])*.52
                y=float(e.get("y",h/2))-size*.55
                align=e.get("align","center")
                if align=="left": x=float(e.get("x",0))
                elif align=="right": x=float(e.get("x",w))-size*.5*len(e["text"])*.52
                fontcolor=safe_color(e.get("fill"),"#ffffff")
                weight=max(100,min(int(e.get("weight",700)),900))
                text=esc_drawtext(e["text"])
                filters.append(f"{chain}drawtext=text='{text}':x={x:.2f}:y={y:.2f}:fontsize={size}:fontcolor={fontcolor}:borderw={max(0,int(e.get('border',0)))}:shadowcolor=black@0.35:shadowx=2:shadowy=2[v{i}_{j}]")
                chain=f"[v{i}_{j}]"
            elif typ in {"rect","line"}:
                x=int(e.get("x",w/2)); y=int(e.get("y",h/2))
                bw=max(1,int(e.get("width",220))); bh=max(1,int(e.get("height",8 if typ=="line" else 120)))
                if typ=="line": bh=max(1,int(e.get("strokeWidth",8)))
                filters.append(f"{chain}drawbox=x={x}:y={y}:w={bw}:h={bh}:color={fill}@{max(0,min(float(e.get('opacity',1)),1))}:t=fill[v{i}_{j}]")
                chain=f"[v{i}_{j}]"
            elif typ=="bar":
                x=int(e.get("x",w*.2)); y=int(e.get("y",h*.5)); bw=max(1,int(e.get("width",w*.6))); bh=max(1,int(e.get("height",24)))
                val=max(0,min(float(e.get("value",.7)),1))
                track=safe_color(e.get("track"),"#334155")
                filters.append(f"{chain}drawbox=x={x}:y={y}:w={bw}:h={bh}:color={track}:t=fill[v{i}_{j}a]")
                filters.append(f"[v{i}_{j}a]drawbox=x={x}:y={y}:w={max(1,int(bw*val))}:h={bh}:color={fill}:t=fill[v{i}_{j}]")
                chain=f"[v{i}_{j}]"
        out=f"scene{i}"
        filters.append(f"{chain}format=yuv420p[{out}]")
        labels.append(f"[{out}]")
    if len(labels)==1:
        filters.append(f"{labels[0]}null[outv]")
    else:
        filters.append("".join(labels)+f"concat=n={len(labels)}:v=1:a=0[outv]")
    return inputs, ";".join(filters)

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("project",type=Path)
    ap.add_argument("--output",type=Path,required=True)
    ap.add_argument("--ffmpeg",default="ffmpeg")
    args=ap.parse_args()
    if not shutil.which(args.ffmpeg): print("ERROR: FFmpeg executable not found.",file=sys.stderr); return 2
    try: project=json.loads(args.project.read_text(encoding="utf-8"))
    except Exception as exc: print(f"ERROR: Cannot read project JSON: {exc}",file=sys.stderr); return 2
    errors=validate(project)
    if errors: print("ERROR: "+"\n".join(errors),file=sys.stderr); return 2
    args.output.parent.mkdir(parents=True,exist_ok=True)
    inputs,graph=build_filter(project)
    cmd=[args.ffmpeg,"-hide_banner","-loglevel","error","-y",*inputs,"-filter_complex",graph,"-map","[outv]","-an","-c:v","libx264","-preset","ultrafast","-crf","20","-pix_fmt","yuv420p","-movflags","+faststart",str(args.output)]
    run=subprocess.run(cmd,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if run.returncode:
        print("ERROR: FFmpeg render failed: "+run.stderr[-3000:],file=sys.stderr); return run.returncode
    if not args.output.is_file() or args.output.stat().st_size==0: print("ERROR: Render output missing or empty.",file=sys.stderr); return 2
    print(json.dumps({"status":"rendered","output":str(args.output),"bytes":args.output.stat().st_size,"duration_seconds":sum(float(s["duration"]) for s in project["scenes"]),"scenes":len(project["scenes"]),"dimensions":f'{project.get("width",1080)}x{project.get("height",1920)}',"fps":project.get("fps",30),"audio":"none"},indent=2))
    return 0

if __name__=="__main__": raise SystemExit(main())
