from flask import Flask, render_template
import random
import plotly.graph_objs as go
import plotly.io as pio
import plotly.subplots as sp
from sorting_utils import quicksort_animation, mergesort_animation
from blockchain_utils import simulate_blockchain

app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(debug=True)



