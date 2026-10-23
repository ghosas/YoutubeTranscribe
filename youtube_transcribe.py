#!/usr/bin/env python3

import sys
import subprocess
from pathlib import Path
from urllib.parse import parse_qs, urlparse
from faster_whisper import WhisperModel


# --------------------------------------------------
# Configuration
# --------------------------------------------------

DOWNLOAD_DIR = Path.home() / "Downloads"
MODEL_SIZE = "small"

# Deno is used by yt-dlp for YouTube's JavaScript processing
YT_DLP = "yt-dlp"
JS_RUNTIME = "deno"


# --------------------------------------------------
# Validate command-line argument
# --------------------------------------------------

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <YouTube URL>")
    sys.exit(1)

youtube_url = sys.argv[1]


# --------------------------------------------------
# Download audio using yt-dlp
# --------------------------------------------------

print("\n[1/3] Downloading audio from YouTube...\n")
filename= f"{DOWNLOAD_DIR}/%(title)s [%(id)s].%(ext)s"
if Path(filename).exists():
    print(f"Audio file already exists: {filename}")
    rename = input("Do you want to rename the existing file? (y/n): ")
    if rename.lower() == "y":
        new_filename = input("Enter the new filename (without extension): ")
        new_filename_with_ext = f"{DOWNLOAD_DIR}/{new_filename}.mp3"
        Path(filename).rename(new_filename_with_ext)
        print(f"Renamed existing file to: {new_filename_with_ext}") 
command = [
    YT_DLP,
    "--js-runtimes", JS_RUNTIME,
    "-x",
    "--audio-format", "mp3",
    "-o", str(DOWNLOAD_DIR / "%(title)s [%(id)s].%(ext)s"),
    youtube_url,
]

try:
    subprocess.run(command, check=True)
except subprocess.CalledProcessError:
    print("\nERROR: yt-dlp failed.")
    sys.exit(1)


# --------------------------------------------------
# Find the downloaded MP3
# --------------------------------------------------

# yt-dlp uses the video ID in the filename.
# Extract the ID from the URL for reliable identification.

video_id = parse_qs(urlparse(youtube_url).query).get("v", [""])[0]

mp3_files = [
    path for path in DOWNLOAD_DIR.glob("*.mp3")
    if path.name.endswith(f"[{video_id}].mp3")
]

if not mp3_files:
    print("ERROR: Could not find downloaded MP3.")
    sys.exit(1)

audio_file = mp3_files[0]

print(f"\nAudio file: {audio_file.name}")


# --------------------------------------------------
# Create output filename
# --------------------------------------------------

output_file = audio_file.with_suffix(".txt")


# --------------------------------------------------
# Load Whisper
# --------------------------------------------------

print("\n[2/3] Loading Whisper model...")
print(f"Model: {MODEL_SIZE}")
print("Device: CPU")
print("Language: English\n")

model = WhisperModel(
    MODEL_SIZE,
    device="cpu",
    compute_type="int8"
)


# --------------------------------------------------
# Transcribe
# --------------------------------------------------

print("[3/3] Transcribing...\n")

segments, info = model.transcribe(
    str(audio_file),
    language="en",
    beam_size=5
)


# --------------------------------------------------
# Write plain-text transcript
# --------------------------------------------------

with open(output_file, "w", encoding="utf-8") as f:

    for segment in segments:
        text = segment.text.strip()

        if text:
            f.write(text + "\n")


print("\n----------------------------------------")
print("Transcription complete")
print("----------------------------------------")
print(f"Language detected : {info.language}")
print(f"Confidence        : {info.language_probability:.2f}")
print(f"Transcript        : {output_file}")
print("----------------------------------------\n")