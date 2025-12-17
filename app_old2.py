from flask import Flask

# Initialize the Flask app
app = Flask(__name__)

# Default home route
@app.route("/")
def home():
    return "Welcome to RB-App cockpit!"

# Simple hello route
@app.route("/hello")
def hello():
    return "Hello, recruiter! This is a test route."

# Example dashboard route (optional starter)
@app.route("/dashboard")
def dashboard():
    # For now, just return text. Later you can embed charts or HTML panels.
    return "This is the recruiter-facing dashboard panel."

# Entry point
if __name__ == "__main__":
    # Run in debug mode for auto-reload during development
    app.run(debug=True)