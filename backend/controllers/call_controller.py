from flask import request, jsonify, Response
from twilio.rest import Client
from datetime import datetime
from config.db import calls
import os

# ✅ Print credentials to verify (remove in production)
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_TOKEN = os.getenv("TWILIO_TOKEN")
TWILIO_PHONE = os.getenv("TWILIO_PHONE")
PUBLIC_URL = os.getenv("PUBLIC_URL")

print("=" * 50)
print("TWILIO CONFIG CHECK:")
print(f"SID: {TWILIO_SID[:10]}..." if TWILIO_SID else "SID: NOT SET")
print(f"TOKEN: {TWILIO_TOKEN[:10]}..." if TWILIO_TOKEN else "TOKEN: NOT SET")
print(f"TWILIO_PHONE: {TWILIO_PHONE}")
print(f"PUBLIC_URL: {PUBLIC_URL}")
print("=" * 50)

client = Client(TWILIO_SID, TWILIO_TOKEN)


# 1️⃣ START CALL (BRIDGE TWO PEOPLE)
def make_call():
    try:
        data = request.json

        agent_phone = data.get("agentPhone")      # Friend A
        customer_phone = data.get("customerPhone")  # Friend B
        salesperson_id = data.get("salespersonId")

        print(f"📞 CALL REQUEST:")
        print(f"   Agent: {agent_phone}")
        print(f"   Customer: {customer_phone}")
        print(f"   Salesperson: {salesperson_id}")

        if not agent_phone or not customer_phone:
            return jsonify({"message": "Both phone numbers required"}), 400

        # ✅ Validate phone format (must be E.164 format: +919876543210)
        if not agent_phone.startswith('+'):
            agent_phone = '+' + agent_phone
        if not customer_phone.startswith('+'):
            customer_phone = '+' + customer_phone

        print(f"   Formatted Agent: {agent_phone}")
        print(f"   Formatted Customer: {customer_phone}")

        # ✅ Create TwiML URL
        twiml_url = f"{PUBLIC_URL}/api/call/voice?customer={customer_phone}"
        print(f"   TwiML URL: {twiml_url}")

        # ✅ Make the call
        call = client.calls.create(
            to=agent_phone,
            from_=TWILIO_PHONE,
            url=twiml_url,
            record=True,
            status_callback=f"{PUBLIC_URL}/api/call/status",  # Optional: track status
            status_callback_event=['initiated', 'ringing', 'answered', 'completed']
        )

        print(f"✅ Call initiated! SID: {call.sid}, Status: {call.status}")

        # Save to DB
        calls.insert_one({
            "salespersonId": salesperson_id,
            "agent": agent_phone,
            "customer": customer_phone,
            "callSid": call.sid,
            "status": call.status,
            "createdAt": datetime.utcnow()
        })

        return jsonify({
            "message": "Call initiated",
            "callSid": call.sid,
            "status": call.status,
            "agent": agent_phone,
            "customer": customer_phone
        })

    except Exception as e:
        print("❌ TWILIO ERROR:", str(e))
        import traceback
        print(traceback.format_exc())
        return jsonify({
            "message": "Failed to start call",
            "error": str(e)
        }), 500


# 2️⃣ TWIML – CONNECT BOTH PHONES + RECORD
def voice_connect():
    customer = request.args.get("customer")
    
    print(f"🎙️ TwiML REQUEST - Connecting to: {customer}")

    # ✅ Fixed TwiML with proper syntax
    twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="Polly.Joanna">Connecting your call. Please wait.</Say>
    <Dial record="record-from-answer" recordingStatusCallback="{PUBLIC_URL}/api/call/recording">
        {customer}
    </Dial>
</Response>
"""
    
    print(f"📋 Sending TwiML:")
    print(twiml)
    
    return Response(twiml, mimetype="text/xml")


# 3️⃣ RECORDING CALLBACK (Optional)
def recording_callback():
    recording_url = request.values.get("RecordingUrl")
    call_sid = request.values.get("CallSid")
    
    print(f"🎤 Recording available: {recording_url}")
    
    calls.update_one(
        {"callSid": call_sid},
        {"$set": {"recordingUrl": recording_url}}
    )
    
    return "", 200


def get_recordings():
    """Get all recorded calls"""
    recordings = list(calls.find({"callType": "webrtc"}).sort("createdAt", -1))
    
    return jsonify([{
        "callId": r["callSid"],
        "salesperson": r["salespersonId"],
        "customer": r["customer"],
        "duration": r["duration"],
        "transcript": r.get("transcript", "N/A"),
        "analysis": r.get("analysis", {}),
        "createdAt": r["createdAt"].isoformat(),
        "audioPath": r.get("audioFilePath", "N/A")
    } for r in recordings])


# 4️⃣ STATUS CALLBACK (Optional - to track call progress)
def status_callback():
    call_sid = request.values.get("CallSid")
    call_status = request.values.get("CallStatus")
    call_duration = request.values.get("CallDuration")
    
    print(f"📊 Call Status Update: {call_sid} - {call_status}")
    
    calls.update_one(
        {"callSid": call_sid},
        {"$set": {
            "status": call_status,
            "duration": int(call_duration) if call_duration else 0
        }}
    )
    
    return "", 200


# 5️⃣ END CALL (OPTIONAL)
def end_call():
    data = request.json
    call_sid = data.get("callSid")
    duration = data.get("duration")

    if not call_sid:
        return jsonify({"message": "callSid missing"}), 400

    calls.update_one(
        {"callSid": call_sid},
        {"$set": {
            "status": "completed",
            "duration": duration
        }}
    )

    return jsonify({"message": "Call updated"})