# 📜 D-1 DATA RECORD — The Shinobi Data Ledger

*(Workshop D-1 · one per shinobi · SG 18 practice · short formative evidence — this is
NOT the graded SG 18 Activity 1 exercise or its Annex A rubric)*

**Squad:** ______ **Date:** ______ **Class period:** ______
**Data Scribe (Loremaster):** ____________ **Cleaner / Lab Operator (Arena-Master):** ____________
**Quality Inspector (Scout):** ____________ **Audit Officer (4th):** ____________
**Which TODO did YOU fill at the keyboard?** TODO ______

---

## §1 · THE PREDICTION (Phase 0)

*What would go wrong if the village assigned teams from the raw ledger as-is? One way
the decision would be wrong:*

_______________________________________________________________

## §2 · INSPECT THE SCROLL (Phase 1 — the structure map)

The mission list lives at: `__________["__________"]` (a **list**)
One record is a: **__________** (JSON `null` becomes: **__________**)
Printed first count: `Raw records loaded: ` ______

## §3 · DATA AUDIT (Phase 2 — found by eye, before cleaning)

- **Incomplete record:** mission_id ______ — its **`team`** field is missing / `null` / blank: ☐
- **Exact duplicate:** mission_id ______ — identical copy? ☐ yes ☐ no
- **Three inconsistencies:**
  1. ____________________________ (type: whitespace / case / text-vs-number / village alias)
  2. ____________________________
  3. ____________________________

## §4 · EXPECTED vs OBSERVED (Phases 3–4)

| Check | Expected | Ours | ✓ |
| --- | --- | --- | --- |
| Raw records loaded | 8 | ____ | ☐ |
| Exact duplicates removed | 1 | ____ | ☐ |
| Incomplete records flagged | 1 | ____ | ☐ |
| Clean records retained | 6 | ____ | ☐ |
| `missions_cleaned.json` saved (6 ids: 101 102 103 105 106 107) | yes | ____ | ☐ |
| Raw file still has 8 records (READ-ONLY law) | yes | ____ | ☐ |
| Rewards are **ints** incl. `0` for mission 103 | yes | ____ | ☐ |

## §5 · THE EVIDENCE — exactly two screenshots

| # | The screenshot must show — all together |
| --- | --- |
| **1** | the terminal: `Raw records loaded: 8`, the `[DUPLICATE]` line, the `[FLAG]` line, `Clean records retained: 6`, and the **by-rank block** (A/B/C + total) — no red traceback |
| **2** | `missions_cleaned.json` open in the Explorer/editor: **6 records**, normalized values visible (102 = status `open`, village `Cedar Hold`, reward `450` as a number), and mission 103's reward `0` |

Screenshots attached: ☐ 1 ☐ 2

## §6 · THE DECISION AND ITS LIMIT (Phase 5)

*Most open missions in this ledger:* rank ______ (______ missions of 4).
**The limit, in your own words:** this count shows ______________ in this sample. It
does **not** by itself prove ______________ — counts are evidence for further
consideration, not a resource-allocation policy.

## §7 · WHY CLEANING MATTERED (Phase 6)

**One data-quality issue** you found (from §3) and what it would have done to the
decision:

_______________________________________________________________

---

## ✅ MISSION COMPLETE — completion conditions

- [ ] JSON **read from the supplied file** (`json.load`, `"r"` mode)
- [ ] Data held in **appropriate Python structures** (list of dicts)
- [ ] **Missing and duplicate** records identified and reported with reasons
- [ ] **Normalization/conversion rules applied** (strip, lowercase, village map, int)
- [ ] **Zero preserved** (mission 103's reward still `0`)
- [ ] **Separate cleaned JSON** saved; raw file unchanged
- [ ] **Audit counts match** expected results (§4 all checked)
- [ ] I can **explain one data-quality issue** and **one decision** the cleaned data
      supports — with its limit (§6–§7)

**Rescue cards used:** R__ ______ **Rank earned:** ______ **Sensei stamp:** ______

*Fictional data throughout — no student or personal records. SG 18 Activity 1 (graded,
Annex A) and its Anime exercise are unaffected by this formative record.*