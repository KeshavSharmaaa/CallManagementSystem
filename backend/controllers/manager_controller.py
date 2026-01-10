from flask import request, jsonify
from config.db import leads
from datetime import datetime

def assign_lead(manager):
    data = request.json
    leads.insert_one({
        "name": data["name"],
        "phone": data["phone"],
        "assignedTo": data["salespersonId"],
        "assignedBy": manager["id"],
        "status": "new",
        "createdAt": datetime.utcnow()
    })
    return jsonify({"message": "Lead assigned"})
