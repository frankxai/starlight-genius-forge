const fs=require('node:fs'),assert=require('node:assert/strict');
const path=require('node:path'); const htmlPath=process.argv[2] || path.resolve(__dirname,'../ui/idea-swarm-cockpit.html');
const oldHarness=fs.readFileSync(path.resolve(path.dirname(htmlPath),'../scripts/test_save_restore_v7.js'),'utf8').split('let passed=0;')[0];
const {setup,file,packet}=new Function('require','process',oldHarness+'\nreturn {setup,file,packet};')(require,{argv:['node','fixture',htmlPath]});
let passed=0;const failures=[];
async function test(name,run){try{await run();passed++;}catch(e){failures.push({name,error:e.message});}}
function duplicate(key,value,encodedKey=JSON.stringify(key)){const original=JSON.stringify(packet());return original.slice(0,-1)+','+encodedKey+':'+JSON.stringify(value)+'}';}
async function reject(text){const x=setup();const before={text:x.els.idea.value,tags:x.els.tags.value};await x.restore(file(text));assert.equal(x.els.restoreBtn.disabled,true,'ambiguous file must not enable replacement');await x.apply();assert.equal(x.els.idea.value,before.text);assert.equal(x.els.tags.value,before.tags);assert.match(x.els.restorePreview.textContent,/could not/);}
(async()=>{
 for(const key of ['version','rawText','tags','source','sourceRef'])await test('reject duplicate '+key,()=>reject(duplicate(key,key==='version'?1:'silently substituted')));
 for(const key of ['version','rawText','tags','source','sourceRef'])await test('reject equal duplicate '+key,()=>reject(duplicate(key,packet()[key])));
 await test('reject escaped rawText duplicate',()=>reject(duplicate('rawText','substituted','"\\u0072awText"')));
 await test('reject escaped version duplicate',()=>reject(duplicate('version',1,'"\\u0076ersion"')));
 await test('reject three rawText keys',()=>reject(duplicate('rawText','second').slice(0,-1)+',"rawText":"third"}'));
 await test('reject duplicate after an earlier valid selection',async()=>{const x=setup();await x.restore(file(packet()));assert(!x.els.restoreBtn.disabled);await x.restore(file(duplicate('rawText','different')));assert(x.els.restoreBtn.disabled);});
 for(const rawText of ['{"rawText":"quoted value", "rawText":"literal data"}','comma, brace } bracket [ colon : and escaped \\ quote "','🧠 中文\r\nrawText sourceRef "source"', 'before\\after'])await test('preserve key-like literal '+JSON.stringify(rawText),async()=>{const p={...packet(),rawText};const x=setup();await x.restore(file(p));assert(!x.els.restoreBtn.disabled);await x.apply();await x.save();assert.deepEqual(JSON.parse(x.saved()),p);});
 await test('escaped unique field names preserve exact values',async()=>{const text=JSON.stringify(packet()).replace('"rawText":','"\\u0072awText":');const x=setup();await x.restore(file(text));assert(!x.els.restoreBtn.disabled);await x.apply();await x.save();assert.deepEqual(JSON.parse(x.saved()),packet());});
 await test('whitespace reordered unique fields accepted',async()=>{const p=packet();const text=' {\n'+Object.keys(p).reverse().map(k=>JSON.stringify(k)+':'+JSON.stringify(p[k])).join(',\n')+'\n} ';const x=setup();await x.restore(file(text));assert(!x.els.restoreBtn.disabled);await x.apply();await x.save();assert.deepEqual(JSON.parse(x.saved()),p);});
 await test('nested value stays rejected',()=>reject(JSON.stringify({...packet(),tags:{rawText:1}})));
 await test('trailing comma stays rejected',()=>reject(JSON.stringify(packet()).slice(0,-1)+',}'));
 console.log(JSON.stringify({tests:passed+failures.length,passed,failed:failures.length,failures}));process.exitCode=failures.length?1:0;
})();
