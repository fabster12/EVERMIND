#!/usr/bin/env python3
"""Build an .srt from scenes.json, timed against the measured narration.

Each scene's narration is split into caption-sized chunks and distributed
across that scene's speech window in proportion to character count. The voice
is synthetic and paced evenly, so proportional splitting tracks it closely.
"""
import json
import pathlib
import re
import subprocess
import sys
import wave
import contextlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
AUDIO = ROOT / "audio"
OUT = ROOT / "renders" / "evermind_vp_pitch.srt"

LEAD, TAIL = 0.4, 0.9
FLOOR = {"title": 6, "statement": 5, "steps": 7, "numbers": 7, "shots": 8,
         "bars": 7, "list": 7, "boxes": 6, "years": 7, "gallery": 8, "outro": 5}

MAX_CHARS = 84      # two lines of ~42
MIN_CUE = 1.2


def wav_duration(p: pathlib.Path) -> float:
    with contextlib.closing(wave.open(str(p))) as w:
        return w.getnframes() / w.getframerate()


def chunk(text: str):
    """Split narration into caption-sized pieces on sentence then clause."""
    sentences = re.findall(r"[^.!?]+[.!?]?", text)
    out = []
    for s in (x.strip() for x in sentences):
        if not s:
            continue
        if len(s) <= MAX_CHARS:
            out.append(s)
            continue
        # too long: break on commas, then on width
        part, buf = [], ""
        for piece in re.split(r"(?<=,)\s+", s):
            if len(buf) + len(piece) + 1 <= MAX_CHARS:
                buf = f"{buf} {piece}".strip()
            else:
                if buf:
                    part.append(buf)
                buf = piece
        if buf:
            part.append(buf)
        for p in part:
            while len(p) > MAX_CHARS:
                cut = p.rfind(" ", 0, MAX_CHARS)
                cut = cut if cut > 0 else MAX_CHARS
                out.append(p[:cut].strip())
                p = p[cut:].strip()
            if p:
                out.append(p)
    return out


def wrap(line: str) -> str:
    if len(line) <= 44:
        return line
    cut = line.rfind(" ", 0, 46)
    return line if cut <= 0 else line[:cut] + "\n" + line[cut + 1:]


def ts(sec: float) -> str:
    if sec < 0:
        sec = 0
    h, rem = divmod(sec, 3600)
    m, s = divmod(rem, 60)
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int(round((s - int(s)) * 1000)):03d}"


def main() -> int:
    scenes = json.loads((ROOT / "scenes.json").read_text(encoding="utf-8"))

    cues, idx, clock = [], 0, 0.0
    for i, sc in enumerate(scenes, 1):
        wav = AUDIO / f"scene-{i:02d}.wav"
        spoken = wav_duration(wav) if wav.exists() else 0.0
        dur = max(FLOOR.get(sc["kind"], 6), spoken + LEAD + TAIL)

        pieces = chunk(sc["narration"])
        total = sum(len(p) for p in pieces) or 1
        speak_start = clock + LEAD
        at = speak_start
        for p in pieces:
            share = spoken * (len(p) / total)
            end = at + max(MIN_CUE, share)
            idx += 1
            cues.append((idx, at, min(end, speak_start + spoken + 0.35), wrap(p)))
            at = end
        clock += dur

    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text("\n".join(
        f"{n}\n{ts(a)} --> {ts(b)}\n{txt}\n" for n, a, b, txt in cues
    ), encoding="utf-8")

    print(f"{OUT}  {len(cues)} cues, {clock/60:.1f} min")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
