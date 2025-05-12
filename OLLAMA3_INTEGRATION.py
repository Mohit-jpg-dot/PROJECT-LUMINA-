from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import logging

# === Setup ===
app = Flask(__name__)
CORS(app)  # Enable cross-origin requests

# Logging configuration
logging.basicConfig(level=logging.INFO)

# === Ollama Settings ===
OLLAMA_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "llama3"  # Change to the name of your local model

# === Routes ===
@app.route('/get-answer', methods=['GET'])
def get_answer():
    text = request.args.get('text')
    model = request.args.get('model', DEFAULT_MODEL)

    if not text:
        return jsonify({"error": "Missing 'text' parameter"}), 400

    logging.info(f"Received request with text: {text}, using model: {model}")

    payload = {
        "model": model,
        "prompt": text,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        data = response.json()
        answer = data.get("response", "No response from model.")
        return jsonify({"answer": answer})
    except requests.RequestException as e:
        logging.error(f"Request to Ollama failed: {e}")
        return jsonify({"error": "Failed to connect to Ollama"}), 500
    except Exception as e:
        logging.exception("Unexpected error:")
        return jsonify({"error": "Internal server error"}), 500

# === Run App ===
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=False)
#http://127.0.0.1:5050/get-answer?text=Hello
#http://192.168.2.16:5050/get-answer?text=Hello (use this on another device on the same Wi-Fi)

