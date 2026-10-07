# Deploying RogueEdu (Render + GitHub)

One free path, on purpose — it **teaches the real-world workflow**:
GitHub fork → branch → pull request → review → merge → automatic
redeploy. Every merged arena folder appears as a card on the class
arcade at `/games` about two minutes after its PR merges.

## Read this first: how the game behaves in the cloud

- The app keeps games **in memory** (the `GAMES` dict). If the server
  sleeps or restarts, players get a **fresh game** on their next visit —
  the accepted tradeoff for free hosting, and `POST /api/reset` means a
  reset was always one click anyway.
- The start command runs **exactly one worker** (`--workers 1`). Two
  workers would keep two separate memory worlds, and players'
  keypresses would land in different games. Never "fix" slowness by
  raising workers on a free tier.
- Before merging a student PR: the CI check
  (`.github/workflows/tests.yml`) must be green, and the pair must have
  run the doctor locally.

## One-time setup (teacher, ~20 minutes)

1. **Push this repo to GitHub** as the class repo (from the repo root):

       git init
       git add .
       git commit -m "RogueEdu"
       git branch -M main
       git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
       git push -u origin main

2. On [render.com](https://render.com): **New + → Web Service** →
   connect your GitHub account → pick the repo.
3. Configure:
   - **Runtime**: Python 3
   - **Build command**: `pip install -r requirements.txt`
   - **Start command**: `gunicorn --chdir rogue_edu app:app --workers 1 --threads 4 --bind 0.0.0.0:$PORT`
     (a `Procfile` with the same command already lives in the repo — Render finds it)
   - **Environment variable**: `SECRET_KEY` = any long random string
4. **Create Web Service.** The first build takes a minute; Render gives
   you a `https://YOUR-APP.onrender.com` URL. Open `/games` on that URL —
   that is the class arcade.

## The student loop (Weeks 5–6)

1. **Fork** the class repo on GitHub — the fork is their copy where
   they have write permission.
2. **Clone** the fork on the lab computer (HTTPS + Git Credential
   Manager), create a branch, edit **their own folder** under
   `rogue_edu/arenas/<their_pair>/`, run the doctor, commit, push.
3. **Open a pull request** (fork → class repo). CI runs the full test
   gate on the PR; a classmate leaves one review comment.
4. **Merge.** Render redeploys automatically. **Sync fork** (the GitHub
   button) keeps a student's fork current with the class repo.
5. Everyone refreshes `/games` — the new card is on the class arcade.
   Say it out loud: *your commit is now running in production.*

## Sleep note

On the free tier the service spins down after ~15 idle minutes. The
first visitor waits a few seconds (they may need one refresh), then it
is awake again. Games do not survive the nap — a fresh board is
waiting. Present this as a fact of free hosting, not a failure.

## Smoke-checking a deploy

From the repo root: `make smoke` boots the real server locally and
probes every page (`/`, `/games`, `/play/sample_pair`, the step API).
Run it before pushing or after a suspicious merge. It is deliberately
NOT part of `make test` — process flakiness must never break the gate.

## Local development is unchanged

Windows students keep using `venv\Scripts\python rogue_edu\app.py` —
gunicorn is Linux-only and is only ever executed by the hosting
platform, never on your laptop.
