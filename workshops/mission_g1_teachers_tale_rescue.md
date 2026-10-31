# 🌀 MISSION G-1 — TEACHER'S TALE & RESCUE GUIDE (teacher-only)

Student scroll: `mission_g1_three_shinobi_one_game.md`
Everything here was verified in a disposable rehearsal lab; nothing was pushed to any
real remote.

---

## THE TALE — "Three PASS, and the village still burned" (~2 min, projector, optional)

**Tell it as a story of a past squad. The point lands harder when it isn't theirs.**

> A squad once ran this exact mission. The Loremaster merged cleanly — Git said the
> merge strategy did its work, no conflicts. The Scout ran the chakra check:
>
> ```
> Summary: 3 passed, 0 warnings, 0 failures.
> ```
>
> The squad celebrated. Then they played. A slime wandered more than four tiles from
> the hero — and the village burned:
>
> ```
> NameError: name 'WaitAction' is not defined
> ```
>
> The Arena-Master had taught the slime patience — *wait until the hero is close* —
> but the word `WaitAction` was never added to the import line at the top of
> `classes.py`. Python reads that word only when a slime finally WALKS FAR. The
> mission's check never walks far: the doctor's mock view always answers
> `distance_to_hero == 1`, so the new wait-branch is never exercised. Every machine
> passed a check the real game could fail.
>
> The fix was one word on the import line — one commit:
> `fix: import WaitAction -- the patient branch crashed without it`.

**Ask the class, then give the triad:**
- Did the merge succeed? **Yes.**
- Did the chakra check pass? **Yes.**
- Did the game work? **No.**

> **A clean merge proves histories combined. A check proves its own small path.
> Only running the game proves the game.** Three evidence categories — that is why
> your scroll demands all three.

**Honest footnote:** the current G-1 contributions (Elder's line + second Slime)
cannot trigger this crash — nobody edits the imports. The Tale is a true story from
a braver contribution. If a squad adds behavior of their own, the Tale becomes their
story too.

---

## RESCUE STORY (teacher-only) — "Merged onto the wrong branch"

A real incident from the same rehearsal, kept because it WILL happen on mission day:

**What happened:** an integrator meant to switch to a demo branch but the switch
failed silently — they stayed on `main` and merged a demo branch straight into it.
One bad import line went to the shared remote. Every fresh clone of `main` died with
`ImportError: cannot import name 'GroveElder'`.

**The recovery (verified, ~1 minute):**
```
git log --oneline --graph -6        # find the merge commit's short hash
git revert -m 1 <hash>              # undo exactly that merge, as a new commit
git push                            # the village heals — history never rewritten
```
- `-m 1` = "keep this side (main), undo the merged-in side." Git writes a NEW commit;
  nothing is deleted; teammates just pull and they are healed too.
- **Prevention you already built:** the Scout's law — say **"I am on main"** aloud,
  status bar checked, before every merge.
- If a student merged a feature branch onto `main` prematurely: same recipe. Revert,
  then merge properly when it's time.

---

## RESCUE CARDS (print or keep on the teacher machine)

**Card #1 — Publish/Push fails or sign-in is dead.**
`Ctrl+Shift+P` → **GitHub: Sign In**. If the machine cannot sign in today: squad
switches to Version B (offline branches) and earns full rank. Fix the machine after
class. Never debug auth in front of 30 students.

**Card #2 — Merge picker shows no `origin/feature/...` branches.**
Run `Ctrl+Shift+P` → **Git: Fetch** first, then **Git: Merge Branch…** again.
(Local branches appear without the prefix; remote ones need a fetch to be visible.)

**Card #3 — "Please clean your repository working tree before checkout."**
(SG 13's own example — now it's real.) Uncommitted edits block a branch switch.
Decide: **Commit** them if they're wanted, or Source Control → **Discard Changes** (↩)
if not. Discarding only touches *uncommitted* work — history is safe.

**Card #4 — Chakra check FAILs after a merge.**
1. Status bar: are you on `main`? (Wrong-branch merge → see the Rescue Story.)
2. Open `classes.py` / `game_config.py`: are BOTH contributions present and exactly
   as the scroll wrote them? A half-typed line is the usual criminal.
3. Still broken: Card #5.

**Card #5 — Nuclear option (nothing is lost).**
Delete the local folder, **Clone Git Repository** again, `cd rogue_edu`, chakra
check. Everything **committed and pushed** is on GitHub; the clone restores it.
Uncommitted local edits are gone — that is the one true cost of never committing.

**Card #6 — `ModuleNotFoundError: No module named 'flask'` on launch.**
The chakra check needs no environment (plain `python`); launching the game uses the
lab's **shared RogueEdu environment**, built once per computer, outside every clone:

```
~/rogue-edu-env/Scripts/python.exe app.py      # from the clone's rogue_edu folder
```

If that path is missing or broken, the sensei rebuilds it (about 2 minutes):

```
python -m venv ~/rogue-edu-env
~/rogue-edu-env/Scripts/pip install -r requirements.txt   # from any clone's root
```

Verified versions: Flask 3.1.3 / Werkzeug 3.1.9 (gunicorn and pytest ride along in
requirements.txt; the game itself needs only flask). System Python stays clean —
never `pip install flask` globally on lab machines.

---

## OPTIONAL DEMO — a merge fight, on purpose (2 min, projector)

**Reserved for SG 14. Do not run this during the live G-1 workshop.**

Prepare before class on a scratch copy of the squad template:
1. Branch `demo/a`: change `game_config.py`'s import line to add `GroveElder`.
   Branch `demo/b`: change the SAME line to add `GuardSlime`. Push both.
2. On `main`: merge `demo/a` (clean), then `demo/b` → Git asks to resolve:
   ```
   <<<<<<< HEAD
   from student_starter.classes import BraveKnight, Elder, GroveElder, Slime
   =======
   from student_starter.classes import BraveKnight, Elder, GuardSlime, Slime
   >>>>>>> origin/demo/b
   ```
3. Name the parts (ours / theirs), keep both class names, commit. Then show the
   opposite mercy: **Git: Undo Last Commit** if you want to restore the fight for the
   next class. (Full abort on a running merge: `git merge --abort`.)
   **The demo proves the scroll's honesty:** distinct files make conflicts *unlikely*,
   not impossible — same line, same fight.

---

## CLI TRANSLATION TABLE (Git Bash ↔ what VS Code clicked)

| VS Code action | Git Bash equivalent |
| --- | --- |
| Clone Git Repository | `git clone <url>` |
| Source Control **M** badge | `git status` |
| `+` Stage | `git add rogue_edu/student_starter/classes.py` |
| Commit (message box) | `git commit -m "lore: ..."` |
| Status bar → Create new branch | `git switch -c feature/elder-lore` |
| Status bar → switch branch | `git switch main` |
| Publish Branch / Push | `git push -u origin feature/elder-lore` |
| ⋯ menu → Pull | `git pull` |
| `Git: Fetch` | `git fetch origin` |
| `Git: Merge Branch…` → `origin/feature/x` | `git merge origin/feature/x` |
| History graph (GitLens/built-in) | `git log --oneline --graph -6` |
| Discard Changes (↩) | `git restore <file>` |
| Undo Last Commit | `git reset --soft HEAD~1` |

Chakra check and app launch (from the `rogue_edu` folder):
```
python check_my_class.py                       # chakra check — no env needed
~/rogue-edu-env/Scripts/python.exe app.py      # launch — shared env (card #6)
```
