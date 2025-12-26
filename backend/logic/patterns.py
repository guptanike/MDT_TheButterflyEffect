# backend/logic/patterns.py

def detect_pattern(impact):
    """
    Detects behavioral pattern based on impact values
    """

    negative_count = sum(1 for v in impact.values() if v < 0)
    positive_count = sum(1 for v in impact.values() if v > 0)

    if negative_count >= 2:
        return "Negative Habit Loop (Compounding Loss)"
    elif positive_count >= 2:
        return "Positive Growth Loop (Compounding Gain)"
    else:
        return "Neutral / Mixed Behavior Pattern"