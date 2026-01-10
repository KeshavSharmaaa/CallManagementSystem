from flask import request, jsonify
from datetime import datetime
from config.db import followups


# =========================
# ADD FOLLOW-UP
# =========================
def add_followup(salesperson):
    data = request.json

    followups.insert_one({
        "leadId": data["leadId"],
        "salespersonId": salesperson["id"],
        "managerId": data["managerId"],
        "scheduledTime": datetime.fromisoformat(data["scheduledTime"]),
        "completed": False,
        "completedAt": None
    })

    return jsonify({"message": "Follow-up scheduled successfully"})


# =========================
# COMPLETE FOLLOW-UP
# =========================
def complete_followup(salesperson):
    data = request.json

    result = followups.update_one(
        {
            "_id": data["followupId"],
            "salespersonId": salesperson["id"]
        },
        {
            "$set": {
                "completed": True,
                "completedAt": datetime.utcnow()
            }
        }
    )

    if result.matched_count == 0:
        return jsonify({"message": "Follow-up not found"}), 404

    return jsonify({"message": "Follow-up marked as completed"})
