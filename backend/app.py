from flask import Flask, request, jsonify
from flask_cors import CORS

# Logic imports
from logic.calculator import calculate_impact
from logic.patterns import detect_pattern
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

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "Backend running",
        "message": "Micro Decision Taker API is live"
    })

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    frequency_hours = int(data.get("frequency", 1))
    time_days = int(data.get("time_period", 1))


    # Safety check
    if not data or "decision_id" not in data:
        return jsonify({
            "error": "decision_id is required"
        }), 400

    decision_id = data["decision_id"]

    # Core logic
    impact = calculate_impact(decision_id)
    butterfly_intensity = calculate_butterfly_intensity(
    impact,
    frequency_hours,
    time_days
    )
    pattern = detect_pattern(impact)
    explanation = explain_butterfly(decision_id, impact)

    # Final response
    return jsonify({
        "decision": decision_id,
        "pattern": pattern,
        "butterfly_effect": impact,
        "explanation": explanation,
        "butterfly_intensity": butterfly_intensity
    })

# -------------------------------
# App Runner
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)