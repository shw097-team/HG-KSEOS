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
from typing import NoReturn

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

# ---------------------------------------------------------------- trust profile selection (B1 r10 step 1)
# The r5/'machine' profile needs Administrator + a machine CNG key + a ProgramData ACL. A normal
# factory WorkOrder does not, so the OWNER authorised a user-scoped alternative. The receiver must
# therefore resolve WHICH trust root to read instead of hardcoding the ProgramData constant. An
# unknown profile value is refused - never silently defaulted - because defaulting would let a typo
# select a weaker root.
MACHINE_PROFILE = 'machine'
USER_PROFILE = 'user'
PROFILES = (MACHINE_PROFILE, USER_PROFILE)
USER_REGISTRY_SCHEMA = 'HGK-USER-TRUST-REGISTRY/1'
USER_SCOPE_FILENAME = 'scope.json'

# ------------------------------------------------- mission-scoped machine root selection (WP06)
# A B1 registry file admits exactly ONE mission (`registry['mission_id']` is compared against every
# reference at :478). The user profile says which mission via its scope sidecar; the machine profile
# had no such channel, so the single ProgramData constant was also the only mission it could admit.
# The OWNER's answer is SELECTION, not a second trust root and not a re-scoped anchor: the only thing
# that may vary is WHICH already-OS-protected registry file the receiver reads.
#
# The request can never choose its own root. `mission_selector()` takes no argument and reads one
# config value the host supervisor sets for the process; `authorize()` separately refuses, by name,
# any request key that names a registry, a profile or a mission.
MISSION_SELECTOR_ENV = 'HGK_MISSION_ID'
TRUST_PROFILE_ENV = 'HGK_TRUST_PROFILE'
MACHINE_MISSIONS_DIRNAME = 'missions'
MISSION_ID_PATTERN = re.compile(r'[A-Za-z0-9][A-Za-z0-9._-]{0,63}\Z')
REQUEST_ROOT_KEYS = ('registry', 'registry_path', 'registry_file', 'trust_root', 'trust_profile',
                     'trust_store', 'scope_path', 'mission_id', 'mission_selector')

# ------------------------------------------------- supervisor-bound scope (WP06 r2)
# HGK_MISSION_ID and HGK_TRUST_PROFILE are ordinary environment variables, so ANY process can set
# them - including the worker that is about to be admitted. An environment variable is therefore not
# a binding: on its own it moves which registry is read, which is exactly the redirection this seam
# exists to prevent. The supervisor records its decision ONCE, in a file that carries the same OS
# protection as the registry, and the worker may only CONFIRM that record - never choose it, never
# blank it, never weaken the profile it fixes.
#
# Honest ceiling: this is a mechanism, not a principal proof. The record's authority is the OS DACL
# on <base>/supervisor/ (measured by `assert_protected`), so a worker running as the SAME user that
# can write that directory can write the record too - which is why the record must live in the
# protected base and why `SUPERVISOR_BINDING_UNPROTECTED` refuses instead of trusting it. Proving a
# DIFFERENT, higher-privileged supervisor principal needs HOST_OPERATIONS; nothing here asserts it.
SUPERVISOR_DIRNAME = 'supervisor'
SUPERVISOR_BINDING_FILENAME = 'scope.json'
SUPERVISOR_BINDING_SCHEMA = 'HGK-SUPERVISOR-SCOPE/1'


def _mission_id_ok(raw):
    return (bool(MISSION_ID_PATTERN.match(raw)) and '..' not in raw and not raw.endswith('.')
            and not any(c in raw for c in ('/', '\\', ':')))


def _binding_dir():
    return REGISTRY.parent / SUPERVISOR_DIRNAME


def _binding_path(path=None):
    return absolute_root(path) if path is not None else _binding_dir() / SUPERVISOR_BINDING_FILENAME


def _binding_document(raw):
    """Parse the supervisor's decision. Unknown fields are ignored, a wrong shape is refused."""
    doc = strict_json(raw)
    if not isinstance(doc, dict) or doc.get('schema') != SUPERVISOR_BINDING_SCHEMA:
        refuse('SUPERVISOR_BINDING_SHAPE')
    profile = doc.get('trust_profile')
    if profile not in PROFILES:
        refuse('SUPERVISOR_BINDING_SHAPE')
    mission = doc.get('mission_id')
    if mission is not None and (not isinstance(mission, str) or not _mission_id_ok(mission)):
        refuse('SUPERVISOR_BINDING_SHAPE')
    return {'schema': SUPERVISOR_BINDING_SCHEMA, 'mission_id': mission, 'trust_profile': profile,
            'bound_at': doc.get('bound_at'), 'bound_by_pid': doc.get('bound_by_pid')}


def supervisor_binding(path=None):
    """The supervisor's recorded scope decision, or None when this host was never bound.

    Read fresh on every call (no cache): a memo keyed on stat() would let a same-size rewrite hide
    behind an unchanged timestamp, and this value decides which trust root is read.
    """
    p = _binding_path(path)
    if not p.is_file():
        return None
    try:
        assert_protected(p)
    except InvariantViolation:
        # A record the worker can rewrite is not a supervisor decision; refuse rather than obey it.
        refuse('SUPERVISOR_BINDING_UNPROTECTED')
    with pinned_file(p) as stream:
        return _binding_document(stream.read())


def bind_supervisor_scope(mission_id=None, profile=MACHINE_PROFILE, path=None, bound_at=None):
    """Supervisor-side, ONE writer: record the scope this host may operate under.

    `mission_id=None` is a decision too - it pins the unscoped ProgramData constant - so it is
    recorded rather than left implicit. The call is immutable: a second, different binding is
    refused, because a re-bindable decision is not a decision. The host must apply the protected
    DACL to <base>/supervisor/ after this returns; until it does, `supervisor_binding()` refuses
    the record as unprotected.
    """
    if profile not in PROFILES:
        refuse('TRUST_PROFILE')
    if mission_id is not None:
        if not isinstance(mission_id, str) or not _mission_id_ok(mission_id):
            refuse('MISSION_SELECTOR_SHAPE')
    p = _binding_path(path)
    if p.is_file():
        with pinned_file(p) as stream:
            existing = _binding_document(stream.read())
        if (existing['mission_id'], existing['trust_profile']) != (mission_id, profile):
            refuse('SUPERVISOR_BINDING_IMMUTABLE')
        return existing
    doc = {'schema': SUPERVISOR_BINDING_SCHEMA, 'mission_id': mission_id, 'trust_profile': profile,
           'bound_at': bound_at or datetime.now(timezone.utc).isoformat(),
           'bound_by_pid': os.getpid()}
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_name(p.name + '.tmp')
    tmp.write_text(json.dumps(doc, sort_keys=True), encoding='utf-8')
    os.replace(tmp, p)
    return doc


def mission_selector():
    """The mission this process was pinned to, from CONFIG only - never from a request.

    Deliberately takes no argument: no request dict, bundle or argv line can reach it. Four
    mutations are refused by name instead of resolved: a malformed id, a selector that disagrees
    with the supervisor record (worker reselection), a blank selector while a record exists (the
    silent fallback to B1's unscoped constant), and any non-empty selector on a host with no
    supervisor record at all (an unprotected environment override - refused whether or not the
    supervisor directory exists).

    Unbound hosts keep B1 exactly as it was: no selector means the ProgramData constant.
    """
    raw_present = MISSION_SELECTOR_ENV in os.environ
    raw = (os.environ.get(MISSION_SELECTOR_ENV) or '').strip()
    if raw and not _mission_id_ok(raw):
        refuse('MISSION_SELECTOR_SHAPE')
    bound = supervisor_binding()
    if bound is None:
        if raw:
            # No supervisor record: an environment variable is not a binding. A worker sets its own
            # environment, so honouring the selector here is the unprotected override this whole
            # function exists to stop - and it must not depend on whether the supervisor directory
            # happens to exist, because that made the refusal host-dependent and left the R4a shape
            # (unbound host + non-empty selector + another mission's registry already present) open.
            refuse('SUPERVISOR_BINDING_ABSENT')
        return None
    if raw_present and not raw:
        refuse('MISSION_SELECTOR_BLANK')
    if raw:
        if bound['mission_id'] is None or raw != bound['mission_id']:
            refuse('MISSION_SELECTOR_WORKER_RESELECT')
        return raw
    # Absent is not a fallback: the record alone decides, and it may legitimately decide "unscoped".
    return bound['mission_id']


def machine_registry_path(mission=None):
    """Fixed layout under the one protected base dir: <base>/missions/<mission>/registry.json.

    Only a validated mission id varies; the level and the file name are literals, so the result can
    neither escape `REGISTRY.parent` nor be a caller-supplied path.
    """
    if mission is None:
        return REGISTRY
    return REGISTRY.parent / MACHINE_MISSIONS_DIRNAME / mission / REGISTRY.name


def trust_profile():
    """machine|user, with the supervisor record as the pin when this host is bound.

    Legacy (no record): the value of HGK_TRUST_PROFILE, defaulting to machine - today's behaviour,
    unchanged. Bound: the record fixes the profile, and the environment may only repeat it. A worker
    that asks for `user` while the supervisor fixed `machine` is refused as a DOWNGRADE by name -
    silently honouring it would let the worker swap an Administrator-only root for a DPAPI-user one.
    """
    bound = supervisor_binding()
    raw_present = TRUST_PROFILE_ENV in os.environ
    raw = (os.environ.get(TRUST_PROFILE_ENV) or '').strip().lower()
    if bound is None:
        if not raw:
            raw = MACHINE_PROFILE
        if raw not in PROFILES:
            refuse('TRUST_PROFILE')
        return raw
    pinned = bound['trust_profile']
    if raw_present and not raw:
        refuse('TRUST_PROFILE_BLANK')
    if raw and raw != pinned:
        if pinned == MACHINE_PROFILE and raw == USER_PROFILE:
            refuse('TRUST_PROFILE_DOWNGRADE')
        refuse('TRUST_PROFILE_CONFLICT')
    return pinned


def user_registry_path():
    from . import user_trust
    return user_trust.paths()['registry']


def registry_path(profile=None):
    """The one place that decides which root backs the receiver.

    Machine-profile order, fixed and complete: (1) no mission selector -> the ProgramData constant,
    exactly as before; (2) a mission selector -> that mission's registry under the same protected
    base. There is no third step and no fallback: if the selected mission's file is absent the
    receiver refuses, because falling back to (1) would silently admit a DIFFERENT mission.
    """
    if (profile or trust_profile()) != MACHINE_PROFILE:
        return user_registry_path()
    return machine_registry_path(mission_selector())


# ------------------------------------------------- real Windows ACL / SID measurement (WP06 r2)
# `assert_protected` above answers "is this registry protected" with one boolean, and it answers it
# for the unscoped constant. A mission registry is a DIFFERENT file at a DEEPER path, so the same
# rule has to be re-measured there plus three facts a bare boolean cannot carry: which DACL entries
# exist, whether the declared checker SID can actually READ the file, and whether the ancestor chain
# that leads to it is itself steerable (reparse) or writable by a world principal.
#
# Every number below comes from the OS through GetNamedSecurityInfo/Authz-style APIs in this process;
# none of it is inferred from the registry's own JSON, and no PowerShell module is required.
FILE_READ_DATA = 0x1
FILE_WRITE_DATA = 0x2
FILE_APPEND_DATA = 0x4
FILE_WRITE_EA = 0x10
FILE_DELETE_CHILD = 0x40
FILE_READ_ATTRIBUTES = 0x80
FILE_WRITE_ATTRIBUTES = 0x100
DELETE = 0x10000
READ_CONTROL = 0x20000
WRITE_DAC = 0x40000
WRITE_OWNER = 0x80000
SYNCHRONIZE = 0x100000
CHECKER_MIN_MASK = FILE_READ_DATA | FILE_READ_ATTRIBUTES | READ_CONTROL
# The same mask assert_protected band-tests, kept identical on purpose: the mission path must not be
# a relaxed copy of the machine rule.
PROTECTED_WRITE_MASK = 0x000D0156
# An ancestor that grants only "create a new child" cannot change an EXISTING child; one that grants
# delete-child / delete / WRITE_DAC / WRITE_OWNER can replace it, so those are the fatal bits.
ANCESTOR_FATAL_MASK = DELETE | FILE_DELETE_CHILD | WRITE_DAC | WRITE_OWNER
WORLD_SIDS = ('S-1-1-0', 'S-1-5-7', 'S-1-5-11', 'S-1-5-32-545', 'S-1-5-4', 'S-1-5-32-546')
SYSTEM_OWNER_SIDS = ('S-1-5-18', 'S-1-5-32-544')

_WIN = {}


def _win():
    """ctypes bindings for the ACL APIs, built once. No PowerShell, no module path, no policy."""
    if _WIN:
        return _WIN
    import ctypes
    from ctypes import wintypes as w

    class ACE_HEADER(ctypes.Structure):
        _fields_ = [('AceType', ctypes.c_ubyte), ('AceFlags', ctypes.c_ubyte),
                    ('AceSize', ctypes.c_ushort)]

    class ACE_ACCESS(ctypes.Structure):
        _fields_ = [('Header', ACE_HEADER), ('Mask', ctypes.c_uint32), ('SidStart', ctypes.c_uint32)]

    class ACE_OBJECT(ctypes.Structure):
        _fields_ = [('Header', ACE_HEADER), ('Mask', ctypes.c_uint32), ('Flags', ctypes.c_uint32)]

    class ACL_SIZE(ctypes.Structure):
        _fields_ = [('AceCount', ctypes.c_uint32), ('AclBytesInUse', ctypes.c_uint32),
                    ('AclBytesFree', ctypes.c_uint32)]

    class TRUSTEE(ctypes.Structure):
        _fields_ = [('pMultipleTrustee', ctypes.c_void_p), ('MultipleTrusteeOperation', ctypes.c_uint32),
                    ('TrusteeForm', ctypes.c_uint32), ('TrusteeType', ctypes.c_uint32),
                    ('ptstrName', ctypes.c_void_p)]

    adv = ctypes.WinDLL('advapi32', use_last_error=True)
    kernel = ctypes.WinDLL('kernel32', use_last_error=True)
    P = ctypes.POINTER
    adv.GetNamedSecurityInfoW.argtypes = [w.LPWSTR, ctypes.c_int, ctypes.c_uint32, P(ctypes.c_void_p),
                                          P(ctypes.c_void_p), P(ctypes.c_void_p), P(ctypes.c_void_p),
                                          P(ctypes.c_void_p)]
    adv.GetNamedSecurityInfoW.restype = ctypes.c_uint32
    adv.GetAclInformation.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_uint32, ctypes.c_int]
    adv.GetAce.argtypes = [ctypes.c_void_p, ctypes.c_uint32, P(ctypes.c_void_p)]
    adv.GetSecurityDescriptorControl.argtypes = [ctypes.c_void_p, P(ctypes.c_uint16), P(ctypes.c_uint32)]
    adv.ConvertSidToStringSidW.argtypes = [ctypes.c_void_p, P(w.LPWSTR)]
    adv.ConvertStringSidToSidW.argtypes = [w.LPCWSTR, P(ctypes.c_void_p)]
    adv.GetEffectiveRightsFromAclW.argtypes = [ctypes.c_void_p, P(TRUSTEE), P(ctypes.c_uint32)]
    adv.GetEffectiveRightsFromAclW.restype = ctypes.c_uint32
    adv.ConvertSecurityDescriptorToStringSecurityDescriptorW.argtypes = [
        ctypes.c_void_p, ctypes.c_uint32, ctypes.c_uint32, P(w.LPWSTR), P(ctypes.c_uint32)]
    adv.ConvertSecurityDescriptorToStringSecurityDescriptorW.restype = ctypes.c_int
    adv.LookupAccountSidW.argtypes = [w.LPCWSTR, ctypes.c_void_p, w.LPWSTR, P(ctypes.c_uint32),
                                      w.LPWSTR, P(ctypes.c_uint32), P(ctypes.c_int)]
    kernel.LocalFree.argtypes = [ctypes.c_void_p]
    kernel.LocalFree.restype = ctypes.c_void_p
    _WIN.update(locals())
    return _WIN


def _sid_to_string(sid_ptr):
    api = _win()
    import ctypes
    out = ctypes.c_wchar_p()
    if not api['adv'].ConvertSidToStringSidW(sid_ptr, ctypes.byref(out)):
        refuse('TRUST_ACL_QUERY')
    try:
        return out.value
    finally:
        api['kernel'].LocalFree(ctypes.cast(out, ctypes.c_void_p))


def _sid_from_string(text):
    api = _win()
    import ctypes
    out = ctypes.c_void_p()
    if not api['adv'].ConvertStringSidToSidW(text, ctypes.byref(out)):
        refuse('TRUST_ACL_QUERY')
    return out


def _named_security(path):
    """Owner, group, DACL, protection flag and SDDL for one real path."""
    api = _win()
    import ctypes
    owner = ctypes.c_void_p(); group = ctypes.c_void_p()
    dacl = ctypes.c_void_p(); sacl = ctypes.c_void_p(); sd = ctypes.c_void_p()
    rc = api['adv'].GetNamedSecurityInfoW(str(path), 1, 0x7, ctypes.byref(owner), ctypes.byref(group),
                                          ctypes.byref(dacl), ctypes.byref(sacl), ctypes.byref(sd))
    if rc:
        return None
    control = ctypes.c_uint16(); revision = ctypes.c_uint32()
    api['adv'].GetSecurityDescriptorControl(sd, ctypes.byref(control), ctypes.byref(revision))
    sddl = ''
    out = ctypes.c_wchar_p()
    if api['adv'].ConvertSecurityDescriptorToStringSecurityDescriptorW(sd, 1, 0x7,
                                                                       ctypes.byref(out), None):
        sddl = out.value or ''
        api['kernel'].LocalFree(ctypes.cast(out, ctypes.c_void_p))
    return {'sd': sd, 'owner': owner, 'group': group, 'dacl': dacl,
            'protected': bool(control.value & 0x1000), 'sddl': sddl}


def acl_facts(path):
    """The measured DACL of one path: owner SID, every ACE, and whether inheritance is closed."""
    if os.name != 'nt':
        refuse('PROTECTED_WINDOWS_READER_REQUIRED')
    api = _win()
    import ctypes
    sec = _named_security(path)
    if sec is None:
        return {'path': str(path), 'exists': False, 'error': 'GetNamedSecurityInfo'}
    entries = []
    count = api['ACL_SIZE']()
    if sec['dacl'].value and api['adv'].GetAclInformation(sec['dacl'], ctypes.byref(count),
                                                          ctypes.sizeof(count), 2):
        for i in range(count.AceCount):
            ptr = ctypes.c_void_p()
            if not api['adv'].GetAce(sec['dacl'], i, ctypes.byref(ptr)):
                refuse('TRUST_ACL_QUERY')
            hdr = ctypes.cast(ptr, ctypes.POINTER(api['ACE_HEADER'])).contents
            entry = {'index': i, 'type': int(hdr.AceType), 'flags': int(hdr.AceFlags),
                     'inherited': bool(hdr.AceFlags & 0x10), 'mask': 0, 'sid': None}
            if hdr.AceType in (0, 1, 2, 3):
                entry['mask'] = int(ctypes.cast(ptr, ctypes.POINTER(api['ACE_ACCESS'])).contents.Mask)
                entry['sid'] = _sid_to_string(ctypes.c_void_p(ptr.value + 8))
            elif hdr.AceType in (5, 6):
                obj = ctypes.cast(ptr, ctypes.POINTER(api['ACE_OBJECT'])).contents
                entry['mask'] = int(obj.Mask)
                offset = 12 + (16 if obj.Flags & 0x1 else 0) + (16 if obj.Flags & 0x2 else 0)
                entry['sid'] = _sid_to_string(ctypes.c_void_p(ptr.value + offset))
            else:
                entry['shape'] = 'unsupported'
            entries.append(entry)
    facts = {'path': str(path), 'exists': True,
             'owner': _sid_to_string(sec['owner']) if sec['owner'].value else None,
             'group': _sid_to_string(sec['group']) if sec['group'].value else None,
             'dacl_protected': sec['protected'], 'sddl': sec['sddl'], 'aces': entries}
    api['kernel'].LocalFree(ctypes.cast(sec['sd'], ctypes.c_void_p))
    return facts


def effective_rights(path, sid):
    """What the file's DACL grants to exactly that SID (GetEffectiveRightsFromAcl)."""
    if os.name != 'nt':
        refuse('PROTECTED_WINDOWS_READER_REQUIRED')
    api = _win()
    import ctypes
    sec = _named_security(path)
    if sec is None:
        return None
    sidbuf = _sid_from_string(sid)
    try:
        trustee = api['TRUSTEE']()
        trustee.TrusteeForm = 0        # TRUSTEE_IS_SID
        trustee.TrusteeType = 0        # TRUSTEE_IS_UNKNOWN
        trustee.ptstrName = sidbuf
        mask = ctypes.c_uint32(0)
        rc = api['adv'].GetEffectiveRightsFromAclW(sec['dacl'], ctypes.byref(trustee),
                                                   ctypes.byref(mask))
        return None if rc else int(mask.value)
    finally:
        api['kernel'].LocalFree(sidbuf)
        api['kernel'].LocalFree(ctypes.cast(sec['sd'], ctypes.c_void_p))


def sid_account(sid):
    """Does this SID resolve to a real account on this host, and to which name?"""
    api = _win()
    import ctypes
    sidbuf = _sid_from_string(sid)
    try:
        name = ctypes.create_unicode_buffer(256); domain = ctypes.create_unicode_buffer(256)
        nlen = ctypes.c_uint32(256); dlen = ctypes.c_uint32(256); use = ctypes.c_int(0)
        ok = api['adv'].LookupAccountSidW(None, sidbuf, name, ctypes.byref(nlen), domain,
                                          ctypes.byref(dlen), ctypes.byref(use))
        if not ok:
            return {'sid': sid, 'resolved': False, 'error': ctypes.get_last_error()}
        return {'sid': sid, 'resolved': True, 'name': name.value, 'domain': domain.value}
    finally:
        api['kernel'].LocalFree(sidbuf)


def ancestor_chain(path):
    """Every existing directory from `path` up to the drive root, nearest first."""
    path = absolute_root(path)
    out = []
    for candidate in [path] + list(path.parents):
        if candidate.is_dir():
            out.append(candidate)
    return out


def mission_root_report(path, checker_sid=None, base=None):
    """Measure one mission registry and its ancestry. Facts only - `assert_mission_protected` decides."""
    path = absolute_root(path)
    base = absolute_root(base) if base is not None else REGISTRY.parent
    report = {'path': str(path), 'base': str(base), 'exists': path.is_file(),
              'leaf': acl_facts(path) if path.exists() else None,
              'ancestors': [], 'checker': None, 'verdicts': {}, 'failures': []}

    def verdict(name, ok, detail=None):
        report['verdicts'][name] = bool(ok)
        if detail is not None:
            report['verdicts'][name + '_detail'] = detail
        if not ok:
            report['failures'].append(name)

    leaf = report['leaf'] or {}
    verdict('owner_is_system_or_admin', leaf.get('owner') in SYSTEM_OWNER_SIDS, leaf.get('owner'))
    verdict('dacl_explicit', leaf.get('dacl_protected') is True)
    foreign_write = [a for a in leaf.get('aces', [])
                     if a.get('type') == 0 and (a['mask'] & PROTECTED_WRITE_MASK)
                     and a.get('sid') not in SYSTEM_OWNER_SIDS]
    verdict('no_foreign_write_ace', not foreign_write,
            [f"{a.get('sid')}:{a['mask']:08x}" for a in foreign_write])
    inherited_write = [a for a in leaf.get('aces', [])
                       if a.get('type') == 0 and a.get('inherited') and (a['mask'] & PROTECTED_WRITE_MASK)]
    verdict('no_inherited_write_exposure', not inherited_write,
            [f"{a.get('sid')}:{a['mask']:08x}" for a in inherited_write])

    reparse = []
    fatal_ancestors = []
    for ancestor in ancestor_chain(path):
        facts = acl_facts(ancestor)
        here = str(ancestor).lower().rstrip('\\')
        strict = here == str(base).lower().rstrip('\\') or \
            here.startswith(str(base).lower().rstrip('\\') + os.sep)
        # Mapped rights, not raw ACE masks: C:\ carries a legacy Authenticated-Users ACE of
        # 0xE0010000 whose SPECIFIC bits read as DELETE but whose mapped grant is only append/create.
        # Testing the raw mask there would refuse the real ProgramData chain for a bit the OS does
        # not actually grant - so the ancestor verdict is computed with GetEffectiveRightsFromAcl.
        world = []
        for sid in WORLD_SIDS:
            rights = effective_rights(ancestor, sid)
            if not rights:
                continue
            bits = rights & (PROTECTED_WRITE_MASK if strict else ANCESTOR_FATAL_MASK)
            if bits:
                world.append({'sid': sid, 'rights': f'{rights:08x}', 'matched': f'{bits:08x}',
                              'strict': strict})
        if os.path.islink(ancestor) or getattr(ancestor.lstat(), 'st_file_attributes', 0) & 0x400:
            reparse.append(str(ancestor))
        if world:
            fatal_ancestors.append({'path': str(ancestor), 'world_write': world})
        report['ancestors'].append({'path': str(ancestor), 'strict': strict,
                                    'owner': facts.get('owner'),
                                    'dacl_protected': facts.get('dacl_protected'),
                                    'world_write': world})
    verdict('ancestors_no_reparse', not reparse, reparse)
    verdict('ancestors_no_world_write', not fatal_ancestors, fatal_ancestors)

    if checker_sid:
        rights = effective_rights(path, checker_sid)
        account = sid_account(checker_sid)
        report['checker'] = {'sid': checker_sid, 'effective_mask': rights,
                             'account': account,
                             'can_read': bool(rights is not None
                                              and rights & FILE_READ_DATA
                                              and rights & READ_CONTROL)}
        verdict('checker_sid_can_read', report['checker']['can_read'],
                None if rights is None else f'{rights:08x}')
    return report


def assert_mission_protected(path, checker_sid=None):
    """The machine rule, re-measured on a mission path, plus the facts a boolean cannot carry.

    Refuses by name so the failure is attributable: a mission root protected like the constant but
    unreachable to its own checker is not a usable root, and one under a writable or steered ancestor
    is not a protected one.
    """
    if os.name != 'nt':
        refuse('PROTECTED_WINDOWS_READER_REQUIRED')
    report = mission_root_report(path, checker_sid)
    if not report['exists']:
        refuse('MISSION_REGISTRY_ABSENT' if REGISTRY.parent else 'TRUST_BOOTSTRAP_REQUIRED')
    v = report['verdicts']
    if not v.get('ancestors_no_reparse'):
        refuse('ROOT_REPARSE')
    if not v.get('owner_is_system_or_admin'):
        refuse('TRUST_ACL_UNPROTECTED')
    if not v.get('dacl_explicit') or not v.get('no_foreign_write_ace') \
            or not v.get('no_inherited_write_exposure'):
        refuse('TRUST_ACL_UNPROTECTED')
    if not v.get('ancestors_no_world_write'):
        refuse('TRUST_ANCESTOR_WORLD_WRITABLE')
    if checker_sid and not v.get('checker_sid_can_read'):
        refuse('TRUST_CHECKER_UNREACHABLE')
    return report


def refuse(code)->NoReturn:
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
    # FIX (FAR-B1-v4 D-16): the previous body used Get-Acl / Get-Item / Split-Path, i.e. it depended
    # on Windows PowerShell MODULES loading. On this host PSModulePath inherits a codex runtime module
    # directory, so `Import-Module Microsoft.PowerShell.Security` fails and `Get-Acl` is a
    # CommandNotFoundException: the script exited non-zero for EVERY registry and the ACL check became a
    # permanent false negative (measured: correct ACL, still TRUST_ACL_UNPROTECTED). The check below uses
    # only .NET ACL APIs, so it reads the same facts without any module dependency.
    script=r'''param([string]$RegistryPath)
    $ErrorActionPreference='Stop'
    $paths=New-Object System.Collections.ArrayList
    [void]$paths.Add($RegistryPath)
    $cursor=[System.IO.Path]::GetDirectoryName($RegistryPath)
    $programData=[System.Environment]::GetFolderPath('CommonApplicationData')
    while($cursor){
      [void]$paths.Add($cursor)
      if($cursor -ieq $programData){break}
      $cursor=[System.IO.Path]::GetDirectoryName($cursor)
    }
    foreach($p in $paths){
      $attr=[System.IO.File]::GetAttributes($p)
      if(($attr -band [System.IO.FileAttributes]::ReparsePoint) -ne 0){exit 23}
      if([System.IO.Directory]::Exists($p)){$a=[System.IO.Directory]::GetAccessControl($p)}
      else{$a=[System.IO.File]::GetAccessControl($p)}
      $owner=$a.GetOwner([System.Security.Principal.SecurityIdentifier]).Value
      if(@('S-1-5-18','S-1-5-32-544') -notcontains $owner){exit 24}
      if(($p -ine $programData) -and (-not $a.AreAccessRulesProtected)){exit 25}
      $mask=0x000D0156
      if($p -ieq $programData){$mask=0x000D0040}
      foreach($r in $a.GetAccessRules($true,$true,[System.Security.Principal.SecurityIdentifier])){
        if($r.AccessControlType -ne 'Allow'){continue}
        if(([int]$r.FileSystemRights -band $mask) -eq 0){continue}
        if(@('S-1-5-18','S-1-5-32-544') -contains $r.IdentityReference.Value){continue}
        exit 26
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
    # A sanitised module path keeps any future cmdlet use from inheriting a foreign module root.
    env=dict(os.environ)
    env['PSModulePath']=r'C:\Windows\system32\WindowsPowerShell\v1.0\Modules'
    r=subprocess.run(cmd,input=str(path)+'\n',text=True,encoding='utf-8',errors='replace',capture_output=True,timeout=15,env=env)
    if r.returncode or r.stdout.strip()!='PROTECTED':refuse('TRUST_ACL_UNPROTECTED')

def assert_user_protected(path):
    """The user profile's protection proof: the DACL is explicit and only the current user writes it.

    Deliberately NOT a relaxation of `assert_protected`: the machine rule (owner SYSTEM/Administrators)
    cannot be satisfied by a %LOCALAPPDATA% root, and simply dropping the check would let any local
    principal rewrite the trust anchor. This rule pins the owner to the CURRENT process user, demands an
    explicit (non-inherited) DACL, and refuses any foreign write ACE. Uses .NET ACL APIs only - the same
    reason as `assert_protected`: a foreign PSModulePath made the cmdlet version a permanent false
    negative.
    """
    if os.name!='nt':refuse('PROTECTED_WINDOWS_READER_REQUIRED')
    script=r'''param([string]$RegistryPath)
    $ErrorActionPreference='Stop'
    $me=[System.Security.Principal.WindowsIdentity]::GetCurrent().User.Value
    $cursor=$RegistryPath
    while($cursor){
      if(-not ([System.IO.Directory]::Exists($cursor) -or [System.IO.File]::Exists($cursor))){exit 22}
      $attr=[System.IO.File]::GetAttributes($cursor)
      if(($attr -band [System.IO.FileAttributes]::ReparsePoint) -ne 0){exit 23}
      $cursor=[System.IO.Path]::GetDirectoryName($cursor)
    }
    $a=[System.IO.File]::GetAccessControl($RegistryPath)
    $owner=$a.GetOwner([System.Security.Principal.SecurityIdentifier]).Value
    if($owner -ne $me){exit 24}
    if(-not $a.AreAccessRulesProtected){exit 25}
    $mask=0x000D0156
    foreach($r in $a.GetAccessRules($true,$true,[System.Security.Principal.SecurityIdentifier])){
      if($r.AccessControlType -ne 'Allow'){continue}
      if(([int]$r.FileSystemRights -band $mask) -eq 0){continue}
      if(@($me,'S-1-5-18','S-1-5-32-544') -contains $r.IdentityReference.Value){continue}
      exit 26
    }
    'PROTECTED'
    '''
    import base64 as b64
    script=script.replace('param([string]$RegistryPath)',"$RegistryPath=[Console]::In.ReadLine()")
    cmd=['powershell.exe','-NoProfile','-NonInteractive','-EncodedCommand',b64.b64encode(script.encode('utf-16-le')).decode('ascii')]
    env=dict(os.environ)
    env['PSModulePath']=r'C:\Windows\system32\WindowsPowerShell\v1.0\Modules'
    r=subprocess.run(cmd,input=str(path)+'\n',text=True,encoding='utf-8',errors='replace',capture_output=True,timeout=15,env=env)
    if r.returncode or r.stdout.strip()!='PROTECTED':refuse('USER_TRUST_ACL_UNPROTECTED')

class ProtectedRegistry:
    def __init__(self,path=None):
        # The mission is pinned ONCE, at host construction, from config; it is never re-read per
        # request, so the root cannot change between the guard snapshot and the transaction.
        # `path` is a code-side injection seam (same rule as NativeAdmission(registry=...)); no
        # request value ever reaches it.
        self.path=path
        self.mission=mission_selector()
        self._selector_raw=(os.environ.get(MISSION_SELECTOR_ENV) or '').strip() or None
        self._bound_mission=(supervisor_binding() or {}).get('mission_id')

    def _registry_path(self):
        # The pin above makes a later env change harmless; these two checks make it VISIBLE. A worker
        # that reselects, or that rewrites the supervisor record where the DACL (or a stand-in)
        # allows it, is refused by name instead of being silently ignored.
        current=(os.environ.get(MISSION_SELECTOR_ENV) or '').strip() or None
        if current!=self._selector_raw:
            refuse('MISSION_SELECTOR_WORKER_RESELECT')
        if (supervisor_binding() or {}).get('mission_id')!=self._bound_mission:
            refuse('SUPERVISOR_BINDING_CHANGED')
        if self.path is not None:return absolute_root(self.path)
        return machine_registry_path(self.mission)

    @contextmanager
    def hold_snapshot(self):
        """Keep the protected file and its ancestry pinned through SQL commit.

        A concurrent Owner revoke/replace must retry after an admitted transaction
        releases this read handle; it cannot invalidate half a transaction.
        """
        path=self._registry_path()
        if not path.is_file():
            # Never downgrade a pinned mission to the un-scoped constant: absence is a refusal.
            refuse('MISSION_REGISTRY_ABSENT' if self.mission else 'TRUST_BOOTSTRAP_REQUIRED')
        # A mission root is a different file, so it is re-measured rather than assumed: the machine
        # rule, the explicit DACL, the ancestor chain and (once the document is readable) the
        # declared checker SID's read reach. Unscoped B1 keeps `assert_protected` untouched.
        protect=assert_mission_protected if self.mission else assert_protected
        with held_root(path.parent):
            protect(path)
            with pinned_file(path) as stream:
                raw=stream.read()
                protect(path)
                data=strict_json(raw)
                if not isinstance(data,dict):refuse('REGISTRY_SCHEMA')
                if data.get('schema')!='HGK-NATIVE-REGISTRY/1' or data.get('canonical_profile')!=PROFILE:refuse('REGISTRY_SCHEMA')
                if data.get('status')!='ACTIVE' or not data.get('owner_os_sid') or not data.get('checker_os_sid'):refuse('REGISTRY_INACTIVE')
                if data['owner_os_sid']==data['checker_os_sid'] or data.get('maker_os_sid') in {data['owner_os_sid'],data['checker_os_sid']}:refuse('PRINCIPAL_SEPARATION')
                if not data.get('maker_os_sid') or not isinstance(data.get('approved_files'),list) or not data['approved_files']:refuse('SOURCE_PINS_REQUIRED')
                absolute_root(data.get('root'))
                # One file admits exactly one mission. Selection chose a file; the file now has to
                # agree with the selection, otherwise this is a mis-selection and not a choice.
                if self.mission is not None and data.get('mission_id')!=self.mission:refuse('MISSION_REGISTRY_MISMATCH')
                # Last: the file's own declared checker must be able to read it, measured on the
                # same path under the same pin.
                if self.mission is not None:
                    assert_mission_protected(path,data['checker_os_sid'])
                yield data

    _checker=None

    def snapshot(self):
        with self.hold_snapshot() as data:
            return data

def _ed25519_spki(raw_b64):
    """Raw 32-byte Ed25519 public key -> DER SubjectPublicKeyInfo, so verify_signature stays one path."""
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
    try:
        raw=base64.b64decode(raw_b64,validate=True)
    except Exception:refuse('USER_KEY_ENCODING')
    if len(raw)!=32:refuse('USER_KEY_SHAPE')
    try:
        pub=Ed25519PublicKey.from_public_bytes(raw)
    except Exception:refuse('USER_KEY_SHAPE')
    der=pub.public_bytes(serialization.Encoding.DER,serialization.PublicFormat.SubjectPublicKeyInfo)
    return base64.b64encode(der).decode('ascii')

def normalize_user_registry(data,scope_doc):
    """Turn the user-scoped trust anchor + its scope sidecar into the receiver's registry shape.

    Honest ceiling: this profile proves the issue/verify/revoke chain and key isolation by storage.
    It does NOT prove maker/checker OS-principal separation - the key is DPAPI-protected for the SAME
    user, so a process running as that user can ask DPAPI to unprotect it. `assurance_level` carries
    that ceiling into every receipt instead of hiding it.
    """
    if not isinstance(data,dict) or data.get('schema')!=USER_REGISTRY_SCHEMA:refuse('USER_REGISTRY_SCHEMA')
    if data.get('status')!='ACTIVE':refuse('REGISTRY_INACTIVE')
    owner=data.get('owner_os_sid');checker=data.get('checker_os_sid');maker=data.get('maker_os_sid')
    if not (owner and checker and maker):refuse('PRINCIPAL_MISSING')
    if len({owner.casefold(),checker.casefold(),maker.casefold()})!=3:refuse('PRINCIPAL_SEPARATION')
    if data.get('algorithm')!='Ed25519':refuse('KEY_ALGORITHM')
    key_id=data.get('key_id')
    if not isinstance(key_id,str) or not re.fullmatch(r'[A-Za-z0-9_-]{8,64}',key_id):refuse('USER_KEY_ID')
    if data.get('private_key_location') is None:refuse('USER_KEY_PROVENANCE')
    raw=json.dumps(data,sort_keys=True)
    if 'PRIVATE KEY' in raw or '"private_key"' in raw:refuse('USER_KEY_MATERIAL_IN_REGISTRY')
    anchor_epoch=data.get('policy_epoch')
    if type(anchor_epoch) is not int:refuse('POLICY_EPOCH')
    if not isinstance(scope_doc,dict):refuse('USER_PROFILE_SCOPE_REQUIRED')
    scope=scope_doc.get('scope')
    if not isinstance(scope,dict) or not scope.get('database_path') or not scope.get('head'):refuse('USER_PROFILE_SCOPE_REQUIRED')
    if type(scope_doc.get('policy_epoch')) is not int:refuse('USER_PROFILE_SCOPE_REQUIRED')
    if scope_doc['policy_epoch']!=anchor_epoch:refuse('USER_PROFILE_EPOCH_CONFLICT')
    for field in ('mission_id','source_manifest_sha256','policy_sha256','max_ttl_seconds','root','approved_files','task_kinds'):
        if field not in scope_doc:refuse('USER_PROFILE_SCOPE_REQUIRED')
    absolute_root(scope_doc['root'])
    kind=scope.get('task_kind')
    registered=scope_doc['task_kinds'].get(kind) if isinstance(scope_doc['task_kinds'],dict) else None
    if not registered or registered.get('state')!='REGISTERED':refuse('UNREGISTERED_KIND')
    return {'schema':'HGK-NATIVE-REGISTRY/1','canonical_profile':PROFILE,'status':'ACTIVE',
            'trust_profile':USER_PROFILE,'assurance_level':data.get('assurance_level'),
            'owner_os_sid':owner,'checker_os_sid':checker,'maker_os_sid':maker,
            'mission_id':scope_doc['mission_id'],'source_manifest_sha256':scope_doc['source_manifest_sha256'],
            'policy_sha256':scope_doc['policy_sha256'],'policy_epoch':anchor_epoch,
            'max_ttl_seconds':scope_doc['max_ttl_seconds'],'scope':scope,
            'root':scope_doc['root'],'approved_files':scope_doc['approved_files'],
            'task_kinds':scope_doc['task_kinds'],'task_kind':kind,
            'revoked_nonces':scope_doc.get('revoked_nonces',[]),
            'keys':{key_id:{'algorithm':'Ed25519','public_spki_b64':_ed25519_spki(data.get('public_key')),
                            'purposes':list(KINDS),'revoked':False}}}

class UserProfileRegistry:
    """Reads the %LOCALAPPDATA% trust root instead of the ProgramData constant.

    Same contract as ProtectedRegistry: hold the ancestry, prove the protection, read the bytes once
    under a pin, refuse on drift. The scope sidecar is a SEPARATE file so the trust anchor (which holds
    only public key + principals) is never edited to re-scope a mission.
    """
    def __init__(self,path=None,scope_path=None):
        self.path=absolute_root(path or registry_path(USER_PROFILE))
        self.scope_path=absolute_root(scope_path or (self.path.parent/USER_SCOPE_FILENAME))

    @contextmanager
    def hold_snapshot(self):
        if not self.path.is_file():refuse('USER_TRUST_BOOTSTRAP_REQUIRED')
        if not self.scope_path.is_file():refuse('USER_PROFILE_SCOPE_REQUIRED')
        with held_root(self.path.parent):
            assert_user_protected(self.path)
            assert_user_protected(self.scope_path)
            with pinned_file(self.path) as stream:
                raw=stream.read()
            assert_user_protected(self.path)
            anchor=strict_json(raw)
            with pinned_file(self.scope_path) as stream:
                scope_doc=strict_json(stream.read())
            assert_user_protected(self.scope_path)
            yield normalize_user_registry(anchor,scope_doc)

    def snapshot(self):
        with self.hold_snapshot() as data:
            return data

def default_registry():
    """The receiver the host builds when no injected provider was given."""
    return ProtectedRegistry() if trust_profile()==MACHINE_PROFILE else UserProfileRegistry()

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
                r=subprocess.run(['git','-C',str(root),'rev-parse','HEAD'],capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=10)
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
                r=subprocess.run(['git','-C',str(root),'rev-parse','HEAD'],capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=10)
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
        self.registry=registry or default_registry()

    @contextmanager
    def authorize(self,connection,operation,request,bundle):
        if not isinstance(bundle,dict) or set(bundle)!={'references','lease_generation'}:refuse('BUNDLE_REQUIRED')
        if operation not in PURPOSES:refuse('OPERATION')
        # The trust root is never request-selected. Name the refusal instead of letting a stray key
        # surface as an opaque request-digest mismatch; refuse the mission too, because the config
        # side owns that decision and a request may not even name it.
        if not isinstance(request,dict) or any(key in request for key in REQUEST_ROOT_KEYS):refuse('REQUEST_SELECTED_ROOT')
        if not hasattr(connection,'native_guards'):refuse('TRANSACTION_GUARD_REQUIRED')
        if isinstance(self.registry,(ProtectedRegistry,UserProfileRegistry)):
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
            current=subprocess.run(['git','-C',str(root),'rev-parse','HEAD'],capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=10)
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
