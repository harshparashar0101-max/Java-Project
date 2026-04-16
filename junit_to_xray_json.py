import xml.etree.ElementTree as ET
import json
import os
from datetime import datetime

JUNIT_FILE = "target/surefire-reports/TEST-com.test.LoginTest.xml"
MAPPING_FILE = "xray_mapping.json"
OUTPUT_FILE = "reports/xray_results.json"

os.makedirs("reports", exist_ok=True)

tree = ET.parse(JUNIT_FILE)
root = tree.getroot()

with open(MAPPING_FILE, "r", encoding="utf-8") as f:
    mapping = json.load(f)

tests = []

for testcase in root.findall(".//testcase"):
    classname = testcase.get("classname")
    name = testcase.get("name")

    key = f"{classname}#{name}"

    if key not in mapping:
        print(f"Skipping unmapped test: {key}")
        continue

    status = "PASSED"
    if testcase.find("failure") is not None or testcase.find("error") is not None:
        status = "FAILED"
    elif testcase.find("skipped") is not None:
        status = "TODO"

    tests.append({
        "testKey": mapping[key],
        "status": status
    })

now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

result = {
    "testExecutionKey": "LOGI-70",
    "info": {
        "summary": "Java Jenkins Execution",
        "description": "Execution from Jenkins Java pipeline",
        "startDate": now,
        "finishDate": now
    },
    "tests": tests
}

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(result, f, indent=4)

print(f"Xray JSON created at {OUTPUT_FILE}")