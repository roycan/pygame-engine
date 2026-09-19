# RogueEdu test gate — run with: make test
# The project venv (python3 -m venv venv; venv/bin/pip install -r requirements.txt)
# keeps the gate reproducible regardless of system Python state.
# NOTE: recipe lines below MUST start with TAB characters.

.PHONY: test zip

test:
	venv/bin/pytest -q tests/
	node --test tests/js/*.test.js

zip:
	venv/bin/python tools/package_workshop.py
