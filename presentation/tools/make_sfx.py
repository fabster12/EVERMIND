#!/usr/bin/env python3
"""Generate subtle UI sound effects locally with ffmpeg.

No sourced audio, so nothing to license. Three cues:
  tick    - soft click as a stat / list item appears
  swoosh  - filtered noise sweep on a scene change
  chime   - two-note resolve on the closing card
All are quiet by design; they sit under the narration, not beside it.
"""
import pathlib
import subprocess
import sys

OUT = pathlib.Path(__file__).resolve().parent.parent / "assets" / "sfx"
SR = 48000


def run(args) -> bool:
    r = subprocess.run(args, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-400:], file=sys.stderr)
    return r.returncode == 0


def tick(dest: pathlib.Path) -> bool:
    # short sine blip with a fast exponential decay
    return run([
        "ffmpeg", "-y",
        "-f", "lavfi", "-i", f"sine=frequency=1850:duration=0.085:sample_rate={SR}",
        "-af", "afade=t=out:st=0.012:d=0.073:curve=exp,volume=0.13",
        "-ac", "1", str(dest),
    ])


def swoosh(dest: pathlib.Path) -> bool:
    # band-passed noise, swept and faded - reads as a soft transition
    return run([
        "ffmpeg", "-y",
        "-f", "lavfi", "-i", f"anoisesrc=d=0.45:c=pink:r={SR}:a=0.5",
        "-af", ("highpass=f=500,lowpass=f=4200,"
                "afade=t=in:st=0:d=0.14:curve=qsin,"
                "afade=t=out:st=0.16:d=0.29:curve=exp,volume=0.10"),
        "-ac", "1", str(dest),
    ])


def chime(dest: pathlib.Path) -> bool:
    # C6 then G6, overlapped, long soft tail
    return run([
        "ffmpeg", "-y",
        "-f", "lavfi", "-i", f"sine=frequency=1046:duration=1.1:sample_rate={SR}",
        "-f", "lavfi", "-i", f"sine=frequency=1568:duration=1.1:sample_rate={SR}",
        "-filter_complex",
        ("[0:a]afade=t=out:st=0.05:d=1.0:curve=exp,volume=0.12[a];"
         "[1:a]adelay=130|130,afade=t=out:st=0.18:d=0.9:curve=exp,volume=0.09[b];"
         "[a][b]amix=inputs=2:normalize=0"),
        "-ac", "1", str(dest),
    ])


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    made = 0
    for name, fn in (("tick", tick), ("swoosh", swoosh), ("chime", chime)):
        dest = OUT / f"{name}.wav"
        if fn(dest) and dest.exists():
            kb = dest.stat().st_size / 1024
            print(f"  {name}.wav  {kb:.0f} KB")
            made += 1
    print(f"\n{made}/3 effects in {OUT}")
    return 0 if made == 3 else 1


if __name__ == "__main__":
    raise SystemExit(main())
