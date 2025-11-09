# parser.py

"""
parser.py — Java Log Analyzer PoC

Parses Java-style log files (Log4j / SLF4J / Spring Boot) and extracts
timestamp, log level, and message. Designed for quick verification by reviewers
or recruiters within a reproducible environment.

Usage:
    python3 parser.py
"""

import os
import re
from datetime import datetime


# Example log lines:
# 2025-11-06 10:21:17 ERROR com.example.Controller - Failed to handle request...
# 2025-11-06 10:25:42,312 [main] INFO  org.springframework... - Starting MyApp
# 2025-11-06T10:32:45.101 INFO com.example.Service - Health check passed
LOG_PATTERN = re.compile(
    r"""^\s*
    (?P<timestamp>\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}(?:[.,]\d{3})?)  # 2000-01-01 12:34:56[,123]
    .*?                                                                  # Skip thread names and extra columns non-greedily
    (?P<level>INFO|WARN|ERROR)                                           # Log level
    \s+.*?-\s+                                                           # Logger name etc. → " - " → Message
    (?P<message>.*)                                                      # Message body
    $""",
    re.VERBOSE,
)

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
    if not os.path.exists(file_path):
        print(f"[Error] Log file not found: {file_path}")
        return

    with open(file_path, "r") as f:
        entries = [parse_log_line(line) for line in f]
    errors = [e for e in entries if e and e["level"] == "ERROR"]

    total = sum(1 for e in entries if e)
    print(f"Analyzed {total} log lines.")
    print(f"Total ERROR entries: {len(errors)}\n")

    for e in errors[:5]:  # Show top 5 for brevity
        print(f"{e['timestamp']} - {e['message']}")

if __name__ == "__main__":
    analyze_log("sample.log")
