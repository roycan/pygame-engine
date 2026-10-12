#!/usr/bin/env python3
"""Child-side of the arena validation probe (import + create_game()).

Run by ``rogue_edu/arenas/__init__.py`` in a SUBPROCESS so that an
untrusted arena's import-time or build-time behavior -- including a
non-terminating loop, which no try/except can catch -- can be
terminated by the parent (subprocess timeout => kill) instead of
wedging a gunicorn worker thread.

Contract:
    * exit 0                      -> the arena imported and built a game
    * exit nonzero                -> stderr carries a short error summary
    * killed by parent timeout    -> parent records "timed out"
    * ``--timeout-ready <sec>``   -> accepted no-op; the parent owns ALL
      timing policy. The child must never decide timeout duration.

This script does ONE thing, prints nothing on success, and is safe to
run against hostile student code precisely because its whole lifetime
is bounded by the parent's kill.
"""

from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, help="path to game_config.py")
    parser.add_argument(
        "--timeout-ready",
        type=float,
        default=0,
        help="accepted no-op: timeout policy belongs to the parent process",
    )
    args = parser.parse_args()

    here = Path(__file__).resolve().parents[1] / "rogue_edu"
    if str(here) not in sys.path:
        sys.path.insert(0, str(here))

    config_path = Path(args.config)
    try:
        spec = importlib.util.spec_from_file_location("rogueedu_probe_target", config_path)
        if spec is None or spec.loader is None:
            print(f"ImportError: could not create an import spec for {config_path}", file=sys.stderr)
            return 2
        module = importlib.util.module_from_spec(spec)
        sys.modules["rogueedu_probe_target"] = module
        spec.loader.exec_module(module)
        factory = getattr(module, "create_game", None)
        if not callable(factory):
            print("AttributeError: game_config.py does not define create_game()", file=sys.stderr)
            return 3
        factory()  # a config that imports but explodes at build time is broken
    except SyntaxError as exc:
        print(f"SyntaxError: {exc}", file=sys.stderr)
        return 4
    except Exception as exc:  # noqa: BLE001 - the summary IS the payload
        print(f"{type(exc).__name__}: {exc}", file=sys.stderr)
        return 5
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
