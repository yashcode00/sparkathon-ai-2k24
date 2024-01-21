import uuid
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def landing_page():
    return "Redirecting to Streamlit app..."

@app.route("/get_started")
def get_started():
    session_id = str(uuid.uuid4())
    return jsonify({"session_id": session_id})

if __name__ == "__main__":
    app.run(port=8000, debug=True)
