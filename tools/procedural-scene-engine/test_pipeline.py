#!/usr/bin/env python3
"""Integration test for the one-command offline video pipeline."""
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from run_pipeline import run

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "examples/procedural-scenes/render-fixture.json"

class PipelineIntegrationTests(unittest.TestCase):
    def test_generates_narration_renders_and_verifies_mp4(self):
        if not all(shutil.which(name) for name in ("ffmpeg", "ffprobe", "espeak-ng")):
            self.skipTest("FFmpeg, FFprobe and eSpeak NG are required.")
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            project = json.loads(FIXTURE.read_text(encoding="utf-8"))
            project["narration"] = {"text": "Olá! Este vídeo foi criado sem serviços externos.", "voice": "pt-br"}
            project_file = folder / "project.json"
            project_file.write_text(json.dumps(project, ensure_ascii=False), encoding="utf-8")
            output = folder / "result.mp4"
            report = run(project_file, output)
            self.assertEqual(report["status"], "verified")
            self.assertEqual(report["provider_calls"], 0)
            self.assertTrue(report["narration_generated_offline"])
            self.assertTrue(report["audio"]["present"])
            self.assertGreater(report["bytes"], 0)
            self.assertTrue((folder / "generated-narration.wav").is_file())

    def test_rejects_narration_path_traversal(self):
        if not all(shutil.which(name) for name in ("ffmpeg", "ffprobe", "espeak-ng")):
            self.skipTest("FFmpeg, FFprobe and eSpeak NG are required.")
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            project = json.loads(FIXTURE.read_text(encoding="utf-8"))
            project["narration"] = {"text": "teste", "output": "../outside.wav"}
            project_file = folder / "project.json"
            project_file.write_text(json.dumps(project), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "inside the project directory"):
                run(project_file, folder / "bad.mp4")

if __name__ == "__main__":
    unittest.main(verbosity=2)
