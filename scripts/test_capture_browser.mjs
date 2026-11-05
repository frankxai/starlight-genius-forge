// Real Chromium downloads and file-input restoration. Use synthetic data only.
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {createServer} from 'node:http';
import {createRequire} from 'node:module';
import {mkdtemp, readFile, realpath, rm, writeFile} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const dependencyRoot = process.env.CAPTURE_BROWSER_ROOT;
assert.ok(dependencyRoot, 'Set CAPTURE_BROWSER_ROOT to the isolated Playwright package directory');
const require = createRequire(path.join(dependencyRoot, 'package.json'));
const {chromium} = require('playwright');
const html = await readFile(path.join(root, 'ui/idea-swarm-cockpit.html'));
const report = {
  head: execFileSync('git', ['rev-parse', 'HEAD'], {cwd: root, encoding: 'utf8'}).trim(),
  sourceSha256: createHash('sha256').update(html).digest('hex'),
  verifierSha256: createHash('sha256').update(await readFile(fileURLToPath(import.meta.url))).digest('hex'),
  playwright: require('playwright/package.json').version,
  browser: null, cases: [], pageErrors: [],
  limits: ['Synthetic inputs; no founder data', 'No native OS picker or power-loss proof',
    'No vault integration, customer acceptance or clipboard byte-fidelity proof'],
};
const fixtureRoot = await mkdtemp(path.join(tmpdir(), 'capture-browser-'));
const server = createServer((request, response) => {
  if (request.url !== '/') {response.writeHead(404); response.end(); return;}
  response.writeHead(200, {'Content-Type': 'text/html; charset=utf-8', 'Cache-Control': 'no-store'});
  response.end(html);
});
let browser;
let timedOut = false;
const timer = setTimeout(() => {
  timedOut = true;
  void browser?.close();
  server.closeAllConnections();
  server.close();
}, 180_000);
timer.unref();
let sequence = 0;
async function check(name, action) {
  const started = Date.now();
  try {
    await action();
    report.cases.push({name, status: 'passed', milliseconds: Date.now() - started});
    console.log(`PASS ${name}`);
  } catch (error) {
    report.cases.push({name, status: 'failed', error: String(error), milliseconds: Date.now() - started});
    throw error;
  }
}
async function packetFile(bytes) {
  const filename = path.join(fixtureRoot, `fixture-${++sequence}.json`);
  await writeFile(filename, bytes);
  return filename;
}
async function download(page) {
  const pending = page.waitForEvent('download');
  await page.locator('#captureBtn').click();
  const transfer = await pending;
  assert.match(transfer.suggestedFilename(), /^idea-capture-[0-9a-f]{32}\.json$/);
  const filename = path.join(fixtureRoot, `download-${++sequence}.json`);
  await transfer.saveAs(filename);
  assert.equal(await transfer.failure(), null);
  return {filename, bytes: await readFile(filename)};
}
async function restore(page, filename) {
  await page.locator('#restoreFile').setInputFiles(filename);
  await page.waitForFunction(() => !document.getElementById('restoreBtn').disabled);
}
async function refusesFile(page, bytes) {
  const before = {text: await page.locator('#idea').inputValue(), tags: await page.locator('#tags').inputValue()};
  await page.locator('#restoreFile').setInputFiles([]);
  await page.waitForFunction(() => document.getElementById('restorePreview').textContent.startsWith('Select a private capture file'));
  await page.locator('#restoreFile').setInputFiles(await packetFile(bytes));
  await page.waitForFunction(() => document.getElementById('restorePreview').textContent.includes('could not be read'));
  assert.equal(await page.locator('#restoreBtn').isDisabled(), true);
  assert.equal(await page.locator('#idea').inputValue(), before.text);
  assert.equal(await page.locator('#tags').inputValue(), before.tags);
}
try {
  if (process.env.CAPTURE_EXPECTED_HEAD) assert.equal(report.head, process.env.CAPTURE_EXPECTED_HEAD);
  await new Promise((resolve, reject) => {server.once('error', reject); server.listen(0, '127.0.0.1', resolve);});
  const address = `http://127.0.0.1:${server.address().port}/`;
  browser = await chromium.launch({headless: true, timeout: 30_000});
  report.browser = browser.version();
  for (const width of [375, 768, 1440]) {
    const context = await browser.newContext({acceptDownloads: true, viewport: {width, height: 900}, reducedMotion: 'reduce'});
    try {
      // The test does not need third-party fonts or any external network endpoint.
      await context.route('**/*', route => route.request().url().startsWith(address)
        ? route.continue() : route.abort());
      let page = await context.newPage();
      const trackPage = candidate => {
        candidate.setDefaultTimeout(10_000);
        candidate.on('pageerror', error => report.pageErrors.push(String(error)));
      };
      trackPage(page);
      await page.goto(address);
      let saved;
      await check(`${width}: actual Unicode download retains browser input values`, async () => {
        await page.locator('#idea').fill('  Synthetic vision: café 漢字 🧠\nSecond line\n  ');
        await page.locator('#tags').fill('  arcanea, café, 🧠 , duplicate, duplicate  ');
        const expected = {version: 1, rawText: await page.locator('#idea').inputValue(),
          tags: await page.locator('#tags').inputValue(), source: 'idea-swarm-cockpit', sourceRef: null};
        saved = await download(page);
        assert.deepEqual(JSON.parse(saved.bytes.toString('utf8')), expected);
        assert.equal(await page.locator('#idea').inputValue(), expected.rawText);
        assert.match(await page.locator('#out').textContent(), /Download requested/);
        assert.doesNotMatch(await page.locator('#out').textContent(), /saved and read back exactly/);
      });
      const original = {version: 1, rawText: '  Original\r\n漢字 🧠\r\n  ',
        tags: '  first\r\nsecond, duplicate, duplicate  ', source: 'synthetic-local-export', sourceRef: 'synthetic-note-001'};
      await check(`${width}: BOM file preview requires deliberate keyboard restore and retains provenance`, async () => {
        const before = await page.locator('#idea').inputValue();
        await restore(page, await packetFile(Buffer.from('\ufeff' + JSON.stringify(original), 'utf8')));
        assert.equal(await page.locator('#idea').inputValue(), before);
        await page.locator('#restoreBtn').focus();
        await page.keyboard.press('Enter');
        assert.equal(await page.locator('#idea').inputValue(), original.rawText.replaceAll('\r\n', '\n'));
        assert.equal(await page.evaluate(() => document.activeElement.id), 'idea');
        saved = await download(page);
        assert.deepEqual(JSON.parse(saved.bytes.toString('utf8')), original);
      });
      await check(`${width}: downloaded capture survives closing the page and supports edit/undo`, async () => {
        await page.close();
        page = await context.newPage(); trackPage(page);
        await page.goto(address);
        assert.equal(await page.locator('#idea').inputValue(), '');
        await page.locator('#idea').fill('Unsaved replacement draft');
        await page.locator('#tags').fill('replacement');
        await restore(page, saved.filename);
        await page.locator('#restoreBtn').click();
        const reopened = await download(page);
        assert.deepEqual(JSON.parse(reopened.bytes.toString('utf8')), original);
        await page.locator('#idea').fill('Deliberate edited continuation');
        const edited = JSON.parse((await download(page)).bytes.toString('utf8'));
        assert.equal(edited.rawText, 'Deliberate edited continuation');
        assert.equal(edited.tags, original.tags);
        assert.equal(edited.sourceRef, original.sourceRef);
        await page.locator('#undoRestoreBtn').focus();
        await page.keyboard.press('Enter');
        assert.equal(await page.locator('#idea').inputValue(), 'Unsaved replacement draft');
        assert.equal(await page.locator('#tags').inputValue(), 'replacement');
        assert.equal(await page.locator('#undoRestoreBtn').isDisabled(), true);
      });
      await check(`${width}: ambiguous, malformed and incompatible files preserve the current draft`, async () => {
        const valid = JSON.stringify(original);
        await refusesFile(page, Buffer.from(valid.replace('"version":1', '"version":1,"ver\\u0073ion":1')));
        await refusesFile(page, Buffer.from(JSON.stringify({...original, tags: ['incompatible']})));
        await refusesFile(page, Buffer.from(JSON.stringify({...original, rawText: '\ud800'})));
        await refusesFile(page, Buffer.from([0xff, 0xfe, 0x00]));
        await refusesFile(page, Buffer.alloc(8 * 1024 * 1024 + 1, 0x20));
      });
    } finally {await context.close();}
  }
  const context = await browser.newContext({acceptDownloads: true});
  try {
    await context.route('**/*', route => route.request().url().startsWith(address)
      ? route.continue() : route.abort());
    const page = await context.newPage();
    page.setDefaultTimeout(10_000);
    page.on('pageerror', error => report.pageErrors.push(String(error)));
    await page.goto(address);
    let transfers = 0;
    page.on('download', () => ++transfers);
    const base = {version: 1, rawText: '', tags: '', source: 'idea-swarm-cockpit', sourceRef: null};
    const limit = 8 * 1024 * 1024;
    const overhead = Buffer.byteLength(JSON.stringify(base, null, 2) + '\n');
    const boundaryText = 'x'.repeat(limit - overhead);
    await check('boundary: exact 8 MiB download can be reopened', async () => {
      await page.locator('#idea').fill(boundaryText);
      const saved = await download(page);
      assert.equal(saved.bytes.length, limit);
      await restore(page, saved.filename);
      await page.locator('#restoreBtn').click();
      assert.equal(await page.locator('#idea').inputValue(), boundaryText);
    });
    for (const [name, text, tags, message] of [
      ['one byte above 8 MiB', boundaryText + 'x', '', /exceeds the 8 MiB/],
      ['unpaired text surrogate', '\ud800', '', /invalid Unicode/],
      ['unpaired tag surrogate', 'Valid synthetic draft', '\ud800', /invalid Unicode/],
    ]) await check(`boundary: ${name} refuses download with draft intact`, async () => {
      // DOM assignment is deliberate for malformed UTF-16; it is not a clipboard test.
      await page.evaluate(({text, tags}) => {
        document.getElementById('idea').value = text;
        document.getElementById('tags').value = tags;
      }, {text, tags});
      const before = transfers;
      await page.locator('#captureBtn').click();
      assert.match(await page.locator('#out').textContent(), message);
      assert.equal(await page.locator('#idea').inputValue(), text);
      assert.equal(await page.locator('#tags').inputValue(), tags);
      assert.equal(transfers, before);
    });
  } finally {await context.close();}
  assert.equal(timedOut, false, 'Browser verification exceeded three minutes');
  assert.deepEqual(report.pageErrors, [], 'Unexpected browser runtime errors');
} catch (error) {
  report.failure = String(error);
  process.exitCode = 1;
  console.error(error);
} finally {
  clearTimeout(timer);
  await browser?.close();
  server.closeAllConnections();
  if (server.listening) await new Promise(resolve => server.close(resolve));
  await writeFile(path.join(root, 'capture-browser-report.json'), JSON.stringify(report, null, 2) + '\n');
  const temp = await realpath(tmpdir());
  const fixtures = await realpath(fixtureRoot);
  const relative = path.relative(temp, fixtures);
  assert.ok(relative && !relative.startsWith('..') && !path.isAbsolute(relative)
    && path.basename(fixtures).startsWith('capture-browser-'), 'Refuse cleanup outside owned temporary fixtures');
  await rm(fixtures, {recursive: true, force: true});
}
