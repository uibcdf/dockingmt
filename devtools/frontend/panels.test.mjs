import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { EventEmitter } from 'node:events';
import { readFileSync } from 'node:fs';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';
import { SourceTextModule } from 'node:vm';
import { JSDOM, VirtualConsole } from 'jsdom';

// Extract literals with Python's AST; never import the scientific packages or
// translate/reimplement the shipped JavaScript. PYTHON selects the interpreter.
const sources = JSON.parse(execFileSync(process.env.PYTHON ?? 'python', [
  fileURLToPath(new URL('./extract_panels.py', import.meta.url)),
], { encoding: 'utf8' }));
const examples = JSON.parse(readFileSync(new URL('./panel_states.json', import.meta.url)));
const wireCopy = value => JSON.parse(JSON.stringify(value));

// Only the widget model surface used by these panels is doubled. This is not
// a comm/server/Viewer implementation and supplies no molecular behavior.
class Model extends EventEmitter {
  constructor(key, state) {
    super();
    this.attributes = { [key]: wireCopy(state) };
    this.sent = [];
  }
  get(key) { return this.attributes[key]; }
  send(message) { this.sent.push(wireCopy(message)); }
  update(key, state) {
    this.attributes[key] = wireCopy(state);
    this.emit(`change:${key}`);
  }
}

async function mount(t, kind, state = examples[`${kind}_empty`], model = null) {
  const errors = [];
  const console = new VirtualConsole();
  console.on('jsdomError', error => errors.push(error.message));
  const dom = new JSDOM('<div id="panel"></div>', {
    runScripts: 'outside-only', virtualConsole: console,
  });
  let cleanup = () => {};
  t.after(() => {
    try {
      cleanup();
      assert.deepEqual(errors, [], 'DOM event handlers must not fail silently');
    } finally {
      dom.window.close();
    }
  });
  const el = dom.window.document.querySelector('#panel');
  model ??= new Model(kind, state);
  const module = new SourceTextModule(sources[kind], {
    context: dom.getInternalVMContext(), identifier: `bindingmt:${kind}`,
  });
  await module.link(() => { throw new Error('Unexpected panel module import'); });
  await module.evaluate();
  cleanup = module.namespace.render({ model, el });
  assert.equal(typeof cleanup, 'function', 'a panel must return its cleanup callback');
  return { dom, el, model, cleanup, q: selector => el.querySelector(selector) };
}

const action = (id, payload = {}) => ({ type: 'action', id, payload });
const rows = panel => [...panel.el.querySelectorAll('#bmt-tbody tr')];
const stateFor = name => wireCopy(examples[name]);

test('interaction view retains the whole table and permits only the bound geometry', async t => {
  const p = await mount(t, 'explorer', examples.explorer_interactions);
  assert.equal(rows(p).length, 3);
  assert.equal(p.q('#bmt-pose-input').value, '3');
  for (const id of ['bmt-prev', 'bmt-next', 'bmt-pose-input']) {
    assert.equal(p.q(`#${id}`).disabled, true, id);
  }
  assert.equal(rows(p)[0].getAttribute('aria-disabled'), 'true');
  assert.match(rows(p)[0].title, /no loaded geometry/);
  rows(p)[0].click();
  rows(p)[1].click();
  p.q('#bmt-next').click();
  assert.equal(p.model.sent.length, 1);
  rows(p)[2].click();
  assert.deepEqual(p.model.sent.at(-1), action('set_pose', { index: 2 }));
  assert.match(p.q('#bmt-interaction-note').textContent, /position 3/);
  assert.match(p.q('#bmt-interaction-analyses').textContent, /hbonds: not evaluated/);
  assert.match(p.q('#bmt-interaction-analyses').textContent, /hydrophobic: evaluated, 0 observations/);
});

test('interaction availability and literal metadata refresh and clear with the scene', async t => {
  const state = stateFor('explorer_interactions');
  state.interaction_analyses[0].name = '<img src=x onerror=alert(1)>';
  const p = await mount(t, 'explorer', state);
  assert.equal(p.q('#bmt-interaction-analyses').querySelector('img'), null);
  assert.match(p.q('#bmt-interaction-analyses').textContent, /<img src=x/);
  state.interaction_geometry_available = false;
  state.interaction_geometry_reason = 'The loaded system no longer matches this pose interaction view.';
  state.poses.forEach(pose => { pose.geometry_available = false; });
  state.interaction_analyses = [];
  p.model.update('explorer', state);
  assert.match(p.q('#bmt-interaction-note').textContent, /no longer matches/);
  assert.equal(p.q('#bmt-interaction-analyses').textContent, '');
  rows(p)[2].click();
  assert.equal(p.model.sent.length, 1);
  p.model.update('explorer', examples.explorer_poses);
  assert.equal(p.q('#bmt-interaction-note').textContent, '');
  assert.equal(p.q('#bmt-interaction-analyses').textContent, '');
  assert.equal(p.q('#bmt-pose-input').disabled, false);
});

test('empty explorer requests context and disables unavailable navigation/visuals', async t => {
  const p = await mount(t, 'explorer');
  assert.deepEqual(p.model.sent, [{ type: 'query', id: 'viewer.context' }]);
  assert.equal(p.q('#bmt-pose-count').textContent, '0 poses');
  assert.equal(p.q('#bmt-pose-input').value, '');
  for (const id of ['bmt-prev', 'bmt-next', 'bmt-pose-input', 'bmt-toggle-ref', 'bmt-toggle-box']) {
    assert.equal(p.q(`#${id}`).disabled, true, id);
  }
  p.q('#bmt-next').click();
  p.q('#bmt-toggle-ref').click();
  assert.equal(p.model.sent.length, 1);
  p.q('#bmt-refresh').click();
  assert.deepEqual(p.model.sent.at(-1), action('refresh'));
});

test('rows retain position, missing identity/rank, zero and declared score meaning', async t => {
  const p = await mount(t, 'explorer', examples.explorer_poses);
  const table = rows(p).map(row => [...row.cells].map(cell => cell.textContent));
  assert.deepEqual(table.map(row => row.slice(0, 3)), [
    ['1', 'seventh', '7'], ['2', 'Unavailable', 'Unassigned'], ['3', 'first', '1'],
  ]);
  assert.equal(table[0][3], 'custom=12.00 (unit unknown)');
  assert.equal(table[1][3], 'Unavailable');
  const scores = [...rows(p)[2].cells[3].children];
  assert.equal(scores[0].textContent,
    `control=-2.00 (${examples.explorer_poses.poses[2].scores[0].unit})`);
  assert.deepEqual(JSON.parse(scores[0].title), examples.explorer_poses.poses[2].scores[0].definition);
  assert.equal(scores[1].textContent, 'vina=0.00 (unit unknown)');
  assert.equal(scores[1].title, 'Score meaning undeclared');
  assert.match(p.q('#bmt-comparison-note').textContent, /RMSD unavailable/);
  assert.equal(p.model.sent.length, 1, 'display must not request computations');
});

test('row clicks send collection indices independently of scientific rank', async t => {
  const p = await mount(t, 'explorer', examples.explorer_poses);
  for (const index of [2, 0, 1]) rows(p)[index].click();
  assert.deepEqual(p.model.sent.slice(1), [
    action('set_pose', { index: 2 }), action('set_pose', { index: 0 }), action('set_pose', { index: 1 }),
  ]);
});

test('navigation and one-based input send only their explicit action', async t => {
  const state = stateFor('explorer_poses');
  state.active_index = 1;
  const p = await mount(t, 'explorer', state);
  assert.equal(p.q('#bmt-pose-input').value, '2');
  p.q('#bmt-prev').click();
  p.q('#bmt-next').click();
  p.q('#bmt-pose-input').value = '3';
  p.q('#bmt-pose-input').dispatchEvent(new p.dom.window.Event('change'));
  assert.deepEqual(p.model.sent.slice(1), [
    action('prev_pose'), action('next_pose'), action('set_pose', { index: 2 }),
  ]);
});

test('invalid positions never send a selection message', async t => {
  const p = await mount(t, 'explorer', examples.explorer_poses);
  for (const value of ['', '0', '-1', '4', '1.5', 'invalid']) {
    p.q('#bmt-pose-input').value = value;
    p.q('#bmt-pose-input').dispatchEvent(new p.dom.window.Event('change'));
  }
  assert.equal(p.model.sent.length, 1);
});

for (const channel of ['namespace', 'custom']) {
  test(`explorer follows ${channel} state without echoing navigation`, async t => {
    const p = await mount(t, 'explorer', examples.explorer_poses);
    const state = stateFor('explorer_poses');
    state.active_index = 2;
    if (channel === 'namespace') p.model.update('explorer', state);
    else p.model.emit('msg:custom', { type: 'state', state });
    assert.equal(p.q('#bmt-pose-input').value, '3');
    assert.equal(p.q('#bmt-next').disabled, true);
    assert.equal(p.q('#bmt-prev').disabled, false);
    assert.equal(rows(p)[2].classList.contains('bmt-row--active'), true);
    assert.equal(rows(p)[0].classList.contains('bmt-row--active'), false);
    assert.equal(p.model.sent.length, 1);
    p.model.emit('msg:custom', { type: 'unrelated', state: examples.explorer_empty });
    assert.equal(rows(p).length, 3);
  });
}

test('reference/domain toggles use current availability and visibility', async t => {
  const p = await mount(t, 'explorer', examples.explorer_poses);
  assert.equal(p.q('#bmt-toggle-ref').disabled, true);
  assert.equal(p.q('#bmt-toggle-ref').title, examples.explorer_poses.reference_reason);
  p.model.update('explorer', {
    ...examples.explorer_poses, reference_available: true, domain_available: true,
    reference_visible: true, domain_visible: false,
  });
  assert.equal(p.q('#bmt-toggle-ref').textContent, 'Hide Reference');
  assert.equal(p.q('#bmt-toggle-box').textContent, 'Show Search Box');
  p.q('#bmt-toggle-ref').click();
  p.q('#bmt-toggle-box').click();
  assert.deepEqual(p.model.sent.slice(1), [action('toggle_reference'), action('toggle_search_domain')]);
});

test('backend errors and cleared results replace stale explorer state', async t => {
  const p = await mount(t, 'explorer', examples.explorer_poses);
  p.model.update('explorer', { ...examples.explorer_poses, status: 'error', error: 'Provider refused' });
  assert.equal(p.q('#bmt-status').textContent, 'Error: Provider refused');
  assert.equal(p.q('#bmt-status').classList.contains('bmt-status--error'), true);
  p.model.update('explorer', examples.explorer_empty);
  assert.equal(p.q('#bmt-status').textContent, '');
  assert.equal(p.q('#bmt-status').classList.contains('bmt-status--error'), false);
  assert.match(p.q('#bmt-tbody').textContent, /No docking poses/);
  assert.equal(p.q('#bmt-prev').disabled, true);
});

test('pose identities and score text remain literal DOM text', async t => {
  const state = stateFor('explorer_poses');
  state.poses[0].pose_id = '<img src=x onerror="throw 1">';
  state.poses[0].scores[0].name = '<script>throw 1</script>';
  const p = await mount(t, 'explorer', state);
  assert.equal(rows(p)[0].cells[1].textContent, state.poses[0].pose_id);
  assert.match(rows(p)[0].cells[3].textContent, /<script>/);
  assert.equal(p.q('#bmt-tbody').querySelectorAll('img, script').length, 0);
});

test('empty domain disables rendering while retaining explicit Refresh', async t => {
  const p = await mount(t, 'domain');
  assert.equal(p.q('#bmt-domain-toggle').disabled, true);
  assert.match(p.q('#bmt-props').textContent, /No search domain/);
  p.q('#bmt-domain-toggle').click();
  p.q('#bmt-domain-refresh').click();
  assert.deepEqual(p.model.sent, [{ type: 'query', id: 'viewer.context' }, action('refresh')]);
});

test('supplied domain displays declared angstrom geometry and requests rendering', async t => {
  const p = await mount(t, 'domain', examples.domain_supplied);
  assert.deepEqual([...p.el.querySelectorAll('.bmt-value')].map(el => el.textContent), [
    '(1.00, 2.00, 3.00)', '2.00 × 4.00 × 6.00', '48.0',
  ]);
  assert.equal(p.q('#bmt-domain-toggle').textContent, 'Render Search Domain');
  p.q('#bmt-domain-toggle').click();
  assert.deepEqual(p.model.sent.at(-1), action('render_domain'));
});

for (const channel of ['namespace', 'custom']) {
  test(`domain follows ${channel} state and switches render/hide/show actions`, async t => {
    const p = await mount(t, 'domain', examples.domain_supplied);
    const update = state => channel === 'namespace'
      ? p.model.update('domain', state)
      : p.model.emit('msg:custom', { type: 'state', state });
    update({ ...examples.domain_supplied, domain_available: true, visible: true });
    assert.equal(p.q('#bmt-domain-toggle').textContent, 'Hide Search Domain');
    p.q('#bmt-domain-toggle').click();
    assert.deepEqual(p.model.sent.at(-1), action('toggle_domain'));
    update({ ...examples.domain_supplied, domain_available: true, visible: false });
    assert.equal(p.q('#bmt-domain-toggle').textContent, 'Show Search Domain');
    update(examples.domain_empty);
    assert.equal(p.q('#bmt-domain-toggle').disabled, true);
    assert.match(p.q('#bmt-props').textContent, /No search domain/);
  });
}

for (const units of [{ length_unit: 'nm' }, { volume_unit: 'nm**3' }]) {
  test(`unsupported domain units disable actions: ${JSON.stringify(units)}`, async t => {
    const p = await mount(t, 'domain', { ...examples.domain_supplied, ...units });
    assert.equal(p.q('#bmt-domain-toggle').disabled, true);
    assert.equal(p.q('#bmt-props').textContent, 'Unsupported search-domain display units.');
    p.q('#bmt-domain-toggle').click();
    assert.equal(p.model.sent.length, 1);
    p.model.update('domain', examples.domain_supplied);
    assert.equal(p.q('#bmt-domain-toggle').disabled, false);
    assert.equal(p.q('#bmt-status').textContent, '');
  });
}

test('domain exposes provider errors without interpreting their text as markup', async t => {
  const error = '<strong>Provider refused</strong>';
  const p = await mount(t, 'domain', { ...examples.domain_supplied, status: 'error', error });
  assert.equal(p.q('#bmt-status').textContent, error);
  assert.equal(p.q('#bmt-status').children.length, 0);
});

for (const kind of ['explorer', 'domain']) {
  test(`${kind} cleanup removes only its subscriptions and remount reads current state`, async t => {
    const p = await mount(t, kind);
    const external = () => {};
    p.model.on('msg:custom', external);
    assert.equal(p.model.listenerCount('msg:custom'), 2);
    assert.equal(p.model.listenerCount(`change:${kind}`), 1);
    const oldHTML = p.el.innerHTML;
    p.cleanup();
    assert.deepEqual(p.model.listeners('msg:custom'), [external]);
    assert.equal(p.model.listenerCount(`change:${kind}`), 0);
    const populated = examples[kind === 'explorer' ? 'explorer_poses' : 'domain_supplied'];
    p.model.update(kind, populated);
    p.model.emit('msg:custom', { type: 'state', state: populated });
    assert.equal(p.el.innerHTML, oldHTML, 'unmounted panel must not follow later messages');
    const next = await mount(t, kind, populated, p.model);
    assert.equal(p.model.listenerCount(`change:${kind}`), 1);
    if (kind === 'explorer') assert.equal(rows(next).length, 3);
    else assert.equal(next.q('#bmt-domain-toggle').textContent, 'Render Search Domain');
    next.q(kind === 'explorer' ? '#bmt-refresh' : '#bmt-domain-refresh').click();
    assert.deepEqual(p.model.sent.at(-1), action('refresh'));
    next.cleanup();
    assert.deepEqual(p.model.listeners('msg:custom'), [external]);
    p.model.off('msg:custom', external);
  });

  test(`${kind} instances retain independent DOM and subscriptions`, async t => {
    const a = await mount(t, kind);
    const b = await mount(t, kind);
    const oldHTML = b.el.innerHTML;
    a.model.update(kind, examples[kind === 'explorer' ? 'explorer_poses' : 'domain_supplied']);
    assert.equal(b.el.innerHTML, oldHTML);
    a.cleanup();
    assert.equal(b.model.listenerCount(`change:${kind}`), 1);
    b.q(kind === 'explorer' ? '#bmt-refresh' : '#bmt-domain-refresh').click();
    assert.deepEqual(b.model.sent.at(-1), action('refresh'));
  });
}
