// T6.3 gate (Tier B): renderer logic via a stub 2D context + jsdom log panel.
const test = require('node:test');
const assert = require('node:assert');
const { JSDOM } = require('jsdom');

const dom = new JSDOM(`<!DOCTYPE html><html><body>
  <canvas id="board" width="500" height="500"></canvas>
  <div id="dialogue-box" class="message is-warning is-hidden">
    <div class="message-header"><p id="dialogue-speaker">???</p></div>
    <div class="message-body"><p id="dialogue-text"></p></div>
  </div>
  <ul id="log-list"></ul>
  <pre id="inspector"></pre>
</body></html>`);
global.document = dom.window.document;
global.window = dom.window;

const game = require('../../rogue_edu/static/game.js');

// A recording stub 2D context: every method call and property set is logged.
function stubCtx() {
  const calls = [];
  const handler = {
    get(target, prop) {
      if (prop in target) return target[prop];
      return function (...args) {
        calls.push({ method: String(prop), args });
      };
    },
    set(target, prop, value) {
      target[prop] = value;
      calls.push({ method: 'set:' + String(prop), args: [value] });
      return true;
    },
  };
  return { calls, ctx: new Proxy({}, handler) };
}

const payload = {
  turn: 3,
  game_over: false,
  won: false,
  win_condition: 'clear_and_reach_goal',
  goal_pos: [9, 9],
  goal_locked: true,
  active_dialogue: null,
  board_state: {
    width: 10,
    height: 10,
    hero: { name: 'H', x: 1, y: 1, hp: 12, max_hp: 20, symbol: '🦸' },
    villains: [{ name: 'S', x: 5, y: 5, hp: 3, max_hp: 10, symbol: '👾' }],
    npcs: [{ name: 'E', x: 2, y: 8, symbol: '🧙' }],
    walls: [{ x: 4, y: 4, symbol: '🧱' }],
  },
  events: [
    { beginner_text: 'H moves east.', actor: 'H', action: 'MoveAction', result: 'SUCCESS', tile_pos: [2, 1] },
    { beginner_text: 'S waits.', actor: 'S', action: 'WaitAction', result: 'SUCCESS', tile_pos: [5, 5] },
  ],
  log: ['an older line', 'H moves east.', 'S waits.'],
};

function fillTextArgs(calls) {
  return calls.filter((c) => c.method === 'fillText').map((c) => c.args[0]);
}

test('renderBoard draws every entity symbol on the stub context', () => {
  const { calls, ctx } = stubCtx();
  game.renderBoard(payload, ctx, 50);
  const symbols = fillTextArgs(calls);
  for (const expected of ['🦸', '👾', '🧙', '🧱']) {
    assert.ok(symbols.includes(expected), `missing symbol ${expected}`);
  }
});

test('goal renders locked when goal_locked, open otherwise', () => {
  const locked = stubCtx();
  game.renderBoard(payload, locked.ctx, 50);
  assert.ok(fillTextArgs(locked.calls).includes('🔒'));
  assert.ok(!fillTextArgs(locked.calls).includes('🏆'));

  const open = stubCtx();
  game.renderBoard({ ...payload, goal_locked: false }, open.ctx, 50);
  assert.ok(fillTextArgs(open.calls).includes('🏆'));
});

test('hero tile border lands on the hero cell (1,1) -> px (51,51)', () => {
  const { calls, ctx } = stubCtx();
  game.renderBoard(payload, ctx, 50);
  const heroBorder = calls.find(
    (c) => c.method === 'fillRect' && c.args[0] === 51 && c.args[1] === 51
  );
  assert.ok(heroBorder, 'expected a fillRect at the hero cell');
  assert.equal(heroBorder.args[2], 48); // cell - 2
});

test('highlightEventTile draws a dashed red stroke on the referenced tile', () => {
  const { calls, ctx } = stubCtx();
  game.highlightEventTile([2, 1], ctx, 50);
  const dash = calls.find((c) => c.method === 'setLineDash');
  assert.ok(dash, 'expected setLineDash for the dashed box');
  const stroke = calls.find((c) => c.method === 'strokeRect');
  assert.deepEqual(stroke.args, [102, 52, 46, 46]);
  assert.ok(calls.some((c) => c.method === 'set:strokeStyle' && c.args[0] === '#ff3860'));
});

test('renderLogs renders history + clickable current events + raw JSON inspector', () => {
  game.renderLogs(payload);
  const rows = document.querySelectorAll('#log-list .log-row');
  assert.equal(rows.length, 3);
  const clickable = document.querySelectorAll('#log-list .log-row.is-clickable');
  assert.equal(clickable.length, 2);
  assert.equal(clickable[0].dataset.x, '2');
  assert.equal(clickable[1].dataset.y, '5');
  const inspector = document.getElementById('inspector');
  assert.ok(inspector.textContent.includes('"result": "SUCCESS"'));
  assert.ok(inspector.textContent.includes('"tile_pos": ['));
});

test('clicking a current-turn event row selects it for highlighting', () => {
  const first = document.querySelector('#log-list .log-row.is-clickable');
  first.click();
  assert.ok(first.classList.contains('selected'));
  // Deselection on the next click is handled by renderLogs/highlightFromLog.
});

test('updateDialogue shows the box with speaker + text while active', () => {
  const withDialogue = {
    ...payload,
    active_dialogue: 'Walls never move, but slimes never sleep.',
    events: [
      { beginner_text: 'Elder Maple says: Walls never move.', actor: 'Elder Maple', action: 'SpeakAction', result: 'SUCCESS', tile_pos: [2, 8] },
    ],
  };
  game.updateDialogue(withDialogue);
  const box = document.getElementById('dialogue-box');
  assert.ok(!box.classList.contains('is-hidden'), 'dialogue box should be visible');
  assert.equal(document.getElementById('dialogue-text').textContent, 'Walls never move, but slimes never sleep.');
  assert.equal(document.getElementById('dialogue-speaker').textContent, 'Elder Maple');
});

test('updateDialogue hides the box once dialogue is dismissed', () => {
  game.updateDialogue({ ...payload, active_dialogue: null });
  const box = document.getElementById('dialogue-box');
  assert.ok(box.classList.contains('is-hidden'), 'dialogue box should hide after dismissal');
});
