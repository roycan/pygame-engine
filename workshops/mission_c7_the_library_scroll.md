# 🧪 WORKSHOP C-7 — THE LIBRARY SCROLL: EQUIP THE DATA LAB

*SG 17 — Frameworks and Libraries Integration · companion to Activity 3 (Data Visualizer)*

**Version C — 35 minutes, one mission, one class period.** (Versions A and B at the end
of this scroll.)

A Biology research team has delivered a data set: bacteria counts sampled every hour
for five hours. Their request is simple and urgent — *"We have numbers in a column. We
need to SEE the growth. Equip a Python project with a plotting tool, show us the
curve, and tell us what it means."*

**The shinobi truth of this mission:** you do not build every tool yourself. You need
to understand what a tool does, install it correctly, use it appropriately, and verify
its results.

No engine today, no repos, no game — one folder, one library, one graph, one
explanation.

---

## THE SQUAD — roles that rotate with the keyboard

| Shinobi | Mission role | Duty |
| --- | --- | --- |
| **Loremaster** | **Env-Keeper** | owns the environment: creates `.venv`, locks the interpreter, guards the `(.venv)` prefix |
| **Arena-Master** | **Tool-Bearer** | owns the tool: runs the install, verifies it with `pip show`, records Version + Location |
| **Scout** | **Evidence-Scout** | owns evidence: checks each expected result aloud, captures the three screenshots, writes the trend sentence |
| *4th member* | **Rescue Officer** | watches for trouble first: calls the 90-seconds-stuck rule, tracks which rescue card fired |

**The rotation law — read this twice.** The roles are *seats, not cells*: the
**keyboard rotates every phase**, and every shinobi personally performs the core steps
(create, install, import, run) before the mission ends.

- **One computer per shinobi:** everyone does every step on their own machine. Roles
  decide who reads each expected result aloud and whose screen the squad double-checks
  first.
- **Shared squad computer:** the keyboard passes per phase — Phase 1 Loremaster →
  Phase 2 Arena-Master → Phase 3 Scout → Phase 4 anyone who has not yet typed a
  command. The Evidence-Scout still calls every check aloud. Nobody graduates without
  having typed the install and the run.

## VILLAGE LAWS (carried + two new)

1. **Predict before you run.**
2. **One change at a time.**
3. **90 seconds stuck → raise your hand.** (The Rescue Officer fires it first.)
4. **Evidence is your rank.**
5. **NEW — Install only what the mission names.** This scroll says `matplotlib`.
   Nothing else.
6. **NEW — No shinobi alters the village gates.** No execution policies, no system
   settings, no administrator requests. If a gate is stuck, that is a *rescue-card*
   situation, not a permission situation.

---

## ⏱ THE MISSION AT A GLANCE — 35 minutes

| Min | Phase | Outcome |
| --- | --- | --- |
| 2 | 0 · Briefing | prediction written |
| 5 | 1 · Prepare the Lab | `.venv` exists; interpreter locked and verified |
| 5 | 2 · Acquire the Tool | matplotlib installed **in your `.venv`** and verified |
| 12 | 3 · Build the Visualizer | code runs; graph window; PNG saved |
| 5 | 4 · Improve the Result | one customization; PNG updated; trend sentence |
| 4 | 5 · Dependency Traffic Jam | conflict scenario reasoned on paper |
| 2 | 6 · Mission Completion | evidence checked; environment closed cleanly |

---

## PHASE 0 · BRIEFING (2 min)

Last meeting you **raced** hand-made square roots against `math.sqrt` — the library
won, and it wasn't close. Same race, bigger stadium today: nobody hand-writes a
graphics engine.

**PREDICT — write it in your Lab Record before touching a keyboard:**

> *Why would a developer use a plotting library instead of writing plotting code from
> scratch? Give one reason besides "it's shorter."*

## PHASE 1 · PREPARE THE LAB (5 min)

1. Create a new folder named **`Lab_Visualizer`**. Open it in VS Code
   (**File → Open Folder**).
2. Open the terminal (**Ctrl + `**) and create the project's private lab bench:

```powershell
py -m venv .venv
```

**Expected result:** a new `.venv` folder appears in the Explorer. If a popup appears
bottom-right offering to select the new environment — click **Yes**. If not:
**Ctrl + Shift + P → "Python: Select Interpreter" → the one with `.venv`** in its path.

3. Lock and verify — prove the terminal's Python *is* the lab bench:

```powershell
python -c "import sys; print(sys.executable)"
```

**Expected result:** a path ending in
**`Lab_Visualizer\.venv\Scripts\python.exe`**. The two things that must agree —
the **selected interpreter** (bottom status bar) and this printed path — are the same
environment. That agreement is the whole professional workflow in one line.

## PHASE 2 · ACQUIRE THE TOOL (5 min)

The kit we need is **matplotlib** — a third-party plotting library from PyPI, the
Python package index. It is established, widely used, and documented — check the name
before you ever install (that habit is the security law; "open source" still has
license rules, and matplotlib's lets you use it with credit in school work).

```powershell
python -m pip install matplotlib
```

**Expected result:** `Successfully installed matplotlib-3.x.x …` (other package names
may appear — matplotlib pulls in helpers it depends on; that is normal).

Verify it landed **in your lab bench**, not somewhere else:

```powershell
python -m pip show matplotlib
```

**Expected result:** `Name: matplotlib`, a `Version:` line, and a `Location:` line
that **contains `.venv`**. If Location does not show `.venv`, you installed into the
wrong workshop — **Rescue Card R4**.

*Why `python -m pip` and not bare `pip`?* The `python -m` form guarantees pip belongs
to **the interpreter you selected** — the tool and the lab can never disagree.

**Sort the words once, Grade-9 style:** **pip** is the *package manager* — the
delivery truck. **matplotlib** is a *third-party package* — bought from PyPI. **math**
— the one you raced last meeting — is different: a *standard-library module* that
ships with Python; no truck needed. A *framework* like **Flask** (the engine under
RogueEdu) is a bigger kit that shapes your whole program. And `import` is a Python
*statement* in your code — it opens the box; it never downloads anything.

## PHASE 3 · BUILD THE VISUALIZER (12 min)

Create **`plot_results.py`** in `Lab_Visualizer` and enter this scroll's template
(your sensei also posts it on the LMS — type it; the typing is where the reading
happens):

```python
import matplotlib.pyplot as plt

# Sample research data — ILLUSTRATIVE, not real measurements
hours = [0, 1, 2, 3, 4, 5]
bacteria_count = [100, 150, 300, 650, 1200, 2500]

plt.plot(hours, bacteria_count, marker='o', color='green')

plt.title("Bacteria Population Growth")
plt.xlabel("Time (Hours)")
plt.ylabel("Number of Bacteria")
plt.grid(True)

print("Generating graph...")
plt.savefig("bacteria_growth.png", dpi=150)   # save FIRST
plt.show()                                    # then display
```

Run it **with the `(.venv)` prefix visible** in the terminal:

```powershell
python plot_results.py
```

**Expected result:** the terminal prints `Generating graph...`, no red traceback, and
a graph window opens: green line, round points, title, both axis labels, grid.
**`bacteria_growth.png`** appears in the Explorer (960×720 pixels). Close the graph
window when the squad has read it.

**Why save before show:** `plt.show()` hands control to the window — and closing it
can clear the figure. **Save first, display second**; the PNG is your evidence either
way.

## PHASE 4 · IMPROVE THE RESULT (5 min)

One change at a time — this is still the law.

1. Change **one** feature: the marker (`'o'` → `'s'`), the color, the line style
   (`linestyle='--'`), or the title text. Say the change out loud *before* saving.
2. Re-run. **Expected result:** the window shows your change; the PNG file updates.
3. Read the curve like a researcher and write **one trend sentence** in the Lab
   Record. (Hints if the squad stalls: how many times bigger is the count each hour?
   Which hour-to-hour jump is steepest? What is the total growth over five hours?)

**Finished early?** *Extension:* change **two more** features and re-run — then
explain to the squad which version the Biology team should submit, and why.

## PHASE 5 · DEPENDENCY TRAFFIC JAM (4 min)

**Paper only — nobody installs anything.** Two libraries, one project:

> *Project BioSim uses **AgarGrower** (grows the colony data) and **GraphMaster**
> (plots it). AgarGrower's documentation demands `jsonkit` version **1.0**.
> GraphMaster's documentation demands `jsonkit` version **2.0**. Both live in the same
> project. Installing both demands breaks one library or the other — a **dependency
> conflict**, the "traffic jam."*

Discuss, then answer in the Lab Record:

1. A squadmate says: *"Easy — put it in a virtual environment."* Why does that **not**
   fix this jam? *(Think: what do virtual environments separate — and what do they
   not separate?)*
2. Name **one** thing your squad would investigate or do next. *(Reasonable moves:
   read both libraries' docs for version flexibility; check whether one library has a
   newer release; find an alternative to one library; ask the tool-bearer what pip
   reported when the conflict appeared.)*

**The model to take away:** virtual environments isolate packages **between projects**
— BioSim's shelf never touches your game's shelf. Inside **one** project, two
libraries demanding incompatible versions of the same tool is a conflict the
environment will **not** resolve for you. You resolve it: investigate, read, choose.

## PHASE 6 · MISSION COMPLETION (2 min)

Check the Lab Record: prediction ✓, interpreter path ✓, `pip show` ✓, three
screenshots ✓, trend sentence ✓, library sentence ✓, jam answer ✓.

Close the lab bench cleanly:

```powershell
deactivate
```

**Expected result:** the `(.venv)` prefix disappears. The thousands-of-lines toolbox
stays on the shelf in `.venv` — ready for next time.

**Rank earned:** ______ **Sensei stamp:** ______

---

## 🩹 RESCUE CARDS

**R1 · `py` is not recognized** (and `python` isn't either). Python itself is missing
or not registered — a machine problem, **not a command problem**. No command you type
will fix it. Raise your hand; your sensei decides (another machine, or the IT ticket).
*Sensei note: this is exactly the case a `pip --version` check cannot cure.*

**R2 · `py -m pip --version` fails but `py` works.** Rare. Try
`py -m ensurepip --upgrade`, then re-check. Still failing → sensei.

**R3 · Wrong interpreter selected.** Symptom: the status bar shows a path with no
`.venv`, or the verify command prints a path outside `Lab_Visualizer`. Fix:
**Ctrl + Shift + P → Python: Select Interpreter → the `.venv` one**; then **open a
NEW terminal** (the old one keeps its old environment) and re-verify.

**R4 · "Successfully installed" — but it went somewhere else.** You skipped the
prefix check: the `(.venv)` was missing when you installed. Fix: R3 first (select +
new terminal), confirm the `(.venv)` prefix, then run the install command again. Pip
will say *"Requirement already satisfied"* if the right copy is already there.

**R5 · Activation failed** (PowerShell script errors, or the prefix never appears).
Skip activating entirely — call the environment's Python **by its full path**:

```powershell
.\.venv\Scripts\python.exe -m pip install matplotlib
.\.venv\Scripts\python.exe plot_results.py
```

Same lab bench, same result, zero settings touched. *(Never edit execution policies.)*

**R6 · `ModuleNotFoundError: No module named 'matplotlib'`.** The running Python is
not the one that installed it. Check in order: (1) is `(.venv)` visible on THIS
terminal line? (2) re-run the interpreter verify command — does the path end in
`.venv\Scripts\python.exe`? (3) `python -m pip show matplotlib` — is `Location:` in
`.venv`? Whichever check fails points at the fix (R3 or R4).

**R7 · No graph window appears.** Check the terminal first: is there a traceback?
Fix that line. No traceback? Check the taskbar — the window may be behind VS Code.
Still nothing: confirm the last two lines of the script are `savefig` then `show`,
and that you ran the file (not just saved it).

**R8 · Download is slow or failing.** Do not retry-loop past one attempt. Tell your
sensei — there is a prepared contingency. Your rank for this mission will be marked
**assisted**, honestly, in the Lab Record.

---

## VERSION B — 20 MINUTES (accelerated)

**Prerequisites (teacher-prepared, non-negotiable):** every machine already has
`Lab_Visualizer` **with `.venv` created**; matplotlib **already installed** in it; the
template `plot_results.py` posted on the LMS.
**Scope (20 min):** select + verify interpreter (4) → confirm install with
`pip show` (3) → type/run the visualizer, PNG saved (8) → one customization + trend
sentence (5). Traffic jam: teacher-led, 60 seconds, from the scroll's scenario.
**Honest boundary:** Version B demonstrates *use* of an environment someone else
built. It does **not** demonstrate creating one, and the install competency is shown
only as verification, not installation.

## VERSION A — 10 MINUTES (fallback)

**Prerequisites:** same prepared machines as Version B, **plus** the template file
already open in VS Code.
**Scope (10 min):** verify the interpreter path (2) → run the code, graph + PNG (4) →
one customization, re-run, one trend sentence (4).
**Honest boundary:** Version A is a **fallback experience**. It generates and
customizes a graph, and nothing more — it does **not** independently demonstrate the
installation competency (create environment, install package, verify placement). Treat
A as "the squad has seen the workflow," not as evidence of mastery.

---

*Sample data disclosure: the bacteria numbers are illustrative teaching data, not
measurements from a real experiment. The research team is fictional; the workflow is
not.*
