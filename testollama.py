from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

OLLAMA_API_URL = "http://localhost:11434/api/generate"

@app.route("/analyze", methods=["POST"])
def analyze():
    user_code = request.json.get("code")
    if not user_code:
        return jsonify({"error": "No code provided"}), 400

    prompt = f"Analyze the following Python code for security vulnerabilities:\n\n{user_code}"

    payload = {
        "model": "codellama",
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_API_URL, json=payload)
        response.raise_for_status()
        result = response.json()
        return jsonify({"analysis_result": result.get("response", "")})
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Request failed: {e}"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
