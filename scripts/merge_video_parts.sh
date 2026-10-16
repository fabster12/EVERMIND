#!/usr/bin/env bash
# Join presentation/renders/part1.mp4 .. partN.mp4 (in numeric order) into
# presentation/renders/evermind_vp_pitch.mp4.
#
#   ./scripts/merge_video_parts.sh
#
# Requires ffmpeg on PATH. No ffmpeg? Use scripts/merge_video_parts.py
# instead (uv run scripts/merge_video_parts.py) - it fetches its own ffmpeg.
#
# Stream-copies (no re-encode) since the parts already share the same
# codec/bitrate from one render pass. The joined file is gitignored - it's
# over GitHub's 100 MB limit and rebuilds from the parts in seconds.

set -euo pipefail

cd "$(dirname "$0")/.."

if ! command -v ffmpeg >/dev/null 2>&1; then
    echo "ffmpeg not found on PATH." >&2
    echo "Install it, or run: uv run scripts/merge_video_parts.py" >&2
    exit 1
fi

RENDERS="presentation/renders"
OUT_NAME="evermind_vp_pitch.mp4"

shopt -s nullglob
parts=("$RENDERS"/part*.mp4)
shopt -u nullglob

if [ ${#parts[@]} -eq 0 ]; then
    echo "No part*.mp4 files found in $RENDERS" >&2
    exit 1
fi

# Sort numerically by the digits in the filename so part2 < part10.
IFS=$'\n' sorted=($(printf '%s\n' "${parts[@]}" | sort -t p -k2 -n))
unset IFS

listing="$RENDERS/_concat.txt"
> "$listing"
for p in "${sorted[@]}"; do
    echo "  $(basename "$p")"
    echo "file '$(basename "$p")'" >> "$listing"
done

echo "joining ${#sorted[@]} parts -> $RENDERS/$OUT_NAME"

# Entries in the concat list are relative to the list file, so run ffmpeg
# with cwd = RENDERS instead of passing full paths.
(
    cd "$RENDERS"
    ffmpeg -y -f concat -safe 0 -i "_concat.txt" \
        -c copy -movflags +faststart "$OUT_NAME"
)

rm -f "$listing"

mb=$(du -m "$RENDERS/$OUT_NAME" | cut -f1)
echo ""
echo "$RENDERS/$OUT_NAME  (${mb} MB)"
