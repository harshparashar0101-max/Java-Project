import glob
import json
import os
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

MAPPING_FILE = "xray_mapping.json"
OUTPUT_FILE = "reports/xray_results.json"
TEST_EXECUTION_KEY = "LOGI-70"


def find_junit_file() -> str:
    files = glob.glob("target/surefire-reports/TEST-*.xml")
    if not files:
        raise FileNotFoundError("No JUnit XML file found in target/surefire-reports/")
    print(f"Using JUnit file: {files[0]}")
    return files[0]


def load_mapping() -> dict:
    with open(MAPPING_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def get_status(testcase) -> str:
    if testcase.find("failure") is not None:
        return "FAILED"
    if testcase.find("error") is not None:
        return "FAILED"
    if testcase.find("skipped") is not None:
        return "TODO"
    return "PASSED"


def main():
    junit_file = find_junit_file()
    mapping = load_mapping()

    os.makedirs("reports", exist_ok=True)

    tree = ET.parse(junit_file)
    root = tree.getroot()

    tests = []

    for testcase in root.findall(".//testcase"):
        classname = testcase.get("classname", "").strip()
        name = testcase.get("name", "").strip()

        mapping_key = f"{classname}#{name}"

        if mapping_key not in mapping:
            print(f"Skipping unmapped test: {mapping_key}")
            continue

        status = get_status(testcase)

        tests.append({
            "testKey": mapping[mapping_key],
            "status": status
        })

    if not tests:
        raise ValueError("No mapped tests found. Please check xray_mapping.json and JUnit classname/method names.")

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    result = {
        "testExecutionKey": TEST_EXECUTION_KEY,
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

    print(f"Xray JSON created at: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()