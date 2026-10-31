"""WP17 independent VERIFY_ONLY review; never dispatch installer or access private keys."""
import base64, copy, datetime as dt, hashlib, importlib.util, json, os, sqlite3, subprocess, sys, time
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
sys.dont_write_bytecode = True
ROOT=Path('C:/wg/queue/WP-FHS-17'); OFF=ROOT/'officer'; RUN=OFF/'sitting-20261031002259'
HG=Path('C:/Projects/Agent_Workspace/HG-KSEOS'); NONCE='NONCE-WP-FHS-17-AUTO-20261031002259'
def now(): return dt.datetime.now(dt.timezone.utc).isoformat()
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def rec(p): return {'path':str(p),'state':'PRESENT' if p.is_file() else 'MISSING','sha256':sha(p) if p.is_file() else None,'bytes':p.stat().st_size if p.is_file() else None}
def write(p,obj):
    assert p.resolve().is_relative_to(OFF.resolve())
    p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def read(p): return json.loads(p.read_text(encoding='utf-8'))
start=now(); RUN.mkdir(parents=True,exist_ok=True)
for name in ['verification.raw.json','verdict.json','hash-manifest.json','hash-manifest.receipt.json']:
    p=OFF/name
    if p.is_file(): (RUN/('previous-'+name)).write_bytes(p.read_bytes())
subject=read(ROOT/'evidence/SUBJECT.json'); body=Path(subject['source']['file']).parent
required='''oracle.json
candidate/need.json
candidate/source-pin.json
candidate/package-index.json
candidate/write-set.json
evidence/registry-before.json
evidence/admission.json
evidence/install.json
evidence/fresh-load.json
evidence/invoke.json
fixtures/cap-boot-dependency-inversion.json
fixtures/loaded-origin-mismatch.json
evidence/negative-results.json
evidence/rollback-resume.json
tools/reproduce.ps1
evidence/run-index.json
evidence/registry-after.json'''.splitlines()
external=[Path(subject['source']['file']),body/'08_TECHNOLOGY_DEFAULT_HOTSWAP.md']+[HG/p for p in ['scripts/occupant_install.py','scripts/issue_grant.py','src/hg_kseos/providers.py','src/hg_kseos/native_admission.py','src/hg_kseos/spine.py','src/hg_kseos/cli.py','config/issuer/issuer.pub','config/issuer/OWNER_AUTHORIZATION.json','config/issuer/nonce-ledger.jsonl']]+[Path(p) for p in ['C:/wg/grants/wp17_grant.json','C:/wg/main-merge/evidence/r18/WP0203_17_BINDINGS.json','C:/wg/repo/fhs_msc_handoff_20261030/evidence/WP-FHS-03-04-08-ADMISSION-CHAIN/AO-verdict.json','C:/wg/repo/fhs_msc_handoff_20261030/evidence/WP-FHS-02-POLICY-LOADED-CONSUMER/TRANSCRIPTION.json','C:/wg/ao13/ao_r28j.json']]
inputs=list(dict.fromkeys([ROOT/'brief.md']+sorted(p for p in (ROOT/'evidence').rglob('*') if p.is_file())+[ROOT/p for p in required]+external))
before=[rec(p) for p in inputs]
write(RUN/'check-contract.json',{'nonce':NONCE,'mode':'VERIFY_ONLY','registered_at':start,'maker_oracle':rec(ROOT/'evidence/ORACLE.json'),'frozen_inputs':before,'rule':'PASS requires all native clauses, exact negatives and independent reproducibility. Demonstrated contradictions FAIL; missing Raw alone INCONCLUSIVE. Software signing without HSM is not itself a failed clause.','alias_interpretation':'Appended brief maps uppercase maker evidence for review; no rejection solely for relocation/case.','planned_read_only_probes':['public Ed25519 signature, key id, owner hash, TTL, issuance ledger','validate_grant only with unsigned seam downgrade and existing ABSENT target','standalone inspected print probe'],'no_effect_boundary':'No installer dispatch, issue/init, private key access, canonical state mutation or candidate repair.'})
doc11=external[0].read_text(encoding='utf-8'); doc08=external[1].read_text(encoding='utf-8')
card=doc11.split('<a id="current-b8c0abdfb9dc52ea4f52"></a>',1)[1].split('<a id=',1)[0]
write(RUN/'source-clauses.json',{'card':card,'body08_3_1':doc08.split('### 3.1 ',1)[1].split('### 3.2 ',1)[0],'closing':doc08[doc08.rfind('## R2-08-ASSET：'):],'installer_numbered':[{'line':i,'text':x} for i,x in enumerate((HG/'scripts/occupant_install.py').read_text(encoding='utf-8').splitlines(),1)],'issuer_numbered':[{'line':i,'text':x} for i,x in enumerate((HG/'scripts/issue_grant.py').read_text(encoding='utf-8').splitlines(),1)]})
pkg=read(ROOT/'evidence/PACKAGE_INDEX.json'); checks=[]
for item in pkg['files']:
    p=(Path(pkg['root'])/item['path']).resolve(); assert p.is_relative_to(ROOT.resolve())
    observed=rec(p); checks.append({'declared':item,'observed':observed,'matches':observed['sha256']==item['sha256'] and observed['bytes']==item['bytes']})
grant=read(Path('C:/wg/grants/wp17_grant.json')); pub=base64.b64decode((HG/'config/issuer/issuer.pub').read_text().strip())
payload={k:v for k,v in grant.items() if k not in ('signature_b64','signature_alg','assurance_level')}
signature_valid=False; signature_error=None
try:
    Ed25519PublicKey.from_public_bytes(pub).verify(base64.b64decode(grant['signature_b64']),json.dumps(payload,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')); signature_valid=True
except Exception as e: signature_error=repr(e)
ledger=[json.loads(x) for x in (HG/'config/issuer/nonce-ledger.jsonl').read_text().splitlines() if x.strip()]
grant_check={'signature_valid_against_supplied_public_key':signature_valid,'signature_error':signature_error,'key_id_matches':hashlib.sha256(pub).hexdigest()[:16]==grant['key_id'],'owner_hash_matches':sha(HG/'config/issuer/OWNER_AUTHORIZATION.json')==grant['owner_authorization_sha256'],'ttl_live_at_check':time.time()<grant['expires_at'],'issuance_ledger_rows':[x for x in ledger if x.get('nonce')==grant['nonce']],'admission_digest_matches':sha(Path('C:/wg/grants/wp17_grant.json'))==read(ROOT/'evidence/ADMISSION.json')['grant_sha256'],'ceiling':'Valid signature does not prove original Issuer registration, receiver authorization, nonce spending or canonical target binding. No private key opened.'}
write(RUN/'public-grant-check.json',grant_check)
# Import inspected installer with bytecode disabled; call only its pure validation function.
spec=importlib.util.spec_from_file_location('officer_inspected_installer',HG/'scripts/occupant_install.py'); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
mutant=copy.deepcopy(grant); mutant['assurance_level']='CONFORMANCE_ONLY_TEST_SEAM'; mutant.pop('signature_b64',None); mutant['references']=[{'untrusted':'officer invalid signature control'}]
ws=mutant['writeset']; root=ROOT/'evidence/occupant-root'
result=mod.validate_grant(mutant,ws,root)
write(RUN/'validation-probes.json',{'operation':'validate_grant only; no writes or dispatch','input_grant':rec(Path('C:/wg/grants/wp17_grant.json')),'mutant':mutant,'root':str(root),'targets_before':[rec(root/x['path']) for x in ws],'expected':'Reject unsigned production-grant downgrade and false ABSENT preimage','observed_refusal_code':result,'accepted_by_validator':result is None,'ceiling':'Validation-only counterexample; no native HOST_OP or dedicated WP06 fixture executed.'})
probe=root/'occupant_probe.py'; assert sha(probe)=='22991e801ba7a6f36a5d6e2cfe8c2c26e8736ba2f6b14727ec1d63787c0bea08'
args=[sys.executable,'-B',str(probe),'real-input-20261030']
write(RUN/'probe.command.json',{'args':args,'cwd':str(ROOT),'start':now(),'runtime':sys.version,'executable':rec(Path(sys.executable)),'environment':{'PYTHONDONTWRITEBYTECODE':'1'},'ceiling':'Standalone echo probe, no original Host integration'})
proc=subprocess.run(args,cwd=ROOT,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),capture_output=True,timeout=20)
(RUN/'probe.stdout.txt').write_bytes(proc.stdout); (RUN/'probe.stderr.txt').write_bytes(proc.stderr); write(RUN/'probe.exit.json',{'exit':proc.returncode,'end':now()})
registry={'original_service_readback':'NOT_PERFORMED','reason':'Original SharedSpine._open uses writable sqlite3.connect and PRAGMA journal_mode=WAL outside authorized write root. No relevant connected service tool available.','ceiling':'Supplemental read-only SQLite observation; immutable main file is not live/WAL guaranteed.','attempts':[]}
for suffix in ['?mode=ro','?mode=ro&immutable=1']:
    con=None
    try:
        con=sqlite3.connect((HG/'var/shared-spine/hg-kseos.db').as_uri()+suffix,uri=True,timeout=2); con.row_factory=sqlite3.Row; con.execute('PRAGMA query_only=ON')
        tables=[r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'")]; registry['rows']={}
        for t in ['requirements','acceptances','work_queue','provider_bindings','evidence_refs']:
            if t in tables: registry['rows'][t]=[dict(r) for r in con.execute('SELECT * FROM "'+t+'"') if any(w in json.dumps(dict(r),ensure_ascii=False) for w in ['WP-FHS-17','WP-FHS-00','WP-FHS-02','WP-FHS-03','WP-FHS-06','P0-TOOL','HGK-PROVIDER-FTS5'])]
        registry['attempts'].append({'mode':suffix,'result':'READABLE'}); break
    except sqlite3.Error as e: registry['attempts'].append({'mode':suffix,'error':str(e)})
    finally:
        if con is not None: con.close()
write(RUN/'registry-observation.json',registry)
clauses=[
('PUBLIC_SIGNATURE','PASS' if signature_valid else 'FAIL','Public Ed25519 verification only; software key/HSM ceiling alone does not decide native acceptance.'),
('ORIGINAL_OPS_ADMISSION','FAIL','Validator accepts unsigned downgrade to CONFORMANCE_ONLY_TEST_SEAM. Signed writeset has relative names but no canonical root/object identities or candidate hash. No original Issuer/receiver ACK supplied.'),
('NONCE_PREIMAGE_REPLAY','FAIL','Issuer verify checks nonce exists in issuance ledger, never consumes or rejects a spent nonce. ABSENT targets are not checked for existence; validation-only invalid control accepted with installed targets present.'),
('REAL_CURRENT_NEED','FAIL','85-byte print probe with manifest scope draft, feature probe. No SourceSelectionID/OriginalDisposition, admitted consumer feature or official source/license/dependency pins.'),
('PACKAGE_BYTE_IDENTITY','PASS' if all(x['matches'] for x in checks) else 'FAIL','Every enumerated package and installed file independently hashed. This does not establish loaded-process identity.'),
('SOURCE_SUBJECT_BINDING','PASS' if sha(external[0])==subject['source']['sha256'] and sha(ROOT/'brief.md')==subject['brief']['sha256'] else 'FAIL','Current source and brief compared against SUBJECT byte pins.'),
('FRESH_LOAD_ORIGINAL_CONSUMER','FAIL','Installer records HOST_LOADED after hashing file in parent before subprocess.run. No child PID/session, child-observed loaded origin or original Registry/Consumer ACK.'),
('DAG_INVERSION_NEGATIVE','INCONCLUSIVE','Required otherwise-valid WP06-only mutant/control and exact FIRST_FAIL dispatch/effect trace absent. Installer has no dependency/admission graph check.'),
('LOADED_ORIGIN_MISMATCH_NEGATIVE','FAIL','Tampered negative runs lifecycle to qualification first, then locally compares altered file hash and returns zero. No original loader/consumer rejection, mismatch event or withheld qualification ACK; submitted output truncated.'),
('ROLLBACK_RESUME','INCONCLUSIVE','Uninstall summary lacks per-command Raw and exact preimage accounting; installed files currently exist without reinstall chronology. Same-key no-repeat and UNKNOWN reconciliation not shown. Historical uninstall not disproved.'),
('REPRODUCIBLE_RAW_FRESHNESS','INCONCLUSIVE','Missing frozen run-index, original readbacks, command/environment/stdout/stderr/exit Raw and required dedicated fixture results. Maker frozen flag has no pre-run oracle registration receipt.')]
after=[rec(p) for p in inputs]
verification={'nonce':NONCE,'mode':'VERIFY_ONLY','started_at':start,'ended_at':now(),'input_before':before,'input_after':after,'inputs_stable':before==after,'package_checks':checks,'public_grant_check':grant_check,'validation_probe_accepted_invalid_control':result is None,'standalone_probe_output_matches':proc.returncode==0 and proc.stdout.strip()==b'occupant-ok:real-input-20261030','clause_results':[{'clause':c,'result':r,'finding':f} for c,r,f in clauses],'raw_refs':[str(p.relative_to(ROOT)) for p in sorted(RUN.iterdir()) if p.is_file() and not p.name.startswith('previous-')],'native_reproduction':'NOT_RUN; original bounded admission/consumer chain not established, officer cannot repair or self-accept.','independence':'Only officer outputs written; candidate stable; no installer dispatch or canonical state change.'}
write(OFF/'verification.raw.json',verification)
verdict={'wp':'WP-FHS-17','nonce':NONCE,'author_role':'Independent Acceptance Officer','mode':'VERIFY_ONLY','verdict':'FAIL','accepted':False,'reason':'Signed grant cryptographically verifies, but admission can be bypassed, canonical target and replay/preimage binding are missing, and probe/load/negative evidence does not satisfy native contract.','ceiling':'Independent byte review, public signature check, validation-only counterexample and standalone probe; no native acceptance.','subject_sha256':sha(ROOT/'evidence/SUBJECT.json'),'oracle_sha256':sha(ROOT/'evidence/ORACLE.json'),'manifest_sha256':sha(root/'_package/MANIFEST.json'),'package_index_sha256':sha(ROOT/'evidence/PACKAGE_INDEX.json'),'write_set_sha256':sha(ROOT/'evidence/WRITESET.json'),'brief_sha256':sha(ROOT/'brief.md'),'source_card_file_sha256':sha(external[0]),'body08_sha256':sha(external[1]),'verification_sha256':sha(OFF/'verification.raw.json'),'failed_clauses':[c for c,r,f in clauses if r=='FAIL'],'unverified_clauses':[c for c,r,f in clauses if r=='INCONCLUSIVE'],'host_effect_disposition':'PARK pending original receiver-bound valid OPS admission and complete maker evidence.','canonical_transcription':'NOT_PERFORMED; no successful verdict to transcribe; refusal history preserved.','completed_at':now()}
write(OFF/'verdict.json',verdict)
outputs=[Path(__file__),OFF/'verification.raw.json',OFF/'verdict.json']+sorted(p for p in RUN.iterdir() if p.is_file())
write(OFF/'hash-manifest.json',{'nonce':NONCE,'algorithm':'SHA256','generated_at':now(),'entries':[rec(p) for p in dict.fromkeys(inputs+outputs)],'ceiling':'Finite supplied/indexed bytes and pinned originals; missing required expansions recorded MISSING. No claimed process-loaded hash.','excluded':['officer/hash-manifest.json','officer/hash-manifest.receipt.json']})
write(OFF/'hash-manifest.receipt.json',{'nonce':NONCE,'path':'officer/hash-manifest.json','sha256':sha(OFF/'hash-manifest.json'),'at':now()})
print(json.dumps({'verdict':verdict['verdict'],'inputs_stable':before==after,'signature_valid':signature_valid,'invalid_validation_control_accepted':result is None,'package_matches':all(x['matches'] for x in checks),'probe_output_matches':verification['standalone_probe_output_matches'],'manifest_sha256':sha(OFF/'hash-manifest.json')}))
