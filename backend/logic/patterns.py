# backend/logic/patterns.py

DECISION_TYPE = {
    "D1": "bad",
    "D2": "bad",
    "D3": "bad",
    "D4": "bad",
    "D5": "bad",

    "G1": "good",
    "G2": "good",
    "G3": "good",
    "G4": "good",
    "G5": "good"
}

def detect_pattern(decision_id, impact):
    """
    Detects behavioral pattern based on impact values
    """

    negative_count = sum(1 for v in impact.values() if v < 0)
    positive_count = sum(1 for v in impact.values() if v > 0)

    decision_type = DECISION_TYPE.get(decision_id, "bad")

    if negative_count >= 2:
        return "Negative Habit Loop (Compounding Loss)", decision_type
    elif positive_count >= 2:
        return "Positive Growth Loop (Compounding Gain)", decision_type
    else:
        return "Neutral / Mixed Behavior Pattern", decision_type