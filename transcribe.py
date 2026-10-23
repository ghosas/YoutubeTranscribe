from faster_whisper import WhisperModel

audio_file = "/home/santanughosal/Downloads/Layoffs Hitting 40⧸45+ Employees 😢(Careers Are Ending Earlier Than Ever in IT industry) [1ZNZaagzxqk].mp3"

model = WhisperModel("small", device="cpu", compute_type="int8")

segments, info = model.transcribe(
    audio_file,
    language="en",
    beam_size=5
)

with open("/home/santanughosal/Downloads/transcript.txt", "w", encoding="utf-8") as f:
    for segment in segments:
        line = f"[{segment.start:.1f}s → {segment.end:.1f}s] {segment.text.strip()}\n"
        print(line, end="")
        f.write(line)

print(f"\nDetected language: {info.language}")
print(f"Language probability: {info.language_probability:.2f}")