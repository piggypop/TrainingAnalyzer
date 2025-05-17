from flask import Flask, request, jsonify, render_template
from ai import generate_workout

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/suggestion", methods=["POST", "OPTIONS"])
def get_suggestion():
    if request.method == "OPTIONS":
        response = jsonify({})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        return response, 200

    data = request.get_json()
    profile = data.get("profile")
    model = data.get("model", "deepseek-r1:14b")

    if not profile:
        response = jsonify({"error": "Missing athlete profile."})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response, 400

    suggestion = generate_workout(profile, model)
    response = jsonify({"suggestion": suggestion})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

if __name__ == "__main__":
    app.run(debug=True)
