const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const {webcrypto} = require('node:crypto');
const html = fs.readFileSync(process.argv[2], 'utf8');
const script = html.match(/<script>([\s\S]*?)<\/script>/)[1];
const raw = '\ufeff  '+ 'vision 🧠 中文\r\n'.repeat(230) + '$(`unsafe`) "quote" <script>data</script>\n  ';
const tags = 'hardware, $(`unsafe`), "quotes"';
function setup(fail=false) {
  const make = () => ({value:'',textContent:'', handlers:{}, addEventListener(k,v){this.handlers[k]=v;}});
  const els = Object.fromEntries(['idea','tags','out','captureBtn','clearBtn'].map(k=>[k,make()]));
  const stages = Array.from({length:6},(_,i)=>({classList:{values:new Set(i===0?['active']:[]), toggle(k,on){on?this.values.add(k):this.values.delete(k);},add(k){this.values.add(k);},remove(k){this.values.delete(k);}}}));
  const blobs = [], links = [], revoked = [], timers=[];
  const document = {getElementById:k=>els[k],querySelectorAll:()=>stages,body:{appendChild(){}},createElement(){const link={click(){if(fail)throw Error('synthetic download failure');},remove(){this.removed=true;}};links.push(link);return link;}};
  const URL = {createObjectURL(b){blobs.push(b);return 'blob:synthetic';},revokeObjectURL(u){revoked.push(u);}};
  vm.runInNewContext(script,{document,Blob,URL,crypto:webcrypto,setTimeout:(f,ms)=>timers.push([f,ms])});
  els.idea.value=raw;els.tags.value=tags;
  return {els,stages,blobs,links,revoked,timers,click:()=>els.captureBtn.handlers.click(),clear:()=>els.clearBtn.handlers.click()};
}
let passed=0;const failures=[];
async function test(name,fn){try{await fn();passed++;}catch(e){failures.push({name,error:e.message});}}
(async()=>{
  await test('entire exact Unicode whitespace and tags payload',async()=>{const x=setup();x.click();assert.equal(x.blobs.length,1);const bytes=Buffer.from(await x.blobs[0].arrayBuffer());const p=JSON.parse(bytes.toString('utf8'));assert.equal(p.rawText,raw);assert.equal(p.tags,tags);assert.equal(p.source,'idea-swarm-cockpit');assert.equal(p.sourceRef,null);assert.equal(p.version,1);if(process.argv[3])fs.writeFileSync(process.argv[3],bytes);});
  await test('capture pending and no invented downstream completion',()=>{const x=setup();x.click();assert.match(x.els.out.textContent,/pending/i);assert(x.stages[0].classList.values.has('active'));assert(x.stages.every(s=>!s.classList.values.has('done')));assert(x.stages.slice(1).every(s=>!s.classList.values.has('active')));});
  await test('command contains no executable user text or tags',()=>{const x=setup();x.click();assert(!x.els.out.textContent.includes('$('));assert(!x.els.out.textContent.includes('unsafe'));assert(x.els.out.textContent.includes(`--packet "path/to/${x.links[0].download}"`));});
  await test('download does not clear editable input',()=>{const x=setup();x.click();assert.equal(x.els.idea.value,raw);assert.equal(x.els.tags.value,tags);});
  await test('blank input creates no download',()=>{const x=setup();x.els.idea.value=' \r\n ';x.click();assert.equal(x.blobs.length,0);assert.match(x.els.out.textContent,/Add idea text/);});
  await test('download failure preserves input and honest pending stages',()=>{const x=setup(true);x.click();assert.match(x.els.out.textContent,/could not/);assert.equal(x.els.idea.value,raw);assert.equal(x.els.tags.value,tags);assert(x.stages.every(s=>!s.classList.values.has('done')));assert(x.links[0].removed);});
  await test('temporary link removed without expiring pending download',()=>{const x=setup();x.click();assert(x.links[0].removed);assert.equal(x.revoked.length,0);x.timers.forEach(([fn])=>fn());assert.equal(x.revoked.length,0);assert.match(x.links[0].download,/^idea-capture-[a-f0-9]{32}\.json$/);});
  await test('explicit clear resets fields and stages',()=>{const x=setup();x.click();x.clear();assert.equal(x.els.idea.value,'');assert.equal(x.els.tags.value,'');assert(x.stages[0].classList.values.has('active'));assert(x.stages.every(s=>!s.classList.values.has('done')));});
  console.log(JSON.stringify({tests:8,passed,failed:failures.length,failures}));process.exitCode=failures.length?1:0;
})();
