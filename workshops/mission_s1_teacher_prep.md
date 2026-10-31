# 🌀 MISSION S-1 — SENSEI PREPARATION CHECKLIST

Scroll: `mission_s1_shinobi_blueprint.md` · Record: `mission_s1_record.md` ·
Alignment: `mission_s1_sg15_alignment.md`

**The special thing about S-1:** it needs **no computers, no repos, no env**. It is the
zero-setup day between the git-heavy G missions and the SG 15 deck. Prep = printing +
knowing the client's answers.

---

## A. Print & bring

- [ ] Client letter — printed on the scroll cover (also read aloud by you in character).
- [ ] **One Mission Record page per squad** (`mission_s1_record.md` — print single-sided).
- [ ] **Grid sheets** — the record has a grid, but squads sketch better BIG: a few
      letter-size 10×10 grids for Phase 3 (draw with a ruler once; photocopy).
- [ ] Optional: the SG 15 annex excerpts (Annex A/B/C first pages) to show AFTER the
      mission — "the same boxes, official size" (see alignment file §connection).

## B. Know the verified facts cold (you will be the Gamekeeper)

### B1. The game, verified against `student_starter` + G-2
| Piece | Verified fact |
| --- | --- |
| Board | 10×10 grid; hero 🛡️ at **(1,1)**; Slime at **(7,7)**; Elder 🧙 at **(2,8)** |
| Walls | Rocks **(4,4) (4,5) (5,4)**; Pillars **(6,2) (2,5)** |
| Hero (BraveKnight) | **hp 25, attack 6** |
| Slime (after G-2's approved change) | **hp 14, attack 6** → a hero at 25 hp survives **five** bites (25 ÷ 6 → 5); the hero kills it in **three** bites (14 ÷ 6 → 3) |
| "Attack range" | the Slime bites only when **orthogonally adjacent** (`distance_to_hero == 1`) |
| Warning carriers that already exist | an NPC's dialogue (the **dialogue overlay**: speaker + text, press-any-key), the **Turn Log** (plain-English event lines), walls, stats, placement — all student-accessible |

### B2. Canonical repo vs squad repos (one honest footnote for you)
- The **canonical** `student_starter` still has `attack_power=3, hp=10` (9 bites).
- The client letter's numbers (bite 6, five bites) describe the **squad repos after
  G-2's approved merge**. If a squad insists on checking canonical code, the facts
  differ — say so and move on: the blueprint is about **their** game's next change.

### B3. The interface, verified component names (for the mockup)
| Component | Real name/behavior |
| --- | --- |
| Board | 500×500 canvas grid, one emoji per tile |
| HUD chips | **Turn · HP · Villains Remaining** (above the board) |
| **Dialogue overlay** | warning-styled box over the board: **speaker + text + "Press any key to close"** — appears while a dialogue is active |
| Turn Log | side panel, plain-English lines; current-turn events **clickable** → dashed red outline flashes on the tile they name |
| (Developer Inspector) | raw JSON behind a checkbox — not beginner-facing |

The record's mockup must use **these** components — not an invented "dialogue box menu"
or "HP bar": the engine draws HP only in the HUD chip, and NPC words appear only in the
dialogue overlay (plus their log line).

## C. The Gamekeeper's answers (role-play the client; give these when asked)

- **"What does 'dangerous but fair' mean?"** → The hero must still be able to win with
  careful play. Five bites is the *designed* danger — **the warning is the fix, not
  nerfing the slime.** (If a squad proposes weakening the slime, that contradicts
  G-2's approved change — send them back to the letter's first sentence.)
- **"Where is 'somewhere players will actually see it'?"** → Before the first bite —
  anywhere a player meets it **before entering the slime's bite range** (one tile away
  is too late; the Elder's usual path, or near the slime's territory, is the spirit).
  Exact tile = the squad's design decision; you judge only "would a new player meet it
  in time?"
- **"May we add a wall / move the slime / add an NPC?"** → All allowed if built from
  existing pieces. Not allowed: new engine features (HP bars, menus, signs as new
  sprites beyond emoji, sounds, second maps).
- **"How long should the warning text be?"** → One or two sentences; it pauses the game
  (any key closes it), so players WILL read it — but the slime waits too, so keep it short.
- **Answer questions with requirements, never with implementations.** If they ask "may
  we add an NPC?", answer "may your requirement be solved by an NPC? — that is Phase 3's
  question."

## D. Rescue guidance

| Situation | Move |
| --- | --- |
| Requirements prescribe a solution ("add an NPC that…") | Solution-neutrality test: *"would this sentence still make sense if we solved it with a wall instead?"* Rewrite as player-facing truth |
| Wireframe becomes art project | "Boxes and words, not beauty." Timebox Phase 3; Canva squads get one export, not a design session |
| Squad guesses instead of asking | Point at the ⚠ marks: the letter is *meant* to be under-specified — the questions ARE the deliverable |
| Squad weakens the slime ("make it attack 2") | Contradicts the client's first sentence (the bite grew sharper — that stays). The requirement is a *warning*, not a nerf |
| Squad claims "HP bar" as their design | Engine-drawn HP lives in the HUD chip only — adding one is engine work (out of scope). They may sketch the HUD as it exists |
| Phase 2 silent | Seed: "quote the two vague phrases back to me — what would you ask?" |

## E. Timing & grouping

- Primary = **Version B (20 min)**: 2 + 3 + 5 + 6 + 2 + 2. A = 5–10; C = 25–30 (both
  at the scroll's end).
- **Squads of two:** merge Scribe+Advocate duties; **fours:** add **The Skeptic**
  (challenges assumptions, drafts §5's test). All write on the one record.
- **Contingency:** if the room runs long, Phase 3's consistency pass compresses to a
  30-second pair-check; never cut the ambiguity hunt — it is the lesson.

## F. After the mission (bridge, 2 min if available)

Show the SG 15 Annex A/B/C first pages (or the slide deck next session): "the boxes you
just filled have official names and sizes." The Mission Record is the small sibling of
Activity 1's three annex files — same skeleton, deeper water later.
