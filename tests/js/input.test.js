// Arcade gate: the submitKey seam + in-flight guard (double-tap = ONE POST).
// jsdom has no 2D canvas, so boot() exits early there by design -- these
// tests drive the exported seam directly with a mocked global fetch.
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

const livePayload = {
  turn: 1,
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
    villains: [],
    npcs: [],
    walls: [],
  },
  events: [],
  log: ['an older line'],
};

let posts = [];
let serverReply = livePayload;

global.fetch = function (url, opts) {
  posts.push({ url, key: JSON.parse(opts.body).key });
  return Promise.resolve({ json: () => Promise.resolve(serverReply) });
};

// Let queued promise callbacks run before asserting.
const settle = () => new Promise((resolve) => setImmediate(resolve));

// Seed the module's last-known payload (boot() would do this in a real
// browser; under jsdom there is no canvas, so we call update() directly).
function seed() {
  game.update(livePayload);
}

test('a key sends exactly one POST to /api/step with the right payload', async () => {
  seed();
  posts = [];
  game.submitKey('d');
  await settle();
  assert.equal(posts.length, 1);
  assert.equal(posts[0].url, '/api/step');
  assert.equal(posts[0].key, 'd');
});

test('a double-tap while in flight fires exactly ONE POST', async () => {
  seed();
  posts = [];
  game.submitKey('d');
  game.submitKey('d'); // lands while the first request is still in flight
  game.submitKey('d');
  await settle();
  assert.equal(posts.length, 1, 'the in-flight guard must drop duplicate taps');
});

test('input unlocks after the response arrives (.finally)', async () => {
  seed();
  posts = [];
  game.submitKey('d');
  await settle(); // response resolved -> _busy cleared
  game.submitKey('a');
  await settle();
  assert.deepEqual(posts.map((p) => p.key), ['d', 'a']);
});

test('the response payload drives the render (log re-renders from server state)', async () => {
  seed();
  posts = [];
  serverReply = { ...livePayload, turn: 7, log: ['an older line', 'turn seven happened'] };
  game.submitKey('d');
  await settle();
  const rows = [...document.querySelectorAll('#log-list .log-row')].map((r) => r.textContent);
  assert.deepEqual(rows, ['an older line', 'turn seven happened']);
});

test('unknown keys send nothing', async () => {
  seed();
  posts = [];
  serverReply = livePayload;
  game.submitKey('q');
  await settle();
  assert.equal(posts.length, 0);
});

test('once the game is over, every later key is ignored', async () => {
  seed();
  serverReply = { ...livePayload, game_over: true, turn: 9 };
  posts = [];
  game.submitKey('d'); // this final turn arrives; the server says game over
  await settle(); // ...and update() has now stored the game-over payload
  assert.equal(posts.length, 1);
  posts = [];
  game.submitKey('a'); // locked from here on
  await settle();
  assert.equal(posts.length, 0);
});
