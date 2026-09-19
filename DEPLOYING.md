# Deploying RogueEdu (free options)

Two free ways to put your game on a real URL. Both are fine; pick by workflow:

| | Path A: **PythonAnywhere** | Path B: **Render** |
| --- | --- | --- |
| Accounts needed | PythonAnywhere (email) | GitHub + Render |
| Upload method | The workshop ZIP (upload in browser) | `git push` |
| Sleeps? | **Never sleeps** | Sleeps after ~15 min idle (first visitor waits ~30–60 s, then refresh once) |
| Best for | Grade 9: simplest possible deploy, always-on showcase link | Quarter pairs: real-world push-to-deploy workflow |

## Read this first: how the game behaves in the cloud

- The app keeps games **in memory** (the `GAMES` dict). If the server sleeps or restarts, players get a **fresh game** on their next visit — that is the accepted tradeoff for free hosting, and `POST /api/reset` means a reset was always one click anyway.
- The start command runs **exactly one worker** (`--workers 1`). Two workers would keep two separate memory worlds, and players' keypresses would land in different games. Never "fix" slowness by raising workers on a free tier.

---

## Path A: PythonAnywhere (ZIP upload, ~15 minutes, no GitHub)

You need: the `rogue_edu_workshop.zip` from your teacher (or `make zip`), and a free account at [pythonanywhere.com](https://www.pythonanywhere.com) (no credit card).

1. **Upload the ZIP.** On your PythonAnywhere dashboard open the **Files** tab → *Upload a file* → choose `rogue_edu_workshop.zip` (it lands in your home folder).
2. **Unzip it.** Open a **Bash console** (Consoles tab) and run:

       unzip rogue_edu_workshop.zip

   You now have a `rogue_edu_workshop` folder in your home directory.
3. **Create the virtual environment and install dependencies** (in the same console):

       cd ~/rogue_edu_workshop
       python3 -m venv venv
       venv/bin/pip install -r requirements.txt

4. **Create the web app.** Go to the **Web** tab → *Add a new web app* → next → **Manual configuration** → pick the newest Python → Create.
5. **Point it at your code.** Still on the Web tab:
   - *Source directory*: `/home/YOUR_USERNAME/rogue_edu_workshop/rogue_edu`
   - *Virtualenv*: `/home/YOUR_USERNAME/rogue_edu_workshop/venv`
6. **Edit the WSGI file.** Near the top of the Web tab there is a link like `/var/www/YOUR_USERNAME_pythonanywhere_com_wsgi.py`. Open it, delete the demo content, and put in:

   ```python
   import os
   import sys

   path = "/home/YOUR_USERNAME/rogue_edu_workshop/rogue_edu"
   if path not in sys.path:
       sys.path.insert(0, path)

   os.environ.setdefault("SECRET_KEY", "change-me-to-a-long-random-string")

   from app import app as application
   ```

   (Replace both `YOUR_USERNAME`s. The `SECRET_KEY` line is what makes per-browser game sessions work.)
7. **Reload.** Click the big green **Reload** button on the Web tab, then open `https://YOUR_USERNAME.pythonanywhere.com`. Play.

**Updating your game later:** edit files in the Files tab (or re-upload the ZIP and `unzip -o`), then click **Reload** on the Web tab. No sleep, no cold start — your link works for anyone, any time.

---

## Path B: Render (GitHub push-to-deploy, ~20 minutes)

You need: this repo pushed to a **GitHub** account, and a free account at [render.com](https://render.com).

1. **Push the project to GitHub** (from the repo root, one time):

       git init
       git add .
       git commit -m "RogueEdu"
       git branch -M main
       git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
       git push -u origin main

2. On Render: **New + → Web Service** → connect your GitHub account → pick the repo.
3. Configure:
   - **Runtime**: Python 3
   - **Build command**: `pip install -r requirements.txt`
   - **Start command**: `gunicorn --chdir rogue_edu app:app --workers 1 --threads 4 --bind 0.0.0.0:$PORT`
     (A `Procfile` with the same command already lives in the repo — Render will find it.)
   - **Environment variable**: `SECRET_KEY` = any long random string.
4. **Create Web Service.** The first build takes a minute; Render gives you a `https://YOUR-APP.onrender.com` URL.
5. **Updating:** edit code → `git push` → Render rebuilds and redeploys automatically. That loop is the real-world skill.

**Sleep note:** on the free tier the service spins down after ~15 idle minutes. The first visitor waits a few seconds (they may need one refresh), then it is awake again. Games do not survive the nap — a fresh board is waiting.

---

## Local development is unchanged

Windows students keep using `venv\Scripts\python rogue_edu\app.py` — gunicorn is Linux-only and is only ever executed by the hosting platform, never on your laptop.
