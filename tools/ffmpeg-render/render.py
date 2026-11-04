#!/usr/bin/env python3
"""Render ordered local image/video scenes into MP4 with optional audio and soft subtitles."""
import argparse, json, shutil, subprocess, sys, tempfile
from pathlib import Path

def fail(message):
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(2)

def run(command):
    result = subprocess.run(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode:
        fail(result.stderr[-5000:] or f"Command failed: {command[0]}")

def resolve_asset(root, value):
    path = (root / value).resolve()
    if not path.is_relative_to(root.resolve()):
        fail(f"Asset path escapes project directory: {value}")
    if not path.is_file():
        fail(f"Asset file not found: {path}")
    return path

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    project_file = Path(args.project).resolve()
    try:
        project = json.loads(project_file.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"Cannot read project JSON: {exc}")
    scenes = project.get("scenes")
    if not isinstance(scenes, list) or not scenes:
        fail("Project must contain a non-empty scenes array")
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        fail("FFmpeg was not found on PATH")
    try:
        width, height = int(project.get("width", 1080)), int(project.get("height", 1920))
        fps = int(project.get("fps", 30))
    except (TypeError, ValueError):
        fail("Width, height, and fps must be integers")
    if not (16 <= width <= 8192 and 16 <= height <= 8192 and 1 <= fps <= 120):
        fail("Invalid width, height, or fps")
    root = project_file.parent
    normalized, total = [], 0.0
    for index, scene in enumerate(scenes):
        if not isinstance(scene, dict):
            fail(f"Scene {index} must be an object")
        try:
            duration = float(scene.get("duration", 0))
        except (TypeError, ValueError):
            fail(f"Scene {index} duration must be numeric")
        kind = scene.get("type")
        if duration <= 0 or duration > 3600:
            fail(f"Scene {index} duration must be between 0 and 3600 seconds")
        if kind not in ("image", "video"):
            fail(f"Scene {index} type must be image or video")
        normalized.append((kind, resolve_asset(root, str(scene.get("src", ""))), duration))
        total += duration
    audio = []
    for key in ("voiceover", "music"):
        if project.get(key):
            offset_key = key + "_offset"
            try:
                offset = float(project.get(offset_key, 0))
            except (TypeError, ValueError):
                fail(f"{offset_key} must be a number of seconds")
            if offset < 0 or offset > 3600:
                fail(f"{offset_key} must be between 0 and 3600 seconds")
            audio.append((key, resolve_asset(root, project[key]), offset))
    captions = resolve_asset(root, project["captions"]) if project.get("captions") else None
    if captions and captions.suffix.lower() != ".srt":
        fail("captions must reference an .srt SubRip file")
    output = Path(args.output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="ai-video-render-") as temp:
        temp = Path(temp)
        segments = []
        for i, (kind, source, duration) in enumerate(normalized):
            segment = temp / f"scene-{i:03d}.mp4"
            cmd = [ffmpeg, "-y", "-hide_banner", "-loglevel", "error"]
            if kind == "image":
                cmd += ["-loop", "1", "-framerate", str(fps), "-i", str(source)]
            else:
                cmd += ["-stream_loop", "-1", "-i", str(source)]
            vf = f"scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2,setsar=1,fps={fps},format=yuv420p"
            cmd += ["-t", str(duration), "-vf", vf, "-an", "-c:v", "libx264",
                    "-preset", "veryfast", "-crf", "23", "-movflags", "+faststart", str(segment)]
            run(cmd)
            segments.append(segment)
        concat = temp / "concat.txt"
        concat.write_text("".join(f"file '{p.as_posix()}'\n" for p in segments), encoding="utf-8")
        silent = temp / "silent.mp4"
        run([ffmpeg, "-y", "-hide_banner", "-loglevel", "error", "-f", "concat",
             "-safe", "0", "-i", str(concat), "-c", "copy", str(silent)])
        cmd = [ffmpeg, "-y", "-hide_banner", "-loglevel", "error", "-i", str(silent)]
        for _, path, _ in audio:
            cmd += ["-i", str(path)]
        if captions:
            cmd += ["-i", str(captions)]
        filters, labels = [], []
        for n, (key, _, offset) in enumerate(audio, start=1):
            label = f"a{n}"
            volume = "0.22" if key == "music" and len(audio) > 1 else "1.0"
            delay = int(round(offset * 1000))
            filters.append(f"[{n}:a]volume={volume},adelay={delay}:all=1,apad[{label}]")
            labels.append(f"[{label}]")
        if len(labels) == 1:
            filters.append(f"{labels[0]}anull[aout]")
        elif len(labels) > 1:
            filters.append(f"{''.join(labels)}amix=inputs={len(labels)}:duration=longest:dropout_transition=2[aout]")
        if filters:
            cmd += ["-filter_complex", ";".join(filters)]
        cmd += ["-map", "0:v:0"]
        if labels:
            cmd += ["-map", "[aout]"]
        if captions:
            cmd += ["-map", f"{1 + len(audio)}:0", "-c:s", "mov_text"]
        cmd += ["-t", str(total), "-c:v", "copy"]
        if labels:
            cmd += ["-c:a", "aac", "-b:a", "192k"]
        cmd += ["-movflags", "+faststart", str(output)]
        run(cmd)
    if not output.is_file() or output.stat().st_size == 0:
        fail("Render output is missing or empty")
    print(json.dumps({"status":"succeeded","output":str(output),"bytes":output.stat().st_size,
                      "duration_seconds":round(total,3),"scenes":len(scenes),
                      "audio_tracks":len(audio),"soft_subtitles":bool(captions)}, indent=2))

if __name__ == "__main__":
    main()
