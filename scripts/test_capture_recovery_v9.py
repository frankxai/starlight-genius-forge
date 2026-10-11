from pathlib import Path
import importlib.util,json,tempfile,io,contextlib,sys,hashlib
script=Path(sys.argv[1]);out=Path(sys.argv[2]);out.mkdir(exist_ok=True)
spec=importlib.util.spec_from_file_location('capture_recovery_under_test',script);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
cases=[]
def invoke(args):
    stream=io.StringIO()
    with contextlib.redirect_stdout(stream),contextlib.redirect_stderr(stream):
        try:return mod.main(args),None,stream.getvalue()
        except Exception as error:return None,type(error).__name__,stream.getvalue()
for name in ['identity','text_hash','raw_tags_hash','normalized_tags','source_ref_type','card_path','stage','existing_output_conflict']:
    with tempfile.TemporaryDirectory(dir=out) as tmp:
        root=Path(tmp);mod.ROOT=root;mod.IDEAS=root/'docs/ideas';mod.OUTBOX=mod.IDEAS/'_outbox'
        code,error,_=invoke(['--text','Preserve original constellation 🧠\r\nsecond line','--tags',' exact,, 中文 ','--source','codex','--source-ref','task:synthetic-recovery'])
        assert code==0 and error is None
        journal=next((mod.OUTBOX/'_pending').glob('*.json'));meta=json.loads(journal.read_bytes());identity=meta['ideaId']
        if name=='identity':meta['ideaId']=identity+'a'
        elif name=='text_hash':meta['rawText']='changed original'
        elif name=='raw_tags_hash':meta['rawTags']='changed original tags'
        elif name=='normalized_tags':meta['tags']=['substituted']
        elif name=='source_ref_type':meta['sourceRef']={'not':'a locator'}
        elif name=='card_path':meta['cardPath']='other.md'
        elif name=='stage':meta['stage']='completed'
        elif name=='existing_output_conflict':(root/meta['cardPath']).write_bytes(b'Preserve a newer owner edit\n')
        journal.write_bytes(json.dumps(meta,ensure_ascii=False).encode())
        before={str(p.relative_to(root)):p.read_bytes() for p in root.rglob('*') if p.is_file()}
        code,error,output=invoke(['--recover-id',identity])
        after={str(p.relative_to(root)):p.read_bytes() for p in root.rglob('*') if p.is_file()}
        passed=code==2 and error is None and before==after and 'Cannot recover capture:' in output
        cases.append({'case':name,'pass':passed,'exit_code':code,'exception':error,'all_files_unchanged':before==after})
    assert not Path(tmp).exists()
receipt={'source_sha256':hashlib.sha256(script.read_bytes()).hexdigest(),'cases':cases,'passed':sum(x['pass'] for x in cases),'failed':sum(not x['pass'] for x in cases),'scope':'actual Python recovery with damaged synthetic journals; no browser/production claim','temporary_outputs_cleaned':True}
(out/'receipt.json').write_bytes((json.dumps(receipt,indent=2)+'\n').encode());print(json.dumps(receipt))
sys.exit(0 if receipt['failed']==0 else 1)
