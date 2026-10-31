"""Independent WP17 evidence review. No installer dispatch or candidate repair."""
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys

ROOT = Path('C:/wg/queue/WP-FHS-17').resolve()
OFF = ROOT / 'officer'
RUN = OFF / 'sitting-20261030233843'
NONCE = 'NONCE-WP-FHS-17-AUTO-20261030233843'
HG = Path('C:/Projects/Agent_Workspace/HG-KSEOS')

def now():
    return dt.datetime.now(dt.timezone.utc).isoformat()

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def record(p):
    return {'path': str(p), 'state': 'PRESENT' if p.is_file() else 'MISSING',
            'sha256': sha(p) if p.is_file() else None,
            'bytes': p.stat().st_size if p.is_file() else None}

def write(p, obj):
    assert p.resolve().is_relative_to(OFF)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def read(rel):
    return json.loads((ROOT / rel).read_text(encoding='utf-8'))

start = now()
RUN.mkdir(parents=True, exist_ok=True)
for name in ('verification.raw.json', 'hash-manifest.json', 'hash-manifest.receipt.json', 'verdict.json'):
    p = OFF / name
    if p.is_file():
        (RUN / ('previous-' + name)).write_bytes(p.read_bytes())
subject = read('evidence/SUBJECT.json')
body = Path(subject['source']['file']).parent
expected = '''oracle.json
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
supplied = sorted((ROOT / 'evidence').rglob('*'))
supplied = [p for p in supplied if p.is_file()]
external = [Path(subject['source']['file']), body / '08_TECHNOLOGY_DEFAULT_HOTSWAP.md',
            HG / 'scripts/occupant_install.py', HG / 'src/hg_kseos/providers.py',
            HG / 'src/hg_kseos/native_admission.py', HG / 'src/hg_kseos/spine.py',
            HG / 'src/hg_kseos/cli.py', Path('C:/wg/occupants/grant.seam.json'),
            Path('C:/wg/main-merge/evidence/r18/WP0203_17_BINDINGS.json'),
            Path('C:/wg/repo/fhs_msc_handoff_20261030/evidence/WP-FHS-03-04-08-ADMISSION-CHAIN/AO-verdict.json'),
            Path('C:/wg/repo/fhs_msc_handoff_20261030/evidence/WP-FHS-02-POLICY-LOADED-CONSUMER/TRANSCRIPTION.json'),
            Path('C:/wg/ao13/ao_r28j.json')]
inputs = list(dict.fromkeys([ROOT / 'brief.md'] + supplied + [ROOT / p for p in expected] + external))
before = [record(p) for p in inputs]
write(RUN / 'check-contract.json', {'nonce': NONCE, 'at': start, 'mode': 'VERIFY_ONLY',
    'maker_oracle': record(ROOT / 'evidence/ORACLE.json'), 'fixed_inputs': before,
    'relocation_interpretation': 'Appended brief supplies uppercase evidence aliases; inspect them substantively, do not reject solely for casing or relocation.',
    'decision_rule': 'Native PASS requires original production OPS authority, real CurrentNeed and original consumer chain, exact dedicated negatives and reproducible Raw. Explicit conformance-only authority fails native admission. Missing Raw alone is INCONCLUSIVE.',
    'scope': 'Read candidate and original sources; officer-only writes; no repair or HOST_OP.'})

doc11 = external[0].read_text(encoding='utf-8')
anchor = '<a id="current-b8c0abdfb9dc52ea4f52"></a>'
card = doc11.split(anchor, 1)[1].split('<a id=', 1)[0]
doc08 = external[1].read_text(encoding='utf-8')
write(RUN / 'source-clauses.json', {'source_files': [record(p) for p in external],
    'card': card, 'body08_3_1': doc08.split('### 3.1 ', 1)[1].split('### 3.2 ', 1)[0],
    'closing': doc08[doc08.rfind('## R2-08-ASSET：'):],
    'installer_numbered': [{'line': i, 'text': line} for i, line in enumerate(external[2].read_text(encoding='utf-8').splitlines(), 1)]})
admission = read('evidence/ADMISSION.json')
package = read('evidence/PACKAGE_INDEX.json')
pkgroot = Path(package['root']).resolve()
package_checks = []
for item in package['files']:
    p = (pkgroot / item['path']).resolve()
    assert p.is_relative_to(ROOT)
    observed = record(p)
    package_checks.append({'declared': item, 'observed': observed,
        'matches': observed['sha256'] == item['sha256'] and observed['bytes'] == item['bytes']})

# The inspected 85-byte script only prints its argument. Reproduce that limited
# behavior without installation, mutation, imports of candidate modules or grants.
probe = ROOT / 'evidence/occupant-root/occupant_probe.py'
assert sha(probe) == '22991e801ba7a6f36a5d6e2cfe8c2c26e8736ba2f6b14727ec1d63787c0bea08'
args = [sys.executable, '-B', str(probe), 'real-input-20261030']
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
write(RUN / 'probe.command.json', {'args': args, 'cwd': str(ROOT), 'started_at': now(),
    'runtime': sys.version, 'executable': record(Path(sys.executable)),
    'environment': {'PYTHONDONTWRITEBYTECODE': '1'}, 'ceiling': 'Standalone print probe only; not original Host Consumer or admission'})
proc = subprocess.run(args, cwd=ROOT, env=env, capture_output=True, timeout=20)
(RUN / 'probe.stdout.txt').write_bytes(proc.stdout)
(RUN / 'probe.stderr.txt').write_bytes(proc.stderr)
write(RUN / 'probe.exit.json', {'exit': proc.returncode, 'ended_at': now()})

registry = {'original_service_readback': 'NOT_PERFORMED',
    'reason': 'Original SharedSpine._open opens writable database and sets journal_mode=WAL outside permitted write root.',
    'ceiling': 'Read-only database context only; immutable main file is not guaranteed live/WAL snapshot.', 'attempts': []}
db = HG / 'var/shared-spine/hg-kseos.db'
for suffix in ('?mode=ro', '?mode=ro&immutable=1'):
    con = None
    try:
        con = sqlite3.connect(db.as_uri() + suffix, uri=True, timeout=2)
        con.row_factory = sqlite3.Row
        con.execute('PRAGMA query_only=ON')
        tables = [r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'")]
        registry['rows'] = {}
        for table in ('requirements', 'acceptances', 'work_queue', 'provider_bindings'):
            if table in tables:
                rows = [dict(r) for r in con.execute('SELECT * FROM "' + table + '"')]
                registry['rows'][table] = [r for r in rows if any(w in json.dumps(r, ensure_ascii=False) for w in ('WP-FHS-17', 'WP-FHS-00', 'WP-FHS-02', 'WP-FHS-03', 'WP-FHS-06', 'P0-TOOL', 'HGK-PROVIDER-FTS5'))]
        registry['attempts'].append({'mode': suffix, 'result': 'READABLE'})
        break
    except sqlite3.Error as exc:
        registry['attempts'].append({'mode': suffix, 'error': str(exc)})
    finally:
        if con is not None:
            con.close()
write(RUN / 'registry-observation.json', registry)

clauses = [
 ('ORIGINAL_OPS_ADMISSION', 'FAIL', 'ADMISSION explicitly declares CONFORMANCE_ONLY_TEST_SEAM; referenced grant contains seam signatures. No production original Issuer/receiver ACK. Single-account explanation does not meet contract.'),
 ('REAL_CURRENT_NEED', 'FAIL', 'Manifest is a draft print probe, NEED-WP17-OCCUPANT-PROBE. No admitted consumer SourceSelectionID/OriginalDisposition or required substantive feature binding.'),
 ('PACKAGE_BYTE_IDENTITY', 'PASS' if all(x['matches'] for x in package_checks) else 'FAIL', 'Enumerated file byte checks only; no inference of actual loaded bytes.'),
 ('SOURCE_SUBJECT_BINDING', 'PASS' if sha(external[0]) == subject['source']['sha256'] and sha(ROOT / 'brief.md') == subject['brief']['sha256'] else 'FAIL', 'Source and current brief checked against supplied SUBJECT pins.'),
 ('FRESH_HOST_LOAD_AND_ORIGINAL_CONSUMER', 'FAIL', 'Installer hashes parent-resolved file and records HOST_LOADED before subprocess.run; no child PID/session/origin readback or original Registry/Consumer call. Printed output reproduced only as standalone probe.'),
 ('DAG_INVERSION_NEGATIVE', 'INCONCLUSIVE', 'No valid-control/WP06-only mutant, evaluated edge set, dispatch trace or exact FIRST_FAIL Raw supplied; installer has no DAG input/check.'),
 ('LOADED_ORIGIN_MISMATCH_NEGATIVE', 'FAIL', 'Submitted tampered result exits 1 with truncated output; source negative only compares hashes locally, does not re-enter original consumer or withhold qualified ACK.'),
 ('OTHER_SUBMITTED_NEGATIVES', 'FAIL', 'Traversal observed GRANT_ASSURANCE_UNDECLARED instead of PATH_TRAVERSAL (exit 3); no-grant summary alone is not dedicated DAG evidence.'),
 ('ROLLBACK_RESUME', 'FAIL', 'ROLLBACK claims removed files and empty residue, but both installed files currently exist. No reinstall chronology, exact restoration, same-key ACK or UNKNOWN reconciliation Raw; historic uninstall is not independently disproved.'),
 ('REPRODUCIBLE_RAW_AND_FRESHNESS', 'INCONCLUSIVE', 'Missing run-index, command/environment/stdout/stderr/exit Raw, original before/after ACK, license/source/dependency pins and changed-file/test index. Maker oracle frozen flag has no pre-run registration receipt.')]
after = [record(p) for p in inputs]
verification = {'nonce': NONCE, 'mode': 'VERIFY_ONLY', 'started_at': start, 'ended_at': now(),
    'input_before': before, 'input_after': after, 'inputs_stable': before == after,
    'package_checks': package_checks, 'clause_results': [{'clause': c, 'result': r, 'finding': f} for c, r, f in clauses],
    'grant_digest_matches_reference': sha(Path(admission['grant_file'])) == admission['grant_sha256'],
    'native_reproduction': 'NOT_RUN: production admission absent; officer cannot repair or execute HOST_OP under seam.',
    'probe_output_matches': proc.returncode == 0 and proc.stdout.strip() == b'occupant-ok:real-input-20261030',
    'raw_refs': [str(p.relative_to(ROOT)) for p in sorted(RUN.iterdir()) if p.is_file() and not p.name.startswith('previous-')],
    'independence': 'User-dispatched independent evidence review; no candidate edits, installer dispatch or canonical state mutation.',
    'loaded_sha_ceiling': 'On-disk package/installed equality verified; current process loaded-byte identity not established.'}
write(OFF / 'verification.raw.json', verification)
verdict = {'wp': 'WP-FHS-17', 'nonce': NONCE, 'author_role': 'Independent Acceptance Officer',
    'mode': 'VERIFY_ONLY', 'verdict': 'FAIL', 'accepted': False,
    'reason': 'Explicit conformance-only grant cannot satisfy original OPS/Issuer native admission; additional contract violations recorded.',
    'claim_ceiling': 'Independent file evidence review and standalone probe reproduction only; no native acceptance.',
    'subject_sha256': sha(ROOT / 'evidence/SUBJECT.json'), 'oracle_sha256': sha(ROOT / 'evidence/ORACLE.json'),
    'manifest_sha256': sha(ROOT / 'evidence/occupant-root/_package/MANIFEST.json'),
    'package_index_sha256': sha(ROOT / 'evidence/PACKAGE_INDEX.json'),
    'brief_sha256': sha(ROOT / 'brief.md'), 'source_card_file_sha256': sha(external[0]), 'body08_sha256': sha(external[1]),
    'verification_sha256': sha(OFF / 'verification.raw.json'),
    'failed_clauses': [c for c, r, f in clauses if r == 'FAIL'], 'unverified_clauses': [c for c, r, f in clauses if r == 'INCONCLUSIVE'],
    'host_effect_disposition': 'PARK pending valid original OPS grant and bounded receiver manifest.',
    'canonical_transcription': 'NOT_PERFORMED; no successful verdict to transcribe. Historical refusal preserved.',
    'freshness': {'subject_scope': subject['scope'], 'package_scope': 'draft', 'policy_epoch_claim': subject['policy_epoch'], 'operation': subject['operation'], 'binding_verified': False},
    'completed_at': now()}
write(OFF / 'verdict.json', verdict)
outputs = [Path(__file__), OFF / 'verification.raw.json', OFF / 'verdict.json'] + [p for p in sorted(RUN.iterdir()) if p.is_file()]
write(OFF / 'hash-manifest.json', {'nonce': NONCE, 'algorithm': 'SHA256', 'generated_at': now(),
    'entries': [record(p) for p in list(dict.fromkeys(inputs + outputs))],
    'expansion_ceiling': 'All supplied evidence files and exact referenced installed payloads hashed. Required maker run/changed-source expansion absent; no production loaded-origin proof.',
    'excluded': ['officer/hash-manifest.json', 'officer/hash-manifest.receipt.json']})
write(OFF / 'hash-manifest.receipt.json', {'nonce': NONCE, 'path': 'officer/hash-manifest.json',
    'sha256': sha(OFF / 'hash-manifest.json'), 'at': now()})
print(json.dumps({'verdict': 'FAIL', 'accepted': False, 'inputs_stable': before == after,
    'package_checks_match': all(x['matches'] for x in package_checks), 'probe_output_matches': verification['probe_output_matches'],
    'failed_clauses': verdict['failed_clauses'], 'manifest_sha256': sha(OFF / 'hash-manifest.json')}))
