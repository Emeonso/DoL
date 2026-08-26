#!/usr/bin/env python3
"""Adjust reveal values in the source clothing item definitions.

By default this is a dry run. Pass --apply to rewrite the files.
Adjusted values have a minimum of 1.
Only exact ``reveal: <number>`` property lines in
``game/base-clothing/clothing-*.js`` are changed.
"""

from __future__ import annotations

import argparse
import re
import sys
from decimal import Decimal
from pathlib import Path


REVEAL_LINE = re.compile(
    r"^(?P<indent>\s*)reveal:\s*(?P<value>-?\d+(?:\.\d+)?)(?P<suffix>\s*,?\s*(?:\r?\n)?)$"
)
MIN_REVEAL = Decimal(1)


def format_number(value: Decimal) -> str:
    """Keep whole-number reveal values whole, including zero."""
    if value == value.to_integral_value():
        return str(int(value))
    return format(value, "f")


def process_file(path: Path, offset: Decimal, apply: bool) -> tuple[int, Decimal, Decimal]:
    """Report or apply one file and return count, original total, adjusted total."""
    with path.open("r", encoding="utf-8", newline="") as source:
        lines = source.readlines()

    changed = 0
    original_total = Decimal(0)
    adjusted_total = Decimal(0)
    output: list[str] = []

    for line in lines:
        match = REVEAL_LINE.match(line)
        if not match:
            output.append(line)
            continue

        original = Decimal(match.group("value"))
        adjusted = max(original - offset, MIN_REVEAL)
        original_total += original
        adjusted_total += adjusted
        changed += 1
        output.append(
            f"{match.group('indent')}reveal: {format_number(adjusted)}"
            f"{match.group('suffix')}"
        )

    if apply and changed:
        with path.open("w", encoding="utf-8", newline="") as target:
            target.writelines(output)

    return changed, original_total, adjusted_total


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Degrees of Lewdity workspace root (default: inferred from this script)",
    )
    parser.add_argument(
        "--offset",
        type=Decimal,
        default=Decimal(200),
        help="Amount to subtract from every reveal value (default: 200)",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Rewrite the source files; without this flag, only report changes",
    )
    args = parser.parse_args()

    if args.offset < 0:
        parser.error("--offset must be zero or greater")

    source_dir = args.root / "game" / "base-clothing"
    files = sorted(source_dir.glob("clothing-*.js"))
    if not files:
        print(f"No clothing source files found under {source_dir}", file=sys.stderr)
        return 1

    mode = "APPLY" if args.apply else "DRY RUN"
    print(
        f"{mode}: subtracting {format_number(args.offset)} from reveal values "
        f"(minimum output: {format_number(MIN_REVEAL)})"
    )
    print(f"Scope: {source_dir / 'clothing-*.js'}")

    total_count = 0
    total_original = Decimal(0)
    total_adjusted = Decimal(0)
    for path in files:
        count, original, adjusted = process_file(path, args.offset, args.apply)
        if count:
            total_count += count
            total_original += original
            total_adjusted += adjusted
            print(
                f"{path.name}: {count} values, "
                f"total {format_number(original)} -> {format_number(adjusted)}"
            )

    print(
        f"TOTAL: {total_count} reveal values, "
        f"total {format_number(total_original)} -> {format_number(total_adjusted)}"
    )
    if not args.apply:
        print("No files changed. Re-run with --apply to write the adjustment.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
