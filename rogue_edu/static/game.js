/* RogueEdu browser client: canvas renderer + WASD input + dual-view log.
 *
 * Architecture (tested by tests/js/*.test.js):
 *   - PURE helpers live at the top and touch NO DOM: keyToIntent,
 *     handleKey, gridToPixel, highlightBox. node --test exercises them.
 *   - renderBoard/renderLogs/highlightEventTile accept injected
 *     arguments (a canvas context, or nothing) so the jsdom tests can
 *     pass a stub context and assert draw calls -- no pixels required.
 *   - boot() wires the DOM; it exits early when no 2D canvas exists
 *     (e.g. under jsdom), which keeps requiring this file side-effect-safe.
 *   - submitKey(key) is the ONE input seam: the keyboard listener AND
 *     the on-screen D-pad (via synthetic KeyboardEvents) both reach it.
 *     An in-flight guard (_busy) drops duplicate taps/keys so key spam
 *     can never fire concurrent POSTs against the server's engine.
 */
"use strict";

// =====================================================================
// PURE HELPERS -- no DOM, no canvas, fully unit-testable
// =====================================================================

/** Map a player key to an engine intent. Returns {dx, dy}, "wait", or null. */
function keyToIntent(key) {
  const map = {
    w: { dx: 0, dy: -1 },
    a: { dx: -1, dy: 0 },
    s: { dx: 0, dy: 1 },
    d: { dx: 1, dy: 0 },
    space: "wait",
  };
  return Object.prototype.hasOwnProperty.call(map, key) ? map[key] : null;
}

/** Gate input: once the game is over, no key does anything. */
function handleKey(key, state) {
  if (!state || state.game_over) return null;
  return keyToIntent(key);
}

/** Tile (x, y) at `cell` px -> pixel rect + center point. */
function gridToPixel(x, y, cell) {
  return { x: x * cell, y: y * cell, cx: x * cell + cell / 2, cy: y * cell + cell / 2 };
}

/** High-contrast dashed outline geometry for a tile. */
function highlightBox(tile, cell) {
  return { x: tile[0] * cell + 2, y: tile[1] * cell + 2, w: cell - 4, h: cell - 4 };
}

// =====================================================================
// RENDERER -- accepts an injected 2D context so tests can pass a stub
// =====================================================================

function renderBoard(payload, ctx, cell) {
  const bs = payload.board_state;
  const w = bs.width * cell;
  const h = bs.height * cell;

  // Background + grid lines.
  ctx.fillStyle = "#f5f5f5";
  ctx.fillRect(0, 0, w, h);
  ctx.strokeStyle = "#dbdbdb";
  for (let i = 0; i <= bs.width; i++) {
    ctx.beginPath();
    ctx.moveTo(i * cell, 0);
    ctx.lineTo(i * cell, h);
    ctx.stroke();
  }
  for (let j = 0; j <= bs.height; j++) {
    ctx.beginPath();
    ctx.moveTo(0, j * cell);
    ctx.lineTo(w, j * cell);
    ctx.stroke();
  }

  // Goal tile: bright when reachable, locked in clear_and_reach mode.
  if (payload.goal_pos) {
    const g = gridToPixel(payload.goal_pos[0], payload.goal_pos[1], cell);
    ctx.fillStyle = payload.goal_locked ? "#e8e8e8" : "#ffdd57";
    ctx.fillRect(g.x, g.y, cell, cell);
    drawSymbol(ctx, payload.goal_locked ? "🔒" : "🏆", g.cx, g.cy, cell);
  }

  // Entities, each on a colored border tile (emoji-portability fallback).
  bs.walls.forEach((wall) => drawTile(ctx, wall, cell, "#8a8a8a"));
  bs.npcs.forEach((npc) => drawTile(ctx, npc, cell, "#00d1b2"));
  bs.villains.forEach((v) => drawTile(ctx, v, cell, "#ff3860"));
  bs.villains.forEach((v) => drawHpBar(ctx, v, cell));
  drawTile(ctx, bs.hero, cell, "#3273dc");
  drawHpBar(ctx, bs.hero, cell);
}

function drawTile(ctx, e, cell, borderColor) {
  const p = gridToPixel(e.x, e.y, cell);
  ctx.fillStyle = borderColor;
  ctx.fillRect(p.x + 1, p.y + 1, cell - 2, cell - 2);
  ctx.fillStyle = "#ffffff";
  ctx.fillRect(p.x + 3, p.y + 3, cell - 6, cell - 6);
  drawSymbol(ctx, e.symbol || "?", p.cx, p.cy, cell);
}

function drawSymbol(ctx, symbol, cx, cy, cell) {
  ctx.fillStyle = "#363636";
  ctx.font = Math.floor(cell * 0.5) + "px serif";
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";
  ctx.fillText(symbol, cx, cy);
}

function drawHpBar(ctx, e, cell) {
  if (typeof e.hp !== "number" || typeof e.max_hp !== "number" || e.max_hp <= 0) return;
  const p = gridToPixel(e.x, e.y, cell);
  const ratio = Math.max(0, Math.min(1, e.hp / e.max_hp));
  ctx.fillStyle = "#48c774";
  ctx.fillRect(p.x + 4, p.y + cell - 8, (cell - 8) * ratio, 4);
}

/** Dashed red outline around a log-referenced tile. */
function highlightEventTile(tile, ctx, cell) {
  if (!tile) return;
  const b = highlightBox(tile, cell);
  ctx.strokeStyle = "#ff3860";
  ctx.lineWidth = 3;
  ctx.setLineDash([6, 3]);
  ctx.strokeRect(b.x, b.y, b.w, b.h);
  ctx.setLineDash([]);
  ctx.lineWidth = 1;
}

// =====================================================================
// LOG PANEL -- beginner text by default, raw JSON behind the toggle
// =====================================================================

/** Past log lines render plain; the CURRENT turn's events are clickable
 * rows carrying data-x/data-y for spatial highlighting. */
function renderLogs(payload) {
  const list = typeof document !== "undefined" ? document.getElementById("log-list") : null;
  if (list) {
    list.innerHTML = "";
    const lines = payload.log || [];
    const eventCount = (payload.events || []).length;
    lines.slice(0, lines.length - eventCount).forEach(function (line) {
      appendLogRow(list, line, null);
    });
    (payload.events || []).forEach(function (ev) {
      appendLogRow(list, ev.beginner_text, ev.tile_pos);
    });
  }
  const inspector = typeof document !== "undefined" ? document.getElementById("inspector") : null;
  if (inspector) {
    inspector.textContent = JSON.stringify(payload.events || [], null, 2);
  }
}

function appendLogRow(list, text, tilePos) {
  const li = document.createElement("li");
  li.className = "log-row" + (tilePos ? " is-clickable" : "");
  li.textContent = text;
  if (tilePos) {
    li.dataset.x = String(tilePos[0]);
    li.dataset.y = String(tilePos[1]);
    li.addEventListener("click", function () {
      highlightFromLog(li);
    });
  }
  list.appendChild(li);
}

// =====================================================================
// DOM WIRING (skipped safely when no real canvas exists)
// =====================================================================

let _ctx = null;
let _cell = 50;
let _lastPayload = null;
let _busy = false; // one input request in flight at a time (see submitKey)

function update(payload) {
  _lastPayload = payload;
  if (_ctx) {
    renderBoard(payload, _ctx, _cell);
  }
  renderLogs(payload);
  updateHud(payload);
  updateDialogue(payload);
}

/** Show/hide the dialogue overlay from payload.active_dialogue.
 * The speaker name is pulled from the latest SpeakAction event. */
function updateDialogue(payload) {
  if (typeof document === "undefined") return;
  const box = document.getElementById("dialogue-box");
  if (!box) return;
  if (payload.active_dialogue) {
    const text = document.getElementById("dialogue-text");
    const speaker = document.getElementById("dialogue-speaker");
    if (text) text.textContent = payload.active_dialogue;
    if (speaker) {
      const talk = (payload.events || [])
        .filter(function (e) { return e.action === "SpeakAction"; })
        .pop();
      speaker.textContent = talk ? talk.actor : "Dialogue";
    }
    box.classList.remove("is-hidden");
  } else {
    box.classList.add("is-hidden");
  }
}

function updateHud(payload) {
  const set = function (id, text) {
    const el = typeof document !== "undefined" ? document.getElementById(id) : null;
    if (el) el.textContent = text;
  };
  const bs = payload.board_state || {};
  set("hud-turn", String(payload.turn));
  set("hud-hp", bs.hero ? bs.hero.hp + "/" + bs.hero.max_hp : "-");
  // Dead villains are omitted from board_state, so length == living count.
  set("hud-villains", String((bs.villains || []).length));
}

function highlightFromLog(rowEl) {
  if (typeof document === "undefined") return;
  document.querySelectorAll(".log-row.selected").forEach(function (el) {
    el.classList.remove("selected");
  });
  rowEl.classList.add("selected");
  if (!_ctx || !_lastPayload) return; // test/DOM-less environments
  renderBoard(_lastPayload, _ctx, _cell);
  highlightEventTile(
    [parseInt(rowEl.dataset.x, 10), parseInt(rowEl.dataset.y, 10)],
    _ctx,
    _cell
  );
}

/** The ONE input seam: both the keyboard listener and the on-screen
 * D-pad (synthetic KeyboardEvents) end here. The _busy guard means key
 * spam or a double-tap fires at most ONE POST per turn -- concurrent
 * steps against the server's engine are impossible by construction.
 * Cleared in .finally(), so even a failed request unlocks input. */
function submitKey(key) {
  if (_busy) return; // a request is already in flight: drop duplicates
  const intent = handleKey(key, _lastPayload);
  if (intent === null) return; // game over (or pre-first-paint): locked
  if (typeof fetch === "undefined") return; // non-browser environment
  _busy = true;
  fetch("/api/step", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ key: key }),
  })
    .then(function (res) {
      return res.json();
    })
    .then(update)
    .catch(function () {
      /* server unreachable; keep the last known board */
    })
    .finally(function () {
      _busy = false;
    });
}

function boot() {
  const canvas = typeof document !== "undefined" ? document.getElementById("board") : null;
  if (!canvas || !canvas.getContext) return;
  const ctx = canvas.getContext("2d");
  if (!ctx) return; // jsdom has no 2D canvas without the native package
  _ctx = ctx;

  if (typeof document !== "undefined") {
    const toggle = document.getElementById("inspector-toggle");
    if (toggle) {
      toggle.addEventListener("change", function () {
        const inspector = document.getElementById("inspector");
        if (inspector) inspector.classList.toggle("is-hidden", !toggle.checked);
      });
    }
  }

  document.addEventListener("keydown", function (ev) {
    const key = ev.code === "Space" ? "space" : (ev.key || "").toLowerCase();
    if (["w", "a", "s", "d", "space"].indexOf(key) === -1) return;
    ev.preventDefault();
    submitKey(key);
  });

  // First paint: render the server-embedded state immediately so the
  // board is never blank. This also seeds _lastPayload, which the
  // input gate requires before accepting input.
  if (typeof window !== "undefined" && window.__INITIAL_STATE__) {
    update(window.__INITIAL_STATE__);
  }
}

if (typeof document !== "undefined" && document.addEventListener) {
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
}

// Node-only export guard (browsers never define `module`).
if (typeof module !== "undefined" && typeof module.exports !== "undefined") {
  module.exports = {
    keyToIntent: keyToIntent,
    handleKey: handleKey,
    gridToPixel: gridToPixel,
    highlightBox: highlightBox,
    renderBoard: renderBoard,
    renderLogs: renderLogs,
    highlightEventTile: highlightEventTile,
    updateDialogue: updateDialogue,
    update: update,
    submitKey: submitKey,
  };
}
