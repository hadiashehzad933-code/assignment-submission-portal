from flask import Flask, request, jsonify
from pathlib import Path
import json

app = Flask(__name__)

REPORT_FILE = Path(__file__).resolve().parent / "test-report.json"

@app.route("/report", methods=["POST"])
def receive_report():
    report = request.get_json(silent=True)

    if not isinstance(report, dict):
        return jsonify({"error": "Invalid JSON report"}), 400

    REPORT_FILE.write_text(
        json.dumps(report, indent=4),
        encoding="utf-8"
    )

    return jsonify({
        "message": "Report received successfully",
        "file": str(REPORT_FILE)
    }), 200

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001)
