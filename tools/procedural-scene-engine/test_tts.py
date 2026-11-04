#!/usr/bin/env python3
"""Smoke test for optional offline narration synthesis."""
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
TOOL=ROOT/"tools/procedural-scene-engine/tts.py"

class OfflineTtsTests(unittest.TestCase):
    def test_generates_local_wav_without_network(self):
        if not shutil.which("espeak-ng"):
            self.skipTest("eSpeak NG is not installed.")
        with tempfile.TemporaryDirectory() as tmp:
            output=Path(tmp)/"voice.wav"
            result=subprocess.run(["python3",str(TOOL),"Olá! Este é um teste de narração.","--output",str(output),"--voice","pt-br"],text=True,capture_output=True)
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertGreater(output.stat().st_size,44)
            self.assertEqual(output.read_bytes()[:4],b"RIFF")

if __name__=="__main__": unittest.main(verbosity=2)
