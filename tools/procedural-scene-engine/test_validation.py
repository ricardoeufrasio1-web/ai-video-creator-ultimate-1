#!/usr/bin/env python3
"""Input validation tests for the provider-free procedural renderer."""
import json
import tempfile
import unittest
from pathlib import Path

from render import validate

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "examples/procedural-scenes/render-fixture.json"

class ProceduralValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.folder = Path(self.temp.name)
        self.project = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def tearDown(self):
        self.temp.cleanup()

    def test_accepts_basic_project(self):
        self.assertEqual(validate(self.project, self.folder), [])

    def test_rejects_audio_path_traversal(self):
        outside = self.folder.parent / "private-audio.wav"
        self.project["voiceover"] = {"src": "../private-audio.wav"}
        errors = validate(self.project, self.folder)
        self.assertTrue(any("must stay inside" in error for error in errors))

    def test_rejects_missing_local_audio(self):
        self.project["music"] = {"src": "not-here.wav"}
        errors = validate(self.project, self.folder)
        self.assertTrue(any("asset file not found" in error for error in errors))

    def test_rejects_unknown_camera(self):
        self.project["scenes"][0]["camera"] = "teleport"
        errors = validate(self.project, self.folder)
        self.assertTrue(any("Unsupported camera" in error for error in errors))

    def test_rejects_transition_longer_than_scene(self):
        self.project["transition"] = {"type": "crossfade", "duration": 2, "effect": "fade"}
        errors = validate(self.project, self.folder)
        self.assertTrue(any("longer than the transition" in error for error in errors))

if __name__ == "__main__":
    unittest.main(verbosity=2)
