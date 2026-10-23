# 🌀 RogueEdu Onboarding — Mission Scroll (Genin Edition · Git Bash)

  

**Name:** ______________ **Team:** ______ **Rank earned:** ______

  

**Roles (rotate every mission):**

**Operator** — the only hands on the keyboard ·

**Navigator** — reads the scroll aloud, keeps the steps ·

**Scout** — watches the result and records the evidence ✍️

  

**Village laws:**

1. **Predict before you run.** A wrong prediction is information, not failure.

2. **One change at a time.** Then run and observe.

3. After **90 seconds** of being stuck → raise your hand. That's the rule, not defeat.

4. Write your evidence in the scroll. Evidence is your rank.

  

**Shell law:** every command in this scroll is **Git Bash**. Your prompt must show

`MINGW64 … $` — that's how you know you're in the right shell.

  

**Today's lesson is 40 minutes.** Missions D-1 → D-3 are setup. C-1 and C-2 are the

actual shinobi work. Stay with your team; help other teams *after* your rank is earned.

  
## As an alternative to Mission D-1, you can do Mission 0: 

https://roycan.github.io/rogueedu-mission-zero/


---

  

## 🥷 MISSION D-1 — Clone the Repository (rank: D)

  

**Objective:** copy the RogueEdu village scroll from GitHub to your PC.

  Git link: https://github.com/roycan/pygame-engine.git

**Steps (Operator types, Navigator reads):**



2. Open Git Bash
   
3. Type these, one line at a time, Enter after each:

```bash

mkdir -p ~/RogueEdu

cd ~/RogueEdu

git clone https://github.com/roycan/pygame-engine.git

cd pygame-engine

code .

```


1. Open **VS Code**. If a "Trust the authors" popup appears → click **Yes, I trust**.
   If it says "restricted mode" at the top, click on "manage", then click on "trust"
 
2. On **your own PC at home**, Git may open a browser window once — sign in with any

   GitHub account, come back to VS Code. In class this is usually skipped.

  

**Expected result:** a line like `Resolving deltas: 100% ...` and then a clean prompt.

  3. Open Terminal → **New Terminal** (`Ctrl + backtick`). 
     type `bash`


**✅ Completion check (Scout):** type `ls` — you see 
```
DEPLOYING.md  Procfile   TEACHER_GUIDE.md   package.json  pytest.ini        rogue_edu  tools
Makefile      README.md  package-lock.json  plans         requirements.txt  tests      workshops
```


**If it differs:** stop after 90 seconds → raise hand → teacher decides (help or

pre-cloned USB). *Do not delete folders to "fix" it.*

  

---

  

## 🥷 MISSION D-2 — Open the Mission Scroll (rank: D)

  

**Objective:** read the village's own README and locate the two launch commands.

  

**Steps:**

1. In VS Code's Explorer (left side), click **README.md** — it opens as a preview.

2. Find the section **"Quick start"**. The Scroll speaks Linux — and so do you now:

   Git Bash reads `venv/bin/...` lines almost as-is, but on Windows the interpreter

   lives in **`venv/Scripts/python.exe`**. Your translations:


| Scroll says                                     | You type (Git Bash)                                          |
| ----------------------------------------------- | ------------------------------------------------------------ |
| `python3 -m venv venv`                          | `python -m venv venv`                                        |
| `venv/bin/pip install -r requirements.txt`      | `venv/Scripts/python.exe -m pip install -r requirements.txt` |
| `python check_my_class.py` (inside `rogue_edu`) | `venv/Scripts/python.exe rogue_edu/check_my_class.py`        |
| `python app.py` (inside `rogue_edu`)            | `cd rogue_edu` then `../venv/Scripts/python.exe app.py`      |


3. Skip `npm install …` and `make test` — those are for the village's builders, not

   today's mission.

  

**Expected result:** Navigator can point at all four commands in the README.

  

**✅ Completion check (Scout):** the table above is annotated ✓ next to each row.

  

**If it differs:** cannot find README.md? Re-check you are inside `pygame-engine` —

your prompt's path should end in `pygame-engine`.

  

---

  

## 🥷 MISSION D-3 — Activate the Village (rank: D)

  

**Objective:** build your jutsu workspace (virtual environment), pass the chakra check,

and wake the game.

  

**Steps (repo root `/c/RogueEdu/pygame-engine`):**

1. `python -m venv venv` — creates your training ground (≈10 s; appears in Explorer).

2. `venv/Scripts/python.exe -m pip install -r requirements.txt` — chakra scrolls

   install (watch for `Successfully installed Flask …`).

3. `venv/Scripts/python.exe rogue_edu/check_my_class.py` — **the chakra check.**

4. `cd rogue_edu` then `../venv/Scripts/python.exe app.py` — **wake the village.**

5. Open Browser and go to→ <http://127.0.0.1:5000> (Edge is fine). Don't close the terminal!

  

**Expected result:**

```

Checking student_starter.classes ...

[PASS] Hero 'BraveKnight' ...

[PASS] Villain 'Slime' ...

[PASS] NPC 'Elder' ...

Summary: 3 passed, 0 warnings, 0 failures.

Beautiful. Run the game: python app.py

```

then the server says `Running on http://127.0.0.1:5000` — and the board appears:

10×10 grid, hero 🛡️, a slime 🟢, an elder 🧙, walls 🧱.

  

**✅ Completion check (Scout):** press **W A S D** — the hero moves. Press **Space** —

nothing moves (a legal wait). Bump into the Elder 🧙 — dialogue opens; any key closes it.

  

**If it differs:** check the terminal, not the browser — the error scrolls live there.

The rescue cards are with your teacher. 90-second rule applies.

  

---

  

## 🥷 MISSION C-1 — Scout the Training Ground (rank: C)

  

**Objective:** observe before you touch code. Predict like a shinobi.

  

**Predict first (Scout writes the team's answers):**

1. What happens if you walk **into a wall**? ______

2. If you step **onto the slime's tile**, what do you predict happens? ______

3. Who do you predict moves **after** you move — and why? ______

  

**Now test (2 minutes):**

- Walk into a wall 🧱 → read the log line under the board.

- Fight the slime: walk into it until it falls (it hits back!).

- The log narrates every event — this is the game telling you what the engine did.

  

**✅ Completion check:** Scout writes one sentence: *"The engine allowed ____, blocked

____, and announced it in the log."*

  

**If it differs:** the board frozen? Check the terminal for a traceback; raise hand

after 90 seconds.

  

---

  

## 🥷 MISSION C-2 — First Controlled Experiment (rank: C)

  

**Objective:** make one prescribed change, predict, observe, revert. Your first jutsu.

  

**The edit (Operator, exactly this):**

1. In VS Code open `rogue_edu` → `student_starter` → **`classes.py`**.

2. Go to **line 38** (click line 38 in the left gutter). It reads:

```python

   super().__init__("Sir Ada", x, y, hp=25, attack_power=6)

```

3. Change **only** `6` → `60`. Save (`Ctrl+S`).

  

**PREDICT (whole team, before running):** your knight now attacks with 60.

What will the game *allow*? What will the engine *say*? ______

  

**Run it:**

4. Terminal: `Ctrl+C`, then **↑ Enter** — Bash history re-runs

   `../venv/Scripts/python.exe app.py`.

5. Refresh the browser. Click the **⚙ Developer Inspector** (bottom of the page) and

   find `attack_power`.

6. Read the terminal — one new line appeared.

  

**Expected result:** the inspector shows **attack_power: 40** (not 60), and the

terminal announces:

```

[SETUP WARNING] Sir Ada: attack_power=60 is out of range [0, 40]; clamped to 40.

```

  

**Explain (write it):** *You* decided 60. The **engine** acted: it clamped to 40 and

announced it. The boundary already existed — today you touched it once.

  

**✅ Completion check:** Scout records the warning line verbatim in the scroll.

  

**Revert (do it now):** change `60` back to `6`, save, `Ctrl+C`, **↑ Enter**, refresh →

inspector shows 6. **Mission complete.**

  

**If it differs:** `IndentationError`? Your `60` replaced more than the `6`, or

indentation moved — undo (`Ctrl+Z`) and redo only the digit swap.

  

---

  

## 🎖 Rank earned

  

| Mission                 | Done | Evidence written |
| ----------------------- | ---- | ---------------- |
| D-1 Clone               | ☐    | ☐                |
| D-2 Read the scroll     | ☐    | ☐                |
| D-3 Activate            | ☐    | ☐                |
| C-1 Scout               | ☐    | ☐                |
| C-2 Experiment + revert | ☐    | ☐                |

  

**Next mission (coming soon):** you'll write your *own* monster class and watch it

appear on the board. Everything today was the door to that.

  

> *"You decide. The engine acts."* — the village's one law.
