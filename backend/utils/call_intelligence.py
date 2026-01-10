from statistics import mean


# -------------------------------------------------
# Helper: Convert score → risk label
# -------------------------------------------------
def map_score_to_risk(score):
    if score >= 0.6:
        return "HIGH"
    elif score >= 0.35:
        return "MEDIUM"
    return "LOW"


# -------------------------------------------------
# Analyze a SINGLE call
# -------------------------------------------------
def analyze_call(call, historical_calls=None):
    """
    call = {
        "duration": int (seconds),
        "outcome": "connected" | "not picked" | "failed"
    }

    historical_calls = list of past calls by same salesperson
    """

    score = 0.0
    reasons = []

    duration = call.get("duration", 0)
    outcome = call.get("outcome", "connected")

    # ---------- Absolute checks ----------
    if duration < 10:
        score += 0.4
        reasons.append("Extremely short call")

    elif duration < 30 and outcome == "not picked":
        score += 0.25
        reasons.append("Short call with no response")

    # ---------- Relative behavior ----------
    if historical_calls:
        avg_duration = mean(c["duration"] for c in historical_calls)

        if avg_duration > 0 and duration < 0.3 * avg_duration:
            score += 0.3
            reasons.append(
                "Call duration deviates from salesperson's normal behavior"
            )

    risk = map_score_to_risk(score)

    return {
        "callRisk": risk,
        "riskScore": round(score, 2),
        "reason": "; ".join(reasons) if reasons else "Call behavior within normal range"
    }


# -------------------------------------------------
# Analyze SALESPERSON PATTERN
# -------------------------------------------------
def analyze_salesperson(calls):
    """
    calls = list of {
        "duration": int,
        "outcome": str
    }
    """

    if not calls:
        return {
            "salespersonRisk": "LOW",
            "riskScore": 0.0,
            "reason": "No calls to analyze"
        }

    score = 0.0
    reasons = []

    durations = [c["duration"] for c in calls]
    outcomes = [c["outcome"] for c in calls]

    total_calls = len(calls)

    # ---------- Pattern 1: Short-call ratio ----------
    short_calls = [d for d in durations if d < 10]
    short_ratio = len(short_calls) / total_calls

    if short_ratio >= 0.3:
        score += 0.4
        reasons.append("High proportion of extremely short calls")

    # ---------- Pattern 2: Outcome repetition ----------
    most_common_outcome = max(set(outcomes), key=outcomes.count)
    outcome_ratio = outcomes.count(most_common_outcome) / total_calls

    if outcome_ratio >= 0.6:
        score += 0.3
        reasons.append(
            f"Repeated outcome pattern detected: {most_common_outcome}"
        )

    # ---------- Pattern 3: Repetitive durations ----------
    if len(set(durations)) <= 2:
        score += 0.3
        reasons.append("Unusually repetitive call durations")

    risk = map_score_to_risk(score)

    return {
        "salespersonRisk": risk,
        "riskScore": round(score, 2),
        "reason": "; ".join(reasons) if reasons else "Salesperson behavior appears consistent"
    }


# -------------------------------------------------
# ADVANCED CALL QUALITY ANALYSIS (MAIN FUNCTION)
# -------------------------------------------------
def analyze_call_quality(calls):
    """
    calls = list of {
        "duration": int,
        "outcome": str
    }
    """

    if not calls:
        return {
            "engagement": {"score": 0, "explanation": "No call data available"},
            "consistency": {"score": 0, "explanation": "No call data available"},
            "effectiveness": {"score": 0, "explanation": "No call data available"},
            "responsiveness": {"score": 0, "explanation": "No call data available"},
            "call_discipline": {"score": 0, "explanation": "No call data available"},
            "risk": {"level": "LOW", "explanation": "No risk signals detected"}
        }

    durations = [c["duration"] for c in calls]
    outcomes = [c["outcome"] for c in calls]
    total_calls = len(calls)

    # -------------------------------------------------
    # Engagement
    # -------------------------------------------------
    short_calls = [d for d in durations if d < 10]
    avg_duration = sum(durations) / total_calls

    engagement_score = max(
        0,
        min(100, int((avg_duration / 120) * 100 - len(short_calls) * 5))
    )

    engagement_explanation = (
        "Calls show reasonable engagement"
        if engagement_score >= 60
        else "High number of very short calls reduced engagement score"
    )

    # -------------------------------------------------
    # Consistency
    # -------------------------------------------------
    duration_variance = max(durations) - min(durations)
    repeated_outcomes_ratio = max(outcomes.count(o) for o in set(outcomes)) / total_calls

    consistency_score = 100
    if duration_variance > 100:
        consistency_score -= 30
    if repeated_outcomes_ratio >= 0.6:
        consistency_score -= 30

    consistency_score = max(0, consistency_score)

    consistency_explanation = (
        "Calling behavior is stable and consistent"
        if consistency_score >= 60
        else "Inconsistent call durations or repeated outcomes detected"
    )

    # -------------------------------------------------
    # Effectiveness
    # -------------------------------------------------
    connected_calls = outcomes.count("connected")
    effectiveness_score = int((connected_calls / total_calls) * 100)

    effectiveness_explanation = (
        "Good proportion of calls resulted in connections"
        if effectiveness_score >= 50
        else "Low connection rate observed"
    )

    # -------------------------------------------------
    # Responsiveness
    # -------------------------------------------------
    missed_calls = outcomes.count("not picked")

    if missed_calls == 0:
        responsiveness_score = 100
    else:
        responsiveness_score = min(
            100,
            int((total_calls / missed_calls) * 40)
        )

    responsiveness_explanation = (
        "Consistent follow-up attempts after missed calls"
        if responsiveness_score >= 60
        else "Limited follow-up attempts after missed calls"
    )

    # -------------------------------------------------
    # Call Discipline
    # -------------------------------------------------
    repetitive_durations = len(set(durations)) <= 2

    call_discipline_score = 100
    if len(short_calls) / total_calls >= 0.3:
        call_discipline_score -= 30
    if repetitive_durations:
        call_discipline_score -= 30

    call_discipline_score = max(0, call_discipline_score)

    call_discipline_explanation = (
        "Calls appear structured and well-paced"
        if call_discipline_score >= 60
        else "Irregular or spam-like calling patterns detected"
    )

    # -------------------------------------------------
    # Overall Risk
    # -------------------------------------------------
    risk_result = analyze_salesperson(calls)

    return {
        "engagement": {
            "score": engagement_score,
            "explanation": engagement_explanation
        },
        "consistency": {
            "score": consistency_score,
            "explanation": consistency_explanation
        },
        "effectiveness": {
            "score": effectiveness_score,
            "explanation": effectiveness_explanation
        },
        "responsiveness": {
            "score": responsiveness_score,
            "explanation": responsiveness_explanation
        },
        "call_discipline": {
            "score": call_discipline_score,
            "explanation": call_discipline_explanation
        },
        "risk": {
            "level": risk_result["salespersonRisk"],
            "explanation": risk_result["reason"]
        }
    }