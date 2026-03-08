from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

GEMINI_KEY = os.environ.get("GEMINI_API_KEY", "")

@app.route("/")
def home():
    return "OK"

@app.route("/api/chat", methods=["POST"])
def chat():
    if not GEMINI_KEY:
        return jsonify({"error": "GEMINI_API_KEY not set"}), 500

    model = request.args.get("model", "gemini-2.0-flash-lite")
    url   = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={GEMINI_KEY}"
    body  = request.get_json()
    res   = requests.post(url, json=body, timeout=30)
    return jsonify(res.json()), res.status_code

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
