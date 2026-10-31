# 🌀 MISSION G-1 FALLBACKS — Versions A & B (Sensei Reference)

Primary mission: `mission_g1_three_shinobi_one_game.md` (Version C, 30 min, three
machines per squad). Use these when hardware, network, or time says otherwise.
Each version is honest about what it teaches and what it defers.

---

## Two machines, one squad — an honest adaptation of Version C

**Setup:** Loremaster drives machine 1; Arena-Master drives machine 2; the Scout
shares machine 1's chair during Phases 0–3 (reading the scroll aloud, running the
fetch watch in the second terminal) and **takes the chair at Phase 4**.

**What still happens exactly as in Version C:** two parallel branches, staging,
commits, publish + push, merge into `main`, push, and the other machine pulling the
changed game.

**What is genuinely lost — say this to the squad:**
- The third independent clone. Version C's Scout *fetches into a machine that never
  held either contribution*; here the Scout integrates from a machine that already
  holds one branch, so the fetch brings only the *other* shinobi's work.
- "Three shinobi, three independent histories" becomes two.
- The Co-Scout (squad of four) can restore some of this by integrating from the
  fourth machine if one exists.

**Nothing is pretended:** the scroll's Phase 4 note "I am on main" and all rescue
cards apply unchanged. The squad earns full rank; the sensei records which squads ran
two-machine.

**Squad of four on three machines:** the Co-Scout / Field Tester's Phase 5 duty
(independent pull + full re-verification) upgrades to also shadowing Phase 2–3.

---

## VERSION A — "The Village Ledger" (10 minutes, one machine, whole squad)

**Teaches:** saved ≠ staged ≠ committed ≠ pushed; local vs remote history.
**Defers:** branches, merging, parallel contribution, pull-changes-your-game.
**Prep assumed:** squad repo exists, machine authed, repo already cloned and the
baseline verified (by sensei or a prior session).

1. **(1 min)** Whole squad at one machine. Open the repo in VS Code, Source Control
   panel clean. **Predict:** what will the **M** badge mean in a minute?
2. **(2 min)** Loremaster edits the Elder's line in `classes.py` (the exact line from
   the scroll, Phase 2). **Save.** Observe: **M** appears — and history did not move.
   *Saving a file is not committing.*
3. **(2 min)** Arena-Master ALSO edits `game_config.py` (change one wall coordinate,
   e.g. `("Rock", 4, 4)` → `("Rock", 4, 3)`). Now stage **only** `classes.py` (`+`).
   Observe the two lists: **Staged** vs **Changes**. *Staging is choosing what the
   envelope will contain.*
4. **(2 min)** Scout types the commit message and clicks **Commit**:
   `lore: Elder warns of the slimes`. Observe: `game_config.py` is STILL modified.
   *One commit, one choice. Committing is not pushing.*
5. **(2 min)** Click **Publish Branch**/**Push**. Sensei opens the squad repo on
   GitHub (projector): find the commit in the remote history. Ask the squad: did any
   OTHER machine change? *(No — history moved on GitHub only. Only a pull does that.)*
6. **(1 min)** Cleanup: select `game_config.py` → **Discard Changes** (the ↩ icon) so
   the squad repo stays clean. *Uncommitted work can be thrown away safely — history
   was never touched.*
7. **Exit evidence:** each shinobi writes the commit hash they see locally, then the
   one GitHub shows. Same characters, two places.

---

## VERSION B — "Two Training Grounds" (20 minutes, one machine, offline-capable)

**Teaches:** branch isolation, merge mechanics, run-the-game proof.
**Defers:** the entire remote leg — publish, push, and pull-as-sync. (If the squad
repo exists and auth works, Phases 3½/4½ below add publish + push back in ~3 min.)

**Prep assumed:** repo cloned, identity configured. No GitHub needed.

1. **(2 min)** Hook (projector): demo dungeon — three villains, three personalities.
   "Today two shinobi upgrade ONE game without stepping on each other."
2. **(3 min)** Loremaster: status bar → new branch `feature/elder-lore` → edit the
   Elder's line (scroll Phase 2) → save. Predict: what does `main` look like right
   now? Switch to `main` and look. **That is a branch.**
3. **(4 min)** Switch to `main` → new branch `feature/second-slime` → Arena-Master
   adds the grove-guard line (scroll Phase 2) → save → stage → commit
   `arena: second slime guards the grove`.
   *(Yes, from `main`: one machine, so the branches take turns. Version C removes
   the taking-turns; say so.)*
4. **(2 min)** Branch safari: switch `main` → `feature/second-slime` → `main` →
   `feature/elder-lore`. Watch the Elder's line change under your feet.
5. **(4 min)** Scout integrates: on `main`, `Git: Merge Branch…` →
   `feature/elder-lore`, then → `feature/second-slime`. *(Local names — no `origin/`
   prefix when the branches were never pushed.)*
6. **(3 min)** Prove the game: ⚖️ chakra check → launch with the lab's shared
   environment (`~/rogue-edu-env/Scripts/python.exe app.py`) → two 🟢, new Elder line.
   **The merge succeeded before anyone ran the game. Only the run proved it.**
7. **(2 min)** Teacher's Tale (see `mission_g1_teachers_tale_rescue.md`) + exit
   question 4 from the scroll.

**Optional remote legs (if auth is ready):** after step 3, Publish Branch pushes each
feature branch to GitHub; after step 5, Push sends `main`. A second machine can then
pull and confirm the combined game — that is Version C with training wheels.
