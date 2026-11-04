#!/usr/bin/env python3
"""Create deterministic local media fixtures for the FFmpeg renderer CI test."""
import math, struct, wave
from pathlib import Path
out = Path(__file__).resolve().parent
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
print("Created fixture.ppm and voice.wav")
