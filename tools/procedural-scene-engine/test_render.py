#!/usr/bin/env python3
"""End-to-end MP4 smoke test for the procedural scene renderer."""
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
RENDERER=ROOT/"tools/procedural-scene-engine/render.py"
FIXTURE=ROOT/"examples/procedural-scenes/render-fixture.json"

class ProceduralRenderTests(unittest.TestCase):
    def test_produces_valid_mp4_without_remote_media(self):
        if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
            self.skipTest("FFmpeg and FFprobe are required.")
        with tempfile.TemporaryDirectory() as tmp:
            output=Path(tmp)/"procedural.mp4"
            run=subprocess.run(["python3",str(RENDERER),str(FIXTURE),"--output",str(output)],text=True,capture_output=True)
            self.assertEqual(run.returncode,0,run.stderr)
            self.assertGreater(output.stat().st_size,0)
            probe=subprocess.run(["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(output)],text=True,capture_output=True,check=True)
            data=json.loads(probe.stdout)
            video=next(s for s in data["streams"] if s["codec_type"]=="video")
            self.assertEqual((video["width"],video["height"]),(320,568))
            self.assertAlmostEqual(float(data["format"]["duration"]),3.0,delta=.15)
            self.assertEqual(video["codec_name"],"h264")

if __name__=="__main__": unittest.main(verbosity=2)
