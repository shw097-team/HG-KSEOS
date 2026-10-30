from prepare import *
from first_work import module
import time,copy,sqlite3,platform,contextlib,io,unittest,socket
from unittest.mock import patch
def main():
 tick=time.perf_counter();results=[];core=module('handoff_check_core',E/'READERS/sbl-tpm-sp/scripts/core.py');pplug=E/'READERS/sbl-tpm-sp'
 sys.path.insert(0,plain(E/'READERS/PIPD/src'));sys.path.insert(0,plain(E/'READERS/HG-KSEOS/src'))
 from pipd_ls_sp import pipeline,validate,profiles,errors
 from hg_kseos import native_admission
 from hg_kseos.spine import SharedSpine
 from hg_kseos.util import sha256_text
 schemas=E/'READERS/PIPD/schemas';pi=read(A/'PI-PKG.json');ts=read(A/'TaskSpecSeed.json')
 def check(name,fn,expected=None):
  try:
   value=fn()
   if expected is not None and value!=expected:raise AssertionError(f'expected {expected!r}; actual {value!r}')
   results.append({'case':name,'status':'PASS','actual':value,'scope':'AUTHOR_STATIC_ORIGINAL_READER_ONLY'})
  except Exception as exc:results.append({'case':name,'status':'FAIL','actual':type(exc).__name__+':'+str(exc),'scope':'AUTHOR_STATIC_ORIGINAL_READER_ONLY'})
 def refusal(fn):
  try:fn()
  except Exception as exc:return {'type':type(exc).__name__,'first_fail':str(exc),'code':getattr(exc,'code',None)}
  raise AssertionError('EXPECTED_NACK_BUT_ACCEPTED')
 check('FUNCTIONAL_PI_FULL_MEMBER_READER',lambda:pipeline.validate_pi(pi,schemas)['verdict'],'PASS')
 check('EMPTY_GOAL',lambda:refusal(lambda:pipeline.intake('',sources=[plain(A/'FIRST_WORK_FUNCTIONAL_SOURCE.md')]))['code'],'INTAKE_INVALID')
 check('FOREIGN_OR_MISSING_SOURCE',lambda:refusal(lambda:pipeline.intake('ordinary goal',sources=[plain(A/'absent_source')]))['code'],'AUTHORITY_UNKNOWN')
 check('CORPUS24',lambda:len(core.corpus_manifest(pplug)['files']),24)
 check('PATH_ESCAPE',lambda:refusal(lambda:core.read_contained(pplug,'../outside'))['first_fail'],'PATH_ESCAPE')
 # Mutate only the tiny manifest fixture while pointing at no real source; the original Reader refuses.
 temp=E/'TEST_FIXTURES/TAMPERED_CORPUS';temp.mkdir(parents=True,exist_ok=True)
 shutil.copytree(pplug/'references/corpus',temp/'references/corpus',dirs_exist_ok=True)
 mf=read(temp/'references/corpus/SourceManifest.json');p=temp/mf['files'][0]['path'];p.write_bytes(p.read_bytes()+b'\nTAMPERED_TEST_ONLY\n')
 check('SOURCE_SHA_DRIFT',lambda:refusal(lambda:core.corpus_manifest(temp))['first_fail'],'SOURCE_DRIFT')
 ledger=core.QuestionLedger();source_sha=sha((A/'FIRST_WORK_FUNCTIONAL_SOURCE.md').read_bytes());ledger.record('Q1',pi['subject_id'],'WP15',source_sha,answer='known')
 check('KNOWNANSWER_NO_REASK',lambda:ledger.inspect('Q1',pi['subject_id'],'WP15',source_sha)['ask'],False)
 check('KNOWNANSWER_SOURCE_CHANGED',lambda:ledger.inspect('Q1',pi['subject_id'],'WP15','0'*64)['ask'],True)
 source_spec=read(A/'RUN/ProductSPEC.json');data={k:v for k,v in source_spec.items() if k not in ['schema','status']}
 for field in ['persona','jtbd','fuo']:
  bad=copy.deepcopy(data);bad.pop(field)
  check('PRODUCT_REQUIRED_'+field,lambda b=bad:refusal(lambda:core.plan_spec('Product',b))['first_fail'],'SPEC_REQUIRED_FIELDS')
 bad=copy.deepcopy(data);bad['acceptance'][0].pop('negative');check('PRODUCT_OWN_NEG_REQUIRED',lambda:refusal(lambda:core.plan_spec('Product',bad))['first_fail'],'SPEC_ACCEPTANCE_ORPHAN')
 arch=read(A/'RUN/ArchitectureSPEC.json');ad={k:v for k,v in arch.items() if k not in ['schema','status']};ad['ownership_seams'][0]['writers'].append('second_writer')
 check('ONE_WRITER_SEAM',lambda:refusal(lambda:core.plan_spec('Architecture',ad))['first_fail'],'ONE_WRITER_PER_SEAM')
 check('DAG_CYCLE',lambda:refusal(lambda:core.affected_work({'A':['B'],'B':['A']},[]))['first_fail'],'DAG_CYCLE_OR_UNKNOWN_DEPENDENCY')
 dag={n['id']:n['depends_on'] for n in read(A/'ORIGINAL_22_WP_DAG.json')['nodes']};all_ready=core.affected_work(dag,[]);check('ORIGINAL22_DAG_ACYCLIC',lambda:len(all_ready['order']),22)
 partial=core.affected_work(dag,['WP-FHS-02']);write(E/'OPS_PARK_AFFECTED_CONE.json',partial)
 check('MISSING_OPS_DOES_NOT_BLOCK_FIRST_WORK',lambda:all(x in partial['ready'] for x in ['WP-FHS-00','WP-FHS-01','WP-FHS-05','WP-FHS-15']),True)
 check('CAP_BOOT_BEFORE_FIRST_EFFECT',lambda:all_ready['order'].index('WP-FHS-17')<all_ready['order'].index('WP-FHS-06'),True)
 check('PROFILE_PROVIDER_OFF_SAFETY_VETO',lambda:profiles.compute_profile('LITE',axes=['intent'],provider_off_required=True)['profile'],'STANDARD')
 with patch('socket.create_connection',side_effect=RuntimeError('AUTHOR_PROVIDER_OFF_NETWORK_DENY')) as net:
  check('OFFLINE_ORIGINAL_READER_ZERO_NETWORK',lambda:(core.corpus_manifest(pplug) is not None and pipeline.validate_pi(pi,schemas)['verdict']=='PASS' and net.call_count==0),True)
  check('PROVIDER_OFF_CONNECTION_ATTEMPT_DENIED',lambda:refusal(lambda:socket.create_connection(('provider.invalid',443)))['first_fail'],'AUTHOR_PROVIDER_OFF_NETWORK_DENY')
 # Real original PD binder validates a measured isolated document fixture, not a fabricated live root.
 root=E/'TEST_FIXTURES/PD_RECEIVER_ROOT';scope=root/'src/first_work';scope.mkdir(parents=True,exist_ok=True)
 for name in ['ProductSPEC','ArchitectureSPEC','ProgramSPEC']:shutil.copy2(A/'RUN'/f'{name}.json',scope/f'{name}.json')
 pd=pipeline.bind_pd(pi,{'root':plain(root),'writable_scope':'src/first_work/**'});write(E/'PD_BINDER_FIXTURE_OUTPUT.json',pd)
 check('PD_ORIGINAL_SCHEMA_READER',lambda:validate.validate_bundle({'PD-PKG':pd},schemas)['verdict'],'PASS')
 check('PD_CONTEXT_ACTUALLY_PROBED',lambda:pd['RepoContext']['tracked_files']>=3,True)
 check('PD_MISSING_CONTEXT_REFUSED',lambda:refusal(lambda:pipeline.bind_pd(pi,None))['code'],'REPO_CONTEXT_MISSING')
 check('PD_SPOOF_FRESHNESS_REFUSED',lambda:refusal(lambda:pipeline.bind_pd(pi,{'root':plain(root),'writable_scope':'src/first_work/**','currentness':'FRESH','currentness_epoch':'0'*64}))['code'],'STALE_PROVIDER')
 check('PD_UNBOUNDED_SCOPE_REFUSED',lambda:refusal(lambda:pipeline.bind_pd(pi,{'root':plain(root),'writable_scope':'**'}))['code'],'EFFECT_UNKNOWN')
 # The original HGK pure request constructors are exercised. No authorize/create_* call is made.
 req=native_admission.taskspec_request('STATIC-TEST-TS-WP15','STATIC-TEST-REQ-WP15',ts['goal'],'original TPM/PIPD owner',Path(plain(root)),{'SOURCE_READ':True,'LOCAL_DRAFT':True,'provider_off':True},['first_work source/POS/NEG'],'same source SHA + same candidate hash')
 task={'taskspec_id':'STATIC-TEST-TS-WP15','writable_root':plain(root),'permissions_json':json.dumps(req['permissions']),'requirement_id':'STATIC-TEST-REQ-WP15'}
 woreq=native_admission.workorder_request('STATIC-TEST-WO-WP15',task,'codex',Path(plain(root)),'STATIC-FIXTURE-HEAD-NOT-A-LIVE-COMMIT')
 write(E/'HGK_PURE_REQUEST_CONSTRUCTOR_READBACK.json',{'taskspec_request':req,'workorder_request':woreq,'canonical_state_created':False,'admission_invoked':False,'ids':'STATIC_TEST_ONLY_NOT_HERMES_WORKID'})
 check('ORIGINAL_HGK_REQUEST_CONSTRUCTORS_ACCEPT',lambda:woreq['taskspec_id']==req['target_id'],True)
 check('HGK_FOREIGN_WORKTREE_REFUSED',lambda:refusal(lambda:native_admission.workorder_request('STATIC-TEST-WO',task,'codex',Path(plain(root.parent/'foreign')),'fixture'))['first_fail'],'ERR_NATIVE_TASKSPEC_ROOT')
 # In-memory SQLite is a fixture connection only; there is no new persistent queue or live Spine.
 con=sqlite3.connect(':memory:');con.row_factory=sqlite3.Row;con.execute('CREATE TABLE leases(resource_id TEXT,holder TEXT,token_hash TEXT,expires_at TEXT)')
 con.execute('INSERT INTO leases VALUES(?,?,?,?)',('STATIC-TEST-WORKID','fixture-worker',sha256_text('fixture-token'),'2099-01-01T00:00:00Z'))
 check('ORIGINAL_LEASE_GUARD_POS',lambda:(SharedSpine._assert_lease(None,con,'STATIC-TEST-WORKID','fixture-worker','fixture-token') is None),True)
 con.execute("UPDATE leases SET expires_at='2000-01-01T00:00:00Z'")
 check('OLD_LEASE_REFUSED',lambda:refusal(lambda:SharedSpine._assert_lease(None,con,'STATIC-TEST-WORKID','fixture-worker','fixture-token'))['first_fail'],'ERR_LEASE_EXPIRED:STATIC-TEST-WORKID');con.close()
 check('UNKNOWN_EFFECT_RECONCILE_BEFORE_RETRY',lambda:core.effect_route('HOST',outcome='UNKNOWN_EFFECT')['next'],'RECONCILE_BEFORE_RETRY')
 check('NO_LIVE_RECEIPT_FOR_READONLY',lambda:core.effect_route('READ_ONLY')['status'],'READY')
 check('NO_FALSE_INDEPENDENT_CHECKER',lambda:refusal(lambda:pipeline.compile_tqaep(pi,{},maker='maker',checker=' maker ',checker_execution_receipt=''))['code'],'TQ_SOD')
 tampered=copy.deepcopy(pi);tampered['stable_semantic_contract']['atoms'][0]['risk_guard']['oracle']['expected']='forbidden'
 check('PI_ATOM_TAMPER_REFUSED',lambda:pipeline.validate_pi(tampered,schemas)['verdict'],'FAIL')
 extra=copy.deepcopy(pi);extra['native_permit']='fake';check('PI_UNDECLARED_AUTHORITY_REFUSED',lambda:pipeline.validate_pi(extra,schemas)['verdict'],'FAIL')
 # A small subset of the existing original tests, with their names and raw stream preserved.
 sys.path.insert(0,plain(E/'READERS/PIPD'))
 suite=unittest.defaultTestLoader.loadTestsFromNames(['tests.test_atomic_requirements.ClauseBoundCompiler.test_every_atom_traces_orphan_free','tests.test_atomic_requirements.ClauseBoundCompiler.test_normative_claim_without_source_is_refused','tests.test_atomic_requirements.ClauseBoundCompiler.test_semantic_collapse_is_refused','tests.test_negative_and_rollback.TestNegative.test_workorder_candidate_must_be_candidate_only','tests.test_negative_and_rollback.TestNegative.test_execution_binding_ack_requires_receiver_binding'])
 # Prefix snapshot test path only; all test outputs stay under this delivery directory.
 buf=io.StringIO();runner=unittest.TextTestRunner(stream=buf,verbosity=2);old=runner.run(suite);textfile(E/'EXISTING_AFFECTED_TESTS_RAW.txt',buf.getvalue());check('EXISTING_5_AFFECTED_TESTS',lambda:old.wasSuccessful(),True)
 report={'scope':'WP15 functional PI + WP00/WP01 prerequisites + receiver contracts only','tests':results,'pass':sum(x['status']=='PASS' for x in results),'fail':sum(x['status']=='FAIL' for x in results),'elapsed_seconds':time.perf_counter()-tick,'native':'NATIVE_NOT_RUN','claim':'STATIC_HANDOFF_CONTRACT_ONLY','PD_fixture_is_live_RepoContext':False}
 write(E/'MINIMAL_STATIC_TESTS.json',report);print(json.dumps({'pass':report['pass'],'fail':report['fail'],'failures':[r for r in results if r['status']=='FAIL']},ensure_ascii=False));return 1 if report['fail'] else 0
if __name__=='__main__':sys.exit(main())
