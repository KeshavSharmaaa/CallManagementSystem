from flask import request, jsonify
from config.db import leads, calls
from bson import ObjectId


# Allowed status transitions
VALID_FLOW = {
    "new": ["contacted"],
    "contacted": ["followup", "lost"],
    "followup": ["converted", "lost"]
}


def update_lead_status(salesperson):
    data = request.json
    lead_id = ObjectId(data["leadId"])
    new_status = data["newStatus"]

    lead = leads.find_one({"_id": lead_id})

    if not lead:
        return jsonify({"message": "Lead not found"}), 404

    # Ownership check
    if lead["assignedTo"] != salesperson["id"]:
        return jsonify({"message": "Unauthorized"}), 403

    current_status = lead["status"]

    # Validate status flow
    if new_status not in VALID_FLOW.get(current_status, []):
        return jsonify({"message": "Invalid lead status transition"}), 400

    # Rule: contacted requires at least one call
    if new_status == "contacted":
        call_count = calls.count_documents({
            "leadId": data["leadId"],
            "salespersonId": salesperson["id"]
        })

        if call_count == 0:
            return jsonify({"message": "Cannot mark contacted without a call"}), 400

    leads.update_one(
        {"_id": lead_id},
        {"$set": {"status": new_status}}
    )

    return jsonify({
        "message": f"Lead moved from {current_status} to {new_status}"
    })
