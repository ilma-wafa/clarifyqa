from flask import Flask, render_template, request, jsonify
from orchestrator import run_clarifyqa

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    requirement = data.get("requirement", "").strip()
    
    if not requirement:
        return jsonify({"error": "No requirement provided"}), 400
    
    try:
        result = run_clarifyqa(requirement)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)