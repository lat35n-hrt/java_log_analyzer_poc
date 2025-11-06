# parser.py

import re
from datetime import datetime

LOG_PATTERN = re.compile(r"(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*(?P<level>INFO|WARN|ERROR)\s*-\s*(?P<message>.*)")

def parse_log_line(line):
    match = LOG_PATTERN.search(line)
    if match:
        return {
            "timestamp": match.group("timestamp"),
            "level": match.group("level"),
            "message": match.group("message"),
        }
    return None

def analyze_log(file_path):
    with open(file_path, "r") as f:
        entries = [parse_log_line(line) for line in f]
    errors = [e for e in entries if e and e["level"] == "ERROR"]
    print(f"Total ERROR entries: {len(errors)}")
    for e in errors[:5]:  # Show top 5 for brevity
        print(f"{e['timestamp']} - {e['message']}")

if __name__ == "__main__":
    analyze_log("sample.log")
