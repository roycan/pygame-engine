"""CI gate: the GitHub Actions workflow runs the FULL gate on PRs.

Students open pull requests against the class repo; a red/green X on
their PR is authentic CI with zero extra teaching. This file pins the
workflow so it cannot silently stop running the whole gate.
"""

import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
WORKFLOW = REPO / ".github" / "workflows" / "tests.yml"


def test_workflow_exists_and_runs_on_pull_requests():
    assert WORKFLOW.is_file(), ".github/workflows/tests.yml is missing"
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "pull_request" in text, "CI must run on student pull requests"
    assert "push" in text, "CI must also guard direct pushes to main"


def test_workflow_runs_the_full_gate():
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "make test" in text, "CI must run the SAME gate as npm test / make test"
    assert "npm ci" in text, "CI must install the pinned jsdom dev dependency"
    assert "actions/setup-python" in text and "actions/setup-node" in text, (
        "toolchains must be pinned via first-party setup actions"
    )


def test_lockfile_is_committed_for_npm_ci():
    lock = REPO / "package-lock.json"
    assert lock.is_file(), "npm ci needs a committed package-lock.json"
    parsed = json.loads(lock.read_text(encoding="utf-8"))
    dev_deps = parsed.get("packages", {}).get("", {}).get("devDependencies", {})
    assert "jsdom" in dev_deps, "the lockfile must pin the jsdom dev dependency"
    # The file must actually be COMMittable: if .gitignore lists it, CI's
    # `npm ci` gets nothing. (This really happened -- anti-false-green.)
    import subprocess

    ignored = subprocess.run(
        ["git", "check-ignore", "-q", "package-lock.json"],
        cwd=REPO, capture_output=True,
    )
    assert ignored.returncode != 0, (
        "package-lock.json is git-ignored -- CI's npm ci would see no lockfile"
    )
