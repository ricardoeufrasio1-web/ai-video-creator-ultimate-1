#!/usr/bin/env python3
"""Negative and input-validation tests for the experimental FFmpeg renderer."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
RENDERER = REPO / "tools" / "ffmpeg-render" / "render.py"


class RendererValidationTests(unittest.TestCase):
    def run_project(self, folder, project):
        project_path = folder / "project.json"
        project_path.write_text(json.dumps(project), encoding="utf-8")
        output = folder / "out.mp4"
        result = subprocess.run(
            [sys.executable, str(RENDERER), str(project_path), "--output", str(output)],
            text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
        return result, output

    def test_empty_scenes_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            result, output = self.run_project(Path(temp), {"scenes": []})
            self.assertEqual(result.returncode, 2)
            self.assertIn("non-empty scenes array", result.stderr)
            self.assertFalse(output.exists())

    def test_path_traversal_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp) / "project"
            folder.mkdir()
            outside = Path(temp) / "outside.ppm"
            outside.write_text("not a real image", encoding="utf-8")
            result, output = self.run_project(folder, {
                "width": 320, "height": 180, "fps": 24,
                "scenes": [{"type": "image", "src": "../outside.ppm", "duration": 1}],
            })
            self.assertEqual(result.returncode, 2)
            self.assertIn("escapes project directory", result.stderr)
            self.assertFalse(output.exists())

    def test_missing_asset_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            result, output = self.run_project(folder, {
                "scenes": [{"type": "image", "src": "missing.png", "duration": 1}],
            })
            self.assertEqual(result.returncode, 2)
            self.assertIn("Asset file not found", result.stderr)
            self.assertFalse(output.exists())


    def test_audio_cue_duplicate_ids_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            (folder / "tone.wav").write_bytes(b"fake audio")
            (folder / "frame.ppm").write_bytes(b"P6\n1 1\n255\n\x00\x00\x00")
            result, output = self.run_project(folder, {
                "scenes": [{"type": "image", "src": "frame.ppm", "duration": 2}],
                "audio_cues": [
                    {"id": "same", "src": "tone.wav", "start": 0, "duration": 1},
                    {"id": "same", "src": "tone.wav", "start": 1, "duration": 1},
                ],
            })
            self.assertEqual(result.returncode, 2)
            self.assertIn("unique non-empty id", result.stderr)
            self.assertFalse(output.exists())

    def test_audio_cue_outside_timeline_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            (folder / "tone.wav").write_bytes(b"fake audio")
            (folder / "frame.ppm").write_bytes(b"P6\n1 1\n255\n\x00\x00\x00")
            result, output = self.run_project(folder, {
                "scenes": [{"type": "image", "src": "frame.ppm", "duration": 2}],
                "audio_cues": [{"id": "cue", "src": "tone.wav", "start": 1.5, "duration": 1}],
            })
            self.assertEqual(result.returncode, 2)
            self.assertIn("fit within the project duration", result.stderr)
            self.assertFalse(output.exists())

    def test_scene_fade_longer_than_scene_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            (folder / "frame.ppm").write_bytes(b"P6\\n1 1\\n255\\n\\x00\\x00\\x00")
            result, output = self.run_project(folder, {
                "scenes": [{"type": "image", "src": "frame.ppm", "duration": 1, "fade_in": 1.1}],
            })
            self.assertEqual(result.returncode, 2)
            self.assertIn("invalid fade values", result.stderr)
            self.assertFalse(output.exists())

    def test_invalid_transition_effect_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            result, output = self.run_project(folder, {
                "transition": {"type": "crossfade", "effect": "teleport", "duration": 0.5},
                "scenes": [
                    {"type": "image", "src": "first.png", "duration": 1},
                    {"type": "image", "src": "second.png", "duration": 1},
                ],
            })
            self.assertEqual(result.returncode, 2)
            self.assertIn("transition.effect must be one of", result.stderr)
            self.assertFalse(output.exists())

    def test_invalid_audio_normalization_range_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            result, output = self.run_project(folder, {
                "scenes": [{"type": "image", "src": "frame.png", "duration": 1}],
                "audio_normalization": {"integrated_lufs": -80},
            })
            self.assertEqual(result.returncode, 2)
            self.assertIn("targets are out of supported ranges", result.stderr)
            self.assertFalse(output.exists())

    def test_invalid_scene_type_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            result, output = self.run_project(folder, {
                "scenes": [{"type": "audio", "src": "x.wav", "duration": 1}],
            })
            self.assertEqual(result.returncode, 2)
            self.assertIn("type must be image or video", result.stderr)
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
