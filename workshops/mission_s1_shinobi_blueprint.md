# 🌀 RogueEdu — WORKSHOP S-1: The Shinobi's Blueprint Mission

*(SG 15 · Fundamentals of the Software Development Life Cycle · Genin Edition · 20 minutes · no code today)*

**From Idea to Application.** Today the village does not fight, clone, or merge. Today
it does what every real software project does **before** any of that: it plans,
interrogates a client, and draws.

![The squad — three shinobi, one blueprint](3-shinobi-squad.png)

**Squad:** ______ **Date:** ______ **Mission Record page:** ☐ received

**Prerequisites:** G-2 completed (the slime bites for 6; you know the Stamp Law) ·
Grade 8 wireframing (refreshed, not re-taught) · **one printed Mission Record per squad** ·
paper grid sheet (or Canva/draw.io if the squad prefers — no new tools, no tutorials).

**Roles (seats, not silos — everyone writes on the one record):**
**Loremaster — The Scribe** · **Arena-Master — The User Advocate** ·
**Scout — The Cartographer** · *Squad of four?* **The Skeptic** joins: challenges
assumptions, predicts how the design could fail.

**Village laws (carried):** predict before you run · one change at a time ·
90 seconds stuck → raise your hand · evidence is your rank.
**Two new laws for today:**
1. **Requirements describe the problem. Design decides the solution.** Never mix them.
2. **No code today.** Today's weapons are words and boxes. The blueprint comes first.

---

## 📜 PHASE 0 — The Gamekeeper's Letter (2 min — read aloud by the Scribe)

> *To the shinobi squads of the RogueEdu village:*
>
> *Since the grove slime's bite grew sharper — one bite now costs **6 hp**, and five
> bites end a 25-hp hero — new players still wander into its reach blind. The game
> should teach caution **before** the first fight, not punish wandering after it.*
>
> *Make the Slime's territory feel **dangerous but fair**, and put the warning
> **somewhere players will actually see it.** You may build only from what the engine
> already gives you: an NPC's words, walls, the monsters' stats, and their placement.
> Show me a blueprint first — the plan, the requirements, and a design mockup.
> Coding comes later.*
>
> *— The Gamekeeper*

**⚠ Underline every vague phrase.** (Hint: there are at least two. You will need them
in Phase 2.) **Predict:** if the squad built nothing at all, is the requirement met?
______ *(That "no" is why Planning exists.)*

---

## 🥷 PHASE 1 — Planning: the Terms of Reference mini (3 min — Scribe leads)

Fill **§1 Initial Project Plan (Terms of Reference)** of the Mission Record:

- **Problem:** one sentence — what is wrong for the player right now?
- **Users / stakeholders:** who plays, who owns the game, who grades the blueprint?
- **Purpose:** what should the changed game achieve?
- **Scope:** what the squad MAY change (existing pieces only: NPC words, walls, stats
  inside the ranges, placement) and what it may NOT (new engine features, HP bars,
  menus — the engine is frozen).
- **Constraints:** stats stay in `[1, 200]` hp / `[0, 40]` attack; when the blueprint is
  later built, the chakra check must pass **without warnings**.
- **Deliverables:** this one Mission Record page.

**Sensei note:** this box is a miniature **Terms of Reference** — SG 15 calls it the
deliverable of Planning. You are doing the real phase, small.

---

## 🥷 PHASE 2 — Requirements Analysis: interrogate the letter (5 min — User Advocate leads)

Fill **§2 Software Requirements** of the record.

1. **Distill the requirement — describe the PROBLEM, not your solution.** Compare your
   draft with this canonical phrasing:
   > **"A new player must receive a clear warning about the danger before entering the Slime's attack range."**
   *(Notice: no NPC, no wall, no dialogue text in it. Those are Design decisions —
   yours to make in Phase 3, not requirements to obey.)*
2. **Add 2–3 functional requirements** the warning idea implies. Test each with the
   solution-neutrality rule: *would this sentence still make sense if the squad solved
   it with a wall instead of an NPC?* If not, it is design wearing a disguise.
3. **One user story:** As a *new player*, I want ______ so that ______.
4. **Validation requirements:** how will we KNOW it works when built? (Stats inside the
   ranges · chakra check `0 warnings` · the warning is met **before** the first bite —
   each one checkable.)
5. **⚠ The ambiguity hunt:** the letter says *"dangerous but fair"* and *"somewhere
   players will actually see it."* Neither tells you **how many bites is fair**, nor
   **where "somewhere" is**. Write **at least two clarification questions** you would
   send the Gamekeeper — questions, not guesses:
   Q1 ________________________________________________
   Q2 ________________________________________________

**Requirement vs design — the wall:** the requirement says *what must be true for the
player*. Which piece you place where is **Design**, and it is the next phase.

---

## 🥷 PHASE 3 — Design: the interface mockup (6 min — Cartographer leads)

First, know the real interface you are designing for (**verified against the engine**):

| Component | What it is |
| --- | --- |
| **The board** | a 10×10 grid (canvas, 500×500 px) — hero 🛡️ at (1,1), Slime at (7,7), Elder at (2,8), Rocks at (4,4)/(4,5)/(5,4), Pillars at (6,2)/(2,5) |
| **HUD chips** | above the board: **Turn · HP · Villains Remaining** |
| **Dialogue overlay** | appears over the board when you bump an NPC: **speaker name + message + "Press any key to close"** |
| **Turn Log** | side panel: plain-English event lines; current-turn events are **clickable** and flash a dashed red outline on the tile they name |

Now design. Decide **which existing piece(s)** satisfy the requirement — an NPC's
words (new NPC? the Elder's dialogue updated? position changed?), a wall that breaks
the ambush, a stat value — **and where**. Then:

1. Sketch the **board** on the record's grid: draw the existing pieces at their real
   coordinates and your proposed change(s) clearly marked.
2. Sketch the **dialogue overlay** as the player will see it: speaker name + the full
   warning text + the "press any key" hint. (If your design speaks through the **Turn
   Log** instead, sketch the log row.)
3. **Consistency pass:** every §2 requirement is visible somewhere in the mockup — and
   every mockup element traces back to a §2 requirement. Anything extra is scope creep;
   anything missing is an unmet requirement.

**Low-fidelity is the point.** Boxes, words, arrows. Beauty is not a requirement.

---

## 🥷 PHASE 4 — What comes next (2 min — all three predict)

1. **Implementation:** the coder who builds your blueprint walks in with G-2's kit.
   Name the order they follow: change → ______ → ______ → Stamp Law → merge → pull →
   and the last arrow: ______.
2. **Testing:** how would you *test* "the warning is met before the first fight"?
   (Chakra check? Play it? Have a new player try it cold?) Write one test anyone could
   perform: ________________________________________________
3. **The approach question — choose, one sentence of why:** would your squad finalize
   the entire blueprint before coding, or build one small piece, playtest it with real
   players, and improve? ________________________________
   *(There is no wrong answer — different projects justify different rhythms. The deck
   will name the rhythms.)*

**And honestly:** Deployment and Maintenance are real phases too — the SG itself
delivers them later (CS4). You have lived **implementation, testing, integration, and
review** in G-1/G-2; you have **not** yet lived deployment or long-term maintenance.

---

## 🥷 PHASE 5 — Evidence & rank (2 min)

Mission Record complete: §1–§5 all filled, at least one ⚠ ambiguity turned into a
question, wireframe traceable to requirements. Rank: ______ **Sensei stamp:** ______

**Exit line for the ledger:** *We did Planning, Requirements Analysis, and Design.
Implementation, Testing, Deployment, Maintenance remain — and we know exactly which
G-2 skills the first of those will use.*

---
---

## ⏱ VERSION A — micro-workshop (5–10 min)

For a short period or a demo day. Same letter; cuts, in order:
- Record §1: three lines only — problem, users, one constraint (2 min).
- §2: the canonical requirement + **one** clarification question (2 min).
- §3: grid sketch, placement only — no dialogue-overlay sketch (2–3 min).
- Phase 4 prediction spoken, not written (1 min).
**Cuts what:** user story, validation list, consistency pass, §4/§5 boxes.

## ⏱ VERSION C — extended (25–30 min)

Version B **plus**, in this order:
- **+2 min:** a second user story (the Gamekeeper's own: *As the Gamekeeper, I want new
  players to reach the slime fight prepared, so that the lesson lands*).
- **+2 min:** a validation-rules table in §2 (stat ranges · warning-before-bite · chakra
  0 warnings · warning text mentions the bite).
- **+3 min:** a two-state wireframe — BEFORE (current board) and AFTER (proposed board).
- **+2 min:** the model mini-debate: each shinobi picks a rhythm (finalize-all-first vs
  build-small-then-adjust) and defends it in one sentence; the squad may disagree —
  record the disagreement.
- **+3 min: Blueprint swap.** Squads exchange records and review with three questions:
  *is every requirement traceable in the mockup? · is the ambiguity flagged as a
  question, not guessed away? · would a stranger know what to build?* — G-2's review
  skills, in blueprint clothing.
**Realistic total: 28–30 min. If time collapses, the swap goes first.**

---

**Sensei prep (verified map/interface reference, Gamekeeper answers, rescue):**
`mission_s1_teacher_prep.md` · **SG 15/16 connections:** `mission_s1_sg15_alignment.md` ·
**Record page:** `mission_s1_record.md`
