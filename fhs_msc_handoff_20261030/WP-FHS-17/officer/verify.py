"""WP17 VERIFY_ONLY: absence is unaccepted; never creates maker evidence."""
import datetime as dt
import hashlib
import json
import pathlib
import sqlite3
import sys

ROOT = pathlib.Path('C:/wg/queue/WP-FHS-17').resolve()
OFF = ROOT / 'officer'
NONCE = 'NONCE-WP-FHS-17-AUTO-20261030232608'
def _resolve_body() -> pathlib.Path:
    """Resolve the frozen subject body. MEASURED 2026-10-31: the 知識庫 tree this file was written against
    no longer exists on this host; the frozen subject lives in the R18 round. Refuse loudly rather than
    verify against nothing -- a checker that silently reads an empty body returns a vacuous pass."""
    import os
    cands = []
    if os.environ.get("HGK_FHS_BODY"):
        cands.append(pathlib.Path(os.environ["HGK_FHS_BODY"]))
    cands += [
        pathlib.Path("C:/Projects/Agent_Workspace/知識庫/實作相關DOC/Fabric vNext/Semantic World OS Fabric"
                     "/FHS/FHS-MSC/FHS-MSC_PIPD-LS-PKG/FHS-MSC_PIPD-LS-PKG_2026-10-30_HANDOFF-PATCH-v1"
                     "/01_FHS-MSC_PIPD-LS-PKG_BODY"),
        pathlib.Path("C:/Projects/Agent_Workspace/var/R18-FHS-SKELETON-SPINE-20261029/subject/01_BODY"),
        pathlib.Path("C:/Projects/Agent_Workspace/var/R19-FHS-20261029/copy_p2_repaired/01_BODY"),
    ]
    for c in cands:
        if c.is_dir() and any(c.glob("*.md")):
            return c
    raise SystemExit("ERR_SOURCE_BODY_MISSING: none of " + "; ".join(str(c) for c in cands))


BODY = _resolve_body()
HG = pathlib.Path('C:/Projects/Agent_Workspace/HG-KSEOS')
EXPECTED = '''brief.md
oracle.json
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

def now():
    return dt.datetime.now(dt.timezone.utc).isoformat()

def write(rel, obj):
    path = ROOT / rel
    assert path.resolve().is_relative_to(OFF)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def inspect(path):
    path = pathlib.Path(path)
    if not path.is_file():
        return {'path': str(path), 'state': 'MISSING', 'sha256': None}
    return {'path': str(path), 'state': 'PRESENT', 'sha256': digest(path), 'size_bytes': path.stat().st_size}

def main():
    start = now()
    # Fixed path set and decision rules are persisted before evidence evaluation.
    criteria = {
        'role': 'Independent Acceptance Officer', 'mode': 'VERIFY_ONLY', 'nonce': NONCE,
        'registered_at': start, 'source': inspect(ROOT / 'brief.md'),
        'maker_oracle': 'oracle.json', 'expected_maker_inputs': EXPECTED,
        'decision_rule': 'Absent decisive Raw or frozen subject => INCONCLUSIVE and unaccepted; no native PASS from presence or registry colour.',
        'positive': 'Existing Issuer authorizes installer; needed occupant is built, installed, fresh-loaded and substantively invoked through original consumer with matching package/installed/LoadedSHA.',
        'primary_negative': 'Valid control with WP00/02/03 ready and WP06 incomplete allows WP17; sole added prerequisite WP06 causes WP-FHS-17.FIRST_FAIL:CAP_BOOT_DEPENDENCY_INVERSION before dispatch, zero effects.',
        'secondary_negative': 'After valid control, foreign loaded bytes with claimed pin cause specific binding mismatch and no qualified ACK.',
        'scope': 'Officer outputs only; no repair, candidate creation, Host effect, registry mutation or release.',
        'ceiling': 'Independent local evidence review, not native execution or canonical acceptance',
    }
    write('officer/check-contract.json', criteria)
    initial = [inspect(ROOT / rel) for rel in EXPECTED]
    write('officer/raw/input-inventory.json', {'at': now(), 'files': initial})
    source_paths = [BODY / '11_WORKPACKAGES_AND_DAG.md', BODY / '08_TECHNOLOGY_DEFAULT_HOTSWAP.md',
                    HG / 'src/hg_kseos/spine.py', HG / 'src/hg_kseos/providers.py',
                    HG / 'src/hg_kseos/native_admission.py', HG / 'src/hg_kseos/cli.py']
    external = [
        pathlib.Path('C:/wg/main-merge/evidence/r18/WP0203_17_BINDINGS.json'),
        pathlib.Path('C:/wg/repo/fhs_msc_handoff_20261030/evidence/WP-FHS-03-04-08-ADMISSION-CHAIN/AO-verdict.json'),
        pathlib.Path('C:/wg/repo/fhs_msc_handoff_20261030/evidence/WP-FHS-02-POLICY-LOADED-CONSUMER/TRANSCRIPTION.json'),
        pathlib.Path('C:/wg/ao13/ao_r28j.json'),
    ]
    pinned = [inspect(p) for p in source_paths + external]
    doc11 = source_paths[0].read_text(encoding='utf-8')
    anchor = '<a id="current-b8c0abdfb9dc52ea4f52"></a>'
    card = doc11.split(anchor, 1)[1].split('<a id=', 1)[0]
    doc08 = source_paths[1].read_text(encoding='utf-8')
    section = doc08.split('### 3.1 ', 1)[1].split('### 3.2 ', 1)[0]
    closing = doc08[doc08.rfind('## R2-08-ASSET：'):]
    write('officer/raw/source-clauses.json', {'inputs': pinned, 'wp17_anchor': anchor,
        'card_text': card, 'card_hash_note': 'Whole original file byte SHA pinned; excerpt is a reading aid, not reserialized source hash.',
        'body08_section_3_1': section, 'body08_closing_disposition': closing})
    # Do not call SharedSpine._open: sqlite read/write plus journal_mode=WAL is
    # incompatible with this review's external-root read-only authorization.
    database = HG / 'var/shared-spine/hg-kseos.db'
    observation = {'at': now(), 'database': str(database), 'original_service_readback': 'NOT_PERFORMED',
        'reason': 'Original SharedSpine._open uses writable sqlite connect and PRAGMA journal_mode=WAL; no admitted write outside output root.',
        'acceptance_ceiling': 'Context only; never original service ACK or guaranteed live/WAL snapshot', 'attempts': []}
    connection = None
    for suffix in ('?mode=ro', '?mode=ro&immutable=1'):
        try:
            connection = sqlite3.connect(database.as_uri() + suffix, uri=True, timeout=2)
            connection.execute('PRAGMA query_only=ON')
            tables = [r[0] for r in connection.execute("SELECT name FROM sqlite_master WHERE type='table'")]
            observation['attempts'].append({'uri_suffix': suffix, 'result': 'READABLE'})
            observation['mode'] = suffix
            break
        except sqlite3.Error as exc:
            observation['attempts'].append({'uri_suffix': suffix, 'result': 'ERROR', 'error': str(exc)})
            if connection:
                connection.close()
            connection = None
    if connection:
        connection.row_factory = sqlite3.Row
        observation['rows'] = {}
        for table in ('requirements', 'acceptances', 'work_queue', 'provider_bindings'):
            if table not in tables:
                observation['rows'][table] = {'error': 'TABLE_NOT_FOUND'}
                continue
            columns = [r[1] for r in connection.execute('PRAGMA table_info("' + table + '")')]
            if table == 'provider_bindings':
                sql, args = 'SELECT * FROM provider_bindings WHERE provider_id LIKE ? OR provider_id=? LIMIT 100', ('P0-TOOL%', 'HGK-PROVIDER-FTS5')
            else:
                idcol = next((c for c in ('requirement_id', 'acceptance_id', 'wp_id', 'work_id', 'item_id', 'id') if c in columns), None)
                if not idcol:
                    observation['rows'][table] = {'columns': columns, 'error': 'KEY_NOT_RESOLVED'}
                    continue
                sql, args = f'SELECT * FROM "{table}" WHERE "{idcol}" LIKE ? LIMIT 100', ('%WP-FHS-%',)
            rows = [dict(r) for r in connection.execute(sql, args)]
            if table != 'provider_bindings':
                rows = [r for r in rows if any('WP-FHS-' + wp in str(r.get(c, '')) for c in columns if c.endswith('_id') or c == 'id' for wp in ('00','02','03','06','17'))]
            observation['rows'][table] = {'query': sql, 'parameters': args, 'records': rows}
        connection.close()
    write('officer/raw/registry-observation.json', observation)
    missing = [rel for rel, record in zip(EXPECTED, initial) if record['state'] == 'MISSING']
    # This officer does not manufacture replacements for absent oracle/index/Raw.
    if not missing:
        raise RuntimeError('Full candidate supplied: requires separate substantive verification; no automatic PASS supported')
    clauses = [
        ('FROZEN_ORACLE_AND_SUBJECT', ['oracle.json','candidate/need.json','candidate/source-pin.json']),
        ('FINITE_PACKAGE_AND_WRITESET', ['candidate/package-index.json','candidate/write-set.json']),
        ('ORIGINAL_OPS_ADMISSION', ['evidence/admission.json','evidence/registry-before.json']),
        ('ACTUAL_INSTALL_FRESH_LOAD_INVOKE', ['evidence/install.json','evidence/fresh-load.json','evidence/invoke.json']),
        ('SPECIFIC_NEGATIVES_AND_VALID_CONTROLS', ['fixtures/cap-boot-dependency-inversion.json','fixtures/loaded-origin-mismatch.json','evidence/negative-results.json']),
        ('ROLLBACK_IDEMPOTENCY_RECONCILIATION', ['evidence/rollback-resume.json']),
        ('REPRODUCIBLE_RAW_AND_CONSUMER_ACK', ['tools/reproduce.ps1','evidence/run-index.json','evidence/registry-after.json']),
    ]
    results = [{'clause': name, 'verdict': 'INCONCLUSIVE', 'missing': [p for p in paths if p in missing],
                'native_execution': 'NOT_RUN'} for name, paths in clauses]
    final_inputs = [inspect(ROOT / rel) for rel in EXPECTED]
    stable = initial == final_inputs and pinned == [inspect(p) for p in source_paths + external]
    verification = {'nonce': NONCE, 'started_at': start, 'finished_at': now(), 'mode': 'VERIFY_ONLY',
        'runtime': sys.version, 'executable': sys.executable, 'cwd': str(pathlib.Path.cwd()),
        'fixed_inputs_before': initial, 'fixed_inputs_after': final_inputs, 'checked_inputs_stable': stable,
        'missing_inputs': missing, 'clause_results': results,
        'original_installer_loader_consumer_paths': 'UNRESOLVED: no subject/package index supplied; provider and admission modules pinned only as known inputs',
        'package_installed_loaded_hash_equality': 'NOT_EVALUABLE',
        'reproduction': {'status': 'NOT_RUN', 'reason': 'No maker reproduce entry point, grant, target manifest, valid control, or native Raw supplied.'},
        'raw_refs': ['officer/raw/input-inventory.json','officer/raw/source-clauses.json','officer/raw/registry-observation.json'],
        'officer_mutations': 'Only officer/ files created; no Host dispatch, candidate repair, canonical state change or acceptance transition.',
        'independence': 'User-dispatched officer context; no maker summary consumed; external lane/model receipt not independently established here.'}
    write('officer/verification.raw.json', verification)
    verdict = {'wp': 'WP-FHS-17', 'nonce': NONCE, 'author_role': 'Independent Acceptance Officer',
        'mode': 'VERIFY_ONLY', 'verdict': 'INCONCLUSIVE', 'accepted': False, 'native_status': 'NOT_RUN',
        'claim_ceiling': 'Independent local absence/evidence review only; no native PASS or canonical acceptance',
        'reason': 'Missing frozen maker oracle, candidate subject, package/write-set indexes, admission and decisive install/load/invoke/negative/rollback Raw.',
        'brief_sha256': digest(ROOT / 'brief.md'), 'source_card_file_sha256': digest(source_paths[0]),
        'body08_sha256': digest(source_paths[1]), 'subject_sha256': None, 'manifest_sha256': None, 'oracle_sha256': None,
        'officer_check_contract_sha256': digest(OFF / 'check-contract.json'),
        'verification_sha256': digest(OFF / 'verification.raw.json'),
        'failed_clauses': [], 'unverified_clauses': [r['clause'] for r in results],
        'missing_inputs': missing, 'hash_manifest': 'officer/hash-manifest.json',
        'host_effect_disposition': 'PARK: original installer OPS grant, receiver-resolved WriteSet and same-subject consumer binding not supplied.',
        'canonical_transcription': 'NOT_PERFORMED; INCONCLUSIVE remains unaccepted; preserve historical refusal.',
        'freshness_binding': {'Subject': None,'SourceSHA': None,'CandidateSHA': None,'Scope': None,'PolicyEpoch': None,'operation_identity': None},
        'completed_at': now()}
    write('officer/verdict.json', verdict)
    # Finalized files only. Manifest cannot contain its own digest or size.
    officer_files = ['officer/verify.py','officer/check-contract.json','officer/raw/input-inventory.json',
        'officer/raw/source-clauses.json','officer/raw/registry-observation.json',
        'officer/verification.raw.json','officer/verdict.json']
    manifest = {'algorithm': 'SHA256', 'nonce': NONCE, 'generated_at': now(),
        'entries': [inspect(ROOT / p) for p in EXPECTED + officer_files] + pinned,
        'expansion_status': 'UNACCEPTED_MISSING_PACKAGE_RUN_AND_WRITESET_INDEXES',
        'installed_loaded_payloads': 'UNRESOLVED: no canonical target/loaded origin supplied; no presence-based substitution',
        'omitted_by_construction': ['officer/hash-manifest.json','officer/hash-manifest.receipt.json']}
    write('officer/hash-manifest.json', manifest)
    write('officer/hash-manifest.receipt.json', {'nonce': NONCE, 'path': 'officer/hash-manifest.json',
        'sha256': digest(OFF / 'hash-manifest.json'), 'at': now()})
    print(json.dumps({'verdict':'INCONCLUSIVE','accepted':False,'missing_count':len(missing),
                      'inputs_stable':stable,'manifest_sha256':digest(OFF / 'hash-manifest.json')}))
    return 2

if __name__ == '__main__':
    sys.exit(main())
