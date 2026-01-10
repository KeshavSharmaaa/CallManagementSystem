from flask import jsonify
from config.db import calls, leads, followups, salespersons
from datetime import datetime


def missed_followups(manager):
    now = datetime.utcnow()

    missed = followups.find({
        "managerId": manager["id"],
        "completed": False,
        "scheduledTime": {"$lt": now}
    })

    return jsonify([
        {
            "leadId": f["leadId"],
            "salespersonId": f["salespersonId"],
            "scheduledTime": f["scheduledTime"].isoformat()

        }
        for f in missed
    ])

def manager_analytics(manager):
    return jsonify({
        "totalCalls": calls.count_documents({"managerId": manager["id"]}),
        "totalLeads": leads.count_documents({"assignedBy": manager["id"]})
    })

def salesperson_performance(manager):
    result = []

    for sp in salespersons.find({"managerId": manager["id"]}):
        sp_id = sp["_id"]

        total_calls = calls.count_documents({"salespersonId": sp_id})

        avg_duration_data = list(calls.aggregate([
            {"$match": {"salespersonId": sp_id}},
            {"$group": {"_id": None, "avg": {"$avg": "$duration"}}}
        ]))
        avg_duration = avg_duration_data[0]["avg"] if avg_duration_data else 0

        conversions = leads.count_documents({
            "assignedTo": sp_id,
            "status": "converted"
        })

        missed_followups = followups.count_documents({
            "salespersonId": sp_id,
            "completed": False
        })

        score = (
            total_calls
            + (conversions * 5)
            + (avg_duration / 60)
            - (missed_followups * 3)
        )

        result.append({
            "salespersonId": str(sp_id),
            "name": sp["name"],
            "totalCalls": total_calls,
            "avgCallDuration": round(avg_duration, 2),
            "conversions": conversions,
            "missedFollowups": missed_followups,
            "score": round(score, 2)
        })

    return jsonify(result)
