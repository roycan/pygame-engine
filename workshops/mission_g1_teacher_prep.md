# 🌀 MISSION G-1 — SENSEI PREPARATION CHECKLIST

Mission: `mission_g1_three_shinobi_one_game.md` · Fallbacks: `mission_g1_fallbacks_ab.md`
Rescue & Tale: `mission_g1_teachers_tale_rescue.md` · SG 13 map: `mission_g1_sg13_alignment.md`

**Nothing in the 30-minute mission may include:** account creation, authentication,
git identity setup, repository creation, or first-time cloning problems. All of it
lives here. SG 13 §1.1 (setup & configure) is the natural home for the setup session.

---

## A. One-time setup (estimate: half a day of prep + one lab session)

### A1. The classroom template repository
- Base it on the canonical RogueEdu `main`, with **exactly two files excluded:
  `tests/test_ci.py` and `tests/test_worksheet.py`** — and **only in the template**.
  Both files stay untouched in the canonical repository.
  - `test_ci.py` guards GitHub Actions workflow files that no longer exist on
    `main` (removed Oct 23) — it fails by design in the canonical repo.
  - `test_worksheet.py` reads `plans/workshop_01_teacher_answer_key.md`, and
    `plans/` is gitignored — so pytest is never green in ANY fresh clone.
- **Student verification does not use pytest, ever.** Students verify with
  `check_my_class.py` (the chakra check) and actual gameplay. pytest remains a
  teacher-side gate only, and only if you keep the rest of the suite in the template
  (the remaining suite passes: verified 176 passed on a merged fresh clone).
- Fix one stale line while building the template if you wish: the two excluded test
  files are the only known reds.

### A2. Squad repositories (~100 students → ~33 teams of 3)
- Create **one team repository per squad** (not one per student). From the template:
  GitHub → "Use this template" → Generate, once per squad. Squads of four → the
  fourth shinobi is Co-Scout / Field Tester (scroll, Phase 5).
- Visibility: private is enough; the squad members need write access (Settings →
  Collaborators, or an org team per section). Write access is required — the Scout
  pushes `main`.
- Post the ~33 URLs on the **LMS** (one message per squad). Students retrieve their
  link there in Phase 0 — nothing is printed.

### A3. Authentication (per machine — this is the big one)
- Every lab machine signs in to GitHub **once** through VS Code
  (`Ctrl+Shift+P` → **GitHub: Sign In** → browser flow) during a setup session.
- Sign-in survives on shared lab machines; if machines are wiped between sessions,
  re-run sign-in during the SG 13 §1.1 session, not on mission day.
- Machines that cannot sign in on mission day → that squad runs **Version B**
  (offline, local branches) and gets full rank. Record which squads.

### A3b. The shared RogueEdu environment (per computer, built once, outside clones)
- Facts first: `app.py` needs **flask** (everything else the game imports is stdlib);
  `check_my_class.py` is stdlib-only and runs on plain `python`. A clone ships no
  venv (gitignored), so the launch interpreter must come from outside the clone.
- Build once per lab computer, in the setup session (Git Bash):
  ```
  python -m venv ~/rogue-edu-env
  ~/rogue-edu-env/Scripts/pip install -r requirements.txt   # from any clone's root
  ```
  `~` is the computer's home folder on every machine — the fixed path is what makes
  the scroll's Phase 5 launch command identical on all ~99 machines.
- **Verify after building** (60 seconds, one fresh clone): `cd rogue_edu` →
  `python check_my_class.py` (expect `Summary: 3 passed`) → launch
  `~/rogue-edu-env/Scripts/python.exe app.py` → open http://127.0.0.1:5000 (expect
  the RogueEdu board) → `Ctrl+C`. Verified in rehearsal: Flask 3.1.3 / Werkzeug 3.1.9
  / gunicorn 26.2.0 / pytest 9.2.0 — gunicorn and pytest ride along in
  requirements.txt; the game itself needs only flask.
- **Do NOT install flask into system Python.** The shared env is disposable:
  delete `~/rogue-edu-env` and rebuild. Broken launch on mission day → rescue card #6.

### A4. Git identity (per machine, once)
```
git config --global user.name "Squad 07 Loremaster"
git config --global user.email "you@example.com"
```
- On shared machines a per-machine name is fine; SG 13 §1.1 covers why identity exists.

### A5. Baseline verification (the sensei, before mission day — students skip the demo)
- Clone one squad repo exactly as a shinobi would. Run:
  ```
  cd rogue_edu
  python check_my_class.py                # chakra check — no venv needed
  ../venv/Scripts/python.exe app.py       # needs flask (A3b) — open http://127.0.0.1:5000, then Ctrl+C
  ```
- Expect `Summary: 3 passed, 0 warnings, 0 failures.` and a playable board.
- This rehearsal IS the students' removed Phase-1 gameplay demo — the trust that lets
  Phase 1 be a chakra check only.

### A6. Rehearse the full mission once (optional but recommended)
- Two or three machines, run Version C start to finish with your own test repo.
  The verified sequence and every expected output string in the scroll came from
  exactly such a rehearsal (three clones, two feature branches, Scout merge, pull
  confirm on all machines).

---

## B. Mission-day checklist (10 minutes before class)

- [ ] Projector shows the squad-URL handout and the scroll.
- [ ] Printed scrolls (1 per squad) + role cards visible on the screen.
- [ ] Every machine: VS Code opens, GitHub avatar shows signed-in.
- [ ] Spot-check two random squad repos: last commit is your template baseline.
- [ ] Timer set for 30 minutes (phases: 1 / 5 / 6 / 5 / 6 / 4 / 3).
- [ ] Rescue guide open on the teacher machine (`mission_g1_teachers_tale_rescue.md`).
- [ ] Spot-check the shared environment on two machines:
      `~/rogue-edu-env/Scripts/python.exe --version` prints without error.
- [ ] No conflict demo today — reserved for SG 14 (script stays in the rescue guide).

---

## C. In-flight classroom management

- **The law that saves you:** every phase boundary, students' keyboards already
  rotate; the Scout announces "I am on main" before Phase 4.
- **Watch for:** squads editing off-territory (Loremaster touching `game_config.py`
  = future conflict — Law 2, one change at a time).
- **Fallen-behind squads:** skip the optional Tale, drop to Version B's local merge,
  or run Version A. Full rank still possible for A/B squads; note it.
- **Fast squads:** give them the Co-Scout duty, or the exit question 5 (fetch vs
  pull) as a teach-back to the class.

---

## D. Recovery (details in the rescue guide)

| Situation | First move |
| --- | --- |
| Machine won't sign in | Squad falls back to Version B; fix auth after class |
| Merge picker shows no `origin/...` branches | `Git: Fetch` first (rescue card #2) |
| "Please clean your repository working tree…" | Commit or Discard (↩) — rescue card #3 |
| Chakra check FAIL after a merge | Check the branch name first — rescue card #4 |
| Squad lost / scared | Re-clone from GitHub — committed work is never lost (card #5) |
