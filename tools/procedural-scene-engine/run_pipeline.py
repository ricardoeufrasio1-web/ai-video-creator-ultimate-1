#!/usr/bin/env python3
"""Run the provider-free procedural video pipeline from one project JSON."""
import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RENDERER = ROOT / "tools/procedural-scene-engine/render.py"
TTS = ROOT / "tools/procedural-scene-engine/tts.py"

def inside(base, relative):
    target = (base / relative).resolve()
    try:
        target.relative_to(base.resolve())
    except ValueError:
        raise ValueError("Generated asset path must stay inside the project directory.")
    return target

def run(project_path, output_path, ffmpeg="ffmpeg", ffprobe="ffprobe"):
    project_path = project_path.resolve()
    base = project_path.parent
    project = json.loads(project_path.read_text(encoding="utf-8"))
    narration = project.pop("narration", None)
    generated_voice = None
    if narration is not None:
        if not isinstance(narration, dict) or not isinstance(narration.get("text"), str) or not narration["text"].strip():
            raise ValueError("narration must be an object with non-empty text.")
        voice_name = narration.get("voice", "pt-br")
        voice_path = inside(base, narration.get("output", "generated-narration.wav"))
        if narration.get("engine", "espeak-ng") != "espeak-ng":\n            raise ValueError("Unsupported offline narration engine. Use a human recording or connected natural-voice provider; eSpeak NG is the only local draft engine.")\n        if narration.get("allow_robotic_espeak") is not True:\n            raise ValueError("eSpeak NG narration is robotic and blocked by default. For draft/test use only, set narration.allow_robotic_espeak=true; for final natural voice use human-recorded audio or an authorized natural-voice provider.")\n        command = [sys.executable, str(TTS), narration["text"], "--output", str(voice_path), "--voice", str(voice_name), "--allow-robotic-espeak"]
        for key, flag in (("speed", "--speed"), ("pitch", "--pitch"), ("amplitude", "--amplitude")):
            if key in narration:
                command += [flag, str(narration[key])]
        result = subprocess.run(command, text=True, capture_output=True)
        if result.returncode:
            raise RuntimeError("Offline narration failed: " + result.stderr[-2000:])
        generated_voice = voice_path
        project["voiceover"] = {"src": voice_path.relative_to(base).as_posix(), "gain": narration.get("gain", 1), "offset": narration.get("offset", 0)}
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".json", prefix=".pipeline-", dir=base, delete=False) as handle:
        temp_project = Path(handle.name)
        json.dump(project, handle, ensure_ascii=False)
    try:
        command = [sys.executable, str(RENDERER), str(temp_project), "--output", str(output_path.resolve()), "--ffmpeg", ffmpeg]
        result = subprocess.run(command, text=True, capture_output=True)
        if result.returncode:
            raise RuntimeError("MP4 render failed: " + result.stderr[-3000:])
    finally:
        temp_project.unlink(missing_ok=True)
    if not shutil.which(ffprobe):
        raise RuntimeError("FFprobe is required to verify the finished MP4.")
    probe = subprocess.run([ffprobe, "-v", "error", "-show_streams", "-show_format", "-of", "json", str(output_path.resolve())], text=True, capture_output=True)
    if probe.returncode:
        raise RuntimeError("FFprobe could not inspect the MP4: " + probe.stderr[-2000:])
    metadata = json.loads(probe.stdout)
    video = next((stream for stream in metadata.get("streams", []) if stream.get("codec_type") == "video"), None)
    if not video:
        raise RuntimeError("Rendered file has no video stream.")
    audio = next((stream for stream in metadata.get("streams", []) if stream.get("codec_type") == "audio"), None)
    report = {
        "status": "verified",
        "output": str(output_path.resolve()),
        "bytes": output_path.stat().st_size,
        "duration_seconds": float(metadata.get("format", {}).get("duration", 0)),
        "video": {"codec": video.get("codec_name"), "width": video.get("width"), "height": video.get("height"), "fps": video.get("r_frame_rate")},
        "audio": {"present": bool(audio), "codec": audio.get("codec_name") if audio else None},
        "scenes": len(project.get("scenes", [])),
        "narration_generated_offline": bool(generated_voice),
        "provider_calls": 0
    }
    return report

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--ffmpeg", default="ffmpeg")
    parser.add_argument("--ffprobe", default="ffprobe")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    try:
        report = run(args.project, args.output, args.ffmpeg, args.ffprobe)
        serialized = json.dumps(report, indent=2, ensure_ascii=False)
        if args.report:
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(serialized + "\n", encoding="utf-8")
        print(serialized)
        return 0
    except Exception as exc:
        print("ERROR: " + str(exc), file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
