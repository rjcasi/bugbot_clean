# BugBot Cockpit

BugBot is a recruiter‑facing interactive cockpit that demonstrates core concepts in **cybersecurity, data structures, machine learning, and robotics**.  
It’s designed as a living organism: each arena is an “organ,” and the Flask app is the “nervous system” that ties them together.

---

## 🚀 Features

### Dashboard
- Central navigation hub linking all arenas.
- Clean UI with consistent styling via `base.html`.

### Sorting Arena
- Visualizes **Quicksort vs Mergesort** side‑by‑side.
- Entropy plots show cycles of order emerging from disorder.

### Blockchain Arena
- Simulates block confirmations and pending transactions.
- Interactive chart of transaction flow into blocks.

### Entropy Arena
- Compares brute force runtimes and attempts for MD5 vs SHA‑256.
- Advanced demo includes bcrypt and Argon2 hashing.

### Robotics Arena
- **Motor Control Demo**: actuator speed and stop sequences.
- **Arm Kinematics**: 2‑joint planar arm workspace visualization.
- **Line Following Simulation**: sensor feedback driving robot path corrections.

---

## 🛠️ Tech Stack
- **Flask** for web routing and cockpit shell.
- **Plotly** for interactive visualizations.
- **Python modules** for each arena (`sorting_utils.py`, `blockchain_utils.py`, `entropy_utils.py`, `robotics_utils.py`).
- **HTML templates** extending `base.html` for consistent UI.

---

## ▶️ How to Run
1. Clone the repo:
   ```bash
   git clone https://github.com/rjcasi/bugbot_clean.git
   cd bugbot_clean

# BugBot Cockpit

BugBot is a lightweight cybersecurity cockpit demo built in Python and Flask.  
It showcases anomaly detection, system health monitoring, and recruiter‑friendly dashboards with interactive Plotly charts.

---

## 🚀 Quickstart

Clone the repo and set up the environment:

```bash
git clone https://github.com/rjcasi/bugbot.git
cd bugbot
python -m venv env
env\Scripts\activate
pip install -r requirements.txt
python app.py

## Sorting Arena Panel
Navigate to `/sorting-arena` in the cockpit to see Quicksort vs Mergesort live.
- **Quicksort:** entropy drops in jagged bursts (pivot partitions).
- **Mergesort:** entropy drops in smooth waves (merging fragments).
- Hover over entropy points to see exactly which elements dropped where.

## Sorting Arena Panel
Navigate to `/sorting-arena` in the cockpit to see Quicksort vs Mergesort live.
- **Quicksort:** entropy drops in jagged bursts (pivot partitions).
- **Mergesort:** entropy drops in smooth waves (merging fragments).
- Hover over entropy points to see exactly which elements dropped where.

{## 🔢 Entropy Arena Panel

Navigate to `/entropy-arena` in the BugBot cockpit to explore **brute force complexity across hashing algorithms**.

### What You’ll See
- **Runtime Chart**  
  A line plot comparing MD5 vs SHA‑256 runtime as password length increases.  
  MD5 rises slowly, SHA‑256 rises faster — deliberately adding computational cost.

- **Attempts Chart**  
  A line plot showing the exponential growth of brute force attempts (26^L).  
  Both curves explode with length, visualizing entropy collapse.

### Symbolic Resonance
This panel dramatizes the **math of entropy collapse**:
- Password length → exponential growth in search space.  
- Algorithm choice → runtime cost per attempt.  
- Together, they show why strong, salted hashes resist brute force.

### Recruiter Takeaway
- **Technical depth:** Demonstrates understanding of hashing, entropy, and computational complexity.  
- **Visualization:** Plotly charts make exponential scaling and algorithmic differences clear.  
- **Cybersecurity insight:** Explains why modern systems use bcrypt/Argon2 — slow by design to resist brute force.  
- **Symbolic meaning:** Chaos of brute force vs resilience of strong hashing.

---

⚡ **Tip for Recruiters:**  
Run `python app.py` and visit `http://localhost:5000/entropy-arena` to watch entropy collapse curves live.## 🤖 Robotics Arena

The Robotics Arena demonstrates how cyber logic extends into physical systems, bridging software with mechanical control. It contains three interactive demos:

- **Motor Control Demo**  
  Simulates actuator control by setting and stopping motor speeds.  
  *Recruiter Impact:* Shows understanding of control loops and actuator logic — the foundation of robotics.

- **Arm Kinematics Visualization**  
  Uses a 2‑joint planar arm to compute end‑effector positions.  
  An interactive Plotly chart displays the reachable workspace.  
  *Recruiter Impact:* Demonstrates math + robotics integration, highlighting how geometry and trigonometry drive robot motion.

- **Line Following Simulation**  
  Simulates sensor feedback (left, right, center) and robot adjustments.  
  *Recruiter Impact:* Highlights sensor‑driven decision making and control logic, a core robotics principle.

### How to Run
1. Start the cockpit app:
   ```bash
   python app.py