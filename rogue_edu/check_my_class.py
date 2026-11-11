#!/usr/bin/env python3
"""check_my_class.py -- your personal code doctor.

Run it from the rogue_edu/ folder after every edit:

    python check_my_class.py                            # the starter file
    python check_my_class.py arenas/ada_and_ivo/game_config   # a pair's arena

With no argument it reads student_starter/classes.py and checks:
  1. your classes inherit from Hero, Villain or NPC,
  2. the required methods exist (act / interact / symbol),
  3. act() and interact() actually RETURN valid Actions when called
     against a mock read-only view.

Given an arena's game_config (a path or a dotted module name), it checks
the sibling classes module the same way AND verifies that TITLE is set
(it names your card on the /games class arcade).

You get [PASS]/[WARN]/[FAIL] lines with friendly fixes -- never a raw
Python traceback. Exit code is 1 if any [FAIL] was printed (handy for
scripts and teachers).
"""

from __future__ import annotations

import importlib
import importlib.util
import sys
from dataclasses import dataclass
from pathlib import Path

from engine.actions import Action, SpeakAction
from engine.base_classes import Hero, NPC, Villain


@dataclass
class Finding:
    """One diagnostic result, ready to print."""
    level: str  # "PASS" | "WARN" | "FAIL"
    title: str
    detail: str = ""


class MockSafeGameView:
    """A tiny stand-in for SafeGameView used to call act()/interact()
    safely. It answers "the hero is one step to your east", so chase and
    attack logic gets exercised deterministically."""

    def get_hero_position(self):
        return (4, 3)

    def distance_to_hero(self, entity):
        return 1

    def get_direction_toward_hero(self, entity):
        return (1, 0)

    def is_tile_passable(self, x, y):
        return True


def inspect_classes(module_name: str = "student_starter.classes") -> list[Finding]:
    """Inspect a module and return findings (pure function, no printing).

    Kept import-and-print-free so the pytest suite can feed it both the
    real student file and deliberately broken fixtures.
    """
    try:
        module = importlib.import_module(module_name)
    except SyntaxError as exc:
        return [
            Finding(
                "FAIL",
                f"Could not read {module_name}: syntax error near line {exc.lineno}.",
                "Look for a missing colon (:), an unclosed bracket, or a "
                "stray character near that line number.",
            )
        ]
    except ImportError as exc:
        return [
            Finding(
                "FAIL",
                f"Could not import {module_name}: {exc}",
                "Check the import lines at the top, e.g. "
                "'from engine.base_classes import Villain'.",
            )
        ]
    except Exception as exc:  # any other import-time crash
        return [
            Finding(
                "FAIL",
                f"Importing {module_name} crashed: {type(exc).__name__}: {exc}",
                "The crash happened while Python read the file top to "
                "bottom. Check code that runs OUTSIDE of methods.",
            )
        ]

    findings: list[Finding] = []

    # ---- Find the classes the STUDENT defined ---------------------------
    student_classes: list[tuple[type, str]] = []
    for obj in vars(module).values():
        if not isinstance(obj, type) or obj.__module__ != module.__name__:
            continue  # imported engine classes are not student work
        if issubclass(obj, Hero) and obj is not Hero:
            student_classes.append((obj, "Hero"))
        elif issubclass(obj, Villain) and obj is not Villain:
            student_classes.append((obj, "Villain"))
        elif issubclass(obj, NPC) and obj is not NPC:
            student_classes.append((obj, "NPC"))
        elif issubclass(obj, (Hero, Villain, NPC)):
            continue  # engine base itself re-exported; ignore
        else:
            findings.append(
                Finding(
                    "WARN",
                    f"Class '{obj.__name__}' does not inherit from Hero, "
                    f"Villain or NPC -- the engine will ignore it.",
                    "Fix: class MySlime(Villain):",
                )
            )

    if not student_classes:
        findings.append(
            Finding(
                "FAIL",
                "No Hero, Villain or NPC subclasses were found.",
                "Start with: class MySlime(Villain): ... then add act(self, view).",
            )
        )
        return findings

    required_methods = {
        "Hero": [],
        "Villain": ["act"],
        "NPC": ["interact"],
    }

    for cls, base_name in student_classes:
        problems = False

        # ---- Required methods ------------------------------------------
        for method in required_methods[base_name] + ["symbol"]:
            fn = getattr(cls, method, None)
            if fn is None or getattr(fn, "__isabstractmethod__", False):
                problems = True
                if method == "act":
                    hint = "Fix: def act(self, view): return WaitAction()"
                elif method == "interact":
                    hint = "Fix: def interact(self, view): return SpeakAction('Hello!')"
                else:
                    hint = "Fix: def symbol(self): return '👾'"
                findings.append(
                    Finding(
                        "FAIL",
                        f"{base_name} '{cls.__name__}' is missing the "
                        f"{method}() method.",
                        hint,
                    )
                )

        # ---- Safe construction ------------------------------------------
        if problems:
            continue  # no point instantiating a half-written class
        try:
            instance = cls(3, 3)
        except TypeError as exc:
            findings.append(
                Finding(
                    "FAIL",
                    f"'{cls.__name__}' could not be constructed with (x, y): {exc}",
                    "Your __init__ should look like: def __init__(self, x, y): "
                    "super().__init__('Name', x, y, hp=10, attack_power=3)",
                )
            )
            continue
        except Exception as exc:
            findings.append(
                Finding(
                    "FAIL",
                    f"Constructing '{cls.__name__}' crashed: "
                    f"{type(exc).__name__}: {exc}",
                    "Anything that runs inside __init__ must be safe: no "
                    "game objects, no view, no moving -- just stats.",
                )
            )
            continue

        # Surface silent stat clamps early (the engine logs these too).
        for warning in getattr(instance, "warnings", []):
            findings.append(
                Finding(
                    "WARN",
                    f"'{cls.__name__}' had a stat clamped: {warning}",
                    "hp lives in [1, 200]; attack_power lives in [0, 40].",
                )
            )

        # ---- Inherited state actually present? --------------------------
        # A constructor that never calls super().__init__() builds just fine
        # but crashes the engine at registration with a bare AttributeError.
        # Catch it HERE, in doctor language, before the game ever runs.
        required_state = ["name", "x", "y"]
        if base_name in ("Hero", "Villain"):
            required_state += ["hp", "max_hp", "attack_power"]
        missing_state = [attr for attr in required_state if not hasattr(instance, attr)]
        if missing_state:
            findings.append(
                Finding(
                    "FAIL",
                    "Instance missing required engine state "
                    f"({'/'.join(missing_state)}). Did you forget to call "
                    "super().__init__(...) in your constructor?",
                    "Fix: first line inside your __init__ should be "
                    "super().__init__('Name', x, y, hp=10, attack_power=3). "
                    "(NPCs: super().__init__('Name', x, y).)",
                )
            )
            continue  # behaviour tests would only repeat this crash

        # ---- Safe behavior test ------------------------------------------
        view = MockSafeGameView()
        if base_name == "Villain":
            try:
                result = instance.act(view)
            except Exception as exc:
                findings.append(
                    Finding(
                        "FAIL",
                        f"Calling {cls.__name__}.act() crashed: "
                        f"{type(exc).__name__}: {exc}",
                        "act(self, view) receives the read-only view -- call "
                        "helpers on it like view.distance_to_hero(self).",
                    )
                )
                continue
            if isinstance(result, Action) and not isinstance(result, SpeakAction):
                findings.append(
                    Finding(
                        "PASS",
                        f"Villain '{cls.__name__}' inherits Villain and "
                        f"act() returned {result!r}.",
                    )
                )
            elif isinstance(result, SpeakAction):
                findings.append(
                    Finding(
                        "WARN",
                        f"{cls.__name__}.act() returned a SpeakAction, but "
                        f"villains must return MoveAction, AttackAction or "
                        f"WaitAction.",
                        "Fix: return MoveAction(1, 0)",
                    )
                )
            else:
                findings.append(
                    Finding(
                        "WARN",
                        f"{cls.__name__}.act() returned {result!r} instead "
                        f"of an Action.",
                        "Fix: return MoveAction(1, 0) (or WaitAction() while "
                        "you are still experimenting).",
                    )
                )
        elif base_name == "NPC":
            try:
                result = instance.interact(view)
            except Exception as exc:
                findings.append(
                    Finding(
                        "FAIL",
                        f"Calling {cls.__name__}.interact() crashed: "
                        f"{type(exc).__name__}: {exc}",
                        "interact(self, view) must return SpeakAction('...').",
                    )
                )
                continue
            if isinstance(result, SpeakAction):
                findings.append(
                    Finding(
                        "PASS",
                        f"NPC '{cls.__name__}' inherits NPC and interact() "
                        f"returned a SpeakAction.",
                    )
                )
            else:
                findings.append(
                    Finding(
                        "WARN",
                        f"{cls.__name__}.interact() returned {result!r} "
                        f"instead of a SpeakAction.",
                        "Fix: return SpeakAction('Hello, traveler!')",
                    )
                )
        else:  # Hero
            findings.append(
                Finding(
                    "PASS",
                    f"Hero '{cls.__name__}' inherits Hero -- the engine "
                    f"drives its turns from your keyboard.",
                )
            )

    return findings


def format_findings(findings: list[Finding]) -> str:
    """Render findings as humanized terminal lines (no tracebacks)."""
    icons = {"PASS": "[PASS]", "WARN": "[WARN]", "FAIL": "[FAIL]"}
    lines = []
    for finding in findings:
        lines.append(f"{icons[finding.level]} {finding.title}")
        if finding.detail:
            lines.append(f"       {finding.detail}")
    counts = {level: 0 for level in icons}
    for finding in findings:
        counts[finding.level] += 1
    lines.append("")
    lines.append(
        f"Summary: {counts['PASS']} passed, {counts['WARN']} warnings, "
        f"{counts['FAIL']} failures."
    )
    if counts["FAIL"]:
        lines.append("Fix the [FAIL] items, then run this script again.")
    elif counts["WARN"]:
        lines.append("No blockers! Consider polishing the [WARN] items.")
    else:
        lines.append("Beautiful. Run the game: python app.py")
    return "\n".join(lines)


def _resolve_target(raw: str | None) -> str:
    """Turn a CLI argument into an importable dotted module name.

    Accepts a dotted module ("arenas.ada_and_ivo.classes") OR a path
    ("arenas/ada_and_ivo/classes.py" -> "arenas.ada_and_ivo.classes").
    No argument -> the default student starter file.
    """
    if raw is None or not raw.strip():
        return "student_starter.classes"
    cleaned = raw.strip()
    if cleaned.endswith(".py"):
        cleaned = cleaned[:-3]
    parts = [p for p in cleaned.replace("\\", "/").split("/") if p not in ("", ".")]
    return ".".join(parts)


def _title_findings(game_config_module: str) -> list[Finding]:
    """The /games class arcade reads TITLE from the arena's game_config."""
    try:
        module = importlib.import_module(game_config_module)
    except Exception:
        return []  # the import problem is already reported by inspect_classes
    declared = getattr(module, "TITLE", None)
    if isinstance(declared, str) and declared.strip():
        return [
            Finding(
                "PASS",
                f"TITLE found: \"{declared}\" -- this names your /games menu card.",
            )
        ]
    return [
        Finding(
            "WARN",
            "No TITLE = \"...\" found in game_config.py.",
            "The /games menu falls back to the folder name. Fix: "
            "TITLE = \"Ada & Ivo's Gauntlet\"",
        )
    ]


def _stale_import_findings(game_config_module: str) -> list[Finding]:
    """Catch the #1 copy-the-template trap: the pair edits THEIR classes.py
    but game_config.py still imports ``_template.classes`` -- so the arena
    card looks healthy, plays fine, and silently runs the TEMPLATE code."""
    try:
        spec = importlib.util.find_spec(game_config_module)
    except (ImportError, AttributeError, ValueError):
        return []  # an unimportable config is already reported elsewhere
    if spec is None or not spec.origin or not spec.origin.endswith(".py"):
        return []
    try:
        text = Path(spec.origin).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []
    for line in text.splitlines():
        stripped = line.strip()
        if not (stripped.startswith(("from ", "import "))):
            continue  # import lines only, per the check's contract
        if "_template.classes" in stripped:
            return [
                Finding(
                    "WARN",
                    "Stale import detected in game_config.py! You are "
                    "importing from _template.classes instead of your "
                    "local classes.py.",
                    "Your edits to classes.py are being ignored. Fix: "
                    "point the import at YOUR folder, e.g. "
                    "from arenas.<your_team>.classes import ...",
                )
            ]
    return []


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    target = _resolve_target(args[0] if args else None)
    findings: list[Finding] = []
    if target.rsplit(".", 1)[-1] == "game_config":
        classes_target = target[: -len("game_config")] + "classes"
        print(f"Checking {classes_target} ...\n")
        findings.extend(inspect_classes(classes_target))
        findings.extend(_title_findings(target))
        findings.extend(_stale_import_findings(target))
    else:
        print(f"Checking {target} ...\n")
        findings.extend(inspect_classes(target))
    print(format_findings(findings))
    return 1 if any(f.level == "FAIL" for f in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
