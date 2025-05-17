#!/bin/bash

# 1. Εκκινεί το μοντέλο AI μέσω Ollama (deepseek)
echo "Starting AI model (deepseek-r1:14b)..."
ollama run deepseek-r1:14b &
OLLAMA_PID=$!
sleep 5

# 2. Ενεργοποιεί το Python virtual environment και ξεκινά το Flask API
cd "$(dirname "$0")"
echo "Starting Trainer Analyzer backend (Flask)..."
source .venv/bin/activate
python app.py &
FLASK_PID=$!
sleep 3

# 3. Ανοίγει τη σελίδα διεπαφής στον browser
echo "Opening training interface in browser..."
xdg-open web/index.html

# 4. Περιμένει τον χρήστη να πατήσει CTRL+C για να τερματιστούν όλα
trap "kill $OLLAMA_PID $FLASK_PID" EXIT
wait
