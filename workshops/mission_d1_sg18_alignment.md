# 📜 MISSION D-1 → SG 18 ALIGNMENT (short reference)

Scroll: `mission_d1_the_shinobi_data_ledger.md` · Record: `mission_d1_data_record.md` ·
Prep: `mission_d1_teacher_prep.md` · Fixture: `mission_d1_missions_raw.json`
SG 18 — Introduction to Data Handling: *Read data from a JSON text file and store it in
appropriate data structures. Clean and transform raw data by handling missing values,
duplicates, and inconsistencies to make it reliable and meaningful.* Learning Standard:
**PS4.T1.LS6 Develop applications to aid in data-driven decision making.** Assessment:
Activity 1 (graded, Annex A 20-pt rubric) · Activity 2 (non-graded) · Activity 3 (extra
credit, own time).

## Status: DRAFT — written from the SG text and a live run of the exact starter and
reference code on this session's reference environment (Python 3, stdlib only);
**not yet classroom-tested.**

## Competency coverage — honest mapping

| SG 18 competency | Status in D-1 | Where | Variant coverage |
| --- | --- | --- | --- |
| **Read a JSON file into appropriate structures** | **Practiced** — `json.load` → dict; `ledger["missions"]` → list of dicts; structure map filled from the file | Phase 1, Record §2 | C full · B full · A **not exercised** (data pre-loaded) |
| **Clean: missing values** | **Practiced** — explicit `None`/blank check (`.get()`) on this fixture's **`team`** field (not a schema-wide sweep), flagged + excluded, with the falsy-`0` trap taught | Phase 3 TODO 1, R4 | C · B pre-filled (**supplied, not practiced**) · A only if it is the one rule |
| **Clean: duplicates** | **Practiced** — exact-duplicate criterion (same id **and** identical contents), reported once, kept one copy; conflict branch flags for review | Phase 3 TODO 2, R5, prep §H | C · B (the one remaining TODO) · A if chosen as its rule |
| **Clean: inconsistencies** | **Practiced** — strip, lowercase status, village mapping, numeric-string→int, zero preserved | Phase 3 rules 3–7, TODO 3, R6/R8 | C full · B (normalization scaffolded-supplied) · A one rule |
| **Data-driven decision (PS4.T1.LS6)** | **Practiced, bounded** — open-by-rank + the mandatory limit sentence: counts are evidence for further consideration, not a resource-allocation policy | Phase 5, Record §6 | C written · B oral only · A **omitted** |

**The brief's ten-step workflow, mapped:** import `json` (template header) · `json.load`
(Phase 1) · extract the list (Phase 1) · inspect fields / identify incomplete (Phase 2 +
TODO 1) · detect exact duplicate (TODO 2) · normalize text (rules 3–5 scaffold) ·
numeric strings → int (TODO 3) · zero preserved (rule 7 + R8) · `json.dump` to a
**separate** file (Phase 4) · print audit summary + by-rank (Phase 3 end / Phase 5).

## Schedule mapping

- **D-1 = one 35-minute block of practice for the cleaning half** — it rehearses
  Learning Resource 2 and opens Activity 2 (45–50 min, non-graded).
- **Does not duplicate Activity 1:** no class definitions, no Anime exercise — D-1 is
  deliberately procedural "data-handling logic" (file → structures → rules → counts).
  Activity 1 stays the graded class-based exercise under Annex A, untouched.
- **Activity 3** (large dataset, extra credit) untouched.
- Fictional data only — original village/squad names, no personal records, no
  copyrighted characters (the SG's own sample content is not reproduced).

## Technical corrections to SG 18 — flagged, not silently applied to the SG

1. **The falsy missing-check** (SG Activity 2 sample: `if not student["math"] or not
   student["science"]`) — treats a legitimate **`0` as missing**, and raises
   **`KeyError`** if the key is absent. D-1 teaches the explicit form
   (`team is None or (isinstance(team, str) and team.strip() == "")` with `.get()`),
   and makes zero-survival a graded check (fixture mission 103, Record §4).
2. **ETL / ELT wording** (SG LR2: *"The data transformation process is Extract, Load,
   and Transform or ETL or it could be Extract, Transform and load (ETL)"*) — both are
   labeled ETL; the first is **ELT**, and transformation is **one stage** of a pipeline,
   not the name of the whole process. Corrected in the scroll's Phase 4 "pipeline words"
   note: **ETL = Extract → Transform → Load; ELT = Extract → Load → Transform;** D-1's
   own flow is extract (`json.load`) → transform (the seven rules) → load (`json.dump`
   to a new file). Concise, Grade-9 length — no architecture lecture.
3. **"No data" ambiguity** (SG Activity 1: *"If the .json file has no data then
   characters should be an empty list"*) — a **zero-byte or malformed file makes
   `json.load()` raise `JSONDecodeError`**; it never silently returns an empty list. A
   *valid* `"missions": []` file loads to 0 records. D-1 states the distinction (R2 +
   prep §B/§D).
4. **Raw-immutable practice:** SG Activity 3's `update_json()` writes back to the source
   (reasonable there); D-1 adopts the opposite law for cleaning — **never overwrite the
   source** — because an auditable clean needs the original evidence (scroll law 5,
   verified in Phase 4).
5. **Colab vs local:** SG snippets assume Google Colab (`!ls -l`, Colab default folder).
   The classroom is Windows + VS Code; D-1 uses the Explorer and a local terminal only
   (R1, prep §D5). No `os` import needed — `json` module only, per mission scope.
6. **Minor:** SG LR2 opens with *"Clearing and transforming data"* (typo for Cleaning) —
   cosmetic, flagged for the CS team.

## What the variants do NOT assess (explicit)

- **C** — full chain: file read → audit → three rules practiced → save → verify →
  written decision-with-limit. The only variant that demonstrates the complete
  competency.
- **B** — missing-check and reward conversion were **supplied**; decision limit skipped.
  Demonstrates reading, duplicate removal, saving, verification — not the full set.
- **A** — fallback experience on **pre-loaded** data: one issue, one rule, verify. Does
  **not** read a JSON file end-to-end and must never be stamped as the complete
  cleaning competency.

## Continuity

- **From S-1:** the record's shape still echoes the annex-style sections (findings →
  evidence → prediction), one page, same voice.
- **From L-1:** identical workshop machinery — template-with-TODOs in the scroll,
  expected-result strings quoted verbatim, rescue cards R1–R8, rotation law, honest
  variant boundaries, "evidence is your rank."
- **From SG 17:** L-1's closing promise lands here — *"today the data was typed into a
  list; next unit, the program reads data from files."* D-1 is that next unit.
- **To SG 19 (CSV):** the cleaning rules (strip, normalize, convert, flag) transfer
  wholesale to CSV; only the reader changes.
- **To the SG 16 proposal arc:** Phase 5's limit sentence trains the same discipline as
  P-1's exclusions — a defensible claim, stated with its boundaries.

## Verification status summary

- **Live-executed this draft:** fixture parses (valid JSON, exactly **8** records) ·
  reference solution run → `8 raw / 1 duplicate / 1 flagged / 6 clean / 4 open /
  A:2 B:1 C:1`, cleaned ids `[101,102,103,105,106,107]`, all rewards `int`, mission
  103's `0` intact, `"450"→450`, `"600"→600`, statuses/villages normalized · starter
  template as shipped runs (exit 0, instructive wrong state: 7/5/[REVIEW]) · raw file
  **sha256 unchanged** after both runs.
- **Executed on WSL/Linux Python 3, stdlib only.** No Windows-specific behavior is
  involved in the code (`json`, path-relative I/O), but the VS Code/Explorer/terminal
  steps have **not** been run on a school Windows machine — not claimed as Windows-
  verified.
- **Not classroom-tested.** Pacing, rotation, and record-sheet flow await your first
  period.
- **Fictional throughout:** villages, squads, records, and the office request are
  invented teaching data (disclosed in scroll + record).

## Remaining gaps

- Hands-on Activity-1-style class/JSON integration is intentionally out of scope here
  (it is the SG's graded exercise).
- The conflicting-ID scenario is discussion-only (prep §H) — students reason about it
  but do not process a conflicting fixture; if you ever want it practiced, it needs its
  own fixture revision (counts would change).
- Empty-JSON distinction is taught as a rescue (R2) but not staged as a hands-on
  exercise — deliberately, to hold the 35-minute line.