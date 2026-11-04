#!/usr/bin/env python3
"""Create deterministic local media fixtures beside the sample render project."""
import math, struct, wave
from pathlib import Path

repo_root = Path(__file__).resolve().parents[2]
out = repo_root / "examples" / "render"
out.mkdir(parents=True, exist_ok=True)
w, h = 320, 180
with (out / "fixture.ppm").open("wb") as f:
    f.write(f"P6\n{w} {h}\n255\n".encode("ascii"))
    for y in range(h):
        for x in range(w):
            f.write(bytes((int(40+150*x/w), int(60+100*y/h), 180)))
rate = 44100
with wave.open(str(out / "voice.wav"), "wb") as wav:
    wav.setnchannels(1); wav.setsampwidth(2); wav.setframerate(rate)
    data = bytearray()
    for i in range(rate):
        data.extend(struct.pack("<h", int(4000*math.sin(2*math.pi*440*i/rate))))
    wav.writeframes(data)
(out / "captions.srt").write_text("1\\n00:00:00,200 --> 00:00:01,800\\nAutomated caption test\\n", encoding="utf-8")\nprint(f"Created render fixtures in {out}")
