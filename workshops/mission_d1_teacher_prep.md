# 📜 D-1 — SENSEI PREPARATION CHECKLIST

Scroll: `mission_d1_the_shinobi_data_ledger.md` · Record: `mission_d1_data_record.md` ·
Alignment: `mission_d1_sg18_alignment.md` · Fixture: `mission_d1_missions_raw.json`

**Zero-install mission:** Python's built-in `json` module only — no third-party
packages, no internet. Prep = distribute two files + one pre-run + print the records.

---

## A. Distribute

- [ ] **Fixture** `mission_d1_missions_raw.json` to every student machine (LMS download
      or shared folder) — keep a pristine copy on the LMS: students must not edit it,
      and restores come from there.
- [ ] **Template** posted on the LMS as a **copy-paste text block** (students create
      `ledger_cleaner.py` and paste — the 35-minute budget has no room to hand-type the
      full scaffold; their typing work is the three TODOs).
- [ ] **Data Record** — one per shinobi.

## B. Pre-class checklist (do these ONCE)

- [ ] Open a clean project folder (fixture + pasted template) in VS Code and run the
      **template as shipped** — it runs (exit 0) but reports the *unfilled* state:
      `Raw records loaded: 8`, `[REVIEW] mission 101 — duplicate status unverified`,
      `Clean records retained: 7`, `D: 1`, `Total open missions: 5`. **This wrong-but-
      running state is the teaching moment** (rescue R5) — know it so you don't
      "fix" a student for it.
- [ ] Fill the three TODOs (answers in §G) and run again — expect verbatim:
      `8 / [DUPLICATE] 101 / [FLAG] 104 / 6 / A:2 B:1 C:1 / Total 4`, file saved
      beside the raw one, raw unchanged. *(Verified live on the reference environment;
      stdlib-only.)*
- [ ] Confirm students can **locate `missions_cleaned.json`** in the Explorer after a
      run (refresh needed sometimes) — this is the most common "it didn't work" report
      that isn't an error.
- [ ] Decide where the template lives if LMS is down: your USB/backup text file.

## C. Timing — where the 35 minutes goes

| Phase | Budget | Overrun risk | Simplification, not extension |
| --- | --- | --- | --- |
| 0 Briefing | 2 | low | take two predictions aloud; written line can come during Phase 2 |
| 1 Inspect | 4 | medium — JSON structure can invite reteaching | the structure map is ON the scroll — point, don't re-lecture; SG 18 LR1 already taught `json.load` |
| 2 Audit | 4 | low | the four finds are numbered on the scroll; a stalled squad gets "find the `null` first" |
| 3 Clean & transform | 12 | **HIGH** — 3 TODOs + runs | the TODOs are one-liners with comments; if >8 min: reveal TODO 3's line aloud and keep the other two; NEVER eat Phase 5's minutes |
| 4 Preserve | 5 | low | Explorer refresh + count = the whole phase |
| 5 Decision | 5 | low | read the two-sentence structure aloud; the §6 limit line is mandatory |
| 6 Review | 3 | low | checklist read-aloud, stamps on the way out |

**Never recover time by cutting Phase 5** — the decision-with-limit IS the
decision-making competency (PS4.T1.LS6); without it this is just a code drill.

## D. Watch-fors (known failure modes)

1. **Writing to the raw file** — the scaffold uses `"r"`; if a student experiments and
   the raw changes, restore from the LMS pristine copy (that's why §4 re-opens it: 8
   records, always).
2. **Deduping on id alone** — would also swallow *conflicting* records silently; TODO 2
   demands a **contents comparison** (`== record`). The `[REVIEW]` branch is the
   honesty valve — point at it in the debrief.
3. **Falsy traps** — `if not team` / `if not reward`: kills legitimate `0`, and is the
   SG's own sample bug (R4). If a student copies it from SG 18's Activity 2 sample,
   name the bug — don't mock it.
4. **Strip vs lower both needed on `" OPEN "`** — strip alone → `OPEN`; lower alone →
   `"open "`; the code does both — have the Inspector say it aloud (R6).
5. **Colab habits** — SG 18's snippets use Google Colab (`!ls -l`, `os.getcwd()`).
   Locally, `!ls` fails in a normal terminal; the Explorer is the folder view. Say this
   once before Phase 1.
6. **Counting the kept copy as "removed"** — duplicates removed = 1 (the extra copy),
   not 2 and not 0; the kept copy stays in `cleaned`.
7. **Output in the wrong folder** — R7; keep the VS Code terminal in the project folder
   from the start.

## E. Variants — prerequisites and honest boundaries

| Version | Time | Prerequisites | Does NOT demonstrate |
| --- | --- | --- | --- |
| **C (primary)** | 35 | fixture + template posted + record printed | — |
| **B** | 20 | template posted with **TODO 1 + TODO 3 pre-filled** (only the duplicate TODO remains) | the missing-value check and numeric conversion (supplied, not practiced); the written decision-limit step |
| **A** | 10 | prepared file whose data **pre-loads** (dict printed), everything done except **one** rule | reading a JSON file end-to-end; the complete cleaning competency — **fallback experience only, never stamp as mastery** |

## F. Arrangements and rotation

- **One computer per student:** everyone fills all three TODOs; roles = who reads each
  expected result aloud; §4 of the record is each student's own evidence. The
  `Which TODO did YOU fill` line is per-machine in this mode — it still audits
  participation because peers cross-check.
- **Shared squad computer:** keyboard **rotates per TODO** in Phase 3 — three shinobi,
  three TODOs; later phases pass again. Data Scribe records, Quality Inspector calls
  expected-vs-actual aloud, Audit Officer verifies exclusions + both output files.
- **Squads of two:** merge Scribe + Cleaner; each fills TODO(s) then swaps.
  **Fours:** Audit Officer owns the raw-unchanged verification + one shared run.

## G. Reference answers (teacher-only — do not pre-distribute)

```
TODO 1:  team = record.get("team")
         team_missing = team is None or (isinstance(team, str) and team.strip() == "")

TODO 2:  exact_duplicate = seen_ids[record["mission_id"]] == record

TODO 3:  if isinstance(reward, str) and reward.strip().lstrip("-").isdigit():
             record["reward"] = int(reward.strip())
```

Scope note: **`team` is the only required field in this fixture** — the starter is not a
general schema validator; it does not sweep every key of every record.

Dict-equality demo (for TODO 2): `{"a": 1} == {"a": 1}` evaluates to **`True`** — Python
compares dicts key-by-key and value-by-value. That is exactly the comparison that
separates an **exact duplicate** from a different record that merely shares the same
ID.

`isinstance(team, str)` = "is this a text value?" — the explicit check that keeps `0`
and `None` out of the "missing" bucket. Accepted alternative for TODO 1 if a student
writes it correctly: `team is None or team == ""` (the fixture's blanks are exactly
`null`, so it passes here — but `null` + blank-string handling is the general form).

## H. The conflicting-ID discussion (optional, Version C debrief — NOT in the core data)

Pose it: *"What if two mission 101s had DIFFERENT teams or rewards — who wins?"* The
scroll's law answers: **neither auto-wins.** First-record-wins is a silent guess; the
`[REVIEW]` branch flags it for human review instead. This is why the core fixture
deliberately contains **no** conflicting IDs — one variable at a time — but the branch
is scaffolded and runs if you add one later. (Adding it changes §4 counts, so only use
it as discussion, not as a graded step.)

## I. Teacher decisions (yours, not assumed)

1. Fixture distribution method (LMS download vs shared folder) + pristine restore copy.
2. Whether the conflicting-ID discussion (§H) runs at all — it is optional debrief.
3. Template as LMS text block (recommended) vs pre-made file in the folder.
4. Records printed on paper vs on-screen (space/paper budget).
5. When to deploy Version B vs C (class day surprises) — the B template must be
   prepared **before** the period if you might need it.

## J. Schedule placement

D-1 is **practice for SG 18's cleaning half** — it rehearses Learning Resource 2
(Cleaning and Transformation) and preps Activity 2 (Data Cleaning Transformation
Coding, 45–50 min, non-graded). It does **not** replace or preview-answers Activity 1
(Anime class, graded, Annex A rubric) — D-1 deliberately contains no class definitions.
Activity 3 (large-dataset challenge) stays extra-credit on the SG's own terms. Position
D-1 before Activity 2's class, or as its opening scaffold if the period runs short.