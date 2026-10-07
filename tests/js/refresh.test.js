// Arcade gate: the refresh-equivalent at the JS layer. A refresh calls
// the render functions again with (new) server state -- rendering twice
// with the same payload must repaint cleanly, never ghost or duplicate.
const test = require('node:test');
const assert = require('node:assert');
const { JSDOM } = require('jsdom');

const dom = new JSDOM(`<!DOCTYPE html><html><body>
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

const payload = {
  turn: 3,
  game_over: false,
  won: false,
  win_condition: 'defeat_all',
  goal_pos: null,
  goal_locked: false,
  active_dialogue: null,
  board_state: {
    width: 10,
    height: 10,
    hero: { name: 'H', x: 1, y: 1, hp: 12, max_hp: 20, symbol: '🦸' },
    villains: [{ name: 'S', x: 5, y: 5, hp: 3, max_hp: 10, symbol: '👾' }],
    npcs: [],
    walls: [],
  },
  events: [
    { beginner_text: 'H moves east.', actor: 'H', action: 'MoveAction', result: 'SUCCESS', tile_pos: [2, 1] },
    { beginner_text: 'S waits.', actor: 'S', action: 'WaitAction', result: 'SUCCESS', tile_pos: [5, 5] },
  ],
  log: ['an older line', 'H moves east.', 'S waits.'],
};

test('update twice (a refresh) leaves exactly one row per line', () => {
  // update() is the full paint path (board when a canvas exists, plus
  // logs, HUD and dialogue): a refresh runs it again with fresh state.
  game.update(payload);
  game.update(payload); // the second paint must CLEAR, not append
  const rows = document.querySelectorAll('#log-list .log-row');
  assert.equal(rows.length, 3);
  assert.equal(document.querySelectorAll('#log-list .log-row.is-clickable').length, 2);
});

test('updateDialogue twice with the same payload stays stable', () => {
  const withDialogue = { ...payload, active_dialogue: 'Hello again.' };
  game.updateDialogue(withDialogue);
  game.updateDialogue(withDialogue);
  assert.equal(document.getElementById('dialogue-text').textContent, 'Hello again.');
  assert.ok(!document.getElementById('dialogue-box').classList.contains('is-hidden'));

  const dismissed = { ...payload, active_dialogue: null };
  game.updateDialogue(dismissed);
  game.updateDialogue(dismissed);
  assert.ok(document.getElementById('dialogue-box').classList.contains('is-hidden'));
});
