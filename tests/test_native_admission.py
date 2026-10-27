"""Maker unit/integration tests against disposable SQLite, never native acceptance.

Transaction-positive tests inject an explicitly synthetic public verifier/registry.
Cryptographic mechanics use public verification vectors; no private keys are created.
"""
import base64,copy,json,sqlite3,subprocess,tempfile,threading,unittest
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from datetime import datetime,timedelta,timezone
from pathlib import Path
from unittest.mock import patch
from hg_kseos import native_admission as n
from hg_kseos.spine import SharedSpine
from hg_kseos.errors import InvariantViolation

class RegistryFixture:
    def __init__(self,data):self.data=data
    def snapshot(self):return copy.deepcopy(self.data)

class NativeAdmissionTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)
        for cmd in (['git','init','-q',str(self.root)],['git','-C',str(self.root),'-c','user.name=fixture','-c','user.email=fixture@invalid','commit','--allow-empty','-qm','fixture']):
            subprocess.run(cmd,check=True,capture_output=True)
        self.head=subprocess.check_output(['git','-C',str(self.root),'rev-parse','HEAD'],text=True).strip()
        with n.held_root(self.root) as rootid:self.rootid=rootid
        self.registry={'status':'ACTIVE','mission_id':'UNISSUED-TEST-FIXTURE','source_manifest_sha256':'1'*64,'policy_sha256':'2'*64,'policy_epoch':1,'owner_os_sid':'FIXTURE-OWNER-NOT-OS','max_ttl_seconds':3600,'scope':{'root_identity':self.rootid,'head':self.head,'request_sha256':[],'task_kind':'UNIT-UNREGISTERED-OUTSIDE-FIXTURE'},'keys':{'fixture':{'purposes':list(n.KINDS)}},'task_kinds':{'UNIT-UNREGISTERED-OUTSIDE-FIXTURE':{'state':'REGISTERED','source_sha256':'3'*64,'operations':list(n.PURPOSES)}},'revoked_nonces':[]}
        self.provider=RegistryFixture(self.registry);self.service=n.NativeAdmission(self.provider)
        self.registry['scope']['database_path']=str((self.root/'disposable.db').resolve())
        self.spine=SharedSpine(self.root/'disposable.db',admission=self.service);self.spine.initialize();self.spine.create_project()
        self.spine.register_requirement('R','fixture','fixture','A','fixture','1','fixture')
        self.spine.acquire_lease('R','fixture','test-only-token')
        self.spine.transition_requirement('R','FROZEN','fixture','test-only-token',0,'E','freeze')
        self.request=n.taskspec_request('TS','R','objective','maker',self.root,{'network':'OFF'},['unit'],'evidence')
        self.permit(self.request)
    def tearDown(self):self.temp.cleanup()
    def permit(self,request,operation='create_taskspec',seed='A',generation=0):
        sha=n.digest_request(request)
        if sha not in self.registry['scope']['request_sha256']:self.registry['scope']['request_sha256'].append(sha)
        now=datetime.now(timezone.utc);refs=[]
        for i,kind in enumerate(n.KINDS):
            payload={'profile':n.PROFILE,'reference_kind':kind,'mission_id':self.registry['mission_id'],'source_manifest_sha256':self.registry['source_manifest_sha256'],'subject_sha256':sha,'policy_sha256':self.registry['policy_sha256'],'policy_epoch':1,'operation':operation,'purpose':n.PURPOSES[operation],'nonce':seed*16+str(i),'issued_at':(now-timedelta(seconds=5)).isoformat(),'expires_at':(now+timedelta(minutes=10)).isoformat(),'lease_generation':generation,'root_identity':self.rootid,'head':self.head,'task_kind':'UNIT-UNREGISTERED-OUTSIDE-FIXTURE','evidence_ref':'fixture-only'}
            refs.append({'key_id':'fixture','payload':payload,'signature':'SYNTHETIC-VERIFIER-SEAM-NOT-SIGNED'})
        return {'references':refs,'lease_generation':generation}
    def create(self,bundle=None,**changes):
        q={**self.request,**changes}
        return self.spine.create_taskspec(q['target_id'],q['requirement_id'],q['objective'],q['owner'],Path(q['root']),q['permissions'],q['tests'],q['evidence_plan'],admission_bundle=bundle)
    def rows(self):
        with self.spine.connect() as c:
            return tuple(c.execute('SELECT COUNT(*) FROM '+t).fetchone()[0] for t in ('taskspecs','native_admission_nonces','native_admission_leases'))+(c.execute("SELECT COUNT(*) FROM canonical_events WHERE entity_type='native_admission'").fetchone()[0],)
    def rejected(self,bundle,code):
        before=self.rows()
        with patch.object(n,'verify_signature',return_value=None):
            with self.assertRaisesRegex(InvariantViolation,code):self.create(bundle)
        self.assertEqual(self.rows(),before)
    def test_unsigned_default_receiver_refuses(self):
        self.rejected(None,'BUNDLE_REQUIRED')
    def test_real_missing_protected_registry_refuses(self):
        self.spine.admission=n.NativeAdmission();bundle=self.permit(self.request)
        with patch.object(n,'REGISTRY',self.root/'absent-registry.json'):
            with self.assertRaisesRegex(InvariantViolation,'TRUST_BOOTSTRAP_REQUIRED'):self.create(bundle)
        self.assertEqual(self.rows(),(0,0,0,0))
    def test_transaction_positive_synthetic_verifier(self):
        with patch.object(n,'verify_signature',return_value=None):self.create(self.permit(self.request))
        self.assertEqual(self.rows(),(1,3,1,1))
    def test_fail_after_entity_insert_rolls_back_all(self):
        original=self.spine._insert_taskspec
        def fault(*args):original(*args);raise RuntimeError('fault-after-insert')
        with patch.object(self.spine,'_insert_taskspec',side_effect=fault),patch.object(n,'verify_signature',return_value=None):
            with self.assertRaisesRegex(RuntimeError,'fault-after-insert'):self.create(self.permit(self.request))
        self.assertEqual(self.rows(),(0,0,0,0))
    def test_duplicate_entity_rolls_back_new_nonces(self):
        with patch.object(n,'verify_signature',return_value=None):
            self.create(self.permit(self.request))
            before=self.rows()
            with self.assertRaises(sqlite3.IntegrityError):self.create(self.permit(self.request,seed='B',generation=1))
            self.assertEqual(self.rows(),before)
    def test_lease_CAS_wrong_generation(self):
        self.rejected(self.permit(self.request,generation=2),'LEASE_CAS')
    def test_nonce_replay(self):
        b=self.permit(self.request)
        with patch.object(n,'verify_signature',return_value=None):self.create(b)
        self.rejected(b,'REPLAY_OR_LEASE_CONFLICT')
    def test_concurrent_duplicate_only_one_commits(self):
        b=self.permit(self.request);barrier=threading.Barrier(2)
        def go():
            barrier.wait()
            try:self.create(b);return 'COMMIT'
            except InvariantViolation:return 'REFUSE'
        with patch.object(n,'verify_signature',return_value=None),ThreadPoolExecutor(max_workers=2) as pool:
            results=list(pool.map(lambda _:go(),range(2)))
        self.assertCountEqual(results,['COMMIT','REFUSE']);self.assertEqual(self.rows(),(1,3,1,1))
    def test_actual_API_subject_tamper(self):
        b=self.permit(self.request)
        with patch.object(n,'verify_signature',return_value=None):
            with self.assertRaisesRegex(InvariantViolation,'REQUEST_SCOPE'):self.create(b,objective='other')
        self.assertEqual(self.rows(),(0,0,0,0))
    def test_wrong_bindings_table(self):
        for field,value in [('mission_id','foreign'),('source_manifest_sha256','f'*64),('subject_sha256','f'*64),('policy_epoch',2),('operation','create_workorder'),('root_identity','wrong'),('head','f'*40),('purpose','WRONG')]:
            with self.subTest(field=field):
                b=self.permit(self.request);b['references'][0]['payload'][field]=value;self.rejected(b,'SAME_SUBJECT_BINDING')
    def test_expired(self):
        b=self.permit(self.request);b['references'][0]['payload']['expires_at']='2000-01-01T00:00:00Z';self.rejected(b,'EXPIRED')
    def test_revoked(self):
        b=self.permit(self.request);self.registry['revoked_nonces']=[b['references'][0]['payload']['nonce']];self.rejected(b,'REVOKED')
    def test_unregistered_kind(self):
        self.registry['task_kinds']={};self.rejected(self.permit(self.request),'UNREGISTERED_KIND')
    def test_caller_verified_rejected(self):
        b=self.permit(self.request);b['verified']=True;self.rejected(b,'BUNDLE_REQUIRED')
    def test_wrong_key_purpose(self):
        self.registry['keys']['fixture']['purposes']=[];self.rejected(self.permit(self.request),'KEY_PURPOSE')
    def test_foreign_kind_scope(self):
        b=self.permit(self.request);b['references'][0]['payload']['task_kind']='OTHER';self.rejected(b,'TASK_KIND_SCOPE')
    def test_wrong_reference_kinds(self):
        b=self.permit(self.request);b['references'][0]['payload']['reference_kind']='other';self.rejected(b,'REFERENCE_KINDS')
    def test_root_identity_tamper(self):
        self.registry['scope']['root_identity']='other';b=self.permit(self.request)
        for r in b['references']:r['payload']['root_identity']='other'
        self.rejected(b,'ROOT_ID')
    def test_actual_HEAD_change(self):
        b=self.permit(self.request)
        subprocess.run(['git','-C',str(self.root),'-c','user.name=fixture','-c','user.email=fixture@invalid','commit','--allow-empty','-qm','changed'],check=True,capture_output=True)
        self.rejected(b,'ROOT_HEAD')
    def test_policy_changes_during_transaction(self):
        original=self.provider.snapshot;counter=0
        def drifting():
            nonlocal counter;counter+=1;data=original()
            if counter>1:data['policy_epoch']=2
            return data
        with patch.object(self.provider,'snapshot',side_effect=drifting):self.rejected(self.permit(self.request),'POLICY_CHANGED')
    def test_workorder_uses_persisted_task_permissions(self):
        with patch.object(n,'verify_signature',return_value=None):self.create(self.permit(self.request))
        with self.spine.connect() as c:t=c.execute('SELECT * FROM taskspecs').fetchone();request=n.workorder_request('WO',t,'codex',self.root,self.head)
        b=self.permit(request,'create_workorder',seed='W')
        with self.spine.transaction() as c:c.execute("UPDATE taskspecs SET permissions_json='{}'")
        with patch.object(n,'verify_signature',return_value=None):
            with self.assertRaisesRegex(InvariantViolation,'REQUEST_SCOPE'):self.spine.create_workorder('WO','TS','codex',self.root,self.head,admission_bundle=b)
        with self.spine.connect() as c:self.assertEqual(c.execute('SELECT COUNT(*) FROM workorders').fetchone()[0],0)
    def test_workorder_positive_synthetic_verifier(self):
        with patch.object(n,'verify_signature',return_value=None):self.create(self.permit(self.request))
        with self.spine.connect() as c:t=c.execute('SELECT * FROM taskspecs').fetchone();q=n.workorder_request('WO',t,'codex',self.root,self.head)
        with patch.object(n,'verify_signature',return_value=None):self.spine.create_workorder('WO','TS','codex',self.root,self.head,admission_bundle=self.permit(q,'create_workorder',seed='W'))
        with self.spine.connect() as c:
            self.assertEqual(c.execute('SELECT COUNT(*) FROM workorders').fetchone()[0],1)
            self.assertEqual(c.execute("SELECT COUNT(*) FROM canonical_events WHERE entity_type='native_admission'").fetchone()[0],2)
    def test_windows_root_handle_blocks_rename(self):
        import os
        if os.name!='nt':self.skipTest('Windows share-delete semantics')
        with n.held_root(self.root):
            with self.assertRaises(OSError):self.root.rename(self.root.with_name(self.root.name+'-moved'))

class CanonicalAndCryptoTests(unittest.TestCase):
    def test_public_RFC8032_and_tamper(self):
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
        from cryptography.hazmat.primitives import serialization
        public=Ed25519PublicKey.from_public_bytes(bytes.fromhex('d75a980182b10ab7d54bfed3c964073a0ee172f3daa62325af021a68f707511a')).public_bytes(serialization.Encoding.DER,serialization.PublicFormat.SubjectPublicKeyInfo)
        sig=bytes.fromhex('e5564300c360ac729086e2cc806e828a84877f1eb8e5d974d873e065224901555fb8821590a33bacc61e39701cf9b46bd25bf5f0595bbe24655141438e7a100b')
        key={'algorithm':'Ed25519','public_spki_b64':base64.b64encode(public).decode()}
        n.verify_signature(key,base64.b64encode(sig).decode(),b'')
        with self.assertRaisesRegex(InvariantViolation,'SIGNATURE'):n.verify_signature(key,base64.b64encode(sig).decode(),b'x')
    def test_cross_language_actual_node(self):
        script=Path(__file__).resolve().parents[1]/'scripts/native-canonical.js'
        for obj in ({'z':True,'a':[None,False,42,-2,{'10':1,'2':'quote"slash\\'}]}, {'':'','epoch':9007199254740991},{}):
            actual=subprocess.run(['node',str(script)],input=json.dumps(obj).encode(),capture_output=True,check=True).stdout
            self.assertEqual(actual,n.canonical(obj))
    def test_restricted_profile_refuses_ambiguous_types(self):
        for obj in ({'x':1.2},{'x':float('nan')},{'x':2**53},{'x':'中文'},{'x':'\ud800'},{'x':'\n'}):
            with self.subTest(obj=repr(obj)),self.assertRaises(InvariantViolation):n.canonical(obj)
    def test_duplicate_JSON(self):
        with self.assertRaisesRegex(InvariantViolation,'DUPLICATE_KEY'):n.strict_json('{"x":1,"x":2}')

if __name__=='__main__':unittest.main()
