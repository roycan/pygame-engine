# 🧪 C-7 LAB RECORD — Equip the Data Lab

*(Workshop C-7 · one per shinobi · SG 17 Activity 3 · submit screenshots on the LMS
as your sensei directs)*

**Squad:** ______ **Date:** ______ **Class period:** ______
**Env-Keeper (Loremaster):** ____________ **Tool-Bearer (Arena-Master):** ____________
**Evidence-Scout (Scout):** ____________ **Rescue Officer (4th):** ____________
**Which steps did YOU personally type?** ______________________________

---

## §1 · THE PREDICTION (Phase 0)

*Why use a plotting library instead of writing plotting code from scratch? One reason
besides "it's shorter."*

_______________________________________________________________

## §2 · THE LAB BENCH (Phase 1 — paste the exact line your terminal printed)

```
python -c "import sys; print(sys.executable)"
```

**Printed path:** ______________________________________________

**Check:** the path ends in `Lab_Visualizer\.venv\Scripts\python.exe` ☐

## §3 · THE TOOL (Phase 2 — paste three lines from `pip show`)

```
Name: ______________
Version: ______________
Location: ______________
```

**Check:** `Location:` contains `.venv` ☐

## §4 · THE EVIDENCE — three screenshots, exactly these

| # | The screenshot must show — all three together in one shot or three shots |
| --- | --- |
| **1** | the terminal: the `(.venv)` prefix, your run command, `Generating graph...`, and **no red traceback** |
| **2** | `python -m pip show matplotlib` output with the `Location:` line visible |
| **3** | the graph window — title, both axis labels, data points, grid — **and** `bacteria_growth.png` visible in the VS Code Explorer |

Screenshots attached (LMS): ☐ 1 ☐ 2 ☐ 3

## §5 · READ THE CURVE (Phase 4)

**One trend sentence** — what does the graph show the Biology team?

_______________________________________________________________

**One library sentence** — what did matplotlib do for you that hand-written code
would not have? (Concrete: what would you have had to build?)

_______________________________________________________________

**My customization** (one change): from ____________ to ____________

## §6 · THE TRAFFIC JAM (Phase 5)

1. Why does "put it in a virtual environment" **not** fix the AgarGrower/GraphMaster
   conflict?

_______________________________________________________________

2. One thing the squad would investigate or do next:

_______________________________________________________________

## §7 · REFLECTION (one honest line)

One thing that surprised you, or one thing you would tell the next squad:

_______________________________________________________________

---

## ✅ MISSION COMPLETE — core conditions

- [ ] Correct project-local interpreter **selected and verified** (§2)
- [ ] matplotlib installed **in the intended environment** (§3, Location)
- [ ] Program **imports and uses** matplotlib (screenshot 1)
- [ ] Graph **displayed and saved** as PNG (screenshot 3)
- [ ] I can explain **one feature or trend** in the graph (§5)
- [ ] I can explain **why a library was useful** (§5)

**Environment closed cleanly** (`deactivate`, prefix gone): ☐
**Rescue cards used:** R__ ______ **Rank earned:** ______ **Sensei stamp:** ______
**Assisted-install marking (internet contingency only):** ☐

*The bacteria data is illustrative teaching data — the workflow is real, the
"research team" is fiction.*
