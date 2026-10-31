# 🧪 L-1 — SENSEI PREPARATION CHECKLIST

Scroll: `mission_l1_the_library_scroll.md` · Record:
`mission_l1_lab_record.md` · Alignment: `mission_l1_sg17_alignment.md`

**Scope reminder:** L-1 occupies **Activity 3's 35 minutes** (Data Visualizer). The
Typing Face-off and Performance Face-off stay in the SG's own schedule — this
workshop contains neither. Prep = one pretest, one print, one contingency.

---

## A. Pre-class checklist (do these ONCE, on a representative student machine)

- [ ] **Python + `py` launcher** work: `py --version` and `py -m pip --version` both
      answer.
- [ ] **VS Code + Python extension** installed (interpreter picker exists).
- [ ] **PyPI reachable** from the lab: install once on the test machine and note the
      time it took.
- [ ] **matplotlib install tested** on that machine — record the version you got.
- [ ] **Graph window + PNG saving verified**: run the scroll's template once; confirm
      the window opens, closes, and `bacteria_growth.png` appears.

**Honest framing of the SG's "first 5 minutes":** the setup check is a *diagnostic*,
not a repair. If `py`/`python` is not recognized, that is a missing/broken Python
installation — an IT task, not something a command run in the first five minutes can
cure. Machines that fail this check are Version-B/C-of-last-resort candidates (pair
the student, or swap machines) — decide before the period starts.

## B. Print & distribute

- [ ] Lab Record — one per shinobi (they may share a squad copy + individual §5 lines
      if paper is tight).
- [ ] `plot_results.py` template on the **LMS** (students still type it into their own
      file; the LMS copy is the reference, not a file to download-and-run).

## C. Timing — where the 35 minutes actually goes

| Phase | Budget | Overrun risk | Simplification, not extension |
| --- | --- | --- | --- |
| 0 Briefing | 2 | low | take predictions verbally; writing happens in §1 later |
| 1 Prepare the Lab | 5 | **HIGH** — first `.venv` for many students | if >6 min: finish it for the class floor, mark those squads for the Version-B debrief question; the scroll's R3/R5 cards are the fast repairs |
| 2 Acquire the Tool | 5 | medium (download speed) | the internet contingency in §E |
| 3 Build the Visualizer | 12 | medium (typing) | template is short; refuse debug spirals >90 s — rescue rule applies to code too |
| 4 Improve the Result | 5 | low | enforce ONE change; early finishers get the extension, not more time for others |
| 5 Traffic Jam | 4 | low | it is discussion, not installation — keep it paper |
| 6 Completion | 2 | low | checklist read-aloud, stamps on the way out |

The two high-risk phases are 1 and 3; **both have hard fallbacks** (pre-created
`.venv` = instant Version B; LMS template kills typing time). Never recover time by
cutting Phase 5 — the conflict-reasoning is the only place the fourth DLC competency
appears.

## D. Watch-fors (the mission's known failure modes)

1. **Installing into the wrong Python** — no `(.venv)` prefix when they press Enter.
   The scroll's Phase 2 expected-result line is the guard; make squads read it aloud.
2. **The `requests` habit** — the official SG's Activity 3 installs
   `matplotlib requests`; this workshop deliberately installs **matplotlib only**
   (the activity never uses requests; see alignment file). If students who read the SG
   ahead ask why, that is the answer — and a good one.
3. **Execution-policy temptation** — a web search will offer
   `Set-ExecutionPolicy ...` for activation errors. Refuse on sight; R5's full-path
   invocation needs **zero** settings changed.
4. **Environment mismatch class** — install in one terminal, run in another. The
   verify line (`sys.executable`) exists precisely to catch this; expect to point at
   it at least once per class.
5. **`plt.show()` blocking confusion** — the window "freezes" VS Code's terminal
   until closed. That is normal; show it once so nobody thinks the machine hung.

## E. Slow-internet / no-internet contingency (teacher-controlled)

- **Option 1 — pretested environment:** copy your tested `Lab_Visualizer` folder
  (with `.venv` inside) to a shared location or USB; squads copy it locally, then run
  Version B's scope from the interpreter-select step.
- **Option 2 — prepared output:** distribute a pre-generated `bacteria_growth.png`
  for the interpretation phase only.
- **Mark it honestly:** students who received a prepared environment complete the
  *use* competencies; the *installation* competency is **not** demonstrated by them.
  Their Lab Record carries the **assisted-install** checkbox. Do not blur this — the
  SG grades Activity 3 on the workflow, not just the picture.

## F. Arrangements

- **One computer per student:** everyone performs every step; roles decide who reads
  expected results aloud. Circulate for the §2 path check — it is the one students
  fake fastest.
- **Shared squad computer:** keyboard rotation is printed in the scroll (Phase 1
  Loremaster → 2 Tool-Bearer → 3 Evidence-Scout → 4 anyone who hasn't typed). The
  Record's "which steps did YOU personally type" line is your audit trail.
- **Squads of two:** merge Env-Keeper + Tool-Bearer; Evidence-Scout covers both
  checks. **Fours:** Rescue Officer role activates fully — assign them R-card
  ownership for the debrief.

## G. Variants — prerequisites and honest boundaries

| Version | Time | Prerequisites | Does NOT demonstrate |
| --- | --- | --- | --- |
| **C (primary)** | 35 | pretest done; LMS template up | — |
| **B** | 20 | `.venv` pre-created with matplotlib installed; template on LMS | creating an environment; performing an install (verification only) |
| **A (fallback)** | 10 | B's prerequisites + file already open | environment creation, installation, verification — *seen only, not done* |

Say the boundary out loud when you deploy A or B: these are fallback **experiences**,
not proof of the install competency. A's record should not be stamped as if C
happened.

## H. Teacher decisions (yours, not assumed)

1. LMS posting form of the template (text block vs file) — text, so they type it.
2. Whether Version-B/A squads still submit the full Lab Record (recommended: yes,
   with assisted/variant marking).
3. Whether ILA17 (Exploring Libraries, bonus) may cite L-1 evidence — e.g. the jam
   answer — as its starting point.
4. Machine-swap vs pair-share policy for machines that fail the pretest.
5. Whether the Phase-5 scenario is read aloud by you or silently by squads (read
   aloud is safer for pacing).

## I. SG 17 schedule placement

L-1 fills **Activity 3's own 35-minute block** in the SG's meeting plan. The
Typing/Performance Face-offs and the video resource remain SG-scheduled activities —
the scroll contains only a one-line recall of the face-off result in Phase 0. If your
period also contains the SG's setup minutes, run the pretest checklist before the
period; the first-five-minutes check belongs to you, not to the students.
