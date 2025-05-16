from flask import Flask, request, jsonify
import requests
from datetime import date

app = Flask(__name__)

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "mistral"  # Άλλαξε το αν χρησιμοποιείς άλλο μοντέλο

def call_ollama(prompt):
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        data = response.json()
        return data.get("response", "No response from model.")
    except Exception as e:
        return f"Error: {e}"

@app.route("/suggestion", methods=["POST"])
def get_suggestion():
    data = request.get_json()
    ctl = data.get("ctl")
    atl = data.get("atl")
    tsb = data.get("tsb")
    fitness_goal = data.get("goal", "lose weight and improve aerobic fitness")

    today = date.today().isoformat()

    prompt = f"""You are a professional cycling coach. Based on the following athlete data, generate a structured workout plan for TODAY in a concise, clear format.

Date: {today}
CTL: {ctl}
ATL: {atl}
TSB: {tsb}
Goal: {fitness_goal}

Return the workout in this format:
- Title with today's date and goal
- List warm-up, intervals, cool-down
- Each step should have: duration, intensity zone (e.g., Zone 2), notes
- Add tips for hydration, cadence, and recovery
- Make it brief and ready for execution. Avoid long explanations.

Workout:"""

    suggestion = call_ollama(prompt)
    return jsonify({"suggestion": suggestion})

if __name__ == "__main__":
    app.run(debug=True)
