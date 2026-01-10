import whisper

model = whisper.load_model("base")  # fast + accurate enough

def transcribe_audio(file_path):
    try:
        print(f"🔄 Transcribing: {file_path}")
        result = model.transcribe(file_path)
        transcript = result["text"]
        print(f"✅ Transcript: {transcript}")
        return transcript
    except Exception as e:
        print(f"❌ Transcription error: {e}")
        return f"[Transcription failed: {str(e)}]"