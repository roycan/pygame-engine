# 🌀 MISSION G-2 — SENSEI PREPARATION CHECKLIST

Scrolls: `mission_g2_three_shinobi_one_trusted_change.md` (20 min) +
`mission_g2_ila_conflicting_scrolls.md` (30 min) · Tale/rescue:
`mission_g2_teachers_tale_rescue.md` · SG 14 map: `mission_g2_sg14_alignment.md`

**Carryover from G-1** (do not re-do): squad repositories, GitHub sign-in per machine,
Git identity, shared RogueEdu environment (`~/rogue-edu-env`), review-rubric training,
G-1 mission completed and verified. Everything here is **new for G-2**.

---

## A. GitHub-side preparation (teacher, before class)

### A1. Squad repos must be live on GitHub
- PRs exist only on GitHub. Confirm every squad repo has a pushed `main` (G-1's squads
  did), and squads still have **write** access (Settings → Collaborators).
- G-1 squads that ran the offline fallback and never pushed `main`: have them push main
  in a 5-minute catch-up session **before** G-2 day.

### A2. Merge-button settings (one minute per repo — required, not optional)
- Repo → Settings → General → Pull Requests: tick **Allow merge commits**;
  **uncheck Allow squash merging** and **Allow rebase and merging**.
- Then verify on a throwaway PR: the merge button's dropdown must offer **only
  "Create a merge commit"** — no squash, no rebase options at all.
- Why this is required: the rollback lesson runs on `git revert -m 1`, which needs a
  **merge commit** to revert. A squash-merged or rebased PR changes the revert
  procedure (tale/rescue, Rollback section) — the setting makes the wrong path
  impossible instead of merely discouraged. The scrolls repeat the guard at every
  merge click.

### A3. Extension + auth on every machine
- VS Code: **GitHub Pull Requests and Issues** extension installed (SG 14 §1.1 names it).
- Machine signed in to GitHub (avatar visible in VS Code). Sign-in survives on lab
  machines; re-check on mission morning.
- Auth failure on the day → that squad uses the **web fallback** for PR steps
  (scroll footnotes) — same clicks, browser door.

### A4. Permissions reality — the Stamp Law decision
- Verified against GitHub Docs: on **private** repos, branch protection needs
  Pro/Team/Enterprise; **rulesets** are free only on **public** repos. Squad repos are
  private → **approval-before-merge cannot be machine-enforced**; "Request changes"
  does not block the merge button.
- G-2 therefore teaches the **Stamp Law as squad discipline** (per your decision).
- Optional future upgrade (not now): verify the school's GitHub org for **GitHub
  Education** (Team features free) → then rulesets can enforce reviews on private repos
  for SG 14's later group project.
- **Changed nothing** — no visibility, permissions, rulesets, or protection settings.

---

## B. The rehearsal — REQUIRED before mission day

The live GitHub PR interface was **not** exercised in scratch (scratch verified the git
level underneath: diffs, conflicts, resolutions, reverts — all green). The platform
layer must be walked once by you, using **your own test repository + a second account**
(a colleague's, or the class demo account). Budget: 30 minutes.

Rehearsal checklist (tick every row; expected screens in the tale/rescue guide):
- [ ] From account 1: push `feature/…`, open PR (extension **and** web) — base `main`
- [ ] PR shows Files Changed with the one-line diff
- [ ] Account 2 (reviewer) sees the PR; leaves a **line comment**
- [ ] Account 2: Finish review → **Request changes** (with the WARN evidence story)
- [ ] Account 1: pushes a fix commit → PR updates automatically
- [ ] Account 2: **Approve** (confirm account 1 **cannot** approve its own PR)
- [ ] Merge with **Create a merge commit**; check the history graph on GitHub
- [ ] Account 2 pulls; verifier runs the chakra check
- [ ] **Revert** button on the merged PR → new revert PR → merge → pull → verify
- [ ] Optional conflict leg: two branches editing one line → PR 2 shows the conflict
      banner → resolve via **merge main into branch** in VS Code → push → banner clears
- [ ] Extension dead? Web fallback works end-to-end

If any row fails: fix the setup before class, or pre-plan the web-fallback variant.

---

## C. Mission-day checklist (10 minutes before class)

- [ ] Scrolls printed (classroom + ILA) · review rubric visible
- [ ] Squad repos reachable; last commit on `main` = G-1's verified finish
- [ ] Two random machines: extension present + signed in (avatar)
- [ ] One machine: `~/rogue-edu-env` launches the game (spot check)
- [ ] Timer: 20 min classroom / 30 min ILA · tale/rescue open on teacher machine
- [ ] Projector ready for: the PR page, Files Changed, the Revert button

---

## D. In-flight classroom management

- **The dangerous minute is Phase 3**: reviewers must actually *run* the check — stop
  any squad whose reviewer approves from the description alone. The WARN is the lesson.
- **Author impatience:** "can I just merge?" → Stamp Law, loudly. A no-stamp merge is
  the one G-2 sin.
- **Web vs extension drift:** labels differ slightly between versions; the scrolls
  name *actions* (open PR, Files Changed, line comment, Request changes, Approve,
  Merge) — match the action, not the wording.
- **Fast squads:** start the ILA authoring early, or run recovery drills 3–4 themselves.
- **Falling behind:** classroom contingency = the sensei demonstrates Phase 3's review
  on the projector with one squad's PR while others watch, then all squads complete
  Phases 4–6 themselves.

---

## E. Data-visualization option (optional — your call in the moment)

- Squad repos on GitHub have **Insights → Contributors/Commits**: real bars built from
  the squads' own commits. A 3-minute "read the graph" reflection is available on the
  spot (ILA scroll, optional box).
- Honest framing (per your decision): reading an existing graph **does not by itself**
  satisfy "turn data into visuals." If you want a hands-on micro-activity: each squad
  copies its Insights numbers (commits per shinobi) into a spreadsheet and makes one
  column chart (≈ 5 min, offline-safe). Optional; flag for teacher review.

---

## F. Recovery map (details in tale/rescue)

| Situation | First move |
| --- | --- |
| Author can't approve own PR | By design — reviewer stamps (platform fact) |
| Merge button grayed | Unresolved conversation or conflict — resolve, then merge |
| "This branch has conflicts" | ILA Phase 3 flow — merge main into the branch |
| Extension signed out mid-mission | Web fallback (same actions, browser door) |
| Working-tree block ("clean your repository…") | Commit or Discard — G-1 rescue card #3 |
| Wrong PR base branch | Close PR (no harm) → reopen from the correct branch |
| A merged change must be undone | Rollback flow — Revert button (or `git revert -m 1`, teacher CLI) |
