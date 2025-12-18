from flask import Flask, render_template
import random
import plotly.graph_objs as go
import plotly.io as pio
import plotly.subplots as sp
from modules.sorting_utils import quicksort_animation, mergesort_animation
from modules.blockchain_utils import simulate_blockchain
from modules.entropy_utils import measure_entropy
from modules.robotics_utils import Motor, forward_kinematics, line_follow_step


app = Flask(__name__)

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/sorting-arena")
def sorting_arena():
    arr = [random.randint(1, 50) for _ in range(20)]
    
    quick_frames, quick_entropy, quick_annotations = quicksort_animation(arr.copy())
    merge_frames, merge_entropy, merge_annotations = mergesort_animation(arr.copy())
    
    fig = sp.make_subplots(rows=1, cols=2, subplot_titles=("Quicksort Arena", "Mergesort Arena"))
    
    # Initial bars
    fig.add_trace(go.Bar(y=arr, marker_color='indianred', name="Quicksort"), row=1, col=1)
    fig.add_trace(go.Bar(y=arr, marker_color='steelblue', name="Mergesort"), row=1, col=2)
    
    # Entropy lines with hover annotations
    fig.add_trace(go.Scatter(
        y=quick_entropy,
        text=quick_annotations,
        hoverinfo="text+y",
        mode="lines+markers",
        name="Quicksort Entropy",
        line=dict(color="red")
    ), row=1, col=1)
    
    fig.add_trace(go.Scatter(
        y=merge_entropy,
        text=merge_annotations,
        hoverinfo="text+y",
        mode="lines+markers",
        name="Mergesort Entropy",
        line=dict(color="blue")
    ), row=1, col=2)
    
    fig.update_layout(title="Cycles of Order Emerging from Disorder")
    
    return render_template("sorting_arena.html", plot_html=pio.to_html(fig, full_html=False))

@app.route("/blockchain-arena")
def blockchain_arena():
    chain, pending_counts = simulate_blockchain()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=list(range(len(pending_counts))),
        y=pending_counts,
        mode="lines+markers",
        name="Pending Transactions",
        hoverinfo="text+y",
        text=[f"Block {i}: {count} pending" for i, count in enumerate(pending_counts)]
    ))
    
    fig.update_layout(title="Blockchain Arena: Transactions Confirmed into Blocks")
    
    return render_template("blockchain_arena.html", plot_html=pio.to_html(fig, full_html=False))

@app.route("/entropy-arena")
def entropy_arena():
    lengths, md5_times, sha_times, md5_attempts, sha_attempts = measure_entropy()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=lengths, y=md5_times,
        mode="lines+markers", name="MD5 runtime"
    ))
    fig.add_trace(go.Scatter(
        x=lengths, y=sha_times,
        mode="lines+markers", name="SHA-256 runtime"
    ))
    fig.update_layout(title="Brute Force Runtime vs Password Length")
    
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=lengths, y=md5_attempts,
        mode="lines+markers", name="MD5 attempts"
    ))
    fig2.add_trace(go.Scatter(
        x=lengths, y=sha_attempts,
        mode="lines+markers", name="SHA-256 attempts"
    ))
    fig2.update_layout(title="Brute Force Attempts vs Password Length")
    
    return render_template("entropy_arena.html",
                           plot_runtime=pio.to_html(fig, full_html=False),
                           plot_attempts=pio.to_html(fig2, full_html=False))

@app.route("/entropy-arena-advanced")
def entropy_arena_advanced():
    password = "hunter2"
    
    bcrypt_h = bcrypt_hash(password)
    argon2_h = argon2_hash(password)
    
    return render_template("entropy_arena.html",
                           plot_runtime="",
                           plot_attempts="",
                           bcrypt_hash=bcrypt_h,
                           argon2_hash=argon2_h)



@app.route("/robotics_arena")
def robotics_arena():
    # Demo motor control
    left_motor = Motor("Left")
    right_motor = Motor("Right")
    motor_demo = [
        left_motor.set_speed(50),
        right_motor.set_speed(50),
        left_motor.stop(),
        right_motor.stop()
    ]

    # Demo kinematics
    x, y = forward_kinematics(0.5, 0.5)

    # Demo line-following
    line_demo = [line_follow_step() for _ in range(5)]

    return render_template("robotics_arena.html",
                           motor_demo=motor_demo,
                           kinematics=(x, y),
                           line_demo=line_demo)

if __name__ == "__main__":
    app.run(debug=True)



