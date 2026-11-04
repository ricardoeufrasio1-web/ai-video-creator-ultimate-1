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
    transition = project.get("transition")
    transition_duration = 0.0
    transition_effect = "fade"
    if transition is not None:
        if not isinstance(transition, dict) or transition.get("type") != "crossfade":
            fail("transition must be an object with type crossfade")
        transition_effect = transition.get("effect", "fade")
        allowed_effects = ("fade", "dissolve", "wipeleft", "wiperight", "slideleft", "slideright", "circleopen", "circleclose")
        if transition_effect not in allowed_effects:
            fail("transition.effect must be one of: " + ", ".join(allowed_effects))
        try:
            transition_duration = float(transition.get("duration", 0.5))
        except (TypeError, ValueError):
            fail("transition.duration must be numeric")
        if transition_duration <= 0 or transition_duration > 10:
            fail("transition.duration must be greater than 0 and at most 10 seconds")
        if len(scenes) < 2:
            fail("A transition requires at least two scenes")
    root = project_file.parent
    normalized, scene_duration_total = [], 0.0
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
        try:
            fade_in = float(scene.get("fade_in", 0))
            fade_out = float(scene.get("fade_out", 0))
        except (TypeError, ValueError):
            fail(f"Scene {index} fade_in/fade_out must be numeric")
        if fade_in < 0 or fade_out < 0 or fade_in > duration or fade_out > duration:
            fail(f"Scene {index} has invalid fade values")
        if transition_duration and duration <= transition_duration:
            fail(f"Scene {index} duration must be longer than the crossfade duration")
        motion = scene.get("motion", "none")
        if motion not in ("none", "zoom_in", "zoom_out"):
            fail(f"Scene {index} motion must be none, zoom_in, or zoom_out")
        normalized.append((kind, resolve_asset(root, str(scene.get("src", ""))), duration, fade_in, fade_out, motion))
        scene_duration_total += duration
    total = scene_duration_total - transition_duration * max(0, len(normalized) - 1)
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
    cues = project.get("audio_cues", [])
    if not isinstance(cues, list):
        fail("audio_cues must be an array")
    normalized_cues = []
    cue_ids = set()
    for index, cue in enumerate(cues):
        if not isinstance(cue, dict):
            fail(f"Audio cue {index} must be an object")
        cue_id = str(cue.get("id", "")).strip()
        if not cue_id or cue_id in cue_ids:
            fail(f"Audio cue {index} requires a unique non-empty id")
        cue_ids.add(cue_id)
        try:
            start = float(cue.get("start", 0))
            duration = float(cue.get("duration", total - start))
            gain = float(cue.get("gain", 1))
            fade_in = float(cue.get("fade_in", 0))
            fade_out = float(cue.get("fade_out", 0))
        except (TypeError, ValueError):
            fail(f"Audio cue {index} start/duration/gain/fades must be numeric")
        if start < 0 or duration <= 0 or start >= total or start + duration > total + 0.001:
            fail(f"Audio cue {index} must fit within the project duration")
        if gain < 0 or gain > 4 or fade_in < 0 or fade_out < 0 or fade_in > duration or fade_out > duration:
            fail(f"Audio cue {index} has invalid gain or fade values")
        role = cue.get("role", "sfx")
        if role not in ("narration", "music", "sfx", "ambience", "dialogue"):
            fail(f"Audio cue {index} role is unsupported")
        normalized_cues.append((cue_id, resolve_asset(root, str(cue.get("src", ""))), role,
                                start, duration, gain, fade_in, fade_out))
    normalization = project.get("audio_normalization", False)
    normalization_filter = None
    if normalization:
        if normalization is True:
            normalization = {}
        if not isinstance(normalization, dict):
            fail("audio_normalization must be false or an object")
        try:
            integrated = float(normalization.get("integrated_lufs", -16))
            true_peak = float(normalization.get("true_peak_db", -1.5))
            loudness_range = float(normalization.get("loudness_range", 11))
        except (TypeError, ValueError):
            fail("audio_normalization targets must be numeric")
        if not (-36 <= integrated <= -5 and -9 <= true_peak <= 0 and 1 <= loudness_range <= 20):
            fail("audio_normalization targets are out of supported ranges")
        normalization_filter = f"loudnorm=I={integrated}:TP={true_peak}:LRA={loudness_range}"
    captions = resolve_asset(root, project["captions"]) if project.get("captions") else None
    if captions and captions.suffix.lower() != ".srt":
        fail("captions must reference an .srt SubRip file")
    output = Path(args.output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="ai-video-render-") as temp:
        temp = Path(temp)
        segments = []
        for i, (kind, source, duration, fade_in, fade_out, motion) in enumerate(normalized):
            segment = temp / f"scene-{i:03d}.mp4"
            cmd = [ffmpeg, "-y", "-hide_banner", "-loglevel", "error"]
            if kind == "image":
                cmd += ["-loop", "1", "-framerate", str(fps), "-i", str(source)]
            else:
                cmd += ["-stream_loop", "-1", "-i", str(source)]
            vf = f"scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2,setsar=1,fps={fps},format=yuv420p"
            if motion == "zoom_in":
                vf += f",zoompan=z='min(zoom+0.0015,1.12)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={width}x{height}:fps={fps}"
            elif motion == "zoom_out":
                vf += f",zoompan=z='if(eq(on,1),1.12,max(zoom-0.0015,1.0))':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={width}x{height}:fps={fps}"
            if fade_in:
                vf += f",fade=t=in:st=0:d={fade_in}:color=black"
            if fade_out:
                vf += f",fade=t=out:st={max(0, duration-fade_out)}:d={fade_out}:color=black"
            cmd += ["-t", str(duration), "-vf", vf, "-an", "-c:v", "libx264",
                    "-preset", "veryfast", "-crf", "23", "-movflags", "+faststart", str(segment)]
            run(cmd)
            segments.append(segment)
        silent = temp / "silent.mp4"
        if transition_duration:
            transition_filters = []
            elapsed = normalized[0][2]
            previous = "[0:v]"
            for i in range(1, len(segments)):
                output_label = f"[xf{i}]"
                offset = elapsed - transition_duration
                transition_filters.append(
                    f"{previous}[{i}:v]xfade=transition={transition_effect}:duration={transition_duration}:offset={offset}{output_label}"
                )
                previous = output_label
                elapsed += normalized[i][2] - transition_duration
            transition_cmd = [ffmpeg, "-y", "-hide_banner", "-loglevel", "error"]
            for segment in segments:
                transition_cmd += ["-i", str(segment)]
            transition_cmd += ["-filter_complex", ";".join(transition_filters),
                               "-map", previous, "-an", "-t", str(total),
                               "-c:v", "libx264", "-preset", "veryfast", "-crf", "23",
                               "-pix_fmt", "yuv420p", str(silent)]
            run(transition_cmd)
        else:
            concat = temp / "concat.txt"
            concat.write_text("".join(f"file '{p.as_posix()}'\n" for p in segments), encoding="utf-8")
            run([ffmpeg, "-y", "-hide_banner", "-loglevel", "error", "-f", "concat",
                 "-safe", "0", "-i", str(concat), "-c", "copy", str(silent)])
        cmd = [ffmpeg, "-y", "-hide_banner", "-loglevel", "error", "-i", str(silent)]
        for _, path, _ in audio:
            cmd += ["-i", str(path)]
        for _, path, _, _, _, _, _, _ in normalized_cues:
            cmd += ["-i", str(path)]
        if captions:
            cmd += ["-i", str(captions)]
        filters, labels = [], []
        for n, (key, _, offset) in enumerate(audio, start=1):
            label = f"a{n}"
            volume = "0.22" if key == "music" and len(audio) > 1 else "1.0"
            delay = int(round(offset * 1000))
            filters.append(f"[{n}:a]volume={volume},adelay={delay}:all=1,apad=whole_dur={total}[{label}]")
            labels.append(f"[{label}]")
        for n, (_, _, role, start, duration, gain, fade_in, fade_out) in enumerate(normalized_cues, start=1 + len(audio)):
            label = f"cue{n}"
            chain = f"[{n}:a]atrim=duration={duration},asetpts=PTS-STARTPTS,volume={gain}"
            if fade_in:
                chain += f",afade=t=in:st=0:d={fade_in}"
            if fade_out:
                chain += f",afade=t=out:st={max(0, duration-fade_out)}:d={fade_out}"
            chain += f",adelay={int(round(start*1000))}:all=1,apad=whole_dur={total}[{label}]"
            filters.append(chain)
            labels.append(f"[{label}]")
        if len(labels) == 1:
            filters.append(f"{labels[0]}anull[aout]")
        elif len(labels) > 1:
            filters.append(f"{''.join(labels)}amix=inputs={len(labels)}:duration=longest:dropout_transition=2[aout]")
        if labels and normalization_filter:
            filters.append(f"[aout]{normalization_filter}[anorm]")
        if filters:
            cmd += ["-filter_complex", ";".join(filters)]
        cmd += ["-map", "0:v:0"]
        if labels:
            cmd += ["-map", "[anorm]" if normalization_filter else "[aout]"]
        if captions:
            cmd += ["-map", f"{1 + len(audio) + len(normalized_cues)}:0", "-c:s", "mov_text"]
        cmd += ["-t", str(total), "-c:v", "copy"]
        if labels:
            cmd += ["-c:a", "aac", "-b:a", "192k"]
        cmd += ["-movflags", "+faststart", str(output)]
        run(cmd)
    if not output.is_file() or output.stat().st_size == 0:
        fail("Render output is missing or empty")
    print(json.dumps({"status":"succeeded","output":str(output),"bytes":output.stat().st_size,
                      "duration_seconds":round(total,3),"scenes":len(scenes),
                      "audio_tracks":len(audio) + len(normalized_cues),"audio_cues":len(normalized_cues),
                      "transition":transition.get("type") if transition else "hard_cut",
                      "transition_effect":transition_effect if transition else None,
                      "soft_subtitles":bool(captions),"audio_normalization":bool(normalization_filter and labels)}, indent=2))

if __name__ == "__main__":
    main()
