# Custom Slash Command: /validate
Run terminal test suites and static type checks autonomously:
1. Run static type checker (`npx tsc --noEmit`).
2. Run test suites.
3. If errors occur, parse terminal output and propose atomic fix without manual intervention.

