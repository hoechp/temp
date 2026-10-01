"""Command-line calculator: python -m ultracomplexmath 'exp(pi*i)' --json."""

from __future__ import annotations

import argparse
import json

from .formula import evaluate


def main() -> None:
    parser = argparse.ArgumentParser(description="Eight-dimensional ultracomplex calculator")
    parser.add_argument(
        "expression", help="Formula with explicit multiplication; quote in your shell"
    )
    parser.add_argument("--json", action="store_true", help="Print all eight coefficients as JSON")
    parser.add_argument(
        "--legacy",
        action="store_true",
        help="Accept implicit multiplication and original word operators",
    )
    args = parser.parse_args()
    try:
        if args.legacy:
            from .expressions import Calculation

            result = Calculation(args.expression).result()
        else:
            result = evaluate(args.expression)
    except (ArithmeticError, ValueError, TypeError) as error:
        parser.exit(2, f"error: {error}\n")
    print(json.dumps(result.coefficients, allow_nan=False) if args.json else str(result))


if __name__ == "__main__":
    main()
