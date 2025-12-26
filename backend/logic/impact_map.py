# backend/logic/impact_map.py

def calculate_total_impact(impact):
    """
    Converts micro impacts into a single long-term score.
    Butterfly Effect = accumulation of small changes
    """

    total_score = 0

    for value in impact.values():
        total_score += value

    return total_score

def calculate_butterfly_intensity(impact, frequency, time_period):
    """
    Butterfly Effect Formula:
    intensity = sum(impact values) * frequency * time
    """

    base_impact = sum(impact.values())
    intensity = base_impact * frequency * time_period

    return intensity