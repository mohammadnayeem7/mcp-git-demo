"""
Monitors the mcp-git-demo repo for changes and logs them to mcp_changes.log.
Run: python monitor.py
Stop: Ctrl+C
"""

import subprocess
import time
import os
from datetime import datetime

REPO = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(REPO, "mcp_changes.log")
POLL_INTERVAL = 3  # seconds


def git(*args):
    result = subprocess.run(
        ["git", "-C", REPO] + list(args),
        capture_output=True, text=True
    )
    return result.stdout.strip()


def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {msg}"
    print(line)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def get_state():
    last_commit = git("log", "-1", "--format=%H %s")
    status = git("status", "--short")
    return last_commit, status


def main():
    log("=== Monitor started ===")
    log(f"Watching: {REPO}")
    prev_commit, prev_status = get_state()
    log(f"Current HEAD: {prev_commit or 'no commits yet'}")

    try:
        while True:
            time.sleep(POLL_INTERVAL)
            curr_commit, curr_status = get_state()

            if curr_status != prev_status:
                if curr_status:
                    for line in curr_status.splitlines():
                        log(f"WORKING TREE CHANGE: {line}")
                else:
                    log("Working tree clean")
                prev_status = curr_status

            if curr_commit != prev_commit:
                log(f"NEW COMMIT: {curr_commit}")
                diff_stat = git("diff", "--stat", "HEAD~1", "HEAD")
                if diff_stat:
                    for line in diff_stat.splitlines():
                        log(f"  {line}")
                prev_commit = curr_commit

    except KeyboardInterrupt:
        log("=== Monitor stopped ===")


if __name__ == "__main__":
    main()
