#!/usr/bin/env python3
"""Parse EXPLAIN ANALYZE output and identify red flags."""
import sys
import re

FLAGS = [
    (r"Seq Scan", "Full table scan — consider adding index"),
    (r"Nested Loop.*rows=\d+.*cost=\d+\.\d+\.\.\d+\.\d+", "Nested loop may be expensive for large joins"),
    (r"Sort.*Sort Method: external merge", "Sort spilled to disk — increase work_mem"),
    (r"rows=(\d+).*width=(\d+)", None),
]

def analyze(text: str):
    issues = []
    for pattern, msg in FLAGS:
        if msg and re.search(pattern, text, re.IGNORECASE):
            issues.append(msg)
    if not issues:
        issues.append("No major red flags detected.")
    return issues

if __name__ == "__main__":
    data = sys.stdin.read()
    for issue in analyze(data):
        print(f"[!] {issue}")
