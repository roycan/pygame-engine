#!/usr/bin/env python3
"""Live smoke probe: boots the REAL server and hits every page.

Deliberately OUTSIDE the automated gate (`make test`): process and port
handling is exactly the kind of thing that flakes, and flakes must never
break the gate. Run this before deploying or after a Render merge:

    make smoke        # or: venv/bin/python tools/smoke_deploy.py

Checks: every page loads (200), an unknown arena 404s, and the step API
answers with turn JSON. Exit code 1 on any failure.
"""

from __future__ import annotations

import os
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def _free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def _get(url: str) -> tuple[int, str]:
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            return resp.status, resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as exc:
        return exc.code, ""


def main() -> int:
    gunicorn = REPO / "venv" / "bin" / "gunicorn"
    if not gunicorn.is_file():
        print("[FAIL] venv/bin/gunicorn missing -- run: venv/bin/pip install -r requirements.txt")
        return 1

    port = _free_port()
    command = [
        str(gunicorn),
        "--chdir", "rogue_edu",
        "app:app",
        "--workers", "1",
        "--bind", f"127.0.0.1:{port}",
        "--timeout", "20",
    ]
    env = dict(os.environ, SECRET_KEY="smoke-test-key")
    proc = subprocess.Popen(
        command, cwd=REPO, env=env,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    base = f"http://127.0.0.1:{port}"
    failures: list[str] = []
    try:
        deadline = time.time() + 30
        ready = False
        while time.time() < deadline:
            try:
                status, _ = _get(f"{base}/games")
                if status == 200:
                    ready = True
                    break
            except OSError:
                pass
            time.sleep(0.5)
        if not ready:
            print("[FAIL] the server never became ready within 30s")
            return 1

        checks = [
            ("/", 200, "board"),
            ("/games", 200, "Class Arcade"),
            ("/play/sample_pair", 200, "Sir Rosita"),
            ("/play/does_not_exist", 404, None),
        ]
        for path, want_status, marker in checks:
            status, body = _get(base + path)
            ok = status == want_status and (marker is None or marker in body)
            print(f"{'[PASS]' if ok else '[FAIL]'} GET {path} -> {status} (want {want_status})")
            if not ok:
                failures.append(path)

        request = urllib.request.Request(
            f"{base}/api/step",
            data=b'{"key": "zzz"}',  # no-op probe: proves the API answers
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(request, timeout=10) as resp:
            body = resp.read().decode()
        ok = '"turn"' in body
        print(f"{'[PASS]' if ok else '[FAIL]'} POST /api/step returned turn JSON")
        if not ok:
            failures.append("/api/step")
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()

    if failures:
        print(f"\nSMOKE FAILED: {failures}")
        return 1
    print("\nSmoke passed: every page loads and the API responds.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
