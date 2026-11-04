#!/usr/bin/env python3
"""Render provider-free text/shape scenes to MP4 using FFmpeg's built-in filters."""
import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

COLOR = re.compile(r"^(#[0-9a-fA-F]{6}|[a-zA-Z]{1,20})$")

def safe_color(value, default):
    if isinstance(value, str) and COLOR.fullmatch(value):
        return "0x" + value[1:] if value.startswith("#") else value
    return default

def esc_drawtext(value):
    return str(value).replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'").replace("%", "\\%").replace(",", "\\,")

def validate(project, project_dir):
    errors = []
    if not isinstance(project, dict):
        return ["Project root must be an object."]
    if not isinstance(project.get("title"), str) or not project["title"].strip():
        errors.append("title must be a non-empty string.")
    w, h, fps = project.get("width", 1080), project.get("height", 1920), project.get("fps", 30)
    if not isinstance(w, int) or not 64 <= w <= 4096:
        errors.append("width must be an integer from 64 to 4096.")
    if not isinstance(h, int) or not 64 <= h <= 4096:
        errors.append("height must be an integer from 64 to 4096.")
    if not isinstance(fps, (int, float)) or not 1 <= fps <= 60:
        errors.append("fps must be from 1 to 60.")
    scenes = project.get("scenes")
    if not isinstance(scenes, list) or not scenes:
        errors.append("scenes must be a non-empty array.")
        return errors
    ids = set()
    for i, scene in enumerate(scenes):
        if not isinstance(scene, dict):
            errors.append(f"scenes[{i}] must be an object.")
            continue
        sid = scene.get("id")
        if not isinstance(sid, str) or not sid.strip():
            errors.append(f"scenes[{i}].id is required.")
        elif sid in ids:
            errors.append(f"Duplicate scene id: {sid}")
        else:
            ids.add(sid)
        if not isinstance(scene.get("duration"), (int, float)) or not 0 < scene["duration"] <= 300:
            errors.append(f"scenes[{i}].duration must be >0 and <=300.")
        camera = scene.get("camera", "static")
        if camera not in {"static", "zoom-in", "zoom-out", "pan-left", "pan-right"}:
            errors.append(f"Unsupported camera preset at scenes[{i}].")
        elements = scene.get("elements")
        if not isinstance(elements, list) or not elements:
            errors.append(f"scenes[{i}].elements must be a non-empty array.")
            continue
        for j, element in enumerate(elements):
            if not isinstance(element, dict) or element.get("type") not in {"text", "rect", "line", "bar"}:
                errors.append(f"Unsupported element at scenes[{i}].elements[{j}].")
                continue
            if element["type"] == "text" and not isinstance(element.get("text"), str):
                errors.append(f"Text element {i}:{j} requires string text.")
            for key in ("x", "y", "width", "height", "size", "value", "delay"):
                if key in element and (not isinstance(element[key], (int, float)) or abs(element[key]) > 100000):
                    errors.append(f"Invalid {key} at scenes[{i}].elements[{j}].")
    transition = project.get("transition")
    if transition is not None:
        allowed = {"fade", "dissolve", "wipeleft", "wiperight", "slideleft", "slideright", "circleopen", "circleclose"}
        if not isinstance(transition, dict) or transition.get("type") != "crossfade":
            errors.append("transition.type must be crossfade.")
        else:
            duration = transition.get("duration")
            if len(scenes) < 2:
                errors.append("transition requires at least two scenes.")
            if transition.get("effect", "fade") not in allowed:
                errors.append("Unsupported transition effect.")
            if not isinstance(duration, (int, float)) or not 0.05 <= duration <= 5:
                errors.append("transition.duration must be from 0.05 to 5 seconds.")
            elif any(not isinstance(scene, dict) or not isinstance(scene.get("duration"), (int, float)) or scene["duration"] <= duration for scene in scenes):
                errors.append("Every scene must be longer than the transition duration.")
    for key in ("voiceover", "music"):
        audio = project.get(key)
        if audio is None:
            continue
        if not isinstance(audio, dict) or not isinstance(audio.get("src"), str) or not audio["src"].strip():
            errors.append(f"{key} must contain a local src path.")
            continue
        src = (project_dir / audio["src"]).resolve()
        try:
            src.relative_to(project_dir.resolve())
        except ValueError:
            errors.append(f"{key}.src must stay inside the project directory.")
            continue
        if not src.is_file():
            errors.append(f"{key} asset file not found: {src}")
        gain, offset = audio.get("gain", 1), audio.get("offset", 0)
        if not isinstance(gain, (int, float)) or not 0 <= gain <= 4:
            errors.append(f"{key}.gain must be from 0 to 4.")
        if not isinstance(offset, (int, float)) or not 0 <= offset <= 3600:
            errors.append(f"{key}.offset must be from 0 to 3600 seconds.")
    return errors

def build_filter(project, project_dir):
    width, height, fps = project.get("width", 1080), project.get("height", 1920), project.get("fps", 30)
    inputs, filters, video_labels = [], [], []
    for i, scene in enumerate(project["scenes"]):
        duration = float(scene["duration"])
        background = safe_color(scene.get("background", project.get("background")), "0x101827")
        inputs += ["-f", "lavfi", "-i", f"color=c={background}:s={width}x{height}:r={fps}:d={duration:.6f}"]
        chain = f"[{i}:v]"
        for j, element in enumerate(scene["elements"]):
            kind = element["type"]
            fill = safe_color(element.get("fill"), "0xffffff")
            if kind == "text":
                size = max(8, min(int(element.get("size", int(width * .06))), int(width * .3)))
                text_value = esc_drawtext(element["text"])
                x = float(element.get("x", width / 2)) - size * .5 * len(element["text"]) * .52
                y = float(element.get("y", height / 2)) - size * .55
                if element.get("align") == "left":
                    x = float(element.get("x", 0))
                elif element.get("align") == "right":
                    x = float(element.get("x", width)) - size * .5 * len(element["text"]) * .52
                font_color = safe_color(element.get("fill"), "0xffffff")
                border = max(0, int(element.get("border", 0)))
                delay = max(0, float(element.get("delay", 0)))
                filters.append(f"{chain}drawtext=text='{text_value}':x={x:.2f}:y={y:.2f}:fontsize={size}:fontcolor={font_color}:borderw={border}:shadowcolor=black@0.35:shadowx=2:shadowy=2:enable='gte(t,{delay:.4f})'[v{i}_{j}]")
                chain = f"[v{i}_{j}]"
            elif kind in {"rect", "line"}:
                x, y = int(element.get("x", width / 2)), int(element.get("y", height / 2))
                box_width = max(1, int(element.get("width", 220)))
                box_height = max(1, int(element.get("height", 8 if kind == "line" else 120)))
                if kind == "line":
                    box_height = max(1, int(element.get("strokeWidth", 8)))
                opacity = max(0, min(float(element.get("opacity", 1)), 1))
                delay = max(0, float(element.get("delay", 0)))
                filters.append(f"{chain}drawbox=x={x}:y={y}:w={box_width}:h={box_height}:color={fill}@{opacity}:t=fill:enable='gte(t,{delay:.4f})'[v{i}_{j}]")
                chain = f"[v{i}_{j}]"
            elif kind == "bar":
                x, y = int(element.get("x", width * .2)), int(element.get("y", height * .5))
                box_width, box_height = max(1, int(element.get("width", width * .6))), max(1, int(element.get("height", 24)))
                value = max(0, min(float(element.get("value", .7)), 1))
                track = safe_color(element.get("track"), "0x334155")
                delay = max(0, float(element.get("delay", 0)))
                filters.append(f"{chain}drawbox=x={x}:y={y}:w={box_width}:h={box_height}:color={track}:t=fill:enable='gte(t,{delay:.4f})'[v{i}_{j}a]")
                filters.append(f"[v{i}_{j}a]drawbox=x={x}:y={y}:w={max(1, int(box_width * value))}:h={box_height}:color={fill}:t=fill:enable='gte(t,{delay:.4f})'[v{i}_{j}]")
                chain = f"[v{i}_{j}]"
        camera = scene.get("camera", "static")
        if camera == "zoom-in":
            filters.append(f"{chain}zoompan=z='min(zoom+0.0015,1.12)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={width}x{height}:fps={fps},format=yuv420p[cam{i}]")
            chain = f"[cam{i}]"
        elif camera == "zoom-out":
            filters.append(f"{chain}zoompan=z='if(eq(on,0),1.12,max(1.0,zoom-0.0015))':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={width}x{height}:fps={fps},format=yuv420p[cam{i}]")
            chain = f"[cam{i}]"
        elif camera in {"pan-left", "pan-right"}:
            frame_count = max(1, int(duration * fps))
            x_expr = f"(iw-iw/zoom)*on/{frame_count}" if camera == "pan-left" else f"(iw-iw/zoom)*(1-on/{frame_count})"
            filters.append(f"{chain}zoompan=z='1.06':x='{x_expr}':y='ih/2-(ih/zoom/2)':d=1:s={width}x{height}:fps={fps},format=yuv420p[cam{i}]")
            chain = f"[cam{i}]"
        label = f"scene{i}"
        filters.append(f"{chain}format=yuv420p[{label}]")
        video_labels.append(f"[{label}]")
    transition = project.get("transition")
    if transition:
        duration = float(transition["duration"])
        effect = transition.get("effect", "fade")
        previous = video_labels[0]
        offset = float(project["scenes"][0]["duration"]) - duration
        for index in range(1, len(video_labels)):
            output_label = f"xfade{index}"
            filters.append(f"{previous}{video_labels[index]}xfade=transition={effect}:duration={duration:.6f}:offset={offset:.6f}[{output_label}]")
            previous = f"[{output_label}]"
            if index < len(video_labels) - 1:
                offset += float(project["scenes"][index]["duration"]) - duration
        filters.append(f"{previous}null[outv]")
    elif len(video_labels) == 1:
        filters.append(f"{video_labels[0]}null[outv]")
    else:
        filters.append("".join(video_labels) + f"concat=n={len(video_labels)}:v=1:a=0[outv]")

    total_duration = sum(float(scene["duration"]) for scene in project["scenes"]) - (float(transition["duration"]) * max(0, len(project["scenes"]) - 1) if transition else 0)
    audio_labels = []
    for key in ("voiceover", "music"):
        spec = project.get(key)
        if spec is None:
            continue
        source = (project_dir / spec["src"]).resolve()
        if key == "music":
            inputs += ["-stream_loop", "-1"]
        inputs += ["-i", str(source)]
        input_index = len(project["scenes"]) + len(audio_labels)
        gain, delay = float(spec.get("gain", 1)), int(float(spec.get("offset", 0)) * 1000)
        label = f"audio{input_index}"
        filters.append(f"[{input_index}:a]volume={gain:.4f},adelay={delay}:all=1,apad,atrim=duration={total_duration:.6f}[{label}]")
        audio_labels.append(f"[{label}]")
    if len(audio_labels) == 1:
        filters.append(f"{audio_labels[0]}anull[aout]")
    elif len(audio_labels) > 1:
        filters.append("".join(audio_labels) + f"amix=inputs={len(audio_labels)}:duration=longest:dropout_transition=2,alimiter=limit=0.95[aout]")
    return inputs, ";".join(filters), bool(audio_labels)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--ffmpeg", default="ffmpeg")
    args = parser.parse_args()
    if not shutil.which(args.ffmpeg):
        print("ERROR: FFmpeg executable not found.", file=sys.stderr)
        return 2
    try:
        project = json.loads(args.project.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"ERROR: Cannot read project JSON: {exc}", file=sys.stderr)
        return 2
    project_dir = args.project.resolve().parent
    errors = validate(project, project_dir)
    if errors:
        print("ERROR: " + "\n".join(errors), file=sys.stderr)
        return 2
    args.output.parent.mkdir(parents=True, exist_ok=True)
    inputs, graph, has_audio = build_filter(project, project_dir)
    command = [args.ffmpeg, "-hide_banner", "-loglevel", "error", "-y", *inputs, "-filter_complex", graph, "-map", "[outv]"]
    if has_audio:
        command += ["-map", "[aout]", "-c:a", "aac", "-b:a", "192k"]
    else:
        command += ["-an"]
    command += ["-c:v", "libx264", "-preset", "ultrafast", "-crf", "20", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(args.output)]
    result = subprocess.run(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode:
        print("ERROR: FFmpeg render failed: " + result.stderr[-3000:], file=sys.stderr)
        return result.returncode
    if not args.output.is_file() or args.output.stat().st_size == 0:
        print("ERROR: Render output missing or empty.", file=sys.stderr)
        return 2
    print(json.dumps({
        "status": "rendered", "output": str(args.output), "bytes": args.output.stat().st_size,
        "duration_seconds": sum(float(scene["duration"]) for scene in project["scenes"]),
        "scenes": len(project["scenes"]),
        "dimensions": f'{project.get("width", 1080)}x{project.get("height", 1920)}',
        "fps": project.get("fps", 30), "audio": "mixed local voiceover/music" if has_audio else "none"
    }, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
