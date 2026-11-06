# Custom Slash Command: /review
Audit uncommitted Git diff changes before staging.
Check for:
1. Missing HTTP connection timeouts.
2. Unhandled null / undefined return values.
3. Race conditions or missing database locks (`SELECT ... FOR UPDATE`).
4. Silent exception swallowing (e.g., bare except / empty catch).
5. Hardcoded credentials or sensitive tokens.

