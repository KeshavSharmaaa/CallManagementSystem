from flask import Blueprint, jsonify
import os
import json

call_insights_bp = Blueprint("call_insights", __name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(BASE_DIR, "..", "uploads", "results")  # ✅ CORRECT

@call_insights_bp.route("/call-insights", methods=["GET"])
def get_call_insights():
    if not os.path.exists(RESULTS_DIR):
        print("❌ RESULTS DIR NOT FOUND:", RESULTS_DIR)
        return jsonify({"success": True, "data": []})

    insights = []

    for file in os.listdir(RESULTS_DIR):
        if file.endswith(".json"):
            try:
                with open(os.path.join(RESULTS_DIR, file), "r", encoding="utf-8") as f:
                    insights.append(json.load(f))
            except Exception as e:
                print("❌ Failed to read:", file, e)

    print(f"✅ Loaded {len(insights)} insight files")

    return jsonify({
        "success": True,
        "data": insights
    })
