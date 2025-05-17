from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "deepseek-r1:14b"

PROMPT_TEMPLATE = """You are a professional cycling coach. Based on the following athlete profile, generate a specific structured workout for today. Use exactly this format:

🏋️ Today's Workout – [Short Title] ([Total Duration in minutes])

1. Warm-up
- [duration] [short instructions]

2. Intervals
- [sets x duration] @[% FTP or Zone] [brief description]
- [recovery info]

3. Optional Drill
- [drill type] [duration] [e.g. bodyweight, cadence, etc.]

4. Core
- [duration] [exercises focusing on core/lower back]

5. Cool Down
- [duration] [easy spin/stretching cues]

IMPORTANT:
- Do NOT include explanations, thoughts, context, or <think> tags.
- If core training is included, clarify whether it's off-bike and list safe exercises for athletes recovering from back or pelvic injuries.
- Avoid repeating the same exercises in both Optional Drill and Core sections. Use different exercises or variations.

Athlete Profile:
- Age: {age}
- Weight: {weight} kg
- FTP: {ftp}
- Goal: {goal}
- Time available: {time} min
- Injury history: {injury}
- Terrain: flat
- Equipment: indoor smart trainer"""

def call_ollama(prompt):
    try:
        print("[PROMPT SENT TO OLLAMA]\n", prompt)
        response = requests.post(OLLAMA_URL, json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        })
        print("[RAW RESPONSE]", response.status_code, response.text)
        if response.ok:
            full = response.json().get("response", "No response")
            if "🏋️" in full:
                return "🏋️" + full.split("🏋️", 1)[1]
            return full
        return f"[ERROR] Ollama response failed: {response.status_code}"
    except Exception as e:
        return f"[EXCEPTION] {e}"

@app.route("/", methods=["GET", "POST"])
def index():
    suggestion = None
    if request.method == "POST":
        age = request.form.get("age", "55")
        weight = request.form.get("weight", "120")
        ftp = request.form.get("ftp", "100")
        goal = request.form.get("goal", "regain aerobic fitness after injury")
        time = request.form.get("time", "60")
        injury = request.form.get("injury", "fractured shoulder, ribs, pneumothorax, pelvic fracture")

        prompt = PROMPT_TEMPLATE.format(
            age=age,
            weight=weight,
            ftp=ftp,
            goal=goal,
            time=time,
            injury=injury
        )

        suggestion = call_ollama(prompt)

    return render_template_string("""
    <html>
    <head>
        <title>🚴‍♂️ Trainer Analyzer</title>
        <style>
            body { font-family: sans-serif; margin: 2em; }
            input[type=text], input[type=number] { width: 300px; padding: 5px; }
            .button { padding: 10px 20px; margin-top: 10px; }
        </style>
    </head>
    <body>
    <h1>🚴‍♂️ Trainer Analyzer</h1>
    <form method="POST">
        <p>Age<br><input name="age" type="number" value="55"></p>
        <p>Weight (kg)<br><input name="weight" type="number" value="120"></p>
        <p>FTP (optional)<br><input name="ftp" type="number" value="100"></p>
        <p>Goal<br><input name="goal" type="text" value="regain aerobic fitness after injury"></p>
        <p>Available Time (minutes)<br><input name="time" type="number" value="60"></p>
        <p>Recent Injury (optional)<br><input name="injury" type="text" value="fractured shoulder, ribs, pneumothorax, pelvic fracture"></p>
        <p><input class="button" type="submit" value="Get Workout"></p>
    </form>

    {% if suggestion %}
        <h2>Suggested Workout</h2>
        <pre>{{ suggestion }}</pre>
    {% endif %}
    </body>
    </html>
    """, suggestion=suggestion)

if __name__ == "__main__":
    app.run(debug=True)
