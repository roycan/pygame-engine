# 🌀 MISSION G-2 → SG 14 COMPETENCY ALIGNMENT (short reference)

Scrolls: `mission_g2_three_shinobi_one_trusted_change.md` (classroom, 20 min) ·
`mission_g2_ila_conflicting_scrolls.md` (ILA, 30 min)
SG 14 — Git Collaboration Tool Part 2: *"perform Pull Requests, Code Reviews, Recovery,
and Rollback of your codes; collaborate with at least one teammate using VS Code, Git,
and GitHub by contributing to a shared project, resolving conflicts, and communicating
effectively; turn data into visuals."*

## Directly PRACTICED by students (verified designs)

| SG 14 concept | Where | Verified |
| --- | --- | --- |
| **Pull Request** (propose, describe, update) | Classroom Phases 2–4; ILA Phases 1–3 | Git level in scratch; UI = teacher rehearsal |
| **Code Review** (inspect diff, line comment, Request changes with evidence, Approve) | Classroom Phase 3 & 5; ILA Phase 4 | Diff + evidence loop verified; review UI = rehearsal |
| **Recovery** (restore lost/accidentally changed local work) | ILA Phase 6 + drills 1–4 (tale guide) | All four drills verified |
| **Rollback** (undo shared work safely) | ILA Phase 7 (Revert button → new PR) | `git revert -m 1` verified; button = rehearsal |
| **Resolving conflicts** (real, overlapping, on the feature branch) | ILA Phases 1–5 | Verified end-to-end, both ideas preserved |
| **Collaboration on a shared project** (3 roles, communicate via PR reviews) | All phases | Verified git-level; UI = rehearsal |
| **Responding to review feedback** (push a fix commit to the PR branch) | Classroom Phase 4 | Verified |
| **.gitignore / README** (SG 14 §1.2) | Inspected as living examples in the actual repo (`.gitignore` documents its reasons; `README.md` is the repo's front page) — no toy project needed | Files verified in repo |
| **VS Code + GitHub Pull Requests and Issues extension** (SG 14 §1.1) | Primary interface, with web fallback | Extension name per SG; install verified in prep §A3 |

## Adaptations from the SG's own activity (flagged, with reasons)

- **Squads of three, not pairs.** SG 14 pairs Developers A/B on a README toy project;
  G-2 keeps the established three-shinobi convention on the **real game**. SG 14's
  *content* (branch → PR → review → conflict → resolve → merge) is fully preserved;
  the *vehicle* changes. Roles rotate across the ILA so each shinobi authors, reviews,
  and stewards.
- **Same budget:** SG 14's own numbers are 20 min in class + 30 min ILA — G-2 uses
  exactly those, with an explicit 18+2 split in the classroom scroll.
- **RogueEdu instead of README:** SG 14's toy project produces no verifiable behavior;
  the Stats PR produces a **loud, engine-checked warning** that the reviewer must
  catch — review with a real decision, per your requirement.

## HONEST GAPS (flagged for teacher review, not invented around)

| SG 14 item | Status |
| --- | --- |
| **Data visualization** ("turn data into visuals") | **Alignment gap — kept visible by decision.** The SG names it only in the objectives — no activity teaches it, and RogueEdu has no data-export/viz feature (building one = engine work, out of scope and refused by design). Options offered, none claimed as full coverage: (a) read the squad repo's **GitHub Insights** contributors graph (real data, optional box in the ILA); (b) optional 5-min CSV-to-column-chart spreadsheet micro-activity (prep §E). Reading a graph ≠ creating a visual. **Decision recorded (approval round):** GitHub Insights stays an **optional teacher extension**, not a required G-2 activity; the coverage table intentionally shows this gap rather than padding it. |
| **Required PR approvals / branch protection** | **Not enforceable** on private free-tier repos (verified vs GitHub Docs: classic protection needs Pro/Team/Enterprise on private; rulesets are free only on public repos). Taught as the **Stamp Law** (squad-enforced). Enforcement upgrade path: GitHub Education-verified org — teacher decision, not exercised. |
| **Recovery & Rollback** | SG 14 defines them in a concepts table but **never practices them** in any activity. G-2 adds the missing hands-on (four drills + revert), using methods that do **not** rewrite history. |
| **Terminal-vs-VS Code ILA (10 min, optional)** | Not scheduled; covered indirectly — the tale/rescue CLI table is the correlation artifact the SG asks students to build. |
| **Fork-based PR workflow** | Not used (squad PRs target the same repo's main). Mentioned in the alignment table of SG 14's own intro table; flag that SG 14's wording ("administrator pulls from your repo into their main") describes forks, not squad repos. |

## SG 14 ACCURACY AUDIT (flag for the CS team; source untouched per house rule)

1. **Pull vs Pull Request table:** the PR row describes the **fork** workflow
   ("*requests an administrator to pull changes from your repo into their main repo*").
   True for open source; **wrong for shared-repo teams** like the squads, where a PR
   proposes merging your branch into the *same* repository's `main`, reviewed by
   collaborators. G-2 teaches the distinction explicitly (classroom Phase 2).
2. **"Updates from a PR only appear locally after you manually fetch"** — direction is
   right, verb is loose: after the PR *merges on GitHub*, teammates receive it by
   **pull** (fetch + integrate). Slide-deck-level precision; G-2 scroll says pull.
3. **Recovery / Rollback:** defined ("restore lost work" / "return to a previous stable
   version") but never commanded, never practiced, and Rollback invites `reset --hard`
   thinking by silence. G-2 supplies the practice and the anti-`reset` wall.
4. **Conflict practice:** SG 14's Part 4 says "resolve the merge conflict together and
   commit the fix" — it never says conflicts resolve **on the feature branch**, that
   markers name the two sides (`HEAD` vs `origin/main`), or that the PR updates after
   pushing. G-2 teaches all three (verified).
5. **Approval ≠ enforcement:** the SG's "approve and merge" implies approval gates the
   merge; on private free-tier repos it does not — it is a social contract (Stamp Law).
   Verified against GitHub Docs.
6. **Closing takeaways** describe "planning a project / editing a project plan" —
   they do not match SG 14's own PR/review/conflict activity (copy drift). Flagged to
   the CS team; untouched here.
7. **"VS Code" vs "Visual Code Studio"** (Introduction) — minor typo in the SG.

## VERIFICATION STATUS SUMMARY (carried into every G-2 document's honesty)

- **Verified in scratch (git level):** Stats-PR review loop (WARN → Request changes →
  fix → green), conflict birth → markers → combined resolution → PR update → clean
  merge → playable game, four recovery drills, Wall-PR merge + `git revert -m 1` →
  behavior restored, history intact.
- **Documented, not live-tested (requires teacher rehearsal):** PR creation, Files
  Changed, line comments, Request changes/Approve buttons, merge button, conflict
  banner + web resolver, GitHub **Revert** button, reviewer assignment, author
  cannot self-approve — all covered by the mandatory rehearsal (teacher prep §B).
- **Deferred:** forks, Issues/projects boards, required-reviewer enforcement,
  squash/rebase merges, data-viz build.
