# AudioTranslate

Download audio from a YouTube video and transcribe it to plain text using
[faster-whisper](https://github.com/SYSTRAN/faster-whisper).

## Requirements

- Python 3
- [yt-dlp](https://github.com/yt-dlp/yt-dlp), available on your `PATH`
- [Deno](https://deno.com/), available on your `PATH` for yt-dlp's YouTube
  JavaScript processing
- FFmpeg, required by yt-dlp to extract and convert audio

Install the Python dependencies:

```bash
python -m pip install -r requirements.txt
```

## Usage

Run the script with a YouTube watch URL:

```bash
python youtube_transcribe.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

The script downloads an MP3 to `~/Downloads`, named after the video and its
YouTube ID, then writes a plain-text transcript beside it with the same base
name and a `.txt` extension. It transcribes English using the `small`
faster-whisper model on the CPU. The model may be downloaded the first time it
runs.

## Notes

- The downloaded audio is retained; the script does not delete it after
  transcription.
- Transcription is configured for English. The transcript contains one
  non-empty segment per line, without timestamps.
