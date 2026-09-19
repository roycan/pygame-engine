// Phase 0 gate: proves the Node test harness runs.
const test = require('node:test');
const assert = require('node:assert');

test('node harness runs', () => {
  assert.equal(1 + 1, 2);
});
