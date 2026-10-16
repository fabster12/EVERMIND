#!/usr/bin/env python3
"""Generate per-scene narration WAVs.

Engine order: Piper (neural, offline) -> Windows SAPI (always available).
The engine actually used is printed loudly so there is never any doubt about
what produced the audio in the render.
"""
import json
import pathlib
import subprocess
import sys
import time

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
SCENES = ROOT / "scenes.json"
AUDIO = ROOT / "audio"
MODELS = ROOT / "tools" / "voices"

PIPER_VOICE = "en_US-lessac-medium"
PIPER_BASE = (
    "https://huggingface.co/rhasspy/piper-voices/resolve/main/"
    "en/en_US/lessac/medium/"
)
SAPI_VOICE_HINT = "David"
SAPI_RATE = -1  # -10..10, slightly slower than default

# Kokoro-82M via the bundled hyperframes CLI. Its model host is reachable from
# this network, unlike Piper's, so this is the preferred engine.
KOKORO_VOICE = "am_michael"
KOKORO_SPEED = "0.95"
KOKORO_PYTHON = r"C:\Users\3517418\AppData\Local\Python\pythoncore-3.14-64\python.exe"


def normalise(path: pathlib.Path) -> None:
    """Bring a clip to broadcast-ish loudness.

    Raw TTS lands around -24 LUFS. Players and conferencing tools expect roughly
    -14, so without this the narration is audible in a waveform but sounds like
    silence on laptop speakers at normal volume.
    """
    tmp = path.with_suffix(".norm.wav")
    r = subprocess.run(
        ["ffmpeg", "-y", "-i", str(path),
         "-af", "loudnorm=I=-14:TP=-1.5:LRA=11",
         "-ar", "48000", "-ac", "1", str(tmp)],
        capture_output=True, text=True,
    )
    if r.returncode == 0 and tmp.exists() and tmp.stat().st_size > 1000:
        # Anything holding the WAV open -- a renderer, a snapshot run, a media
        # player -- makes the rename fail with WinError 5 and kills the whole
        # batch. Retry briefly, and treat a lasting lock as this clip's problem
        # rather than the run's.
        for attempt in range(6):
            try:
                tmp.replace(path)
                return
            except PermissionError:
                time.sleep(1.5)
        tmp.unlink(missing_ok=True)
        print(f"  !! {path.name} is locked by another process, keeping raw level")
    else:
        tmp.unlink(missing_ok=True)
        print(f"  !! loudnorm failed for {path.name}, keeping raw level")


def up_to_date(dest: pathlib.Path, text: str) -> bool:
    """True if this clip was already synthesised from exactly this narration.

    Each clip costs a minute or two, so a run that dies partway -- or a script
    edit that only touches a couple of scenes -- should not re-voice the ones
    that are already correct. The narration text is stored beside the WAV and
    compared verbatim. Pass --all to ignore this.
    """
    if "--all" in sys.argv:
        return False
    stamp = dest.with_suffix(".txt")
    return (dest.exists() and dest.stat().st_size > 1000 and stamp.exists()
            and stamp.read_text(encoding="utf-8") == text)


def synth_kokoro(scenes) -> bool:
    import os
    env = dict(os.environ, HYPERFRAMES_PYTHON=KOKORO_PYTHON)
    for i, sc in enumerate(scenes, 1):
        dest = AUDIO / f"scene-{i:02d}.wav"
        if up_to_date(dest, sc["narration"]):
            print(f"  [{i:02d}] {sc['id']}  (unchanged)")
            continue
        txt = AUDIO / f"_scene-{i:02d}.txt"
        txt.write_text(sc["narration"], encoding="utf-8")
        r = subprocess.run(
            ["npx", "hyperframes@0.8.149", "tts", str(txt),
             "-v", KOKORO_VOICE, "-s", KOKORO_SPEED, "-o", str(dest)],
            capture_output=True, text=True, env=env, shell=True, timeout=600,
        )
        txt.unlink(missing_ok=True)
        if not dest.exists() or dest.stat().st_size < 1000:
            print(f"  !! scene {i} failed: {(r.stderr or r.stdout)[-200:]}")
            return False
        normalise(dest)
        # Record what this clip actually says, so a later run can skip it.
        dest.with_suffix(".txt").write_text(sc["narration"], encoding="utf-8")
        print(f"  [{i:02d}] {sc['id']}")
    return True


def try_piper() -> bool:
    try:
        import piper  # noqa: F401
    except ImportError:
        print("  piper not installed")
        return False

    onnx = MODELS / f"{PIPER_VOICE}.onnx"
    cfg = MODELS / f"{PIPER_VOICE}.onnx.json"
    if onnx.exists() and cfg.exists():
        return True

    MODELS.mkdir(parents=True, exist_ok=True)
    import urllib.request
    import ssl

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    for name in (f"{PIPER_VOICE}.onnx", f"{PIPER_VOICE}.onnx.json"):
        dest = MODELS / name
        if dest.exists():
            continue
        url = PIPER_BASE + name + "?download=true"
        try:
            print(f"  downloading {name} ...")
            with urllib.request.urlopen(url, context=ctx, timeout=120) as r:
                dest.write_bytes(r.read())
        except Exception as exc:
            print(f"  piper model fetch failed: {type(exc).__name__}: {str(exc)[:100]}")
            return False
    return onnx.exists() and cfg.exists()


def synth_piper(scenes) -> bool:
    from piper import PiperVoice
    import wave

    voice = PiperVoice.load(str(MODELS / f"{PIPER_VOICE}.onnx"))
    for i, sc in enumerate(scenes, 1):
        dest = AUDIO / f"scene-{i:02d}.wav"
        with wave.open(str(dest), "wb") as wf:
            voice.synthesize_wav(sc["narration"], wf)
        print(f"  [{i:02d}] {sc['id']}")
    return True


def synth_sapi(scenes) -> bool:
    """Windows SAPI via System.Speech. No network, always present."""
    for i, sc in enumerate(scenes, 1):
        dest = AUDIO / f"scene-{i:02d}.wav"
        text = sc["narration"].replace("'", "''")
        ps = (
            "Add-Type -AssemblyName System.Speech; "
            "$s = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
            f"try {{ $s.SelectVoice((($s.GetInstalledVoices() | "
            f"Where-Object {{ $_.VoiceInfo.Name -like '*{SAPI_VOICE_HINT}*' }} | "
            "Select-Object -First 1).VoiceInfo.Name)) } catch {}; "
            f"$s.Rate = {SAPI_RATE}; "
            f"$s.SetOutputToWaveFile('{dest}'); "
            f"$s.Speak('{text}'); $s.Dispose()"
        )
        r = subprocess.run(["powershell", "-NoProfile", "-Command", ps],
                           capture_output=True, text=True)
        if r.returncode != 0 or not dest.exists():
            print(f"  !! scene {i} failed: {r.stderr[:160]}")
            return False
        print(f"  [{i:02d}] {sc['id']}")
    return True


def main() -> int:
    scenes = json.loads(SCENES.read_text(encoding="utf-8"))
    AUDIO.mkdir(exist_ok=True)
    print(f"{len(scenes)} scenes to narrate\n")

    engine = None
    only_sapi = "--sapi" in sys.argv

    if not only_sapi:
        print("=== ENGINE: KOKORO-82M (neural, local) ===")
        if synth_kokoro(scenes):
            engine = "kokoro"
        else:
            print("  kokoro failed, trying piper")

    if engine is None and not only_sapi and try_piper():
        print("\n=== ENGINE: PIPER (neural, offline) ===")
        if synth_piper(scenes):
            engine = "piper"
    if engine is None:
        print("\n=== ENGINE: WINDOWS SAPI (fallback) ===")
        if synth_sapi(scenes):
            engine = "sapi"

    if engine is None:
        print("\nFAILED: no engine produced audio", file=sys.stderr)
        return 1

    (AUDIO / "_engine.txt").write_text(engine, encoding="utf-8")
    print(f"\n*** narration generated with: {engine.upper()} ***")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
