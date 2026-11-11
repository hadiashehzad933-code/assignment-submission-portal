
import os
import json
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

XML_FILE = Path("reports/junit.xml")
REPORT_FILE = Path("test-report.json")

root = ET.parse(XML_FILE).getroot()

test_cases = []

for case in root.iter("testcase"):
    failure = case.find("failure")
    error = case.find("error")
    skipped = case.find("skipped")

    if failure is not None:
        result = "FAILED"
        message = failure.get("message", "") or (failure.text or "")
    elif error is not None:
        result = "FAILED"
        message = error.get("message", "") or (error.text or "")
    elif skipped is not None:
        result = "SKIPPED"
        message = skipped.get("message", "")
    else:
        result = "PASSED"
        message = ""

    test_cases.append({
        "name": case.get("name", "Unknown test"),
        "classname": case.get("classname", ""),
        "result": result,
        "failure_message": message
    })

total = len(test_cases)
failed = sum(t["result"] == "FAILED" for t in test_cases)
skipped_count = sum(t["result"] == "SKIPPED" for t in test_cases)
passed = total - failed - skipped_count

report = {
    "repository": os.getenv("GITHUB_REPOSITORY", "local-test"),
    "branch": os.getenv("GITHUB_REF_NAME", "local"),
    "commit_sha": os.getenv("GITHUB_SHA", "local"),
    "pipeline_run_id": os.getenv("GITHUB_RUN_ID", "local"),
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "tests": test_cases,
    "total_tests": total,
    "passed_tests": passed,
    "failed_tests": failed,
    "skipped_tests": skipped_count,
    "overall_status": "FAILED" if failed else "PASSED"
}

REPORT_FILE.write_text(
    json.dumps(report, indent=4),
    encoding="utf-8"
)

print(json.dumps(report, indent=4))
