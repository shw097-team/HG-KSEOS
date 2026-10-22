# Design notes

Single evidence authority: evidence_refs stays the spine registry; evidence_graph.py (subjects.digest,
artifacts.subject_digest, verifications) is the projection, not a second authority.

Rejected alternatives: (a) an OFF/WARN enforcement-mode switch - Fabric defines no policy that authorises one,
and an agent-chosen default would be a self-serving weakening; (b) scoping the invariant by a per-requirement
governed marker - requirements has no such column, so it would cost another migration for no added enforcement.
