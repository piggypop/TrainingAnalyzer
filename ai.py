# ai.py

import requests
import json

def generate_workout(profile: dict, model: str = "deepseek-r1:14b") -> str:
    """
    Sends a structured prompt to the local Ollama server and returns the suggested workout.
    """
    prompt = build_prompt(profile)
    response = requests.post("http://localhost:11434/api/generate", json={
        "model": model,
        "prompt": prompt,
        "stream": False
    })

    if response.ok:
        return response.json().get("response", "").strip()
    else:
        return f"[ERROR] Ollama response failed: {response.status_code}"

def build_prompt(profile: dict) -> str:
    return f"""
You are a cycling coach AI.

Please generate a short and actionable workout suggestion for today, in 6 clear and useful lines maximum.
Avoid over-explaining. Do not provide analysis. No commentary. No '<think>' section.

Here is the athlete’s data:
- Age: {profile.get("age", "N/A")}
- Gender: {profile.get("gender", "N/A")}
- Height: {profile.get("height_cm", "N/A")} cm
- Weight: {profile.get("weight_kg", "N/A")} kg
- FTP: {profile.get("ftp", "N/A")}W
- Injury: {profile.get("injury_history", "None")}
- Goal: {profile.get("goal", "N/A")}
- Time available today: {profile.get("available_time", "N/A")} minutes
- CTL: {profile.get("ctl", "N/A")}
- ATL: {profile.get("atl", "N/A")}
- TSB: {profile.get("tsb", "N/A")}
- Equipment: {profile.get("equipment", "N/A")}
- Terrain: {profile.get("terrain", "N/A")}

Format it as a clean workout plan with bullet points.
Use short phrases and make it instantly actionable.
""".strip()
