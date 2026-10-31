# 🧪 MISSION L-1 → SG 17 ALIGNMENT (short reference)

Scroll: `mission_l1_the_library_scroll.md` · Record: `mission_l1_lab_record.md` ·
Prep: `mission_l1_teacher_prep.md`
SG 17 — Frameworks and Libraries Integration: *install and use a package manager to
install a library relevant to a specific task · import and use a library to perform a
specific function · compare custom vs library-based performance · identify and
resolve dependency conflicts.* Assessment: Activity 3 Data Visualizer (formative,
graded rubric) + ILA17 (optional, bonus).

## Status: DRAFT — written from the SG text and a live technical run-through on a
scratch environment; **not yet classroom-tested.**

## DLC coverage — honest mapping

| SG 17 competency | Status in L-1 | Where | Variant coverage |
| --- | --- | --- | --- |
| **Install via package manager** (pip, task-relevant library) | **Practiced** — create `.venv`, select interpreter, `python -m pip install matplotlib`, verify placement | Phases 1–2, R3/R4 | C full · B verifies only · A not demonstrated |
| **Import and use a library** (specific function) | **Practiced** — `import matplotlib.pyplot as plt` → labeled, gridded graph | Phases 3–4 | C and B full · A runs + customizes |
| **Compare custom vs library performance** | **Recall only** — one Phase-0 line; the Face-offs own this competency | Phase 0 | deliberately excluded from all variants |
| **Identify/resolve dependency conflicts** | **Practiced, reasoning level** — paper scenario; no environments harmed | Phase 5 | C full · B 60-second teacher-led · A omitted |

**The brief's eight practice items, all mapped:** venv creation (P1) · interpreter
selection + path verification (P1, §2) · pip install (P2) · verify intended
environment (P2 `pip show` Location, §3) · import/use matplotlib (P3) · generate +
save PNG (P3) · explain one observation (P4, §5) · recognize a dependency conflict
(P5, §6).

## Schedule mapping

- **L-1 = Activity 3's 35-minute block.** Not a second meeting; no separate ILA.
- **Excluded by design:** Activity 1 Typing Face-off (20 min), Activity 2 Performance
  Face-off (15 min) — they remain SG-scheduled. L-1's only contact with them is the
  Phase-0 recall line ("the library won, and it wasn't close"). No benchmarking
  activity exists in L-1.
- **SG's "Necessary Setup" 5 minutes:** treated as a teacher diagnostic (prep §A),
  not an in-class repair window (correction 3 below).

## Technical corrections — flagged, not silently applied to the SG

1. **`pip install matplotlib requests`** (SG Activity 3, Phase 1) — `requests` is
   never used by the supplied code. L-1 installs **matplotlib only**: smaller
   download (school Wi-Fi), one clean dependency story, and the "install only what
   the mission names" security habit. Flag for the next SG revision.
2. **No `savefig` in the SG code** — SG's Phase 3 ends at `plt.show()`, yet the
   checklist expects evidence and the LMS expects screenshots. L-1 adds
   `plt.savefig("bacteria_growth.png", dpi=150)` **before** `show()` (closing the
   window can clear the figure — save first is the robust order). Verified: the PNG
   renders 960×720 at dpi 150.
3. **"Run pip --version … clears out the 'Command not recognized' errors"** (SG
   Necessary Setup) — a version check *diagnoses*; it cannot *fix* a missing Python
   installation or PATH break. L-1 says so explicitly (R1, prep §A) and routes broken
   machines to a teacher decision (swap/pair), not to doomed commands.
4. **"The Fix: use virtual environments so they don't fight"** (SG §4.2) — true
   between projects, incomplete as stated: a venv does **not** resolve two packages
   in the *same* project demanding incompatible versions of one dependency. L-1's
   Phase 5 teaches exactly this boundary (isolate across projects; conflicts within a
   project need investigation/choice).
5. **`python -m venv .venv`** (SG) → **`py -m venv .venv`** (L-1, per approved brief):
   the Windows launcher is more robust when `python.exe` is not on PATH. Likewise L-1
   uses `python -m pip …` everywhere instead of the SG table's bare `pip`, so pip
   always belongs to the selected interpreter.
6. **Terminology hygiene (brief):** pip = package manager; `math` = standard-library
   module; matplotlib = third-party package; Flask = framework example (named in the
   SG 16/17 arc, not used here); `import` = a Python statement, not a package-manager
   command. L-1's Phase 2 note carries the one-sentence version.
7. **Acronym/version note:** verified live under Python 3.14 / pip 26.2.2 /
   matplotlib 3.11.2: `Successfully installed matplotlib-…` wording, `pip show`
   field names (Name/Version/Location), and the 960×720 PNG. Windows-specific
   behaviors (`py` launcher, `.venv\Scripts\python.exe` fallback, VS Code picker,
   `deactivate`) follow the documented venv layout mirrored by the Linux run — not
   independently executed in this draft.

## Security & licensing (brief §5) — coverage

Phase 2 carries the practical warning: check package identity and documentation;
prefer established, relevant packages (matplotlib qualifies); licensing before reuse
("open source ≠ no rules" — SG §4.4's own framing); nothing about L-1 weakens
execution policies or system settings (R5 exists so that no one ever wants to).

## What the variants do not assess (explicit)

- **C** — full chain; the only variant that demonstrates the complete installation
  competency.
- **B** — environment pre-built: shows verification + install *confirmation*, use,
  evidence. Does not demonstrate environment creation or a from-scratch install.
- **A** — fallback experience only: run + customize + interpret. Demonstrates **no**
  part of the installation competency and must not be stamped as if it did.

## Continuity

- **From SG 16:** libraries appeared in proposals at the SG 16 deck's four honesty
  levels (exists → purpose → can use → evidence). L-1 is the level-3→4 event for
  matplotlib: by mission's end a student has *used* it and *holds evidence*.
- **From P-1:** squads and roles persist (adapted); the Phase-0 predict habit and
  the Rescue Officer's 90-second trigger are carried mechanics.
- **To ILA17 (Exploring Libraries, bonus):** the Phase-5 jam answer and the §5
  library sentence are natural seed evidence, if you allow it (prep §H3).
- **To SG 18 (Data Handling):** L-1's data is hard-coded; SG 18 reads data from text
  files — the natural next scroll reads the Biology team's *actual* file.

## Verification status summary

- **Live-executed in this draft:** venv creation → interpreter path print →
  `pip install matplotlib` → `pip show` fields → the exact template (with savefig) →
  `Generating graph...` → PNG 960×720 → growth ratios 1.5 / 2.0 / 2.17 / 1.85 / 2.08
  (≈ doubling per hour, ×25 total) supporting the Phase-4 hint lines.
- **Documented, not executed here:** Windows `py` launcher, PowerShell activation
  behavior, VS Code interpreter picker, `deactivate` — per brief + Python/VS Code
  documentation; worth one pass on a lab machine during the prep §A pretest.
- **Fictional:** the research team and the AgarGrower/GraphMaster conflict; the
  bacteria data is illustrative teaching data (disclosed in both student files).
