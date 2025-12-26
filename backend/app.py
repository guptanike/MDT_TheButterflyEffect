from flask import Flask, request, jsonify
from flask_cors import CORS

# Logic imports
from logic.calculator import calculate_impact
from logic.patterns import detect_pattern, DECISION_TYPE
from logic.impact_map import calculate_total_impact, calculate_butterfly_intensity

app = Flask(__name__)
CORS(app)  # Frontend-backend connection allow

# -------------------------------
# Butterfly Effect Explanation
# -------------------------------
def explain_butterfly(decision_id, impact):
    explanations = {
        "D1": "Sleeping late slightly reduces sleep quality. Repeating this daily compounds into poor focus, stress, and long-term productivity loss.",
        "D2": "Studying less today creates small knowledge gaps. Over weeks, these gaps accumulate and strongly impact academic and career growth.",
        "D3": "Excess social media causes minor attention loss. Repetition fragments focus, affecting mental health and career performance.",
        "D4": "Skipping exercise lowers energy slightly. Over time, this compounds into health issues and reduced stress tolerance.",
        "D5": "Eating junk food affects metabolism and brain clarity. Repeated intake reduces energy and decision quality."
    }

    base_text = explanations.get(
        decision_id,
        "Small decisions seem harmless, but their repeated effects compound into major life outcomes."
    )

    total_score = calculate_total_impact(impact)

    return f"{base_text} Base impact score = {total_score}. Repetition amplifies this into a butterfly effect."

# -------------------------------
# Routes
# -------------------------------

def generate_advice(habit_type, butterfly_intensity, dream_job):
    """
    Generates psychologically light reverse-advice
    """

    if habit_type == "bad":
        if butterfly_intensity < -200:
            return (
                f"Honestly? Becoming a {dream_job} like this sounds unrealistic. "
                f"Not insulting you — just facts. Either change these habits, "
                f"or accept average outcomes. Your move."
            )
        else:
            return (
                f"You say you want to be a {dream_job}, but your habits disagree slightly. "
                f"Fix them now — otherwise this dream will slowly fade without you noticing."
            )

    else:  # good habit
        return (
            f"Your current habits actually align with becoming a {dream_job}. "
            f"Keep repeating them — this is exactly how long-term success is built."
        )

def job_requirements():
    return {
        "software engineer": {
            "focus": 5,
            "career": 5,
            "health": 3
        },
        "data scientist": {
            "focus": 5,
            "career": 4,
            "health": 3
        },
        "entrepreneur": {
            "focus": 4,
            "career": 5,
            "health": 4
        },
        "government job": {
            "focus": 4,
            "career": 4,
            "health": 3
        }
    }

def calculate_capability(impact, dream_job):
    # Normalize job name
    dream_job_lower = dream_job.strip().lower()
    
    # Job requirements mapping
    reqs = {
        "software engineer": {"focus":5, "career":5, "health":3},
        "data scientist": {"focus":5, "career":4, "health":3},
        "entrepreneur": {"focus":4, "career":5, "health":4},
        "government job": {"focus":4, "career":4, "health":3},
        "ai engineer": {"focus":5, "career":5, "health":3},
        "doctor": {"focus":5, "career":5, "health":5}
    }

    job = reqs.get(dream_job_lower)
    if not job:
        return 50, "Dream unclear. Your effort looks confused too."

    # Sum weighted impact for keys that matter
    score = sum(impact.get(k, 0) for k in job)
    max_score = sum(job.values())

    # Scale capability 0-100
    capability = int((score + max_score) / (2*max_score) * 100)
    capability = max(0, min(capability, 100))  # clamp 0-100

    # Advice based on percentage
    if capability < 30:
        advice = "Hard truth: At this pace, your dream is almost impossible. Change now or forget it."
    elif capability < 50:
        advice = "You are struggling. Fix habits fast or lower expectations."
    elif capability < 70:
        advice = "Decent progress. Keep discipline high to reach your dream."
    elif capability < 90:
        advice = "Good work! You are on track, just maintain consistency."
    else:
        advice = "Excellent! Your habits perfectly align with your dream. Keep it up."

    return capability, advice

def analyze_dream_job(dream_job, impact):
    """
    Evaluates user's capability to achieve dream job
    using reverse psychology (harsh tone)
    """

    # Difficulty score (higher = tougher)
    job_difficulty = {
        "ai engineer": 18,
        "software engineer": 12,
        "data scientist": 15,
        "doctor": 20,
        "ias": 22,
        "entrepreneur": 14
    }

    base_impact = sum(impact.values())  # negative if bad habits
    difficulty = job_difficulty.get(dream_job.lower(), 12)

    capability_score = base_impact + difficulty

    # Harsh / reverse psychology advice
    if capability_score < 5:
        advice = (
            f"No man, forget about becoming a {dream_job}. "
            "With these habits, this dream is honestly not for you. "
            "Unless you change your daily decisions, just drop it."
        )
    elif capability_score < 10:
        advice = (
            f"You say you want to be a {dream_job}, but your actions say otherwise. "
            "Fix your habits first, then talk about big dreams."
        )
    else:
        advice = (
            f"You actually have a chance to become a {dream_job}. "
            "But one reminder: keep repeating bad decisions and you’ll ruin it."
        )

    return capability_score, advice

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "Backend running",
        "message": "Micro Decision Taker API is live"
    })

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    dream_job = data.get("dream_job", "").lower()
    frequency_hours = int(data.get("frequency", 1))
    time_days = int(data.get("time_period", 1))
    dream_job = data.get("dream_job", "").strip()

    # Safety check
    if not data or "decision_id" not in data:
        return jsonify({
            "error": "decision_id is required"
        }), 400

    decision_id = data["decision_id"]

    habit_type = DECISION_TYPE.get(decision_id, "unknown")

    # Core logic
    impact = calculate_impact(decision_id)
    capability_score, advice = analyze_dream_job(dream_job, impact)
    butterfly_intensity = calculate_butterfly_intensity(
    impact,
    frequency_hours,
    time_days
    )
    dream_job = data.get("dream_job", "your dream career")
    advice = generate_advice(habit_type, butterfly_intensity, dream_job)    
    pattern, habit_type = detect_pattern(decision_id, impact)
    explanation = explain_butterfly(decision_id, impact)
    capability, advice = calculate_capability(impact, dream_job)

    # Final response
    return jsonify({
        "decision": decision_id,
        "pattern": pattern,
        "butterfly_effect": impact,
        "explanation": explanation,
        "butterfly_intensity": butterfly_intensity,
        "dream_job": dream_job,
        "capability_score": capability_score,
        "capability_percent": capability,
        "advice": advice,
        "habit_type": habit_type
    })

# -------------------------------
# App Runner
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)