from flask import Flask, render_template, jsonify
import random

app = Flask(__name__)

# --- Homepage ---
@app.route("/")
def index():
    return render_template("index.html")

# --- Generative AI Panel ---
@app.route("/genai")
def genai_panel():
    logs = [
        {"t": 1, "ip": "192.168.1.10", "event": "LOGIN_FAIL"},
        {"t": 2, "ip": "192.168.1.22", "event": "PORT_SCAN"},
        {"t": 3, "ip": "192.168.1.33", "event": "SQLI_ATTEMPT"},
    ]
    return render_template("genai.html", logs=logs)

# --- ML Detection Panel ---
@app.route("/ml")
def ml_panel():
    anomalies = [random.randint(1, 10) for _ in range(3)]
    return render_template("ml.html", anomalies=anomalies)

# --- Panels Demo ---
@app.route("/panels")
def panels():
    return render_template("panels.html")

# --- API Example ---
@app.route("/api/anomalies")
def api_anomalies():
    anomalies = [random.randint(1, 10) for _ in range(5)]
    return jsonify({"anomalies": anomalies})

if __name__ == "__main__":
    app.run(debug=True, port=5000)