# 🌀 MISSION G-2 — TEACHER'S TALE & RESCUE GUIDE (teacher-only)

Scrolls: `mission_g2_three_shinobi_one_trusted_change.md` ·
`mission_g2_ila_conflicting_scrolls.md`
Everything marked **[verified]** was reproduced in disposable scratch labs. The GitHub
**web/extension layer** was **not** exercised live — rehearse it per
`mission_g2_teacher_prep.md` §B before mission day.

---

## THE TALE — "The Village That Stamped Nothing" (~2 min, tell it before Phase 3)

> A village once merged every scroll the moment it arrived. No stamps, no questions —
> the authors were trusted shinobi, surely. One day a scroll claimed the slime was
> "truly dangerous" — and the village believed the title, because reading the scroll
> felt like distrust between friends. The engine, quieter than any reviewer, clamped
> the 99 down to 40 and whispered a warning nobody ran. The game was fine — but the
> *village* had stopped telling the truth about its own game. Ten missions later,
> nobody knew which claims were real, because nobody had ever checked one.
>
> The Stamp Law is not bureaucracy. **A review is the village telling itself the truth.**

*(Honest framing: this tale is a teaching parable. The warning it cites is real and
verified: `[WARN] 'Slime' had a stat clamped: attack_power=99 is out of range [0, 40];
clamped to 40.`)*

---

## THE CONFLICT SCRIPT [verified end-to-end in scratch]

The exact sequence, outputs, and resolution used to design ILA Phases 1–4. Rehearse it
on a scratch copy before class.

1. From the **same** `main`: `feature/elder-warning` rewrites the Elder's line to
   `"The walls hold, but the slimes bite hardest at your corners!"`;
   `feature/elder-lore` rewrites it to `"Two slimes now guard this grove -- keep your
   back to a corner!"`. Both pushed; both PRs opened against `main`.
2. Scroll 1 merges first — **note: the first PR may fast-forward** (no merge commit).
   That is normal; say it if a squad asks.
3. Scroll 2: GitHub shows **"This branch has conflicts that must be resolved."**
   On the branch machine: `git fetch origin` → `git merge origin/main` →
   **CONFLICT (content)** in `classes.py`, markers exactly:
   ```
   <<<<<<< HEAD
           "Two slimes now guard this grove -- keep your back to a corner!"
   =======
           "The walls hold, but the slimes bite hardest at your corners!"
   >>>>>>> origin/main
   ```
4. Resolution happens **on the feature branch** (never on main, never by hand-editing
   GitHub's copy): on the branch machine — `git fetch origin` → `git checkout
   feature/elder-lore` → `git merge origin/main` → replace the entire marker block with
   `"The walls hold, traveler, and two slimes now guard this grove -- they bite hardest at your corners!"`
   → chakra check green → commit `merge main: keep both warnings -- walls hold AND two
   slimes` → push. **The PR updates and the banner clears.**
5. Stamp (Approve) → merge → pull → the Elder speaks the combined line.
   **Final line verified:** `The walls hold, traveler, and two slimes now guard this
   grove -- they bite hardest at your corners!`

Teacher escape hatch if a squad drowns mid-resolution: `git merge --abort` restores
the pre-merge branch cleanly — then walk Phase 3 again slowly. (Aborting is *not*
failure; it is stopping to read the map.)

---

## RECOVERY DRILLS [all four verified]

Run from any clone. VS Code equivalents in parentheses.

1. **Discard a modified tracked file** (VS Code: Source Control → **Discard Changes** ↩)
   ```
   git restore rogue_edu/student_starter/classes.py
   ```
2. **Unstage the wrong file** (VS Code: the **−** icon next to the staged file)
   ```
   git restore --staged rogue_edu/student_starter/game_config.py
   ```
3. **Recover a deleted tracked file** — deletion is just a working-tree change:
   ```
   rm rogue_edu/student_starter/classes.py
   git restore rogue_edu/student_starter/classes.py
   ```
4. **Restore an older committed version** (VS Code: Timeline / Open Changes → restore):
   ```
   git log --oneline -6                     # pick the good hash
   git restore --source=<hash> rogue_edu/student_starter/game_config.py
   ```
   Verified: `defeat_all` mode restored from an older hash intact, with the newer
   commit still in history.

**The wall between recovery and rollback:** drills 1–4 touch **uncommitted or local**
work — private, silent, nobody else ever knew. Rollback (below) undoes **shared**
history — public, loud, a new commit for everyone to pull.

---

## ROLLBACK — "Protect the Village" [verified at git level; Revert button = platform layer]

Preferred student path (ILA Phase 7): the merged Wall PR's page → **Revert** button →
GitHub opens a *new revert PR* proposing the undo → review stamp → merge → all pull →
pillar gone. **Nothing is erased; the revert is recorded as a new contribution.**

Teacher CLI equivalent (why each piece exists):
```
git revert -m 1 <merge-commit-hash>
```
- `-m 1` = "keep parent 1 (main's side), undo the merged-in side" — **it only works on
  a merge commit**, which is why the scrolls always choose **Create a merge commit**
  (prep §A2).
- If the PR was **fast-forwarded** (first-PR-of-the-day case) there is no merge commit:
  revert the plain commit instead — `git revert <commit-hash>`, no `-m`.
- If the PR was **squash-merged or rebased**, there is no merge commit to `-m 1`:
  revert the single commit instead — `git revert <hash>`. The prep §A2 setting
  (squash/rebase disabled) and the scrolls' merge guards exist so this branch of the
  decision tree never opens mid-lesson.
- Verified result: 6 walls → revert → 5 walls, `(8, 2)` empty, history shows
  `Revert "Merge remote-tracking branch 'origin/pr/extra-wall'"` as a new commit.
- **Never teach `git reset --hard` for shared work** — it rewrites the village's
  memory and orphans every teammate's clone. Recovery drills are for local work;
  revert is for shared work. Say the wall out loud, once per class.

---

## RESCUE CARDS

**Card #1 — The author cannot approve their own PR.** By design (platform fact).
The stamp must come from another shinobi. Squads of three never feel this; solo
testers always do.

**Card #2 — Merge button grayed.** Two usual causes: an unresolved **conversation**
(review comment not marked resolved — resolve conversations, then merge) or the PR
**has conflicts** (ILA Phase 3 flow). Under the Stamp Law, a pending "Request changes"
does *not* gray the button — the squad's stamp discipline is what stops it.

**Card #3 — Extension signed out / PR panel empty.** Use the web fallback:
github.com → squad repo → Pull requests → same actions (comment, review, merge).
Re-sign-in (`Ctrl+Shift+P` → GitHub: Sign In) after class.

**Card #4 — PR opened against the wrong base.** Close the PR (harmless — nothing
merges), create it again with base `main` ← compare `feature/…`. The branch and
commits are untouched.

**Card #5 — "Please clean your repository working tree before checkout."**
Uncommitted changes block a switch (G-1 rescue card #3). Commit them or Discard (↩).
This is **not** a merge conflict — it is a guard on your own unfinished work.

**Card #6 — Squad pulled but "the game didn't change."** Check three things in order:
branch (status bar says `main`?), pull actually ran (SC panel shows sync), and the
feature was on `main` on GitHub (open the repo page). The usual criminal: verifying
from a feature branch.

**Card #7 — Conflict panic.** Read the three markers aloud: `<<<<<<< HEAD` (your
branch's words) · `=======` (the wall) · `>>>>>>> origin/main` (what main received).
Keep both ideas, delete all three marker lines, chakra check, commit, push.
Total panic escape: `git merge --abort` — clean branch, try again with the sensei.

---

## CLI TRANSLATION TABLE (VS Code / GitHub button ↔ Git Bash)

| Action | Git Bash |
| --- | --- |
| Open PR (extension/web) | no equivalent — PRs live on GitHub |
| Files Changed | `git diff main origin/feature/…` |
| Fetch (refresh remote view) | `git fetch origin` |
| Comment / Request changes / Approve | reviews live on GitHub |
| Merge PR (Create a merge commit) | `git checkout main && git merge --no-ff origin/feature/…` |
| Resolve conflicts (merge main into branch) | `git merge origin/main` → edit markers → `git add` → `git commit` |
| `git merge --abort` (escape hatch) | same command |
| Revert button on a merged PR | `git revert -m 1 <merge-hash>` |
| Discard (↩) | `git restore <file>` |
| − (unstage) | `git restore --staged <file>` |
| Timeline → restore version | `git restore --source=<hash> <file>` |
| Pull / push | `git pull` / `git push` |

Chakra check and launch (from `rogue_edu/`): `python check_my_class.py` ·
`~/rogue-edu-env/Scripts/python.exe app.py`.
