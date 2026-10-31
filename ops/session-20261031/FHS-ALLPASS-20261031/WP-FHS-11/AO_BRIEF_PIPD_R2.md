NONCE-ECHO: PIPD-AO2-741767A0

# Acceptance Officer brief, second sitting -- PIPD-LS-SP (one work package)

Your previous sitting returned overall FAIL on two clauses. The maker says both are addressed. Decide whether they are,
from the code and from running it. Do not take the maker's word for anything.

Subject: C:/Projects/Agent_Workspace/PIPD (read-only)
Run: `cd C:/Projects/Agent_Workspace/PIPD && PYTHONPATH=src python -m unittest tests.test_adversarial tests.test_abi tests.test_export_depth`

Clause 2 (was FAIL). You found `_verify_members` refused an unlisted regular file but ACCEPTED unlisted symlink,
directory and hardlink members. Decide now: is every non-regular member refused, listed or not? Try the same three
member types again, plus a listed-but-symlink case.

Clause 4 (was FAIL). You found the quoted digest prefixes had drifted. Current measurement to verify: LITE has 16
members and STANDARD 56, LITE is a strict subset of STANDARD, and their archive digests differ. Verify the counts,
the subset relation and the difference. Report the ACTUAL digests you measure; do not compare against any prefix.

Also re-confirm, briefly: (1) traversal refused, (3) tampered digest refused, (5) ASSURED refuses naming
independent_checker.

Print the verdict JSON as the LAST block of your reply (fenced ```json), shape:
{"nonce":"PIPD-AO2-741767A0","clauses":[{"id":2,"verdict":"PASS|FAIL","evidence":"..."},{"id":4,...}],
 "reconfirmed":[{"id":1,...},{"id":3,...},{"id":5,...}],"overall":"PASS|FAIL"}

Begin your reply with the nonce line exactly as given. Do not modify the subject.
