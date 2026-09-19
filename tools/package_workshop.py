#!/usr/bin/env python3
"""Package the Grade 9 workshop ZIP: dist/rogue_edu_workshop.zip.

The ZIP is the student distribution artifact: everything they need
(game code, tests, README, worksheet) and NOTHING they don't (dev-only
folders and caches). The selection logic lives in `select_files()` so
`tests/test_packaging.py` can verify it deterministically without
building anything.

Run directly (or via `make zip`):

    venv/bin/python tools/package_workshop.py
"""

from __future__ import annotations

import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

#: Top-level files and folders that ship to students.
INCLUDED_TOP_LEVEL = (
    "rogue_edu",
    "tests",
    "workshops",
    "README.md",
    "DEPLOYING.md",
    "requirements.txt",
    "pytest.ini",
    "Makefile",
    "package.json",
    "Procfile",
)

#: Directory names that must never appear inside the ZIP.
EXCLUDED_DIR_NAMES = {
    "venv",
    ".venv",
    "node_modules",
    "temp",
    "inceptions",
    "plans",
    "dist",
    "__pycache__",
    ".pytest_cache",
    ".git",
    ".vscode",
}

EXCLUDED_SUFFIXES = (".pyc", ".log")


def _excluded(path: Path) -> bool:
    relative = path.relative_to(REPO_ROOT)
    if set(relative.parts) & EXCLUDED_DIR_NAMES:
        return True
    return path.name.endswith(EXCLUDED_SUFFIXES)


def select_files(root: Path = REPO_ROOT) -> list[Path]:
    """Every repo file that belongs in the workshop ZIP, sorted."""
    selected: list[Path] = []
    for top in INCLUDED_TOP_LEVEL:
        path = root / top
        if path.is_file():
            selected.append(path)
        elif path.is_dir():
            selected.extend(
                f for f in sorted(path.rglob("*")) if f.is_file() and not _excluded(f)
            )
    return selected


def build_zip(destination: Path | None = None) -> Path:
    """Write the ZIP (everything nested under rogue_edu_workshop/) and
    return its path. Windows' 'Extract All' then yields one clean folder."""
    dest = destination or (REPO_ROOT / "dist" / "rogue_edu_workshop.zip")
    dest.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED) as archive:
        for file in select_files():
            archive.write(file, Path("rogue_edu_workshop") / file.relative_to(REPO_ROOT))
    return dest


if __name__ == "__main__":
    print(f"Wrote {build_zip()}")
