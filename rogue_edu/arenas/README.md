# arenas/ — the Class Arcade

One folder per pair. Every folder here that contains a `game_config.py`
appears automatically as a card on the `/games` menu of the deployed
class site — no registration, no shared file to edit, no merge conflicts
on anyone else's code.

Track 3's rules — what you may touch, the two tiers, and the honest
limits of arena-only work — live in
[`TRACK3_VISUAL_SANDBOX.md`](../../TRACK3_VISUAL_SANDBOX.md:1).

## The recipe (start to merged PR)

1. **Copy the template** and rename the folder to your pair (lowercase,
   digits and underscores only — it becomes your URL slug):

       cp -r rogue_edu/arenas/_template rogue_edu/arenas/ada_and_ivo

2. **Make it yours:**
   - edit `classes.py` — your Hero / Villain / NPC subclasses;
   - edit `game_config.py` — set `TITLE = "..."` (the menu card name),
     place everyone, choose the win condition;
   - update the import line at the top of `game_config.py` to point at
     YOUR folder: `from arenas.ada_and_ivo.classes import ...`.

3. **Pass the doctor** (this is the "must PASS before you may open a PR"
   rule):

       cd rogue_edu
       python check_my_class.py arenas/ada_and_ivo/game_config

4. **Play it locally:** `python app.py`, open `/games`, click your card.

5. **Ship it:** branch → commit → push → **pull request** into the class
   repo. Peer review, teacher merges, Render redeploys — your card
   appears on the class arcade for everyone.

## Rules the menu enforces (so nobody breaks the class site)

- Folder name must match `[a-z0-9_]+` and must NOT start with `_`.
- Your `game_config.py` must define `create_game()` that RETURNS a ready
  `GameEngine`. A folder that cannot build its game shows up as a yellow
  "needs fixing" card **with the error printed on it** — the menu never
  breaks because of one broken arena, but everyone can see who needs help.
- A folder whose import or `create_game()` never finishes (an accidental
  `while True`) shows a yellow **"timed out"** card — validation runs in
  a separate, killable process, so one slow loop can never wedge the
  menu for everyone else. (A loop inside a villain's `act()` is
  different: it can only ever hang that player's own game.)
- Folders starting with `_` are invisible to the menu (`_template` is
  the scaffold, never a game).

## State rule: everything on `self`

**Student game state belongs on `self`.** Mutable class attributes and
module globals are process-shared and are NOT session-isolated: two
players clicking the same arena share one Python process on the server,
so a class-attribute counter (or any `global`) misbehaves for *everyone
at once* — not just for you. Instance attributes (`self.hp`,
`self._step`) live inside each visitor's own engine instance and are
always private to their session. Concretely:

```python
# WRONG  -- shared by every visitor of your arena:
class Slime(Villain):
    times_seen = []            # class attribute: process-shared!

# RIGHT  -- one private copy per player session:
class Slime(Villain):
    def __init__(self, x, y):
        super().__init__("Slime", x, y, hp=8, attack_power=3)
        self.times_seen = 0    # instance attribute: yours alone
```

When the class arcade is live, this rule is the difference between
"works on my screen" and "works on every screen."

## Is your arena losable? (the balance rule)

A game nobody can lose teaches nobody anything. Before your PR, answer
three questions honestly:

1. **Does naive play die?** Face-tank everything, ignore the boss's
   telegraphs — play it badly ON PURPOSE. A careless player must be
   able to lose. (The play-day is the real test: hand it to someone
   who hasn't read your code.)
2. **Does a figured-out strategy win THIN?** The right order — adds
   first, use cover, respect the enrage — should win with less than a
   third of your hero's hp left. A comfortable win means the threat
   was decoration.
3. **Is the danger countable and telegraphed?** Players must be able
   to read hp bars and the log's damage numbers and see the hit coming
   (the Inferno Drake's free-hit enrage turn is the model). Unseen
   damage isn't difficulty — it's a support ticket.

Difficulty is tiered on purpose: `student_starter` and `sample_pair`
stay easy (Week 1 success is the design); the creative arenas are
where the boss bites.

## Worked examples

`sample_pair/` is a finished, merged example (Sir Rosita vs the slime
twins). Read it before starting — it is a real PR in folder form.

`inferno_drake/` is a second finished example: a two-phase BOSS (the
Inferno Drake enrages at half hp — its icon flips 🐉→🔥, its damage
doubles, and the action log renames it "ENRAGED"). Read it when you
want to see subclassing + internal state + method overriding push a
villain further than chase-and-bite.

`necromancer_squad/` is a third: a summoner boss that COMMANDS A
SQUAD. The Necromancer holds a list of SkeletonMinion children and
raises one buried grave (🦴→💀) every third chant; if the master falls
first, every grave rises at once in vengeance. Read it for class
composition, turn counters in internal state, and event-driven
awakening — plus the honest note about why a true mid-game spawn
needs an engine feature (the engine is the sole mutator).

`quest_givers/` is the Track 3 flagship: a questgiver HIERARCHY. A
student-authored `QuestGiver` base runs a quest state machine
(📜 offered → ⚔️ accepted → ✅ done) and its subclasses — `SlayerQuest`
(counts dead wired targets) and `PilgrimageQuest` (counts visited wired
shrines) — override one hook. Read it for the template-method pattern,
wired-reference composition, and quest status told entirely through
symbol, name, and dialogue (no engine changes).
