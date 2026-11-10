# 🌀 RogueEdu — ILA: The Conflicting Scrolls

*(Mission B-2 ILA · SG 14 · Chūnin Edition · 30 minutes · follow-up to the Scroll of Approval)*

**Squad:** ______ **Date:** ______ **Recorded by (Scout's ledger):** ______________

**Prerequisites:** Scroll of Approval complete (the Stats PR is merged and verified) ·
roles **rotate one seat**: the Reviewer becomes an Author, an Author becomes the
Steward — see the table below. Stamp Law still stands: **no merge without a stamp.**

## 🥷 Role rotation (write the names before you start)

| Seat | Classroom cycle | ILA Round 1 — The Conflicting Scrolls | ILA Round 2 — Protect the Village |
| --- | --- | --- | --- |
| **Change Author** | Loremaster | **Arena-Master** (scroll 1) **+ Loremaster** (scroll 2 — two authors by design) | **Scout** |
| **Code Reviewer** | Arena-Master | **Loremaster** (reviews the resolution) | **Loremaster** |
| **Integration Steward** | Scout | **Scout** | **Arena-Master** |

Every shinobi authors, every shinobi has their work judged, every shinobi integrates or
verifies. **The roles are the curriculum — take your seat.**

**⏱ Timing:** 2 briefing · 6 authoring · 3 first merge · 6 conflict + resolution ·
3 stamp + merge · 4 pull + verify · 1 recovery drill · 5 Protect the Village. Total 30.

---

## 🥷 PHASE 0 — Briefing (2 min)

Today the squad meets the **one thing Mission B-1 promised never to require**: a real
merge conflict. Two shinobi will edit **the same line of the same file**. The first
scroll lands; the second **must** conflict. That is not failure — **the conflict is the
lesson**, and resolving it is a planned, normal act of collaboration.

**Predict (Scout's ledger):** when PR 2 conflicts, whose words does the `<<<<<<< HEAD`
marker hold — the first author's or the second's? Why? ______________

---

## 🥷 PHASE 1 — Two Scrolls, One Line (6 min — both Authors in parallel)

**Scroll 1 — Arena-Master (machine 1):**
1. New branch from `main`: `feature/elder-warning`
2. `classes.py` → the Elder's quoted line becomes **exactly**:
   ```python
   "The walls hold, but the slimes bite hardest at your corners!"
   ```
3. Stage, commit `lore: elder warns the slimes bite at corners`, push, **open the PR**
   (base `main`). Title: `lore: corner warning`.

**Scroll 2 — Loremaster (machine 2):**
1. **From `main` again** (not from scroll 1!): new branch `feature/elder-lore`
2. The Elder's quoted line becomes **exactly**:
   ```python
   "Two slimes now guard this grove -- keep your back to a corner!"
   ```
3. Stage, commit `lore: elder warns of the two grove slimes`, push, **open the PR**.

**Both PRs propose better Elder warnings. Both are good. Both cannot land as written —**
they rewrite the same line of the same file. **This is the only reliable way a conflict
is born:** genuinely overlapping, incompatible changes. (Two edits to two *different*
files — like B-1 — never collide on a line.)

---

## 🥷 PHASE 2 — The Steward Lands Scroll 1 (3 min — Scout)

Scout reviews quickly (rubric: one line, on-territory, sensible warning), stamps
(**Approve**), **Merge pull request → Create a merge commit**.
**Ledger:** scroll 1 merged at ____:____. Main now says: ________________________________

---

## 🥷 PHASE 3 — Scroll 2 Meets Reality (6 min — Loremaster drives, squad watches)

1. On GitHub (or the extension), PR 2 now shows: **"This branch has conflicts that must
   be resolved."** The machine refuses to guess. **This is the moment — observe it
   before touching anything.**
2. Resolution happens **on the feature branch** (never on main, never on the web by
   hand-waving). On scroll 2's machine (Git Bash):
   ```
   git fetch origin
   git checkout feature/elder-lore
   git merge origin/main
   ```
3. The editor now shows the disagreement, named by markers:
   ```python
   <<<<<<< HEAD
           "Two slimes now guard this grove -- keep your back to a corner!"
   =======
           "The walls hold, but the slimes bite hardest at your corners!"
   >>>>>>> origin/main
   ```
   **HEAD = your branch's words. Below `=======` = what main already received.**
   (Compare with your Phase 0 prediction: ______)
4. **Resolve by preserving BOTH ideas in one coherent line.** Replace the whole marker
   block (all three marker lines) with **exactly**:
   ```python
           "The walls hold, traveler, and two slimes now guard this grove -- they bite hardest at your corners!"
   ```
5. ⚖️ `python check_my_class.py` → expect `Summary: 3 passed, 0 warnings, 0 failures.`
6. Stage, commit: `merge main: keep both warnings -- walls hold AND two slimes`, **push
   to the same branch**. The PR **updates itself** and the conflict banner disappears.

**The law:** a resolution that silently discards a teammate's idea is a *submission*,
not a *merge*. The village reads both scrolls.

---

## 🥷 PHASE 4 — Stamp & Land the Resolution (3 min — Arena-Master reviews, Scout merges)

Reviewer: open PR 2 → **Files Changed** → confirm the resolution keeps **both** warnings
and deletes all three marker lines (`<<<<<<<`, `=======`, `>>>>>>>` — any survivor means
the fight is still on). ⚖️ Chakra check on the branch: green? **Approve.**
Scout: **Merge** → dropdown → **Create a merge commit** (not squash, not rebase — same
rule as the classroom scroll) → **Ledger:** merged at ____:____.

---

## 🥷 PHASE 5 — The Village Reunites, Again (4 min — all three shinobi)

All machines: switch to `main`, **pull**. Then, each machine:
1. ⚖️ Chakra check → `Summary: 3 passed, 0 warnings, 0 failures.`
2. Launch the game, bump the Elder 🧙, and copy the combined line **verbatim**:
   ________________________________________________________________
3. Confirm **both ideas** survived: the walls ______ AND the two slimes ______.

**✅ Evidence:** PR 2's conflict → resolution → approval → merge, visible in the PR's
timeline; the combined line heard in the game. (Screenshot the PR page for the ledger.)

---

## 🥷 PHASE 6 — Recovery Drill (1 min — all machines, hands on)

You edited `classes.py` by accident (add `# oops` to any line, save). The **M** badge
appears. It is uncommitted — so it is yours to erase:
`git restore rogue_edu/student_starter/classes.py` — or VS Code Source Control →
**Discard Changes** (↩). Dirty files after: ____

*Drills 3–4 (recover a deleted file; restore an older committed version) are
sensei-demonstrated — full script in the tale/rescue guide. Fast squads: run them
yourself from that guide.*

---

## 🥷 PHASE 7 — Protect the Village: Rollback (5 min — rotated seats)

The squad ships a change… then discovers it breaks the puzzle. **Undo a change that is
already shared — without erasing history.**

1. **Author (Scout):** branch `feature/extra-wall` from `main` → in `game_config.py`,
   directly below `("Pillar", 2, 5),` add:
   ```python
           ("Pillar", 8, 2),
   ```
   Commit `arena: extra pillar at (8, 2)`, push, **open PR → review stamp → merge**
   (**Create a merge commit** — not squash, not rebase; the Revert lesson needs a
   merge commit). Pull on all machines: launch the game — **count the pillars:
   ______ (now 6 — the wall blocks the grove path).** The village regrets it.
2. **Rollback:** on GitHub, the merged PR's page → bottom, **Revert** button →
   *Revert pull request* → a **new** PR appears proposing the undo → review stamp →
   merge it. Pull on all machines.
3. ⚖️ Chakra check → green. Game: pillars back to **5**, (8, 2) empty. **The game
   returned — and the history did not lie:** `git log --oneline -4` shows the revert as
   a **new commit**, recorded like any other contribution.

**The distinction that must survive:** **recovery** fixes *your uncommitted* work
(restore, discard — private, silent). **Rollback** undoes *already-shared* work
(revert — public, loud, a new commit for everyone). The village never rewrites
scrolls; it writes corrective scrolls.

---

## 🥷 PHASE 8 — Evidence & Reflection (inside the 30 — record as you go)

**Ledger evidence:** PR numbers for scroll 1, scroll 2, the resolution, and the revert ·
the conflict markers copied verbatim · the combined Elder line · pillar counts before
and after.

**SG 14 reflection (graded — submit to KHUB):**
1. Did you experience conflicts? What produced this one?
2. What steps helped avoid merge conflicts? (Think: B-1's territories.)
3. How did code review improve the final result — give one concrete example.
4. What was challenging about collaborating with Git and GitHub?

**Optional — the village's numbers as pictures:** open your squad repo on GitHub →
**Insights → Contributors**: the bars are your real commits, turned into pictures.
Read it: who authored the most this month? (Whether this satisfies SG 14's
data-visualization objective is a sensei decision — see the alignment file.)

---

**Rescue guide, drills 3–4 & conflict script:** `teacher/mission_b2_teachers_tale_rescue.md`
**Sensei prep:** `teacher/mission_b2_teacher_prep.md` · **SG 14 map:** `teacher/mission_b2_sg14_alignment.md`
