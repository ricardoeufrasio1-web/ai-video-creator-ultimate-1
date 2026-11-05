#!/usr/bin/env python3
"""Optional offline narration helper using eSpeak NG (robotic voice; development fallback only)."""
import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("text",help="Exact narration text.")
    parser.add_argument("--output",type=Path,required=True)
    parser.add_argument("--voice",default="pt-br",help="Installed eSpeak NG voice, e.g. pt-br, en-us, es.")
    parser.add_argument("--speed",type=int,default=145)
    parser.add_argument("--pitch",type=int,default=48)
    parser.add_argument("--amplitude",type=int,default=100)
    parser.add_argument("--engine",default="espeak-ng")
    parser.add_argument("--allow-robotic-espeak",action="store_true",help="Explicitly accept synthetic/robotic quality for a draft or test.")
    args=parser.parse_args()
    if not args.allow_robotic_espeak:
        print("BLOCKED: eSpeak NG sounds synthetic/robotic and is not suitable as final natural narration. Use a human recording or authorized natural-voice provider. For a draft/test only, add --allow-robotic-espeak.",file=sys.stderr)
        return 2
    executable=shutil.which(args.engine)
    if not executable:
        print("ERROR: eSpeak NG is not installed. Install it locally or provide a recorded narration track.",file=sys.stderr)
        return 2
    if not args.text.strip():
        print("ERROR: narration text cannot be empty.",file=sys.stderr)
        return 2
    if not 80<=args.speed<=300 or not 0<=args.pitch<=99 or not 0<=args.amplitude<=200:
        print("ERROR: speed, pitch or amplitude is outside supported range.",file=sys.stderr)
        return 2
    args.output.parent.mkdir(parents=True,exist_ok=True)
    command=[executable,"-v",args.voice,"-s",str(args.speed),"-p",str(args.pitch),"-a",str(args.amplitude),"-w",str(args.output),args.text]
    result=subprocess.run(command,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if result.returncode or not args.output.is_file() or args.output.stat().st_size==0:
        print("ERROR: local speech synthesis failed: "+result.stderr[-2000:],file=sys.stderr)
        return result.returncode or 2
    print(json.dumps({"status":"synthesized_draft","output":str(args.output),"bytes":args.output.stat().st_size,"engine":"eSpeak NG","voice":args.voice,"speed":args.speed,"pitch":args.pitch,"amplitude":args.amplitude,"quality_warning":"Synthetic/robotic draft voice; not final-quality natural narration.","network":"not used"},indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
