# 🌀 MISSION G-1 → SG 13 COMPETENCY ALIGNMENT (short reference)

Mission: `mission_g1_three_shinobi_one_game.md`
SG 13 — Git Collaboration Tool Part 1: *Set up and configure a version control system
for a team-based project; perform the basic git workflow (commit, push, pull from a
cloned remote repository); create, manage, and merge branches.*

## What the mission directly PRACTICES (every shinobi does it)

| SG 13 competency | Where in the mission |
| --- | --- |
| Why version control (benefits) | Phase 2 isolation ("nobody's game broke"), Phase 5 pull-as-sync, the Rescue Story (history heals) |
| **Clone** | Phase 1, all three machines |
| **Stage** | Phase 3, both developers (staged-vs-changes lists visible) |
| **Commit** | Phase 3 + two merge commits in Phase 4 |
| **Publish branch / Push** | Phase 3 (features) and Phase 4 (integrated `main`) |
| **Pull** | Phase 4 (Scout) and Phase 5 (**all three shinobi** — their game changes because they pulled) |
| **Branching** (create, manage) | Phase 2 (create), Phase 3 (publish), status-bar switching throughout |
| **Merging** | Phase 4, via VS Code's **Git: Merge Branch…** interface (what SG 13 teaches) |
| **Collaboration** | The thesis: two independent contributions, one verified game, one shared history |

## What the mission INTRODUCES (not practiced by every shinobi)

| Concept | Treatment |
| --- | --- |
| **Fetch** (vs pull) | Scout observes it live in Phase 2; exit question 5 names the difference: pull = fetch + integrate |
| Remote vs local branches | The `origin/feature/...` prefix in the merge picker; Publish Branch moment |
| Merge conflicts | SG 14 (script ready in the rescue guide) — students never meet one in G-1 |
| Message discipline | The scroll's `lore:` / `arena:` formula; why messages are for the next reader |

## What the mission DEFERS (and where it goes instead)

| Deferred item | Destination |
| --- | --- |
| Setup & configuration (SG 13 §1.1: accounts, auth, identity) | Teacher-prep session BEFORE mission day |
| Individual non-graded practice (clone `GitHubRepo`, `testHello.py` arc) | SG 13's own activity, AFTER the mission — now familiar, solo |
| Conflict resolution as a student skill | SG 14 group missions (deliberate, controlled) |
| PR-based review, issues, forks, stash, worktrees | SG 14 and beyond |

## The eight distinctions — where the mission makes each physical

| Distinction | Experienced at |
| --- | --- |
| Working directory vs staging area | Phase 3 step 2 (the two lists: Changes vs Staged) |
| Staging vs committing | Phase 3 steps 2–3 ("envelope vs sealed") |
| Local commits vs remote commits | Phase 3 step 5 ("two places, one commit") |
| Commit vs push | Version A explicitly; Phase 3 implicitly (Publish Branch is a separate click) |
| Fetch vs pull | Phase 2 (fetch watch) vs Phase 4 step 1; exit Q5 |
| Local vs remote branches | Phase 3 publish; Phase 4 `origin/...` merge picker |
| Branching vs merging | Phase 2 (isolate) vs Phase 4 (combine) |
| Uncommitted changes vs merge conflicts | Rescue card #3 vs the SG 14 conflict demo (script in the rescue guide) |

## The four understandings the SG demands — and their proof moments

1. *Saving a file does not commit it* → the **M** badge that survives Ctrl+S (Phase 3).
2. *Committing does not push it* → the separate **Publish Branch** click (Phase 3).
3. *A push does not update teammates* → Phase 5: the developers' games changed only
   when **they pulled**.
4. *A merge does not guarantee a working app* → the Teacher's Tale (3 PASS + clean
   merge + a dead game) and the triad: **clean merge ≠ working game ≠ sane workflow.**

## Evidence categories (the scroll's rank system)

1. **Git history evidence** — hashes, branch names, merge commits in the graph.
2. **Integration evidence** — conflict-free merge output; a two-parent merge commit
   in the graph. Honest detail: with this exact sequence the FIRST merge can
   fast-forward (no merge commit) — the second creates the two-parent commit. The
   scroll's evidence line asks "how many?" on purpose.
3. **Actual game verification** — chakra check + what was SEEN: two slimes, the
   Elder's new words, identical game on every machine after pull.

## Follow-through

- **SG 13 individual practice** becomes "solo the same arc" on a personal repo:
  clone → branch → small change → commit → push → edit on GitHub → pull.
- **SG 14 Part 2** opens with what this mission deferred: squads meet one real
  conflict on purpose, then graduate to PR-style review while building a team arena
  (per-member `classes.py`, shared `game_config.py`, TITLE card on the `/games` arcade).
