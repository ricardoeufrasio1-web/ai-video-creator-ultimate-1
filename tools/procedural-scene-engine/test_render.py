#!/usr/bin/env python3
"""End-to-end MP4 smoke test for the procedural scene renderer."""
import json
import math
import shutil
import struct
import subprocess
import tempfile
import unittest
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RENDERER = ROOT / "tools/procedural-scene-engine/render.py"
FIXTURE = ROOT / "examples/procedural-scenes/render-fixture.json"

class ProceduralRenderTests(unittest.TestCase):
    def test_produces_valid_mp4_with_local_voiceover(self):
        if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
            self.skipTest("FFmpeg and FFprobe are required.")
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            output = folder / "procedural.mp4"
            project = json.loads(FIXTURE.read_text(encoding="utf-8"))
            voice = folder / "voice.wav"
            with wave.open(str(voice), "wb") as wav:
                wav.setnchannels(1)
                wav.setsampwidth(2)
                wav.setframerate(22050)
                samples = [int(1200 * math.sin(2 * math.pi * 440 * n / 22050)) for n in range(22050)]
                wav.writeframes(b"".join(struct.pack("<h", value) for value in samples))
            project["voiceover"] = {"src": "voice.wav", "gain": 0.6, "offset": 0}
            project_path = folder / "project.json"
            project_path.write_text(json.dumps(project), encoding="utf-8")
            run = subprocess.run(["python3", str(RENDERER), str(project_path), "--output", str(output)], text=True, capture_output=True)
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertGreater(output.stat().st_size, 0)
            probe = subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(output)], text=True, capture_output=True, check=True)
            data = json.loads(probe.stdout)
            video = next(stream for stream in data["streams"] if stream["codec_type"] == "video")
            self.assertEqual((video["width"], video["height"]), (320, 568))
            self.assertAlmostEqual(float(data["format"]["duration"]), 3.0, delta=0.15)
            self.assertEqual(video["codec_name"], "h264")
            self.assertTrue(any(stream["codec_type"] == "audio" for stream in data["streams"]))

if __name__ == "__main__":
    unittest.main(verbosity=2)
