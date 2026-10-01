# Contributing

Use Python 3.12+ and the setup/check commands in README.md. Keep code and
documentation in English. Preserve attribution to the original author.

For mathematical changes:

1. State the algebraic identity and its domain/branch assumptions.
2. Add an independent reference, exact example or property-based regression.
3. Keep exact equality separate from numerical tolerance.
4. Distinguish zero divisors, branch points and numerical conditioning.
5. Update migration notes for any intentional behavior change.

Keep the core dependency-free; optional plotting belongs outside it. Do not
replace explicit zero-divisor errors with silent NaNs, zero snapping or
pseudoinverses. Avoid mutating constants or accepting executable code through
the formula parser. The expression length/depth limits are guardrails, not a
promise of a hardened resource-isolation sandbox for hostile internet traffic.

Before proposing a change, run pytest, Ruff, mypy and the package build.
Check installed-wheel imports from outside the checkout for packaging changes.
`tools/legacy_probe.py` is an audit aid, not a requirement for normal tests.

The code is licensed under 0BSD, as selected by the owner. Do not add
PyPI credentials, automated release publishing or deployment as part of a
routine code change.
