import os
import json
import traceback
import subprocess
from datetime import datetime

from flask import request, jsonify
from pydub import AudioSegment

from utils.transcription import transcribe_audio
from utils.call_intelligence import analyze_call_quality
from config.db import calls


# =====================================================
# 📁 DIRECTORIES
# =====================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "..", "uploads", "calls")
RESULTS_DIR = os.path.join(BASE_DIR, "..", "uploads", "results")

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)


# =====================================================
# 📤 UPLOAD CALL RECORDING
# =====================================================
def upload_call():
    try:
        print("FILES:", request.files)
        print("FORM:", request.form)

        file = request.files.get("audio")
        salesperson_id = request.form.get("salespersonId")
        outcome = request.form.get("outcome", "connected")

        if not file:
            return jsonify({
                "success": False,
                "error": "No audio file uploaded"
            }), 400

        # =================================================
        # 💾 SAVE WEBM FILE
        # =================================================
        timestamp = datetime.utcnow().timestamp()
        safe_filename = file.filename.replace(" ", "_")
        webm_filename = f"{timestamp}_{safe_filename}"
        webm_path = os.path.join(UPLOAD_DIR, webm_filename)

        file.save(webm_path)
        print(f"✅ Saved WEBM: {webm_path}")

        # =================================================
        # 🔄 CONVERT WEBM → WAV (SAFE)
        # =================================================
        wav_path = webm_path.rsplit(".", 1)[0] + ".wav"

        try:
            subprocess.run(
                [
                    "ffmpeg",
                    "-y",
                    "-i", webm_path,
                    "-ar", "16000",
                    "-ac", "1",
                    wav_path
                ],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except subprocess.CalledProcessError:
            return jsonify({
                "success": False,
                "error": "FFmpeg failed to decode WebRTC audio"
            }), 400

        print(f"✅ Converted WAV: {wav_path}")

        # =================================================
        # ⏱️ DURATION
        # =================================================
        audio = AudioSegment.from_wav(wav_path)
        duration_seconds = int(len(audio) / 1000)

        # =================================================
        # 📝 TRANSCRIPTION (WHISPER)
        # =================================================
        transcript = transcribe_audio(wav_path)

        # =================================================
        # 📊 ANALYSIS
        # =================================================
        analysis = analyze_call_quality([
            {
                "duration": duration_seconds,
                "outcome": outcome
            }
        ])

        # =================================================
        # 📦 PREPARE DATA
        # =================================================
        mongo_data = {
            "salespersonId": salesperson_id,
            "audioFilePath": webm_path,
            "wavFilePath": wav_path,
            "duration": duration_seconds,
            "outcome": outcome,
            "transcript": transcript,
            "analysis": analysis,
            "createdAt": datetime.utcnow(),
            "timestamp": timestamp
        }

        # =================================================
        # 🧠 SAVE TO MONGODB
        # =================================================
        result = calls.insert_one(mongo_data)
        mongo_id = str(result.inserted_id)

        print(f"✅ MongoDB saved with _id: {mongo_id}")

        # =================================================
        # 📄 SAVE JSON RESULT (FIXED)
        # =================================================
        json_data = mongo_data.copy()
        json_data["_id"] = mongo_id
        json_data["createdAt"] = json_data["createdAt"].isoformat()

        json_filename = f"{timestamp}_call_{mongo_id}_result.json"
        json_path = os.path.join(RESULTS_DIR, json_filename)

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)

        print(f"✅ JSON saved: {json_path}")

        # =================================================
        # 📤 RESPONSE
        # =================================================
        return jsonify({
            "success": True,
            "callId": mongo_id,
            "salespersonId": salesperson_id,
            "duration": duration_seconds,
            "outcome": outcome,
            "transcript": transcript,
            "analysis": analysis
        }), 200

    except Exception as e:
        print("❌ UPLOAD ERROR:", str(e))
        print(traceback.format_exc())

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
