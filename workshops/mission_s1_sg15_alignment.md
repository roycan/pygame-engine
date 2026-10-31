# 🌀 MISSION S-1 → SG 15 ALIGNMENT (short reference)

Scroll: `mission_s1_shinobi_blueprint.md` · Record: `mission_s1_record.md` ·
Prep: `mission_s1_teacher_prep.md`
SG 15 — Fundamentals of the SDLC: phase table (6 rows), nine SDLC models, Activity 1
(simulation of the first three phases on the Cookie Ordering App, three markdown annex
files, Annex D rubric, 20 pts), Activity 2 (Annex C continuation), Annex E quiz.

## Phase coverage — honest mapping

| SG 15 phase | Status in S-1 | Evidence |
| --- | --- | --- |
| 1 · **Planning** (TOR: description, purpose, users, scope, features, timeline, deliverables) | **Practiced** — Record §1, mini-TOR (no timeline: the Gamekeeper owns it) | §1 fields |
| 2 · **Requirements Analysis** (user stories, validation requirements, security/risk) | **Practiced** — needs, functional requirements, one user story, validation requirements, ambiguity → clarification questions. Security/risk not exercised (nothing to secure in a paper blueprint) | §2 |
| 3 · **Design** (wireframes, flowcharts, class diagrams) | **Practiced** — low-fidelity interface mockup only. Class diagram: optional reminder, never required. Flowcharts: not used (nothing algorithmic to draw yet) | §3 |
| 4 · **Implementation** | **Exposed, not practiced today** — prediction question names the G-2 skills (change → PR → review → merge → pull) | §5.1 |
| 5 · **Testing** | **Exposed** — one written playtest anyone could perform + chakra check as the built-in gate | §5.2 |
| 6 · **Deployment / Maintenance** | **Named, deferred** — the SG itself defers both to CS4 and combines them in one table row; S-1 says so plainly and claims neither | §5 note |

**The SG's own structure, honored:** SG 15's table numbers six rows with
Deployment/Maintenance combined; S-1 teaches **seven distinct activities** and says the
SG combines the last two. No bug-free claims; the SG's own line — "how rigid… depends
on the SDLC model used" — is the anchor for the phases-vs-models distinction, and S-1's
approach question stays **open-ended** (finalize-first vs build-small-and-adjust), never
a forced Waterfall-vs-Agile binary.

## Connection to SG 15 Activity 1 (the official simulation)

- The **Mission Record is the small sibling** of Activity 1's three annex files:
  §1 ↔ Annex A (Initial Project Plan / TOR), §2 ↔ Annex B (SRS: user stories +
  validation), §3 ↔ Annex C (wireframes + design). When students meet the Cookie
  Ordering App annexes, the skeleton is already familiar — only the domain changes.
- **Deliberate domain split:** S-1 uses the **RogueEdu grove** (experiential, playable,
  zero setup); Activity 1 uses the **Cookie Ordering App** (SG's official simulation,
  graded, three markdown files in a repo). The workshop does not pre-empt the graded
  activity — it rehearses its shape.
- S-1's output **feeds forward**: squads may reuse their §2 clarification-question
  habit and §3 consistency pass in Activity 1, and the record's TOR fields reappear
  in the SG 16 **project proposal** (which the SG says the Activity 1 result feeds).

## SG 15 accuracy flags (for the CS team; source untouched)

1. **Iterative-model bullet contamination:** the line "Minimal planning; coding begins
   immediately with evolving requirements" sits inside the *Iterative* bullet and
   contradicts both the Iterative description and the Big Bang bullet that follows.
2. **Security requirements exceed scope:** Annex B §5 demands encryption of passwords
   and payment details, while Annex A states the app processes **no payments**
   (COD/GCash on site) and no user story mentions accounts or login. A real squad
   should flag this inconsistency — S-1 trains exactly that reflex.
3. **Delivery fee** appears only inside a validation formula (total = prices +
   ingredients + delivery fee), never in the TOR, features, or user stories.
4. **Timeline order drift:** the TOR timeline lists "Deployment and Testing" (reversed
   vs the phase table's Testing → Deployment).
5. **Deployment/Maintenance combined** in one numbered row (acknowledged in S-1 and
   here; seven activities taught).
6. **Grouping:** Activity 1 says "group of 2 or 3" — RogueEdu squads are three, with the
   pair/four accommodation (G-series convention).

## Verification status summary

- **Verified before authoring:** every map coordinate, stat, and range quoted in the
  scroll/record (hero 25 hp / attack 6; slime hp 14 / attack 6 after G-2; five bites;
  adjacency-only biting; wall/NPC coordinates; canonical-vs-squad attack-power footnote
  in prep §B2); every interface component named from `templates/index.html` +
  `static/game.js` (board canvas, HUD chips Turn/HP/Villains Remaining, dialogue
  overlay speaker+text+press-any-key, Turn Log with clickable events, Developer
  Inspector); the requirement's solution-neutrality test; phase-minute sums
  (B: 2+3+5+6+2+2 = 20; A and C stated as ranges).
- **Proposed (students' own work, not verified facts):** every wireframe, dialogue text,
  and placement a squad produces — S-1 ships a *template*, not a solution; the teacher
  judges designs only against the recorded requirement-consistency test.
- **Not live-tested:** nothing here runs code, so there is no platform layer to
  rehearse; the only rehearsal needed is you reading the letter in character once.
