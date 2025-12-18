from flask import Flask, jsonify, render_template_string
import plotly.express as px
import plotly.io as pio
import pandas as pd
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to RB-App cockpit!"

@app.route("/hello")
def hello():
    return "Hello, recruiter! This is a test route."

# JSON endpoint serving log data
@app.route("/data")
def data():
    log_path = os.path.join(os.path.dirname(__file__), "data", "logger.py")
    records = []
    if os.path.exists(log_path):
        with open(log_path, "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) == 3:
                    timestamp, event, value = parts
                    try:
                        value = float(value)
                        records.append({"timestamp": timestamp, "event": event, "value": value})
                    except ValueError:
                        pass
    return jsonify(records)

# Dashboard route with AJAX refresh
@app.route("/dashboard")
def dashboard():
    html_template = """
    <html>
        <head>
            <title>RB-App Dashboard</title>
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        </head>
        <body>
            <h1>Recruiter-Facing Dashboard</h1>
            <div id="chart"></div>
            <script>
                async function fetchData() {
                    const response = await fetch('/data');
                    const records = await response.json();
                    if (records.length > 0) {
                        const timestamps = records.map(r => r.timestamp);
                        const values = records.map(r => r.value);
                        const events = records.map(r => r.event);

                        const trace = {
                            x: timestamps,
                            y: values,
                            type: 'scatter',
                            mode: 'lines+markers',
                            text: events,
                            name: 'Log Values'
                        };

                        Plotly.newPlot('chart', [trace], {title: 'Live Log Data'});
                    } else {
                        document.getElementById('chart').innerHTML = "<p>No log data available yet.</p>";
                    }
                }

                // Initial load
                fetchData();
                // Refresh every 5 seconds
                setInterval(fetchData, 5000);
            </script>
        </body>
    </html>
    """
    return render_template_string(html_template)

if __name__ == "__main__":
    app.run(debug=True)