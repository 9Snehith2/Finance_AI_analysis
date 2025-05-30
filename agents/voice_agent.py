from fastapi import FastAPI, File, UploadFile
import whisper
import requests
import pyttsx3
import os

app = FastAPI()
model = whisper.load_model("base")  # You can use "small" or "medium" for better quality

@app.post("/voice-summary")
async def voice_summary(file: UploadFile = File(...)):
    try:
        # Save uploaded file
        audio_path = f"temp_audio_{file.filename}"
        with open(audio_path, "wb") as buffer:
            buffer.write(await file.read())

        # Step 1: Transcribe using Whisper
        result = model.transcribe(audio_path)
        transcribed_text = result["text"]

        # Step 2: Call the summarizer (LLaMA)
        response = requests.post(
            "http://127.0.0.1:8000/generate-summary",
            json={
                "query": "Summarize this user's spoken content.",
                "context_chunks": [transcribed_text]
            }
        )
        summary = response.json().get("response", "No summary returned.")

        # Step 3: Convert summary to speech using pyttsx3
        tts = pyttsx3.init()
        tts.save_to_file(summary, "response_audio.mp3")
        tts.runAndWait()

        return {
            "transcription": transcribed_text,
            "summary": summary,
            "audio_file": "response_audio.mp3"
        }
    except Exception as e:
        return {"error": str(e)}
    finally:
        if os.path.exists(audio_path):
            os.remove(audio_path)
