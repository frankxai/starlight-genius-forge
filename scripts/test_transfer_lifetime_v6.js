const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const {webcrypto} = require('node:crypto');
const script = fs.readFileSync(process.argv[2], 'utf8').match(/<script>([\s\S]*?)<\/script>/)[1];
function setup({fail = false, crypto = webcrypto} = {}) {
  const elements = Object.fromEntries(['idea','tags','out','captureBtn','clearBtn'].map(id => [id, {
    value: '', textContent: '', handlers: {}, addEventListener(k, fn) {this.handlers[k] = fn;}
  }]));
  const stages = Array.from({length: 6}, () => ({classList: {toggle(){}, add(){}, remove(){}}}));
  const links = [], blobs = [], revoked = [], timers = [];
  const document = {getElementById: id => elements[id], querySelectorAll: () => stages,
    body: {appendChild(){}}, createElement() {
      const link = {click(){if (fail) throw Error('synthetic save failure');}, remove(){this.removed = true;}};
      links.push(link); return link;
    }};
  const URL = {createObjectURL(blob){blobs.push(blob); return `blob:synthetic-${blobs.length}`;},
    revokeObjectURL(url){revoked.push(url);}};
  vm.runInNewContext(script, {document, Blob, URL, crypto, setTimeout(fn, ms){timers.push({fn,ms});}});
  elements.idea.value = '\ufeff  Private 🧠\r\nsecond line  ';
  elements.tags.value = '  hardware,, 中文  ';
  return {elements, links, blobs, revoked, timers, click: () => elements.captureBtn.handlers.click(),
    clear: () => elements.clearBtn.handlers.click()};
}
let passed = 0; const failures = [];
async function test(name, fn) {try {await fn(); passed++;} catch (e) {failures.push({name, error:e.message});}}
(async () => {
  await test('separate captures suggest separate private filenames', () => {
    const x = setup(); x.click(); x.elements.idea.value += ' changed'; x.click();
    assert.equal(x.links.length, 2); assert.notEqual(x.links[0].download, x.links[1].download);
    x.links.forEach(link => assert.match(link.download, /^idea-capture-[a-f0-9]{32}\.json$/));
  });
  await test('slow save and later capture or clear do not revoke outstanding downloads', () => {
    const x = setup(); x.click(); x.timers.forEach(timer => timer.fn());
    x.click(); x.clear(); x.timers.forEach(timer => timer.fn()); assert.equal(x.revoked.length, 0);
  });
  await test('command uses double quotes and the suggested filename without private text', () => {
    const x = setup(); x.click();
    assert(x.elements.out.textContent.includes(`--packet "path/to/${x.links[0].download}"`));
    assert(!x.elements.out.textContent.includes('Private')); assert(!x.elements.out.textContent.includes('中文'));
  });
  await test('failed request cleans its URL immediately while preserving both fields', () => {
    const x = setup({fail:true}); const before = [x.elements.idea.value, x.elements.tags.value]; x.click();
    assert.deepEqual(x.revoked, ['blob:synthetic-1']); assert(x.links[0].removed);
    assert.deepEqual([x.elements.idea.value,x.elements.tags.value], before);
    assert.match(x.elements.out.textContent, /could not/);
  });
  await test('missing crypto never falls back to a repeated name or loses the draft', () => {
    const x = setup({crypto:null}); const before = x.elements.idea.value; x.click();
    assert.equal(x.links.length, 0); assert.equal(x.blobs.length, 0);
    assert.equal(x.elements.idea.value, before); assert.match(x.elements.out.textContent, /could not/);
  });
  await test('entropy failure preserves draft without requesting a download', () => {
    const x = setup({crypto:{getRandomValues(){throw Error('synthetic entropy failure');}}}); x.click();
    assert.equal(x.links.length, 0); assert.match(x.elements.idea.value, /Private/);
    assert.match(x.elements.out.textContent, /could not/);
  });
  await test('transfer bytes remain exact across repeated captures', async () => {
    const x = setup(); const before = [x.elements.idea.value,x.elements.tags.value]; x.click(); x.click();
    for (const blob of x.blobs) {const packet = JSON.parse(await blob.text());
      assert.deepEqual([packet.rawText,packet.tags],before); assert.equal(Object.keys(packet).length,5);}
  });
  await test('pending message explains the page must stay open during saving', () => {
    const x = setup(); x.click(); assert.match(x.elements.out.textContent, /keep this page open/i);
    assert.match(x.elements.out.textContent, /pending/i);
  });
  console.log(JSON.stringify({tests:8,passed,failed:failures.length,failures}));
  process.exitCode = failures.length ? 1 : 0;
})();
