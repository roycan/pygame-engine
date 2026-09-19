// T6.2 gate: the pure helpers (no DOM, no canvas) behave exactly as spec'd.
const test = require('node:test');
const assert = require('node:assert');

const game = require('../../rogue_edu/static/game.js');

test('keyToIntent maps WASD and space', () => {
  assert.deepEqual(game.keyToIntent('w'), { dx: 0, dy: -1 });
  assert.deepEqual(game.keyToIntent('a'), { dx: -1, dy: 0 });
  assert.deepEqual(game.keyToIntent('s'), { dx: 0, dy: 1 });
  assert.deepEqual(game.keyToIntent('d'), { dx: 1, dy: 0 });
  assert.equal(game.keyToIntent('space'), 'wait');
  assert.equal(game.keyToIntent('q'), null);
});

test('handleKey locks all input once the game is over', () => {
  assert.equal(game.handleKey('d', { game_over: true }), null);
  assert.equal(game.handleKey('d', null), null);
  assert.deepEqual(game.handleKey('d', { game_over: false }), { dx: 1, dy: 0 });
});

test('gridToPixel computes the tile rect and its center', () => {
  assert.deepEqual(game.gridToPixel(3, 4, 50), { x: 150, y: 200, cx: 175, cy: 225 });
  assert.deepEqual(game.gridToPixel(0, 0, 50), { x: 0, y: 0, cx: 25, cy: 25 });
});

test('highlightBox insets the dashed outline by 2px', () => {
  assert.deepEqual(game.highlightBox([2, 3], 50), { x: 102, y: 152, w: 46, h: 46 });
});
