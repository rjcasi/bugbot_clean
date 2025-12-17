
from flask import Flask, jsonify, render_template_string
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

# Dashboard with multiple panels
@app.route("/dashboard")
def dashboard():
    html_template = """
    <html>
        <head>
            <title>RB-App Dashboard</title>
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                .panel-container { display: flex; flex-wrap: wrap; gap: 20px; }
                .panel { flex: 1; min-width: 400px; border: 1px solid #ccc; padding: 10px; }
                h2 { margin-top: 0; }
            </style>
        </head>
        <body>
            <h1>Recruiter-Facing Cockpit Dashboard</h1>
            <div class="panel-container">
                <div class="panel">
                    <h2>Anomaly Trends</h2>
                    <div id="chart1"></div>
                </div>
                <div class="panel">
                    <h2>System Health</h2>
                    <div id="chart2"></div>
                </div>
                <div class="panel">
                    <h2>Recruiter Notes</h2>
                    <div id="notes"></div>
                </div>
            </div>
            <script>
                async function fetchData() {
                    const response = await fetch('/data');
                    const records = await response.json();
                    if (records.length > 0) {
                        const timestamps = records.map(r => r.timestamp);
                        const values = records.map(r => r.value);
                        const events = records.map(r => r.event);

                        // Panel 1: anomaly trends
                        Plotly.newPlot('chart1', [{
                            x: timestamps,
                            y: values,
                            type: 'scatter',
                            mode: 'lines+markers',
                            text: events,
                            name: 'Log Values'
                        }], {title: 'Live Log Data'});

                        // Panel 2: system health (dummy gauge for now)
                        Plotly.newPlot('chart2', [{
                            type: "indicator",
                            mode: "gauge+number",
                            value: values[values.length-1],
                            title: { text: "System Load" },
                            gauge: { axis: { range: [0, 100] } }
                        }]);

                        // Panel 3: recruiter notes (placeholder text)
                        document.getElementById('notes').innerHTML =
                            "<p>Last event: " + events[events.length-1] +
                            " at " + timestamps[timestamps.length-1] + "</p>";
                    } else {
                        document.getElementById('chart1').innerHTML = "<p>No log data yet.</p>";
                        document.getElementById('chart2').innerHTML = "<p>No health data yet.</p>";
                        document.getElementById('notes').innerHTML = "<p>No notes yet.</p>";
                    }
                }

                // Initial load + refresh every 5s
                fetchData();
                setInterval(fetchData, 5000);
            </script>
        </body>
    </html>
    """
    return render_template_string(html_template)

if __name__ == "__main__":
    app.run(debug=True)
    
import streamlit as st
from red_team import fuzzing
from blue_team import anomaly, defense_rules
from panels import attention, drift, introspection, mutation_timeline, replay_playback
from data import logger

st.set_page_config(page_title="Red/Blue Hacking Cockpit", layout="wide")
st.title("🧠 Red/Blue Hacking Cockpit")

# Tabs for cockpit sections
tab1, tab2, tab3 = st.tabs(["Red Team", "Blue Team", "Panels"])

# --- Red Team ---
with tab1:
    st.header("Red Team: Offensive Modules")
    token = fuzzing.fuzz_tokens()
    result = fuzzing.send_request(token)
    st.write("Single Fuzzing Result:", result)

    st.subheader("Batch Fuzzing")
    logs = [fuzzing.send_request(fuzzing.fuzz_tokens()) for _ in range(5)]
    st.write(logs)

# --- Blue Team ---
with tab2:
    st.header("Blue Team: Defensive Modules")
    logs = [fuzzing.send_request(fuzzing.fuzz_tokens()) for _ in range(10)]
    st.write("Incoming Events:", logs)

    st.subheader("Defense Decisions")
    for event in logs:
        decisions = defense_rules.apply_rules(event)
        st.write(event, "→", decisions)
        # Log each fuzzing event
        logger.log_fuzz_event(event)

    st.subheader("Anomaly Detection")
    df = anomaly.detect_anomalies(logs)
    st.write(df)

    st.subheader("Rule Mutations")
    mutations = defense_rules.evolve_rules()
    st.write(mutations)
    for m in mutations:
        logger.log_mutation(m)

# --- Panels ---
with tab3:
    st.header("Cockpit Panels")

    st.subheader("Attention Overlay")
    attention.show_attention(df)

    st.subheader("Drift Tracker")
    drift.show_drift([{"rule": "entropy>4", "mutation": "lowered to 3.5"}])

    st.subheader("Multi-Agent Introspection")
    introspection.compare_agents(["Allowed", "Blocked"], ["Suspicious", "Allowed"])

    st.subheader("Mutation Timeline")
    mutation_timeline.show_mutation_timeline(mutations)

    st.subheader("Replay & Playback")
    replay_playback.show_replay_playback()
