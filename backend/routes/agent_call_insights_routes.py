import os
import json
from flask import Blueprint, jsonify

agent_call_insights_bp = Blueprint("agent_call_insights", __name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(BASE_DIR, "..", "uploads", "results")


@agent_call_insights_bp.route("/call-insights", methods=["GET"])
def get_agent_call_insights():
    if not os.path.isdir(RESULTS_DIR):
        return jsonify({"success": False, "data": []})

    insights = []

    for file in os.listdir(RESULTS_DIR):
        if file.endswith(".json"):
            file_path = os.path.join(RESULTS_DIR, file)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    insights.append(json.load(f))
            except Exception:
                continue

    return jsonify({
        "success": True,
        "count": len(insights),
        "data": insights
    })
