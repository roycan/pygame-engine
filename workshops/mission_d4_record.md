# 📜 MISSION D-4 — MISSION RECORD (one page per squad)

**Squad:** ______ **Date:** ______ **Shinobi:** Scribe __________ · User Advocate __________ · Cartographer __________ · (Skeptic __________)

**Client:** The Gamekeeper · **Project:** the RogueEdu starter game — the Slime's grove

---

## §1 · INITIAL PROJECT PLAN (Terms of Reference) — *Planning*

| Field | Our answer |
| --- | --- |
| **Problem** | ________________________________________________ |
| **Users / stakeholders** | ________________________________________________ |
| **Purpose** | ________________________________________________ |
| **Scope — we MAY change** | existing pieces only: NPC words, walls, stats inside ranges, placement |
| **Scope — we may NOT** | new engine features, HP bars, menus, anything outside the starter map |
| **Constraints** | hp in [1, 200] · attack in [0, 40] · when built, chakra check shows **0 warnings** |
| **Deliverables** | this Mission Record (plan · requirements · mockup · question · prediction) |

---

## §2 · SOFTWARE REQUIREMENTS — *Requirements Analysis*

**Core requirement (compare your draft to this):**
> A new player must receive a clear warning about the danger before entering the Slime's attack range.

**Our functional requirements:**
1. ________________________________________________
2. ________________________________________________
3. ________________________________________________

**User story:** As a **new player**, I want ____________________ so that ____________________.

**Validation requirements (how we will KNOW):**
- stats inside [1, 200] hp / [0, 40] attack → chakra check shows **0 warnings**
- the warning is met **before** the first bite → testable by playing it cold
- ________________________________________________

**⚠ Ambiguities found in the letter → clarification questions for the Gamekeeper:**
- ⚠ vague phrase: ____________________ → Q1: ____________________________________
- ⚠ vague phrase: ____________________ → Q2: ____________________________________

---

## §3 · DESIGN DOCUMENT — Interface Mockup — *Design*

**Our chosen solution (existing pieces only):** ________________________________

**The board (10×10) — AFTER our change.** Existing: Hero (1,1) · Slime (7,7) · Elder (2,8) · Rocks (4,4)(4,5)(5,4) · Pillars (6,2)(2,5). Mark additions/changes clearly:

```
9 ┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐
8 │   │   │ 🧙 │   │   │   │   │   │   │   │
7 │   │   │   │   │   │   │   │ 🟢 │   │   │
6 │   │   │   │   │   │   │   │   │   │   │
5 │   │   │ 🏛 │   │ 🪨 │   │   │   │   │   │
4 │   │   │   │   │ 🪨 │ 🪨 │   │   │   │   │
3 │   │   │   │   │   │   │   │   │   │   │
2 │   │   │   │   │   │   │ 🏛 │   │   │   │
1 │   │ 🛡 │   │   │   │   │   │   │   │   │
0 └───┴───┴───┴───┴───┴───┴───┴───┴───┴───┘
  0   1   2   3   4   5   6   7   8   9
```

**The dialogue overlay, as the player will see it** (or the Turn Log row, if our design
speaks there):

```
┌─ Speaker: ____________________ ──────────────┐
│                                              │
│  ________________________________________    │
│  ________________________________________    │
│                                              │
│  Press any key to close.                     │
└──────────────────────────────────────────────┘
```

**Consistency pass:** requirement ↔ element traceability
- requirement 1 → element: ____________  ✓/✗
- requirement 2 → element: ____________  ✓/✗
- element without a requirement (scope creep?): ____________  ✓/✗

---

## §4 · UNRESOLVED QUESTION for the Gamekeeper

Our biggest assumption that only the client can confirm:
________________________________________________
________________________________________________
*(If the Gamekeeper answers differently than we assumed, which part of §3 changes? ____________)*

---

## §5 · WHAT'S NEXT? — *Implementation · Testing · beyond*

1. **Implementation** will use these B-2 skills, in order: change → commit/push → ______ → Stamp Law → ______ → pull → ______.
2. **Testing:** one test anyone could perform: ____________________________________
3. **Approach:** finalize the whole blueprint first ⬜ OR build a small piece, playtest, improve ⬜ — because: ____________________________________

*Still ahead of us (deferred by the SG to CS4): **Deployment** and **Maintenance**.*

**Rank earned:** ______ **Sensei stamp:** ______
