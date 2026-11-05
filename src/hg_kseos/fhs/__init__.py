"""FHS W1 engineering surfaces implemented inside HG-KSEOS.

Modules here are *candidate* control-plane wiring: they bind the W1 subject/scope/epoch/WorkID
contracts to the original HGK identities, they never issue a Permit and never accept on the maker's
behalf. Each module names the W1 first-fail it enforces.
"""
