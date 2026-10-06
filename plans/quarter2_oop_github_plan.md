# Quarter 2 Plan — Four OOP Pillars + GitHub Workflow, all through RogueEdu

_A teacher-facing curriculum design. Builds on [`../workshops/workshop_01_meet_the_engine.md`](../workshops/workshop_01_meet_the_engine.md) (the on-ramp) and [`../TEACHER_GUIDE.md`](../TEACHER_GUIDE.md)._

**Format:** 6 weeks × 2 meetings × 45 minutes. Weeks 1–4 = Abstraction, Encapsulation, Inheritance, Polymorphism (one pillar per week). Weeks 5–6 = the GitHub workflow (fork → branch → edit → PR → review → merge → auto-deploy on Render).

---

## 0) The plan in one page

### Recommendation 1 — Reorder the pillars: Abstraction → Encapsulation → Inheritance → Polymorphism

The textbook list order (A, E, **P**, I) puts Polymorphism before Inheritance. Don't teach it that way here. Polymorphism is the **payoff** of inheritance: "swap one subclass for another and nothing else changes" is only impressive once students know what a subclass *is*. In this engine the natural difficulty curve is:

1. **Abstraction** — *use* the small interface the engine gives you (Week 1, mostly reading/playing/writing one method).
2. **Encapsulation** — *respect and explain* the guards that protect the game state (Week 2, mostly predicting and reading log output).
3. **Inheritance** — *extend* a family by writing subclasses (Week 3, real writing begins).
4. **Polymorphism** — *interchange* siblings and watch one line of engine code drive them all (Week 4, the synthesis + Boss Arena).

### Recommendation 2 — Every pillar has a precise, visible home in this codebase

You never have to teach from an artificial example. The anchor code:

| Pillar | Anchor(s) students can see and touch |
| --- | --- |
| Abstraction | [`SafeGameView`](../rogue_edu/engine/view.py) — exactly 4 questions a monster may ask; [`Action`](../rogue_edu/engine/actions.py) dataclasses — intents, not mechanics; abstract [`symbol()`](../rogue_edu/engine/base_classes.py) contract on `GameObject` |
| Encapsulation | [`_clamp_stat()`](../rogue_edu/engine/base_classes.py) + loud `warnings`; [`take_damage()`](../rogue_edu/engine/base_classes.py); `frozen=True` on every Action; the snapshot copy in [`SafeGameView.__init__()`](../rogue_edu/engine/view.py); engine-side [`_sanitized_damage()`](../rogue_edu/engine/core.py) and [`_validated_action()`](../rogue_edu/engine/core.py) |
| Inheritance | The family tree `GameObject → Character → Hero / Villain` and `GameObject → NPC / Wall`; [`super().__init__(...)`](../rogue_edu/student_starter/classes.py) in every starter class; abstract [`act()`](../rogue_edu/engine/base_classes.py) as the "must write" contract |
| Polymorphism | [`_villain_phase()`](../rogue_edu/engine/core.py) — one `for` loop, one `villain.act(view)` call, every monster brain; the three different AIs in [`../rogue_edu/demos/demo_dungeon/entities.py`](../rogue_edu/demos/demo_dungeon/entities.py); the Swap Test in [`game_config.py`](../rogue_edu/student_starter/game_config.py) |

### Recommendation 3 — GitHub goes in Weeks 5–6, not first

A PR should contain something worth merging. After 4 pillar weeks every student owns real monsters and arenas — those become their first branches and PRs. (Do run a 5-minute "watch me fork and PR" teaser during Week 1, Meeting 1, so Week 5 is not cold.)

### Recommendation 4 — Before Week 5, kill merge conflicts structurally

If every student PRs into the same [`classes.py`](../rogue_edu/student_starter/classes.py), conflicts are guaranteed and will eat meeting time. Restructure so **each pair owns a file**: see §7.

### Recommendation 5 — The motivational engine is PR → merge → live game

The class Render deployment redeploys on merge. A student's monster appearing on the *class* URL two minutes after their PR merges is the strongest incentive this platform can produce — schedule it into Meeting 6.1 deliberately.

---

## 1) Week 1 — ABSTRACTION: "Use the window, don't rebuild the house"

**The big idea (say it this way):** a real program has thousands of moving parts. Abstraction means someone hands you a **small set of promises** — *what* you may ask and *what* you may request — so you can build on top of it without holding the whole machine in your head. You already use abstractions daily: `print()` shows text; you never typed the screen-driver code.

**Anchor code:** [`SafeGameView`](../rogue_edu/engine/view.py) and its four methods `get_hero_position`, `distance_to_hero`, `get_direction_toward_hero`, `is_tile_passable`; [`MoveAction`](../rogue_edu/engine/actions.py) / [`AttackAction`](../rogue_edu/engine/actions.py) / [`WaitAction`](../rogue_edu/engine/actions.py); the abstract [`symbol()`](../rogue_edu/engine/base_classes.py).

### Meeting 1.1 (45 min) — Play it, then interrogate it

| Time | Segment |
| --- | --- |
| 0–5 | **Teaser (GitHub seed):** teacher forks the class repo live, edits one emoji, opens a PR, merges it, refreshes the class URL. Say: "Weeks 5–6 you learn to do this. For now, watch what it buys you." |
| 5–15 | **Play** the starter game (WASD/space). Students jot: one thing the game *stopped* them from doing; one thing a monster did that seemed *smart*; one thing they wish existed. |
| 15–25 | **ME:** open [`Slime.act()`](../rogue_edu/student_starter/classes.py) on the projector. Cover the engine files with your hand: "The slime's entire brain is these 5 lines. What did it need to *know* to make those decisions?" Harvest: where the hero is, how far, what's passable. Reveal [`SafeGameView`](../rogue_edu/engine/view.py): exactly these four questions exist — the window, not the house. |
| 25–38 | **US — grid-paper trace:** students draw the 10×10 board, place hero and slime, and hand-compute `distance_to_hero` (Manhattan: `|x1−x2| + |y1−y2|`) and `get_direction_toward_hero` for 3 positions. Now the abstraction is a *checked promise*, not magic: predict, then run and confirm via the event log. |
| 38–45 | **Exit ticket:** "Your monster may ask the view only 4 questions. Name two, and one thing it may *not* do through the view." |

### Meeting 1.2 (45 min) — Write with only the window open

| Time | Segment |
| --- | --- |
| 0–10 | **IDEA first:** why does [`act()`](../rogue_edu/engine/base_classes.py) *return* an Action instead of moving? The restaurant order slip: the cook (engine) owns the kitchen. [`Action`](../rogue_edu/engine/actions.py) dataclasses are the slips. |
| 10–30 | **US/YOU:** every student rewrites their villain's `act()` using *only* view methods + returned Actions (chase-and-bite is fine; a "wait until close, then pounce" variant uses `distance_to_hero` with a bigger threshold). Loop: [`check_my_class.py`](../rogue_edu/check_my_class.py) → restart → refresh. |
| 30–38 | **The deliberate typo lab:** instruct everyone to call `view.fly_to_hero(self)` once. Read the [`__getattr__`](../rogue_edu/engine/view.py) error aloud — *"Did you mean …?"*. Point: a good abstraction catches your mistakes and teaches you its real interface. |
| 38–45 | **Reflect (3 questions):** What does `distance_to_hero` promise? Why is 4 questions enough for any monster? What would break if the view also *let* you move the hero? |

**Misconception to hunt:** "abstraction = the code is hidden somewhere, it's magic." Counter: abstraction = a *published promise* (docstring + signature) you may rely on; the promise is testable — you traced `distance_to_hero` by hand.

---

## 2) Week 2 — ENCAPSULATION: "Every object guards its own rules"

**The big idea:** bundling data with the code that protects it, so the object's rules hold *no matter who uses it* — including you, including future-you, including a classmate's sloppy villain. In this engine, `hp` can never be −50 or 999, *ever*. That guarantee didn't happen by hoping; it was built.

**Anchor code:** [`_clamp_stat()`](../rogue_edu/engine/base_classes.py) and the `warnings` list; [`take_damage()`](../rogue_edu/engine/base_classes.py) (negative damage applies 0; killing blow capped); `@dataclass(frozen=True)` on [`Action`](../rogue_edu/engine/actions.py); [`SafeGameView.__init__()`](../rogue_edu/engine/view.py) storing **copies** (`frozenset`s, no engine reference); the underscore convention (`_width`, `_hero_position`, `_clamp_stat`); engine side: [`_sanitized_damage()`](../rogue_edu/engine/core.py), [`_validated_action()`](../rogue_edu/engine/core.py).

### Meeting 2.1 (45 min) — The Heist Lab (predict → attempt → document)

Students play **attackers**. For each attempt below they must first write a *prediction* ("the game will crash / the cheat will work / nothing"), then run it, then record what actually happened:

| # | Cheat attempt | What actually happens (for you) |
| --- | --- | --- |
| 1 | `hp=999` in `super().__init__` | Clamped to 200 + a loud `[SETUP WARNING]` in the log ([`_clamp_stat`](../rogue_edu/engine/base_classes.py)) |
| 2 | `attack_power=-5` | Clamped to 0, loudly |
| 3 | Override `calculate_attack_damage()` to `return 9999` | Engine reads it but [`_sanitized_damage()`](../rogue_edu/engine/core.py) caps at 40 and logs `CHEAT GUARD` |
| 4 | Return `MoveAction(1, 1)` (diagonal) | [`_validated_action()`](../rogue_edu/engine/core.py) converts to a wait + WARNING |
| 5 | Return `"hello"` from `act()` | "not an Action … treated as a wait" |
| 6 | `AttackAction(dx, dy, damage=99)` | Python raises `TypeError` — the field does not exist; even the *language* backs the rule |

Debrief: the engine never *trusts* student code, and it never *fails silently*. Connect both halves: encapsulation = guarded state + loud reporting.

### Meeting 2.2 (45 min) — Why we build the fence ourselves

| Time | Segment |
| --- | --- |
| 0–10 | **Trace** [`take_damage()`](../rogue_edu/engine/base_classes.py) on the board: hero 25 hp, two 30-damage hits — what does it return *each* time and why does `applied` matter? |
| 10–20 | **Trace** the warning pipeline: `_clamp_stat` appends → `add_villain` → [`_drain_warnings()`](../rogue_edu/engine/core.py) moves it into the setup log. Nothing is ever silently fixed. |
| 20–32 | **YOU:** write a `GuardedGolem(Villain)` whose stats break **all three** guardrails on purpose (hp 999, atk −5, damage-override 9999). Done when the log shows all three warnings/`CHEAT GUARD` lines and the golem still plays legally. |
| 32–45 | **Reflect:** Which guard surprised you most? Why does the *view* store copies instead of the real board? Where else in real life do you meet "loud clamping" (exam score capped at 100; speed limiters)? |

**Misconception to hunt:** "encapsulation = putting underscores before names because the teacher said so." Counter: the underscore is just the *sign* on the fence; the fence is the code that enforces the rule. Ask: "if we deleted `_clamp_stat`, would renaming things to `hp_` protect the game?" (No — naming is a convention; behavior is the guarantee.)

---

## 3) Week 3 — INHERITANCE: "A new class gets a family's code for free"

**The big idea:** when many things share structure, write it **once** on a parent and let children specialize. Students have been *using* inheritance since meeting one (`class Slime(Villain)`); this week they learn to *read* the family tree and reason about what's inherited vs. overridden vs. must-be-written.

**Anchor code:** the tree `GameObject → Character → {Hero, Villain}` and `GameObject → {NPC, Wall}` (all in [`base_classes.py`](../rogue_edu/engine/base_classes.py)); [`super().__init__(...)`](../rogue_edu/student_starter/classes.py); what a `Villain` child gets free: stat clamping, [`is_alive()`](../rogue_edu/engine/base_classes.py), [`take_damage()`](../rogue_edu/engine/base_classes.py); what it must write: [`act()`](../rogue_edu/engine/base_classes.py) (abstract — the contract).

### Meeting 3.1 (45 min) — Read the family tree, then grow it

| Time | Segment |
| --- | --- |
| 0–8 | **ME:** draw the 6-class tree on the board from [`base_classes.py`](../rogue_edu/engine/base_classes.py). Annotate each level: `GameObject` = "has a name and a tile"; `Character` = "has hp/atk and the guards"; `Villain` = "takes turns — must write `act()`". |
| 8–20 | **US — family worksheet:** for `Slime`, students sort a list of members into three columns — *inherited free* (`is_alive`, `take_damage`, clamping), *overridden* (`symbol`, `__init__`), *contract to write* (`act`). |
| 20–35 | **YOU — the Goblin dynasty:** write `Goblin(Villain)` (chase-and-bite, green), then `GoblinKing(Goblin)` that overrides **only** `__init__` stats and `symbol()`, and inherits `act()` untouched. Register both in `game_config.py`. The aha: the King chases with **zero AI code written**. |
| 35–45 | **Crash lab:** delete the `super().__init__` line from `GoblinKing` → run → read the error together (`AttributeError: 'GoblinKing' object has no attribute 'name'`). Now `super()` is not ritual — it is *how the parent's setup gets done*. Fix it, doctor, play. |

### Meeting 3.2 (45 min) — Design with is-a / has-a

| Time | Segment |
| --- | --- |
| 0–10 | **Warm paradox:** "Should `GameEngine` *inherit from* `Villain` so it can contain villains?" No — a game **has** villains; a Slime **is** a villain. Inheritance for is-a; composition (the lists in [`GameEngine.__init__`](../rogue_edu/engine/core.py)) for has-a. Point at [`game_config.py`](../rogue_edu/student_starter/game_config.py) as the has-a file and [`classes.py`](../rogue_edu/student_starter/classes.py) as the is-a file. |
| 10–30 | **YOU — spec sheet sprint:** each student designs a 3-monster family on paper first (base + 2 children that override *different* things: one changes stats, one changes `symbol`, one changes `act`). Then implement. The doctor must pass. |
| 30–45 | **Playtest + exit ticket:** swap computers; the peer must answer "which behavior did this class inherit vs. write?" Exit: "GoblinKing chases but has no `act()`. Explain how, in one sentence." |

**Misconceptions to hunt:** (1) inheritance = copy-paste ("it copies the code in") — counter: the child *is* the parent type; there's one copy, shared. (2) Forgetting `super().__init__` "because it works without it" — the crash lab is the antidote. (3) Believing `act()` may be skipped for a Villain — [`Villain.act`](../rogue_edu/engine/base_classes.py) is `@abstractmethod`; the checker fails them early.

---

## 4) Week 4 — POLYMORPHISM: "One message, many brains"

**The big idea:** code written against a **type** works for **every** subtype. The engine has exactly one loop and calls `villain.act(view)` on each villain — it neither knows nor cares whether that object is a Slime, a Coward, or a GoblinKing. Many forms, one call site. This is the payoff week that ties all three previous pillars together.

**Anchor code:** [`_villain_phase()`](../rogue_edu/engine/core.py) — the `for` loop and the single [`villain.act(view)`](../rogue_edu/engine/core.py) call; the isinstance dispatch on returned Actions (any `Action` subtype is handled uniformly); [`board_state()`](../rogue_edu/engine/core.py) calling `symbol()` on every entity; the three distinct AIs in [`demo_dungeon/entities.py`](../rogue_edu/demos/demo_dungeon/entities.py).

### Meeting 4.1 (45 min) — Predict-then-run on the demo dungeon

| Time | Segment |
| --- | --- |
| 0–10 | **ME:** project [`_villain_phase()`](../rogue_edu/engine/core.py). Highlight that it references `villain` — never `Slime`, never `Coward`. One line of code, every monster brain. |
| 10–25 | **US:** run the demo dungeon (`GAME_CONFIG_MODULE=demos.demo_dungeon.game_config python app.py`). Students predict each monster's next move for 3 board positions *from the code alone*, then verify by playing. [`Chaser`](../rogue_edu/demos/demo_dungeon/entities.py), [`Coward`](../rogue_edu/demos/demo_dungeon/entities.py), [`Patroller`](../rogue_edu/demos/demo_dungeon/entities.py) — same loop, three behaviors. |
| 25–40 | **The Swap Test (the point of the week):** in [`game_config.py`](../rogue_edu/student_starter/game_config.py), change one name — `Slime(x=7, y=7)` → `GoblinKing(x=7, y=7)` — and *nothing else*. Predict what changes, run, confirm: the engine loop didn't change, the config changed one word. That is polymorphism being *useful*: the engine was written once, forever ago, and still runs monsters that did not exist when it was written. |
| 40–45 | **Exit ticket:** "The engine's loop is 8 weeks old and your monster is brand new. Why does your monster work with it without the engine changing?" |

### Meeting 4.2 (45 min) — Boss Arena + Monster Zoo

| Time | Segment |
| --- | --- |
| 0–25 | **YOU — Boss Arena:** each student/pair composes an arena in `game_config.py`: their hero, ≥3 villains drawn from ≥2 *different* classes in their own monster family, walls, and a chosen win condition. Doctor must pass; they must beat (or lose to) their own arena and write down *why* the outcome happened. |
| 25–40 | **Monster Zoo (class ritual):** pairs tour 2 other arenas. For each, they must identify one visible instance of each pillar: something *abstracted* (a view call), something *encapsulated* (a guard that fired in the log), something *inherited* (behavior with no local code), something *polymorphic* (two classes, one loop). |
| 40–45 | **Week synthesis:** the four pillars in one breath — *the view abstracts the world; the guards encapsulate the rules; my monster inherits its family's powers; the engine's one loop is polymorphic over all of us.* This sentence is the unit's summary assessment anchor. |

---

## 5) Weeks 5–6 — GITHUB: "Your code joins a real project"

**Tooling decisions (keep it to the minimum viable git):**
- **Tool:** VS Code's Source Control panel + the terminal for `status/add/commit/push`. Teach **five** commands total; explicitly do *not* teach rebase, stash, cherry-pick, or upstream remotes (the GitHub **Sync fork** button replaces that).
- **Auth:** Git for Windows with Git Credential Manager — the browser popup handles tokens. HTTPS, never SSH.
- **Model the loop as a story:** *save slot* → *parallel universe (branch)* → *show your work (commit message)* → *ask to join (PR)* → *friend checks it (review)* → *it becomes canon (merge)* → *the world updates (Render redeploys)*.

### Meeting 5.1 (45 min) — Why + fork + tour

| Time | Segment |
| --- | --- |
| 0–10 | **WHY version control:** the `final_v2_REALLY_final.py` horror; Google Docs history; game save slots. Two promises git makes: *nothing is ever lost*, and *two people can work at once*. |
| 10–25 | Create GitHub accounts (school-policy check first), **fork** the teacher's class repo. The fork is *your copy of the project where you have write permission*. |
| 25–45 | **Tour the GitHub UI** on the fork: Code / Commits (history = save slots) / Branches / Pull requests / Issues. Homework-free; end by everyone bookmarking their fork URL. |

### Meeting 5.2 (45 min) — Clone → branch → edit → commit → push

| Time | Segment |
| --- | --- |
| 0–15 | Install Git for Windows (or lab-preinstalled); **clone your fork** (HTTPS). Distinguish clone (download to disk) from fork (copy on GitHub) — this pair of words confuses every beginner; draw the three copies: *GitHub upstream → your fork on GitHub → your laptop*. |
| 15–40 | The core loop, done once slowly: `git status` (the new code doctor) → create branch `feature/wobbles-the-coward` → edit [`classes.py`](../rogue_edu/student_starter/classes.py) (small, meaningful change: add one villain) → `add` → `commit` with the message rule *"finish this sentence: If applied, this commit will ___"* → `push` → see the branch on github.com. |
| 40–45 | Exit ticket: "Fork vs. clone vs. branch — one sentence each." |

### Meeting 6.1 (45 min) — Pull requests + review + the live moment

| Time | Segment |
| --- | --- |
| 0–15 | **Open the PR** (fork → upstream): what a **diff** shows (green/red lines = your commit made visible); write a description that names *what* and *why*. |
| 15–30 | **Review day:** every student leaves one comment on a classmate's PR. Comment standard: *name a line + say why* ("line 48: the flee threshold uses `>=`; did you mean `>`?" or a genuine praise-with-reason). Approve or request changes. |
| 30–45 | **THE MONEY MOMENT:** teacher merges one PR live → the class Render URL redeploys automatically → everyone refreshes and plays *that student's* monster on the shared deployment. (Sessions are per-browser-cookie and the Procfile pins `--workers 1`, so one URL serves the whole class with a private game each.) Say it out loud: *your commit is now running in production.* |

### Meeting 6.2 (45 min) — The full cycle, solo, from an issue

| Time | Segment |
| --- | --- |
| 0–5 | Teacher shows the **Issues** tab: 5–8 small, pre-filed feature requests ("Add an NPC that warns about the coward", "Add a second Slime variant with different stats", "Improve the Elder's dialogue"). |
| 5–35 | Every student runs the whole cycle alone: pick an issue → **Sync fork** (button) → branch → edit → commit → push → PR (reference the issue number in the description) → peer review swap → merge. |
| 35–45 | **Debrief the diagram** on the board: issue → branch → commit → PR → review → merge → deploy. Closing line for the quarter's second half: *from now on, every pair-project feature ships this way.* |

---

## 6) Practical cautions (read before Week 5)

1. **Merge conflicts are the #1 time-killer.** Same-file PRs conflict; Grade 9 cannot resolve conflicts yet. Fix it structurally, not heroically — see §7.
2. **A bad merge breaks the class game for everyone.** Mitigate: the "doctor must PASS before you may open a PR" rule, teacher merges only after one peer approval, and (optionally) CI — see §8.
3. **Render free tier sleeps** after ~15 idle minutes; the first visitor refreshes once. Present this as a fact of free hosting, not a failure. For the always-on showcase URL, [`DEPLOYING.md`](../DEPLOYING.md) documents PythonAnywhere as the no-sleep alternative.
4. **Never "fix" slowness with more workers.** The in-memory `GAMES` dict means extra workers split players across worlds; the [`Procfile`](../Procfile) pins `--workers 1` on purpose.
5. **GitHub accounts:** check school/parental-consent policy for minors before Meeting 5.1; have a fallback (students pair up on one account) ready.

---

## 7) Optional prep — pair-owned files (recommended before Week 5)

Restructure the student starter so merge conflicts become nearly impossible:

```text
rogue_edu/student_starter/
    classes.py            ← stays as the taught example (Weeks 1–4)
    cast/                 ← NEW: one file per pair, created by the teacher
        __init__.py
        ada_and_ivo.py    ← that pair's monsters, their file, their PRs
        miguel_and_kim.py
```

Each pair's file defines their classes; [`game_config.py`](../rogue_edu/student_starter/game_config.py) imports them by name (a one-line change per merge, done by whoever merges). PRs then touch only the pair's own file → conflicts essentially never happen, and *ownership* is visible in the repo — which is itself an encapsulation lesson at the project scale.

---

## 8) Optional enhancement — CI on pull requests

The repo already carries a full test suite ([`make test`](../Makefile): 138 pytest + 13 node at last count). A single GitHub Actions workflow (`.github/workflows/tests.yml`) running pytest on every PR would give students a **red/green X on their own PR** — authentic CI with zero extra teaching (the checks tab is read, not written). Worth adding before Week 5; it also automates caution #2 in §6.

---

## 9) Assessment map (low-friction, built into the loop)

| Evidence | Weeks | Graded by |
| --- | --- | --- |
| Exit tickets (predict-the-log, fork/clone/branch) | 1, 4, 5, 6 | 3-point completion + correctness |
| The Heist Lab prediction sheet (predictions vs. reality) | 2 | Honest *predictions* score more than lucky guesses — reward reasoning, not luck |
| Monster family (inheritance free/override/contract worksheet + code) | 3 | [`check_my_class.py`](../rogue_edu/check_my_class.py) PASS + one-sentence verbal defense |
| Boss Arena + four-pillar Zoo sheet | 4 | Working arena + peer-identified pillars |
| One merged PR with a peer review given | 6 | PR link + review link (participation-graded) |
| Ongoing: the class "pillar map" poster each student maintains (one node per week) | 1–6 | Checked at weeks 4 and 6 |

The verbal defenses are where understanding is actually visible: "explain why your code *returns* instead of moving," "what did you inherit from `Goblin`," "why did the engine run your new monster without changing." A student who answers those owns the pillar; a student who can't has found the exact edge of their understanding — which is the next lesson's opening move.
