import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib_venn import venn2
import ipaddress
import pandas as pd

# Existing modules from your older scaffold
from red_team import fuzzing
from blue_team import anomaly, defense_rules
from panels import attention, drift, introspection, mutation_timeline, replay_playback
from data import logger

st.set_page_config(page_title="Red/Blue Hacking Cockpit", layout="wide")
st.title("🧠 Red/Blue Hacking Cockpit")

# Tabs for cockpit sections
tab1, tab2, tab3, tab4 = st.tabs(["Red Team", "Blue Team", "Panels", "Phase Space Monitor"])

# =========================
# --- Red Team Tab ---
# =========================
with tab1:
    st.header("Red Team: Offensive Modules")
    token = fuzzing.fuzz_tokens()
    result = fuzzing.send_request(token)
    st.write("Single Fuzzing Result:", result)

    st.subheader("Batch Fuzzing")
    red_logs = [fuzzing.send_request(fuzzing.fuzz_tokens()) for _ in range(5)]
    st.write(red_logs)

# =========================
# --- Blue Team Tab ---
# =========================
with tab2:
    st.header("Blue Team: Defensive Modules")
    # Generate a fresh stream of events
    blue_logs = [fuzzing.send_request(fuzzing.fuzz_tokens()) for _ in range(10)]
    st.write("Incoming Events:", blue_logs)

    st.subheader("Defense Decisions")
    for event in blue_logs:
        decisions = defense_rules.apply_rules(event)
        st.write(event, "→", decisions)
        # Log each fuzzing event
        logger.log_fuzz_event(event)

    st.subheader("Anomaly Detection")
    df = anomaly.detect_anomalies(blue_logs)
    st.write(df)

    st.subheader("Rule Mutations")
    mutations = defense_rules.evolve_rules()
    st.write(mutations)
    for m in mutations:
        logger.log_mutation(m)

# =========================
# --- Panels Tab ---
# =========================
with tab3:
    st.header("Cockpit Panels")

    # Guard against df/mutations missing if tab2 hasn't run yet (Streamlit runs top-to-bottom)
    if 'df' not in locals():
        df = pd.DataFrame({"note": ["Run Blue Team tab to populate anomaly DataFrame"]})
    if 'mutations' not in locals():
        mutations = [{"note": "Run Blue Team tab to generate rule mutations"}]

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

    # -------------------------
    # IPv4 vs IPv6 Comparison Panel (added)
    # -------------------------
    st.subheader("Networking Sets: IPv4 vs IPv6 Comparison")

    col_v4, col_v6 = st.columns(2)

    with col_v4:
        st.markdown("**IPv4 Subnets (Finite)**")
        ipv4_size = st.slider("IPv4 CIDR", 30, 24, 30, key="ipv4_cidr")
        subnet_A_v4 = set(str(ip) for ip in ipaddress.IPv4Network(f"192.168.1.0/{ipv4_size}"))
        subnet_B_v4 = set(str(ip) for ip in ipaddress.IPv4Network(f"192.168.1.2/{ipv4_size}"))

        fig_v4, ax_v4 = plt.subplots()
        venn2([subnet_A_v4, subnet_B_v4], set_labels=("IPv4 A", "IPv4 B"))
        st.pyplot(fig_v4)

        st.caption("Union A∪B, Intersection A∩B, Differences A−B / B−A map to merged, overlapping, and isolated address sets.")

    with col_v6:
        st.markdown("**IPv6 Subnets (Practically Infinite)**")
        ipv6_size = st.slider("IPv6 CIDR", 126, 120, 126, key="ipv6_cidr")
        subnet_A_v6 = set(str(ip) for ip in ipaddress.IPv6Network(f"2001:db8:1::/{ipv6_size}"))
        subnet_B_v6 = set(str(ip) for ip in ipaddress.IPv6Network(f"2001:db8:1::2/{ipv6_size}"))

        fig_v6, ax_v6 = plt.subplots()
        venn2([subnet_A_v6, subnet_B_v6], set_labels=("IPv6 A", "IPv6 B"))
        st.pyplot(fig_v6)

        st.caption(f"IPv6 address space size: {2**128:,} possible addresses; sliders simulate scalable subnetting.")

    # Replay how packets traverse union vs intersection sets (simple demo)
    st.subheader("Packet Replay over Set Operations")
    which_proto = st.selectbox("Protocol", ["IPv4", "IPv6"], index=0)
    steps = st.slider("Replay steps", 5, 50, 10, key="replay_steps_sets")

    if st.button("Start Set Replay"):
        placeholder = st.empty()
        if which_proto == "IPv4":
            union_set = list(subnet_A_v4.union(subnet_B_v4))
            inter_set = list(subnet_A_v4.intersection(subnet_B_v4))
        else:
            union_set = list(subnet_A_v6.union(subnet_B_v6))
            inter_set = list(subnet_A_v6.intersection(subnet_B_v6))

        for i in range(min(steps, len(union_set))):
            addr = union_set[i]
            mark = "∩" if addr in inter_set else "∪"
            placeholder.markdown(f"**Step {i+1}**: packet → `{addr}` ({mark})")
            # No sleep to keep Streamlit responsive; add time.sleep if you prefer pacing

# =========================
# --- Phase Space Monitor Tab ---
# =========================
with tab4:
    st.header("Semantic Phase Space Monitor")
    st.caption("Agents navigate attractors labeled TRUTH, Belief, Faith, Opinion, Perception, Reality with mechanics overlays.")

    # Controls
    sim_cols = st.columns(4)
    with sim_cols[0]:
        num_agents = st.slider("Agents", 4, 64, 12)
    with sim_cols[1]:
        steps = st.slider("Simulation steps", 50, 1000, 200)
    with sim_cols[2]:
        dt = st.slider("Time step (dt)", 0.01, 0.2, 0.05)
    with sim_cols[3]:
        noise_amp = st.slider("Chaos noise amplitude", 0.0, 0.5, 0.05)

    mode = st.radio("Mechanics overlay", ["Hamiltonian", "Lagrangian"], index=0)

    st.subheader("Attractor strengths")
    a1, a2, a3, a4, a5, a6 = st.columns(6)
    with a1:
        strength_truth = st.slider("TRUTH", 0.0, 5.0, 3.0)
    with a2:
        strength_belief = st.slider("Belief", 0.0, 5.0, 2.5)
    with a3:
        strength_faith = st.slider("Faith", 0.0, 5.0, 2.0)
    with a4:
        strength_opinion = st.slider("Opinion", 0.0, 5.0, 1.2)
    with a5:
        strength_perception = st.slider("Perception", 0.0, 5.0, 1.5)
    with a6:
        strength_reality = st.slider("Reality", 0.0, 5.0, 2.8)

    # Define attractor centers in projected 2D space
    attractors = {
        "TRUTH": {"center": np.array([0.8, 0.8]), "k": strength_truth},
        "BELIEF": {"center": np.array([-0.6, 0.5]), "k": strength_belief},
        "FAITH": {"center": np.array([-0.8, -0.7]), "k": strength_faith},
        "OPINION": {"center": np.array([0.3, -0.6]), "k": strength_opinion},
        "PERCEPTION": {"center": np.array([0.0, 0.0]), "k": strength_perception},
        "REALITY": {"center": np.array([0.6, -0.1]), "k": strength_reality},
    }

    rng = np.random.default_rng(42)
    positions = rng.uniform(-1.0, 1.0, size=(num_agents, 2))
    velocities = np.zeros_like(positions)
    traj = [positions.copy()]

    def attractor_force(pos, spec):
        f = np.zeros_like(pos)
        for a in spec.values():
            delta = a["center"] - pos
            dist = np.linalg.norm(delta, axis=1, keepdims=True) + 1e-6
            f += a["k"] * (delta / dist)
        return f

    def hamiltonian_energy(v):
        return 0.5 * np.sum(v**2, axis=1)

    def lagrangian_action(force_mag, dt_):
        return force_mag * dt_

    energy_series = []
    action_series = []

    for _ in range(steps):
        F = attractor_force(positions, attractors)
        noise = noise_amp * rng.normal(0, 1, size=positions.shape)
        velocities = velocities + (F * dt)
        positions = positions + velocities * dt + noise
        traj.append(positions.copy())

        if mode == "Hamiltonian":
            energy_series.append(hamiltonian_energy(velocities))
        else:
            action_series.append(lagrangian_action(np.linalg.norm(F, axis=1), dt))

    # Plot phase space
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.set_xlabel("Projection X")
    ax.set_ylabel("Projection Y")
    ax.grid(alpha=0.2)

    colors = {
        "TRUTH": "#2ca02c",
        "BELIEF": "#1f77b4",
        "FAITH": "#9467bd",
        "OPINION": "#ff7f0e",
        "PERCEPTION": "#7f7f7f",
        "REALITY": "#d62728",
    }
    for name, spec in attractors.items():
        ax.scatter(*spec["center"], c=colors[name], s=120, marker="X", label=name)

    for i in range(num_agents):
        path = np.array([p[i] for p in traj])
        ax.plot(path[:, 0], path[:, 1], lw=1.0, alpha=0.7, c="#333")
        ax.scatter(path[-1, 0], path[-1, 1], s=20, c="#333")

    ax.legend(loc="upper left", ncol=2, fontsize=8)
    st.pyplot(fig)

    # Mechanics overlay plot
    if mode == "Hamiltonian" and energy_series:
        E = np.array(energy_series)  # steps x agents
        avgE = E.mean(axis=1)
        figE, axE = plt.subplots()
        axE.plot(avgE, label="Average semantic energy")
        axE.set_title("Hamiltonian overlay")
        axE.set_xlabel("Step")
        axE.set_ylabel("Energy (arb.)")
        axE.grid(alpha=0.2)
        axE.legend()
        st.pyplot(figE)
    elif mode == "Lagrangian" and action_series:
        A = np.array(action_series)  # steps x agents
        avgA = A.mean(axis=1)
        figA, axA = plt.subplots()
        axA.plot(avgA, label="Average action (path cost)")
        axA.set_title("Lagrangian overlay")
        axA.set_xlabel("Step")
        axA.set_ylabel("Action (arb.)")
        axA.grid(alpha=0.2)
        axA.legend()
        st.pyplot(figA)

    st.markdown("""
- **Interpretation:** Agents drift under competing epistemic pulls. Stronger TRUTH/REALITY stabilizers reduce chaotic wandering.
- **Chaos knob:** Increasing noise amplifies sensitivity; agents can escape shallow basins like OPINION.
- **Mechanics overlay:** Hamiltonian shows energy stability; Lagrangian highlights path cost under forces.
""")