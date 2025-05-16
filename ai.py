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
You are an experienced cycling coach AI.

Based on the athlete's current condition, please suggest one specific workout for today. Your response should be clear and structured, like you’re giving instructions to a real cyclist.

Here is the athlete’s current profile and metrics:
- Age: {profile.get("age", "N/A")}
- Gender: {profile.get("gender", "N/A")}
- Height: {profile.get("height_cm", "N/A")} cm
- Weight: {profile.get("weight_kg", "N/A")} kg
- FTP: {profile.get("ftp", "N/A")}W
- Recent Injury: {profile.get("injury_history", "None")}
- Goal: {profile.get("goal", "N/A")}
- Training Availability: {profile.get("available_time", "N/A")} minutes today
- CTL (Fitness): {profile.get("ctl", "N/A")}
- ATL (Fatigue): {profile.get("atl", "N/A")}
- TSB (Form): {profile.get("tsb", "N/A")}
- Equipment: {profile.get("equipment", "N/A")}
- Terrain: {profile.get("terrain", "N/A")}

📝 Please provide:
1. Workout Type (e.g., endurance ride, recovery, low cadence drills)
2. Duration
3. Intensity (use power zones, HR zones, or RPE)
4. Detailed Instructions (intervals, cadence, posture cues, etc.)
5. Purpose (1-2 sentences explaining the rationale behind the session)
""".strip()
