# 📜 WORKSHOP C-8 — THE SHINOBI DATA LEDGER: CLEAN BEFORE YOU DECIDE

*SG 18 — Introduction to Data Handling · companion practice for Learning Resource 2 and
Activity 2 (Data Cleaning and Summarizing)*

**Version C — 35 minutes, one mission, one class period.** (Versions A and B at the end
of this scroll.)

The village mission office received a JSON ledger of mission records. The office's
request: *"Some records are duplicated, some are half-empty, and the same village is
spelled three different ways. We need a ledger we can count — before we start sending
squads."*

**The shinobi truth of this mission:** raw data is not automatically trustworthy.
Before using it to make decisions, we must **inspect, clean, transform, and verify** it.

No new classes, no installations, no internet — Python's built-in `json` module, one
supplied file, three TODOs to complete, one cleaned file to defend.

---

## THE SQUAD — roles that rotate with the keyboard

| Shinobi | Mission role | Duty |
| --- | --- | --- |
| **Loremaster** | **Data Scribe** | records every count and decision in the Data Record |
| **Arena-Master** | **Data Cleaner / Lab Operator** | completes a TODO, runs the code, watches the audit lines |
| **Scout** | **Quality Inspector** | checks the actual output against the expected results, out loud |
| *4th member* | **Audit Officer** | verifies exclusions and that both output files are where they belong |

**The rotation law — read this twice.** The roles are *seats, not cells*:

- **One computer per shinobi:** everyone fills **all three TODOs** on their own
  machine. Roles decide who reads each expected result aloud and whose cleaned file the
  squad inspects together.
- **Shared squad computer:** the keyboard rotates **per TODO** in Phase 3 — each
  shinobi sits at the keys for one TODO — then passes again in later phases. Nobody
  graduates without having filled a TODO and pressed Run themselves.

## VILLAGE LAWS (carried + two new)

1. **Predict before you run.**
2. **One change at a time.** (Fill one TODO, run, read the audit lines, then the next.)
3. **90 seconds stuck → raise your hand.** (Any shinobi may call it; the Audit Officer
   tracks which rescue card fired.)
4. **Evidence is your rank.**
5. **NEW — The raw ledger is READ-ONLY.** `mission_c8_missions_raw.json` is opened with
   `"r"` only. Cleaning produces a **new** file; the source never changes. If the raw
   file could rewrite itself, nobody could ever audit what you did.
6. **NEW — Flag, don't guess.** A record that looks wrong gets **reported with its
   reason**, never silently dropped and never "first one wins". When the data is
   ambiguous, the answer is *human review* — the same honesty as B-2's review stamps.

---

## ⏱ THE MISSION AT A GLANCE — 35 minutes

| Min | Phase | Outcome |
| --- | --- | --- |
| 2 | 0 · Mission briefing | prediction written |
| 4 | 1 · Inspect the scroll | file read into Python structures; first count printed |
| 4 | 2 · Data audit | missing / duplicate / inconsistent records found by eye |
| 12 | 3 · Clean and transform | three TODOs completed; audit lines correct |
| 5 | 4 · Preserve the results | `missions_cleaned.json` saved; raw unchanged |
| 5 | 5 · Make a decision | open missions by rank + the honest limit |
| 3 | 6 · Mission review | evidence shown; why cleaning mattered, explained |

---

## PHASE 0 · MISSION BRIEFING (2 min)

**PREDICT — write it in your Data Record before touching a keyboard:**

> *What could go wrong if the village starts assigning teams using this ledger as-is?
> Name one way a decision made on the raw file would be wrong.*

(Hints to argue about: what happens to a mission that appears twice? What happens to a
mission with no team? Is `" OPEN "` the same status as `"open"`?)

## PHASE 1 · INSPECT THE SCROLL (4 min)

1. In VS Code, open the folder that holds **both** files: `mission_c8_missions_raw.json`
   and the posted template. Open the raw JSON and read the first record.
2. Type these six lines into a new file **`peek_ledger.py`** and run it (you will meet
these same lines again inside the full template in Phase 3):

```python
import json

with open("mission_c8_missions_raw.json", "r") as file:
    ledger = json.load(file)        # JSON object -> Python dict
missions = ledger["missions"]       # JSON array  -> Python list of dicts
print(f"Raw records loaded: {len(missions)}")
```

**Expected result:** `Raw records loaded: 8`

**The structure map — this is what `json.load()` hands you:**

| In the JSON file | In Python |
| --- | --- |
| `{ ... }` object | **dict** (key → value) |
| `[ ... ]` array | **list** |
| `"text"` string | **str** |
| `300` number | **int** (or float) |
| `null` | **None** |

So one record (a JSON object) is a **dict**, and `ledger["missions"]` is a **list of
dicts**. Every line you write today navigates that map.

## PHASE 2 · DATA AUDIT (4 min)

**By eye, before the code — find and record (Data Record §3):**

1. **Missing value:** which `mission_id`'s **`team`** is `null`?
2. **Duplicate:** which `mission_id` appears twice? Are the two copies *identical*?
3. **Three inconsistencies:** list at least three — e.g. leading/trailing whitespace,
   ALL-CAPS vs lowercase, a number stored as text, two spellings of one village.

*No cleanup yet — only findings. The audit comes first because the cleaning rules must
be chosen against what you actually saw, not guessed.*

## PHASE 3 · CLEAN AND TRANSFORM (12 min)

**The seven cleaning rules — read them first; they are the contract:**

1. In this dataset the required field is **`team`** — a record whose `team` is
   **missing, `null`, or blank** is flagged and **excluded** from the decision-ready
   output. (The starter checks `team`; it is not a validator for every field of every
   possible schema.)
2. An **exact duplicate** (same `mission_id` **and** identical contents) is reported and
   removed, keeping one copy.
3. Text values get **leading/trailing whitespace removed**.
4. Mission **status uses lowercase** text.
5. Village names follow the mapping: `Cedar` → `Cedar Hold` (and `" Cedar Hold "` →
   `Cedar Hold` once rule 3 has stripped it).
6. Numeric text in `reward` is **converted to int** when valid.
7. A legitimate numeric **`0` is preserved** — never treated as missing.

*A record with the same `mission_id` but **conflicting contents** is never auto-resolved:
it is flagged for human review — that is the `[REVIEW]` branch in the template below
(until TODO 2 is completed it simply reports *duplicate status unverified*), and your
sensei may stage the scenario as a debrief.*

**The template** (posted on the LMS — copy it into a file named `ledger_cleaner.py`;
the raw file stays untouched):

```python
import json

# THE SHINOBI DATA LEDGER — cleaning template (Workshop C-8, SG 18)
# The raw ledger is READ-ONLY: never open it in "w" mode.

RAW_FILE = "mission_c8_missions_raw.json"
CLEAN_FILE = "missions_cleaned.json"

# Cleaning rule 5 — approved village names
VILLAGE_NAMES = {
    "Cedar": "Cedar Hold",
}

# --- Phase 1: read the ledger into Python structures -------------------
with open(RAW_FILE, "r") as file:
    ledger = json.load(file)        # JSON object -> dict
missions = ledger["missions"]       # JSON array -> list of dicts
print(f"Raw records loaded: {len(missions)}")

cleaned = []
seen_ids = {}
duplicates = 0
incomplete = 0

for record in missions:
    # --- TODO 1: incomplete record (team missing)? ---------------------
    team = record.get("team")       # .get() never crashes on a missing key
    team_missing = False            # TODO 1: replace False — True when team
                                    # is null or blank. NEVER `if not team`
                                    # (that would also call 0 "missing"!)
    if team_missing:
        incomplete += 1
        print(f"  [FLAG] incomplete: mission {record.get('mission_id')} - missing team")
        continue

    # --- TODO 2: exact duplicate record? -------------------------------
    if record["mission_id"] in seen_ids:
        exact_duplicate = False     # TODO 2: replace False — True only when
                                    # the stored copy is IDENTICAL to this one
        if exact_duplicate:
            duplicates += 1
            print(f"  [DUPLICATE] mission {record['mission_id']} - identical copy removed")
            continue
        else:
            # Same id, contents not yet compared (or genuinely different):
            # NEVER guess either way — human review!
            print(f"  [REVIEW] mission {record['mission_id']} — duplicate status unverified")
            continue
    seen_ids[record["mission_id"]] = record

    # --- Cleaning rules 3-5: normalize text ---------------------------
    for field in ("team", "village", "rank", "status"):
        value = record[field]
        if isinstance(value, str):
            record[field] = value.strip()

    record["status"] = record["status"].lower()               # rule 4
    record["village"] = VILLAGE_NAMES.get(record["village"], record["village"])  # rule 5

    # --- TODO 3: numeric text -> int ------------------------------------
    reward = record["reward"]
    record["reward"] = reward        # TODO 3: convert digit-strings to int.
                                     # A legit 0 is already an int — keep it.
                                     # (NEVER `if reward:` — 0 would be lost)

    cleaned.append(record)

# --- Phase 2: save a SEPARATE cleaned file (raw stays unchanged) -------
with open(CLEAN_FILE, "w") as file:
    json.dump({"missions": cleaned}, file, indent=4)
print(f"Clean records retained: {len(cleaned)}")
print(f"Cleaned data saved to {CLEAN_FILE}")

# --- Phase 3: decision — open missions by rank ------------------------
open_by_rank = {}
total_open = 0
for record in cleaned:
    if record["status"] == "open":
        total_open += 1
        rank = record["rank"]
        open_by_rank[rank] = open_by_rank.get(rank, 0) + 1

print()
print("--- Open missions by rank ---")
for rank in sorted(open_by_rank):
    print(f"{rank}: {open_by_rank[rank]}")
print(f"Total open missions: {total_open}")
```

**Work the three TODOs — one change at a time.** As shipped (TODOs unfilled), the code
*runs* but reports the wrong counts — that is the point: run it first and read what the
unfilled checks are hiding (**Rescue card R5** explains the as-shipped output). Then
fill **TODO 1**, run; fill **TODO 2**, run; fill **TODO 3**, run.

**Expected result after all three TODOs (verbatim):**

```
Raw records loaded: 8
  [DUPLICATE] mission 101 - identical copy removed
  [FLAG] incomplete: mission 104 - missing team
Clean records retained: 6
Cleaned data saved to missions_cleaned.json

--- Open missions by rank ---
A: 2
B: 1
C: 1
Total open missions: 4
```

**Check TODO 3's effect in the file, not the console:** open
`missions_cleaned.json` — rewards must be **numbers** (`450`, `600`), and mission 103's
reward must still be **`0`**.

## PHASE 4 · PRESERVE THE RESULTS (5 min)

1. Confirm the output file exists in the project folder: **`missions_cleaned.json`**
   (check the VS Code Explorer — refresh if you do not see it).
2. **The READ-ONLY law, verified:** open `mission_c8_missions_raw.json` again — it must
   still contain **all 8 records**, untouched. Your code opens it with `"r"` and only
   `"r"`.
3. Count the cleaned records in the file: **6** (`101, 102, 103, 105, 106, 107`).
4. Record §4: paste your actual counts next to the expected ones.

**Pipeline words — say them once (the correction):** **E**xtract → **T**ransform →
**L**oad = **ETL**; Extract → **L**oad → **T**ransform = **ELT**. Transformation is
*one stage* of the pipeline — not the name of the whole job, whatever any text says.
Your mission is the first shape: Phase 1 **extracted** (`json.load`), Phase 3
**transformed** (the seven rules), and *this* phase **loads** (`json.dump` into a new
file).

**Two files, two roles:** the raw ledger is *evidence of what was received*; the cleaned
ledger is *what you are willing to decide on*. Keeping both is what makes the work
auditable.

## PHASE 5 · MAKE A DECISION (5 min)

From `missions_cleaned.json`, the code reports open missions by rank:

**Expected:** `A: 2` · `B: 1` · `C: 1` · `Total open missions: 4`

**The village's question:** *where is attention needed?*

**Your answer (Data Record §6, in two sentences):**

1. *"In this ledger, rank A missions hold the most open work (2 of 4)."*
2. **The honest limit — write it every time:** counts from one 8-record sample are
   **evidence for further consideration, not a resource-allocation policy.** This does
   **not** by itself prove more teams or more resources must go to rank A — the village
   would also want to know severity, age, squad availability, and whether this ledger is
   even complete. Counts start a conversation; they do not end it.

**Why cleaning came first:** count raw `"status"` values *exactly as written* and you
find only 2 `open` records (102 says `" OPEN "`, 106 says `"OPEN"`), while a careless
count double-counts mission 101's duplicate — **both wrong numbers, both confident.**
Cleaned and normalized, 4 is the number a shinobi can defend.

## PHASE 6 · MISSION REVIEW (3 min)

Check the Data Record end to end: prediction ✓ structure map ✓ audit findings ✓ counts
✓ two screenshots ✓ decision + limit ✓ explanation ✓.

**Rank earned:** ______ **Sensei stamp:** ______

**The sentence to leave with:** the ledger did not become trustworthy because it was
JSON — it became trustworthy because every record was **inspected, cleaned under
written rules, and verified against evidence.**

---

## 🩹 RESCUE CARDS

**R1 · `FileNotFoundError` (raw file not found).** The code looks where the *terminal*
is, not where you are looking. Fix: both files must sit in **one folder** opened in VS
Code (**File → Open Folder**); run from that folder; confirm both appear in the
Explorer. (In Google Colab habits: there is no `!ls` here — the Explorer is your
folder view.)

**R2 · `json.JSONDecodeError`.** Two different problems: (a) the file has a syntax
error — a missing comma or quote; open the raw file and compare its start/end braces;
(b) the file is **zero bytes / truncated** — a zero-byte file is *malformed JSON* and
`json.load()` raises an error. **Never** expect `json.load()` to "silently return an
empty list" for an empty file — that is R2, not a feature. (A *valid* file containing
`"missions": []` is different: it loads fine and yields **0 records** — check `Raw
records loaded:` first.) Restore the fixture from the LMS if needed.

**R3 · `KeyError: 'team'`.** The record has no such key. Use `record.get("team")`
(already scaffolded) — `.get()` returns `None` instead of crashing.

**R4 · Zero counted as missing, or `None` counted as a value.** `if not team:` treats
`0`, `""`, `None`, `[]` all the same — the SG's own sample bug. The fix is an **explicit
check**: `team is None or (isinstance(team, str) and team.strip() == "")`. Mission 103's
`reward = 0` must survive every rule you write.

**R5 · Duplicate count is 0 or 2 — or you see `[REVIEW] mission 101`.** As shipped,
TODO 2 is `False`, so the second 101 falls into the `[REVIEW]` branch — *duplicate status
unverified* (the contents comparison isn't written yet; the code refuses to guess) and
the count reads `Clean records retained: 7`. Filling TODO 2 with a **contents
comparison** (`seen_ids[record["mission_id"]] == record`) flips it to
`[DUPLICATE] ... removed` and the counts to **6 / 4**. Duplicates mean: same id **and**
identical contents — never id alone.

**R6 · Open count is not 4.** Check, in order: (1) status was **stripped AND
lowercased** — rule 4 needs both: strip alone leaves `OPEN`, lower alone leaves
`"open "`; do both; (2) village mapping ran **after** stripping; (3) record 104
(missing team) is **excluded** — an excluded record's `open` status must not be
counted; (4) the duplicate is removed **once**, keeping one copy.

**R7 · `missions_cleaned.json` saved somewhere unexpected.** Output saves relative to
the terminal's working folder (R1). Keep the terminal in the project folder; find the
file in the Explorer (refresh). It should appear **beside** the raw file.

**R8 · Rewards are still strings — or mission 103's 0 vanished.** Convert only digit
strings: `isinstance(reward, str) and reward.strip().lstrip("-").isdigit()` → `int(...)`.
If `0` disappeared you wrote `if reward:` — **0 is falsy but legitimate.** Never decide
"missing" from falsiness.

---

## VERSION B — 20 MINUTES (accelerated)

**Prerequisites (teacher-prepared):** raw fixture on the machine; template posted **with
TODO 1 and TODO 3 already filled** (only TODO 2 remains); Data Record sheet in hand.
**Scope (20 min):** read + structure map (4) → audit by eye (4) → fill TODO 2 (the
duplicate), run, verify `6 / 4` and raw unchanged (7) → save + locate cleaned file (3)
→ oral decision sentence only — no §6 written limit.
**Honest boundary:** Version B demonstrates **file reading, duplicate removal, saving,
and verification** — the missing-value check and numeric conversion were *supplied*, not
practiced, and the written decision-limit exercise is skipped. Do not stamp it as the
full cleaning competency.

## VERSION A — 10 MINUTES (fallback)

**Prerequisites:** a prepared file already open whose data **loads in memory** (raw dict
printed by the template) with everything complete except **one** rule (e.g. the status
lowercase line commented out).
**Scope (10 min):** identify **one** data-quality issue from the printed records (2) →
apply **one** cleaning rule (4) → run and verify the changed output in the printed
summary (4).
**Honest boundary:** Version A is a **fallback experience**. It does **not** read a JSON
file end-to-end and does **not** demonstrate the complete cleaning competency — it
exercises one rule on preloaded data. Treat it as "the squad saw one rule work," never
as mastery.

---

*All data is fictional: original village and squad names, invented records, no student
or personal information. This is short formative practice — the graded exercise remains
SG 18 Activity 1 (Annex A rubric); C-8 does not replace it.*