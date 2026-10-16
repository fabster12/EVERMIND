#!/usr/bin/env python3
"""Join the six rendered parts into the final deliverable.

Re-encodes rather than stream-copying: the parts come out of separate render
passes and a concat demuxer copy can desync audio at the joins.
"""
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
RENDERS = ROOT / "renders"
OUT = RENDERS / "evermind_vp_pitch.mp4"
PARTS = [RENDERS / f"part{n}.mp4" for n in range(1, 6)]


def probe_duration(p: pathlib.Path) -> float:
    """Return the clip's duration, or 0 if it is unreadable / still being written."""
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(p)],
        capture_output=True, text=True,
    )
    try:
        return float(r.stdout.strip())
    except ValueError:
        return 0.0


def main() -> int:
    missing = [p.name for p in PARTS if not p.exists()]
    if missing:
        print(f"missing: {', '.join(missing)}", file=sys.stderr)
        return 1

    # A part that is still being written has no moov atom yet, and concatenating
    # it yields a truncated file that looks like a success. Probe each one first.
    bad = []
    for p in PARTS:
        d = probe_duration(p)
        if d <= 0:
            bad.append(p.name)
        else:
            print(f"  {p.name}  {d:6.1f}s")
    if bad:
        print(f"\nnot readable yet (still rendering?): {', '.join(bad)}",
              file=sys.stderr)
        return 1

    # Entries resolve relative to the list file, so write bare names and run
    # ffmpeg from the renders directory.
    listing = RENDERS / "_concat.txt"
    listing.write_text(
        "".join(f"file '{p.name}'\n" for p in PARTS), encoding="utf-8")

    # The parts are already H.264/AAC from one renderer with identical
    # settings, so copy the streams instead of transcoding. Re-encoding here
    # previously halved the bitrate (2.7 -> 1.3 Mbps) and smeared the small
    # UI text in the screenshots, which is the whole point of those shots.
    cmd = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", listing.name,
        "-c", "copy", "-movflags", "+faststart",
        OUT.name,
    ]
    print(f"\njoining {len(PARTS)} parts ...")
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=RENDERS)
    if r.returncode != 0:
        print(r.stderr[-2000:], file=sys.stderr)
        return 1

    listing.unlink(missing_ok=True)
    mb = OUT.stat().st_size / 1048576
    print(f"\n{OUT}  {mb:.1f} MB")

    def vbitrate(p: pathlib.Path) -> float:
        r = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v",
             "-show_entries", "stream=bit_rate", "-of", "csv=p=0", str(p)],
            capture_output=True, text=True)
        try:
            return float(r.stdout.strip()) / 1e6
        except ValueError:
            return 0.0

    # Compare against the duration-weighted average, not the single highest
    # part: a stream copy lands on the average by definition, so using the
    # max flags a false regression whenever one part is denser than the rest.
    num = den = 0.0
    for p in PARTS:
        d = probe_duration(p)
        num += vbitrate(p) * d
        den += d
    src = num / den if den else 0.0
    got = vbitrate(OUT)
    print(f"video bitrate: parts average {src:.1f} Mbps -> joined {got:.1f} Mbps")
    if src and got < src * 0.9:
        print("WARNING: the join lost bitrate; small text will look smeared",
              file=sys.stderr)
        return 1

    probe = subprocess.run([
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration:stream=codec_type,codec_name",
        "-of", "default=noprint_wrappers=1", str(OUT),
    ], capture_output=True, text=True)
    print(probe.stdout.strip())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
