# FHS W1 r2 — issuer binding request (HG-KSEOS side)

**CANDIDATE ONLY · NO PERMIT · NO SECOND ISSUER · NO KEY MATERIAL.**

**ChangeSet:** `FHS-W1-R2-PREIMPL-20261105`
**Source:** W1 r2 author final, body `e40df2999fbffdb96a32a2e35cddce228abdd82080d5a5bedd415dfc938669ce`, source manifest `06628b6b4c6ba1b0d4d9b31b795141aaf51ade4c7df8304d1af093a229227f60`, ZIP `ce1e27ea948212b4312bf4243d9a6760d39b913e94bb5cc27fd871f378182e8e`

Claim ceiling of this change: **candidate evidence only**. It is not an acceptance, not a release, and it
carries no canonical or native standing.

`ISSUER_BINDING_REQUEST.json` is the same-scope question the W1 round needs answered by the original
HGK Issuer / SharedSpine: a WorkID binding, a Lease/Nonce/CAS reply, the WorldReader state, and the
Policy Loaded epoch for candidate `e40df2999fbf`.

Until that reply exists, every dependent effect stays `HOST_OPS` HOLD. Nothing in this directory is a
permit, an admission, a WorkOrder, or a world receipt.
