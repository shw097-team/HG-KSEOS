NONCE-ECHO: PIPD-AO-E167D692

# Acceptance Officer brief -- PIPD-LS-SP (one work package)

You are the independent checker. The maker has already written and run the suite below; your job is to decide whether
the CLAIMS survive an independent read, not to admire the tests.

Subject: C:/Projects/Agent_Workspace/PIPD (read-only)
Run: `cd C:/Projects/Agent_Workspace/PIPD && PYTHONPATH=src python -m unittest tests.test_adversarial tests.test_abi tests.test_export_depth tests.test_hotswap`

Decide these five claims, each PASS or FAIL, with the command output you relied on:

1. The packager refuses a member path that escapes the root (`ExportMemberUnsafe`), rather than filtering it silently.
2. An archive carrying a member the manifest does not promise is refused by `_verify_members`.
3. A tampered member digest is refused (`ExportVerificationFailed`).
4. `--profile LITE` and `--profile STANDARD` produce DIFFERENT archives (digests `e3e993b0e079` vs `52712b6316fb`) and
   LITE's member set is a subset of STANDARD's.
5. `--profile ASSURED` refuses with `PROFILE_VETO`, naming `independent_checker` as the missing capability.

Print the verdict JSON as the LAST block of your reply (a fenced ```json block). Do not write files -- the caller
records it. If you also write the file, that is fine, but the reply is what is read.
Shape: {"nonce":"PIPD-AO-E167D692","clauses":[{"id":1,"verdict":"PASS|FAIL","evidence":"..."}, ...],"overall":"PASS|FAIL"}

Rules: do not modify the subject. Do not accept a claim because a file exists -- run it. If a command fails, the
clause is FAIL and you say what failed. Begin your reply with the nonce line exactly as given above.
