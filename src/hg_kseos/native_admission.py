"""Versioned B1 admission seam for the EXISTING SharedSpine (unactivated repair).

OS-protected Owner configuration is required. No local key creation, signing,
second database, scheduler, or caller-asserted trust. Test providers are not native
approval. Root handles here protect assignment of a root to a TaskSpec/WorkOrder;
downstream executors must hold and use their own effect handles before file writes.
"""
from __future__ import annotations
import base64
import ctypes
import hashlib
import json
import os
import re
import sqlite3
import subprocess
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

from .errors import InvariantViolation

PROFILE = 'HGK-B1-ASCII-C14N/1'
DOMAIN = b'HGK-B1-ASCII-C14N/1\x00'
KINDS = ('source_freeze', 'task_kind', 'oracle_ratification')
PURPOSES = {'create_taskspec': 'TASKSPEC_ADMISSION', 'create_workorder': 'WORKORDER_ADMISSION'}
def _programdata():
    if os.name!='nt':return Path('/var/lib')
    buf=ctypes.create_unicode_buffer(32768)
    if ctypes.windll.shell32.SHGetFolderPathW(None,0x23,None,0,buf):refuse('OS_KNOWN_FOLDER')
    return Path(buf.value)

REGISTRY = _programdata()/'HG-KSEOS'/'native-admission'/'registry.json'

def refuse(code):
    raise InvariantViolation('ERR_NATIVE_'+code)

def absolute_root(value):
    """Never infer authority from a caller's current working directory."""
    if not isinstance(value, (str, os.PathLike)) or not str(value):
        refuse('ROOT_ABSOLUTE')
    root = Path(value)
    if not root.is_absolute() or '..' in root.parts:
        refuse('ROOT_ABSOLUTE')
    return root

def _unique(pairs):
    out={}
    for k,v in pairs:
        if k in out:refuse('DUPLICATE_KEY')
        out[k]=v
    return out

def strict_json(data):
    try:return json.loads(data,object_pairs_hook=_unique,parse_constant=lambda _:refuse('NONFINITE'))
    except (ValueError,UnicodeError,TypeError):refuse('JSON')

def canonical(value):
    """Restricted ASCII profile, exact keys/strings; NOT RFC8785 JCS.

    JSON permits Unicode in product fields, so request digests hash the existing
    util.canonical_json UTF-8 bytes. Signed envelope identities use this smaller
    cross-language profile and contain only digests and ASCII identity fields.
    """
    def check(x):
        if x is None or type(x) is bool:return
        if type(x) is int:
            if abs(x)>2**53-1:refuse('CANONICAL_INTEGER')
            return
        if type(x) is str:
            if any(ord(c)<32 or ord(c)>126 for c in x):refuse('CANONICAL_ASCII')
            return
        if type(x) is list:
            for item in x:check(item)
            return
        if type(x) is dict:
            for k,v in x.items():
                if type(k) is not str:refuse('CANONICAL_KEY')
                check(k);check(v)
            return
        refuse('CANONICAL_TYPE')
    check(value)
    return DOMAIN+json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=True).encode('ascii')

def digest_request(request):
    from .util import canonical_json
    return hashlib.sha256(canonical_json(request).encode('utf-8')).hexdigest()

def _time(s):
    try:d=datetime.fromisoformat(s.replace('Z','+00:00'))
    except (AttributeError,ValueError,TypeError):refuse('TIME')
    if d.tzinfo is None:refuse('TIMEZONE')
    return d

def verify_signature(key,signature,message):
    """Real public verification. The Owner selects and approves key algorithm.
    RSA supports an existing Windows machine certificate without exporting a key.
    """
    try:
        from cryptography.hazmat.primitives import hashes,serialization
        from cryptography.hazmat.primitives.asymmetric import ed25519,padding,rsa
        from cryptography.exceptions import InvalidSignature
        raw=base64.b64decode(signature,validate=True)
        if 'public_certificate_der_b64' in key:
            from cryptography import x509
            public=x509.load_der_x509_certificate(base64.b64decode(key['public_certificate_der_b64'],validate=True)).public_key()
        else:
            public=serialization.load_der_public_key(base64.b64decode(key['public_spki_b64'],validate=True))
        if key['algorithm']=='RS256' and isinstance(public,rsa.RSAPublicKey) and public.key_size>=3072:
            public.verify(raw,message,padding.PKCS1v15(),hashes.SHA256())
        elif key['algorithm']=='Ed25519' and isinstance(public,ed25519.Ed25519PublicKey):
            public.verify(raw,message)
        else:refuse('KEY_ALGORITHM')
    except ImportError:refuse('CRYPTO_DEPENDENCY')
    except (ValueError,KeyError,TypeError,InvalidSignature):refuse('SIGNATURE')

def assert_protected(path):
    """Inspect OS owner and every writable ACE on registry and its protected dir.
    Do not run caller commands, read credentials or equate a JSON flag with ACLs.
    """
    if os.name!='nt':refuse('PROTECTED_WINDOWS_READER_REQUIRED')
    # Path is passed as process argv, never interpolated into PowerShell code.
    script=r'''param([string]$RegistryPath)
    $ErrorActionPreference='Stop'
    $paths=@($RegistryPath)
    $cursor=Split-Path -Parent $RegistryPath
    $programData=[Environment]::GetFolderPath('CommonApplicationData')
    while($cursor){$paths+=$cursor;if($cursor -eq $programData){break};$cursor=Split-Path -Parent $cursor}
    foreach($p in $paths){
      $i=Get-Item -LiteralPath $p -Force
      if($i.Attributes -band [IO.FileAttributes]::ReparsePoint){exit 23}
      $a=Get-Acl -LiteralPath $p
      $owner=([Security.Principal.NTAccount]$a.Owner).Translate([Security.Principal.SecurityIdentifier]).Value
      if($owner -notin @('S-1-5-18','S-1-5-32-544')){exit 24}
      if($p -ne $programData -and -not $a.AreAccessRulesProtected){exit 25}
      foreach($r in $a.Access){
        $sid=$r.IdentityReference.Translate([Security.Principal.SecurityIdentifier]).Value
        $mask=if($p -eq $programData){0x000D0040}else{0x000D0156}
        if($r.AccessControlType -eq 'Allow' -and ([int]$r.FileSystemRights -band $mask) -ne 0 -and $sid -notin @('S-1-5-18','S-1-5-32-544')){exit 26}
      }
    }
    'PROTECTED'
    '''
    # -File is used because Windows PowerShell -Command does not bind trailing
    # argv to param reliably. Encoded constant script consumes an env-independent
    # literal path via a separate JSON stdin argument.
    import base64 as b64
    script=script.replace('param([string]$RegistryPath)',"$RegistryPath=[Console]::In.ReadLine()")
    cmd=['powershell.exe','-NoProfile','-NonInteractive','-EncodedCommand',b64.b64encode(script.encode('utf-16-le')).decode('ascii')]
    r=subprocess.run(cmd,input=str(path)+'\n',text=True,capture_output=True,timeout=15)
    if r.returncode or r.stdout.strip()!='PROTECTED':refuse('TRUST_ACL_UNPROTECTED')

class ProtectedRegistry:
    @contextmanager
    def hold_snapshot(self):
        """Keep the protected file and its ancestry pinned through SQL commit.

        A concurrent Owner revoke/replace must retry after an admitted transaction
        releases this read handle; it cannot invalidate half a transaction.
        """
        if not REGISTRY.is_file():refuse('TRUST_BOOTSTRAP_REQUIRED')
        with held_root(REGISTRY.parent):
            assert_protected(REGISTRY)
            with pinned_file(REGISTRY) as stream:
                raw=stream.read()
                assert_protected(REGISTRY)
                data=strict_json(raw)
                if not isinstance(data,dict):refuse('REGISTRY_SCHEMA')
                if data.get('schema')!='HGK-NATIVE-REGISTRY/1' or data.get('canonical_profile')!=PROFILE:refuse('REGISTRY_SCHEMA')
                if data.get('status')!='ACTIVE' or not data.get('owner_os_sid') or not data.get('checker_os_sid'):refuse('REGISTRY_INACTIVE')
                if data['owner_os_sid']==data['checker_os_sid'] or data.get('maker_os_sid') in {data['owner_os_sid'],data['checker_os_sid']}:refuse('PRINCIPAL_SEPARATION')
                if not data.get('maker_os_sid') or not isinstance(data.get('approved_files'),list) or not data['approved_files']:refuse('SOURCE_PINS_REQUIRED')
                absolute_root(data.get('root'))
                yield data

    def snapshot(self):
        with self.hold_snapshot() as data:
            return data

@contextmanager
def held_root(root,expected_identity=None,expected_head=None):
    root=absolute_root(root)
    # Refuse reparse at any ancestor, before resolve hides a junction.
    for p in [root]+list(root.parents):
        if p.is_symlink() or getattr(p.lstat(),'st_file_attributes',0)&0x400:refuse('ROOT_REPARSE')
    if os.name=='nt':
        from ctypes import wintypes as w
        kernel=ctypes.WinDLL('kernel32',use_last_error=True)
        kernel.CreateFileW.argtypes=[w.LPCWSTR,w.DWORD,w.DWORD,w.LPVOID,w.DWORD,w.DWORD,w.HANDLE];kernel.CreateFileW.restype=w.HANDLE
        kernel.CloseHandle.argtypes=[w.HANDLE]
        handles=[]
        try:
            # No FILE_SHARE_DELETE: pin all ancestors against rename/replacement.
            for part in reversed([root]+list(root.parents)):
                h=kernel.CreateFileW(str(part),0x80000000,3,None,3,0x02200000,None)
                if h==w.HANDLE(-1).value:refuse('ROOT_HANDLE')
                handles.append(h)
                opened=(ctypes.c_uint32*13)()
                if not kernel.GetFileInformationByHandle(w.HANDLE(h),ctypes.byref(opened)):refuse('ROOT_HANDLE_ID')
                # Check the OPEN_REPARSE_POINT handle too: a path lstat alone
                # cannot detect replacement between lstat and CreateFileW.
                if opened[0]&0x400 or not opened[0]&0x10:refuse('ROOT_REPARSE')
            info=(ctypes.c_uint32*13)()
            if not kernel.GetFileInformationByHandle(w.HANDLE(handles[-1]),ctypes.byref(info)):refuse('ROOT_HANDLE_ID')
            identity=f'{info[7]:08x}:{info[11]:08x}{info[12]:08x}'
            # BY_HANDLE_FILE_INFORMATION layout: volume serial index 7,
            # file index high/low indices 11/12 (all DWORDs).
            if expected_identity and identity!=expected_identity:refuse('ROOT_ID')
            if expected_head:
                r=subprocess.run(['git','-C',str(root),'rev-parse','HEAD'],capture_output=True,text=True,timeout=10)
                if r.returncode or r.stdout.strip()!=expected_head:refuse('ROOT_HEAD')
            yield identity
        finally:
            for h in reversed(handles):kernel.CloseHandle(h)
    else:
        fd=os.open(root,os.O_RDONLY|getattr(os,'O_DIRECTORY',0)|getattr(os,'O_NOFOLLOW',0))
        try:
            st=os.fstat(fd);identity=f'{st.st_dev}:{st.st_ino}'
            if expected_identity and identity!=expected_identity:refuse('ROOT_ID')
            if expected_head:
                r=subprocess.run(['git','-C',str(root),'rev-parse','HEAD'],capture_output=True,text=True,timeout=10)
                if r.returncode or r.stdout.strip()!=expected_head:refuse('ROOT_HEAD')
            yield identity
        finally:os.close(fd)

@contextmanager
def pinned_file(path):
    path=absolute_root(path)
    # held_root pins all parents before checking/opening the leaf.
    if path.is_symlink() or getattr(path.lstat(),'st_file_attributes',0)&0x400:refuse('REGISTRY_REPARSE')
    if os.name!='nt':
        fd=os.open(path,os.O_RDONLY|getattr(os,'O_NOFOLLOW',0))
        with os.fdopen(fd,'rb') as stream:yield stream
        return
    from ctypes import wintypes as w
    import msvcrt
    kernel=ctypes.WinDLL('kernel32',use_last_error=True)
    kernel.CreateFileW.argtypes=[w.LPCWSTR,w.DWORD,w.DWORD,w.LPVOID,w.DWORD,w.DWORD,w.HANDLE];kernel.CreateFileW.restype=w.HANDLE
    h=kernel.CreateFileW(str(path),0x80000000,1,None,3,0x00200000,None)
    if h==w.HANDLE(-1).value:refuse('REGISTRY_HANDLE')
    kernel.CloseHandle.argtypes=[w.HANDLE]
    try:
        info=(ctypes.c_uint32*13)()
        if not kernel.GetFileInformationByHandle(w.HANDLE(h),ctypes.byref(info)):refuse('REGISTRY_HANDLE_ID')
        if info[0]&0x410:refuse('REGISTRY_REPARSE')
        fd=msvcrt.open_osfhandle(h,os.O_RDONLY|os.O_BINARY)
    except BaseException:
        kernel.CloseHandle(h)
        raise
    with os.fdopen(fd,'rb') as stream:yield stream

def pinned_file_bytes(path):
    with held_root(absolute_root(path).parent):
        with pinned_file(path) as stream:return stream.read()

class NativeAdmission:
    def __init__(self,registry=None):
        # Only host construction may inject a provider; caller API JSON cannot.
        self.registry=registry or ProtectedRegistry()

    @contextmanager
    def authorize(self,connection,operation,request,bundle):
        if not isinstance(bundle,dict) or set(bundle)!={'references','lease_generation'}:refuse('BUNDLE_REQUIRED')
        if operation not in PURPOSES:refuse('OPERATION')
        if not hasattr(connection,'native_guards'):refuse('TRANSACTION_GUARD_REQUIRED')
        if isinstance(self.registry,ProtectedRegistry):
            registry=connection.native_guards.enter_context(self.registry.hold_snapshot())
        else:
            # Explicit host-injected test seam, never selected by caller JSON.
            registry=self.registry.snapshot()
        if registry.get('status')!='ACTIVE':refuse('REGISTRY_INACTIVE')
        database=connection.execute('PRAGMA database_list').fetchone()['file']
        if str(Path(database).resolve())!=registry.get('scope',{}).get('database_path'):refuse('CANONICAL_DATABASE')
        request_sha=digest_request(request);scope=registry.get('scope',{})
        if request_sha not in scope.get('request_sha256',[]):refuse('REQUEST_SCOPE')
        if 'base_head' in request and request['base_head']!=scope.get('head'):refuse('WORKORDER_HEAD')
        root=absolute_root(request['root']);target=request['target_id'];now=datetime.now(timezone.utc)
        if type(bundle['lease_generation']) is not int or bundle['lease_generation'] < 0:refuse('LEASE_GENERATION')
        generation=bundle['lease_generation'];refs=bundle['references']
        if not isinstance(refs,list) or len(refs)!=3:refuse('REFERENCES_REQUIRED')
        for reference in refs:
            if not isinstance(reference,dict) or set(reference)!={'key_id','payload','signature'}:refuse('REFERENCE_SHAPE')
            if not isinstance(reference['payload'],dict):refuse('PAYLOAD_SHAPE')
            if not isinstance(reference['payload'].get('reference_kind'),str):refuse('REFERENCE_KINDS')
        if {x['payload'].get('reference_kind') for x in refs}!=set(KINDS):refuse('REFERENCE_KINDS')
        nonces=[]
        for reference in refs:
            if not isinstance(reference,dict) or set(reference)!={'key_id','payload','signature'}:refuse('REFERENCE_SHAPE')
            p=reference['payload']
            required={'profile','reference_kind','mission_id','source_manifest_sha256','subject_sha256','policy_sha256','policy_epoch','operation','purpose','nonce','issued_at','expires_at','lease_generation','root_identity','head','task_kind','evidence_ref'}
            if not isinstance(p,dict) or set(p)!=required:refuse('PAYLOAD_SHAPE')
            if p['task_kind']!=scope.get('task_kind'):refuse('TASK_KIND_SCOPE')
            kind=p['reference_kind'];key=registry.get('keys',{}).get(reference['key_id'])
            if not key or key.get('revoked') or kind not in key.get('purposes',[]):refuse('KEY_PURPOSE')
            expected={'profile':PROFILE,'mission_id':registry['mission_id'],'source_manifest_sha256':registry['source_manifest_sha256'],'subject_sha256':request_sha,'policy_sha256':registry['policy_sha256'],'policy_epoch':registry['policy_epoch'],'operation':operation,'purpose':PURPOSES[operation],'lease_generation':generation,'head':scope['head'],'root_identity':scope['root_identity']}
            if any(p[k]!=v for k,v in expected.items()):refuse('SAME_SUBJECT_BINDING')
            if type(p['policy_epoch']) is not int or type(p['lease_generation']) is not int:refuse('INTEGER_BINDING')
            start=_time(p['issued_at']);end=_time(p['expires_at'])
            if not start<=now<end or (end-start).total_seconds()>registry['max_ttl_seconds']:refuse('EXPIRED')
            if not re.fullmatch(r'[A-Za-z0-9_-]{16,128}',p['nonce']):refuse('NONCE_SHAPE')
            if p['nonce'] in registry.get('revoked_nonces',[]):refuse('REVOKED')
            if not p['evidence_ref']:refuse('EVIDENCE')
            registered=registry.get('task_kinds',{}).get(p['task_kind'])
            if not registered or registered.get('state')!='REGISTERED' or not registered.get('source_sha256') or operation not in registered.get('operations',[]):refuse('UNREGISTERED_KIND')
            verify_signature(key,reference['signature'],canonical(p))
            nonces.append(p['nonce'])
        if len(set(nonces))!=3:refuse('NONCE_DUPLICATE')
        # Signature, subject, policy and scope checks precede the first SQL write.
        # SharedSpine's guard stack outlives authorize() and closes AFTER commit
        # or rollback; it is per connection, so concurrent transactions do not mix.
        if not hasattr(connection,'native_guards'):refuse('TRANSACTION_GUARD_REQUIRED')
        connection.native_guards.enter_context(held_root(root,scope['root_identity'],scope['head']))
        if 'approved_files' in registry:
            if absolute_root(registry.get('root'))!=root:refuse('ARTIFACT_ROOT')
            if not isinstance(registry['approved_files'],list) or not registry['approved_files']:refuse('SOURCE_PINS_REQUIRED')
            for artifact in registry['approved_files']:
                if not isinstance(artifact,dict) or set(artifact)!={'path','sha256'}:refuse('ARTIFACT_SHAPE')
                rel=artifact['path']
                if not isinstance(rel,str) or not rel or Path(rel).anchor or '..' in Path(rel).parts or ':' in rel:refuse('ARTIFACT_SCOPE')
                if not isinstance(artifact['sha256'],str) or not re.fullmatch('[0-9a-f]{64}',artifact['sha256']):refuse('ARTIFACT_DIGEST')
                path=root/rel
                connection.native_guards.enter_context(held_root(path.parent))
                stream=connection.native_guards.enter_context(pinned_file(path))
                if hashlib.sha256(stream.read()).hexdigest()!=artifact['sha256']:refuse('ARTIFACT_CHANGED')
        if True:
            # Re-read protected policy while in the serialized SharedSpine txn.
            if digest_request(self.registry.snapshot())!=digest_request(registry):refuse('POLICY_CHANGED')
            try:
                for nonce in nonces:connection.execute('INSERT INTO native_admission_nonces(nonce,subject_sha256) VALUES(?,?)',(nonce,request_sha))
                if generation==0:
                    connection.execute('INSERT INTO native_admission_leases(resource_id,generation) VALUES(?,1)',(target,))
                else:
                    result=connection.execute('UPDATE native_admission_leases SET generation=generation+1 WHERE resource_id=? AND generation=?',(target,generation))
                    if result.rowcount!=1:refuse('LEASE_CAS')
            except sqlite3.IntegrityError:refuse('REPLAY_OR_LEASE_CONFLICT')
            event_id='EVT-NATIVE-'+hashlib.sha256(('|'.join(nonces)).encode()).hexdigest()
            connection.execute('''INSERT INTO canonical_events(event_id,idempotency_key,entity_type,entity_id,from_state,to_state,actor,expected_version,resulting_version,payload_json,evidence_ref,rollback_pointer,created_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)''',(event_id,event_id,'native_admission',target,None,'ADMITTED',registry['owner_os_sid'],generation,generation+1,json.dumps({'operation':operation,'request_sha256':request_sha,'receipt_digests':[digest_request(r) for r in refs]},sort_keys=True),refs[0]['payload']['evidence_ref'],'RB-'+target,now.isoformat()))
            yield {'event_id':event_id,'request_sha256':request_sha}
            current=subprocess.run(['git','-C',str(root),'rev-parse','HEAD'],capture_output=True,text=True,timeout=10)
            if current.returncode or current.stdout.strip()!=scope['head']:refuse('HEAD_CHANGED_BEFORE_COMMIT')
            if digest_request(self.registry.snapshot())!=digest_request(registry):refuse('POLICY_CHANGED_BEFORE_COMMIT')
            # This checks mutable refs at both boundaries; it does NOT claim an
            # immutable Git ref/security boundary for a future arbitrary executor.

def taskspec_request(taskspec_id,requirement_id,objective,owner,writable_root,permissions,tests,evidence_plan):
    return {'target_id':taskspec_id,'requirement_id':requirement_id,'objective':objective,'owner':owner,'root':str(absolute_root(writable_root)),'permissions':permissions,'tests':tests,'evidence_plan':evidence_plan}

def workorder_request(workorder_id,taskspec,writer,worktree,base_head):
    root=str(absolute_root(worktree))
    if absolute_root(root)!=absolute_root(taskspec['writable_root']):refuse('TASKSPEC_ROOT')
    return {'target_id':workorder_id,'taskspec_id':taskspec['taskspec_id'],'writer':writer,'root':root,'base_head':base_head,'permissions_json':taskspec['permissions_json'],'requirement_id':taskspec['requirement_id']}
