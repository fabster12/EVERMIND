# /// script
# requires-python = ">=3.12"
# dependencies = ["imageio-ffmpeg"]
# ///
"""Join presentation/renders/part1.mp4 .. partN.mp4 (numeric order) into
presentation/renders/evermind_vp_pitch.mp4.

    uv run scripts/merge_video_parts.py

Uses the static ffmpeg binary bundled by the imageio-ffmpeg package instead
of a system install, since not everyone running this has ffmpeg on PATH.
Stream-copies (no re-encode) - the parts already share the same codec and
bitrate from one render pass. The joined file is gitignored: it's over
GitHub's 100 MB limit and rebuilds from the parts in seconds.
"""
import pathlib
import re
import subprocess
import sys

import imageio_ffmpeg

ROOT = pathlib.Path(__file__).resolve().parent.parent
RENDERS = ROOT / "presentation" / "renders"
OUT_NAME = "evermind_vp_pitch.mp4"


def part_number(p: pathlib.Path) -> int:
    m = re.search(r"\d+", p.stem)
    return int(m.group()) if m else 0


def main() -> int:
    parts = sorted(RENDERS.glob("part*.mp4"), key=part_number)
    if not parts:
        print(f"No part*.mp4 files found in {RENDERS}", file=sys.stderr)
        return 1

    for p in parts:
        print(f"  {p.name}")

    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

    # Entries in the concat list are relative to the list file, so write
    # bare names and run ffmpeg with cwd = RENDERS.
    listing = RENDERS / "_concat.txt"
    listing.write_text(
        "".join(f"file '{p.name}'\n" for p in parts), encoding="utf-8")

    print(f"\njoining {len(parts)} parts -> {RENDERS / OUT_NAME}")
    cmd = [
        ffmpeg, "-y", "-f", "concat", "-safe", "0", "-i", listing.name,
        "-c", "copy", "-movflags", "+faststart", OUT_NAME,
    ]
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=RENDERS)
    listing.unlink(missing_ok=True)

    if r.returncode != 0:
        print(r.stderr[-2000:], file=sys.stderr)
        return 1

    out = RENDERS / OUT_NAME
    mb = out.stat().st_size / 1_048_576
    print(f"\n{out}  ({mb:.1f} MB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
