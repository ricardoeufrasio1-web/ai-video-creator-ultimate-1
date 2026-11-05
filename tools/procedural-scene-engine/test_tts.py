#!/usr/bin/env python3
"""Smoke tests for optional offline narration synthesis and its quality gate."""
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
TOOL=ROOT/"tools/procedural-scene-engine/tts.py"

class OfflineTtsTests(unittest.TestCase):
    def test_blocks_robotic_voice_without_explicit_opt_in(self):
        with tempfile.TemporaryDirectory() as tmp:
            output=Path(tmp)/"voice.wav"
            result=subprocess.run(["python3",str(TOOL),"Olá!","--output",str(output)],text=True,capture_output=True)
            self.assertEqual(result.returncode,2)
            self.assertIn("sounds synthetic/robotic",result.stderr)
            self.assertFalse(output.exists())

    def test_generates_local_wav_without_network_when_explicitly_enabled(self):
        if not shutil.which("espeak-ng"):
            self.skipTest("eSpeak NG is not installed.")
        with tempfile.TemporaryDirectory() as tmp:
            output=Path(tmp)/"voice.wav"
            result=subprocess.run(["python3",str(TOOL),"Olá! Este é um teste de narração.","--output",str(output),"--voice","pt-br","--allow-robotic-espeak"],text=True,capture_output=True)
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertGreater(output.stat().st_size,44)
            self.assertEqual(output.read_bytes()[:4],b"RIFF")
            self.assertIn("Synthetic/robotic draft voice",result.stdout)

if __name__=="__main__": unittest.main(verbosity=2)
