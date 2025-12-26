# backend/logic/calculator.py

def calculate_impact(decision_id):
    """
    Calculates micro-level impacts of a decision.
    Butterfly Effect: small action → multi-dimensional impact
    """

    impact_map = {
        "D1": {  # Late sleep
            "health": -3,
            "focus": -4,
            "career": -2
        },
        "D2": {  # Low study time
            "health": -1,
            "focus": -3,
            "career": -4
        },
        "D3": {  # Excess social media
            "health": -2,
            "focus": -4,
            "career": -3
        },
        "D4": {  # Skipping exercise
            "health": -4,
            "focus": -2,
            "career": -1
        },
        "D5": {  # Junk food
            "health": -3,
            "focus": -2,
            "career": -2
        },
        "G1": {  # Consistent Sleep
            "health": 4,
            "focus": 3,
            "career": 2
        },
        "G2": {  # Daily Study
            "health": 1,
            "focus": 4,
            "career": 5
        },
        "G3": {  # Exercise
            "health": 5,
            "focus": 2,
            "career": 1
        },
        "G4": {  # Reading / Learning
            "health": 1,
            "focus": 3,
            "career": 4
        },
        "G5": {  # Healthy Diet
            "health": 4,
            "focus": 2,
            "career": 2
        }
    }

    # Default safe impact (no crash)
    return impact_map.get(decision_id, {
        "health": 0,
        "focus": 0,
        "career": 0
    })