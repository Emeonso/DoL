#!/usr/bin/env python3
"""Report malformed and unbalanced SugarCube structural macros in Twee files."""
from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path

MACRO_START = re.compile(r"<<\s*(/?)\s*([A-Za-z][\w-]*)\b")
MALFORMED_CLOSE = re.compile(r"<<\s*</\s*/")
OPENERS = {"if","for","switch","replace","link","linkappend","linkprepend","linkreplace","widget","capture","button","timed","silently","nobr","prepend","append"}
BRANCHES = {"else":"if","elseif":"if","case":"switch","default":"switch"}

def iter_tokens(line: str, line_number: int, state: dict):
    """Yield real macro tokens across lines, ignoring quoted macro text."""
    if (
        state.get("active")
        and state.get("last_line") != line_number
        and state.get("name", "").lower() != "run"
    ):
        # Macro arguments may span physical lines. A quote that began on a
        # previous line should not hide the terminator of a later line.
        state["quote"] = None
        state["quote_start"] = None
        state["escaped"] = False
    state["last_line"] = line_number

    position = 0
    while position < len(line) or state.get("active"):
        if not state.get("active"):
            start = MACRO_START.search(line, position)
            if not start:
                return
            state.update(
                active=True,
                closing=start.group(1),
                name=start.group(2),
        quote=None,
        quote_start=None,
        passage_link=False,
        escaped=False,
                start_line=line_number,
            )
            position = start.end()

        while position < len(line):
            character = line[position]
            quote = state["quote"]
            if (
                line.startswith("<<", position)
                and (
                    state["name"].lower() == "print"
                    or (
                        state["name"].lower() == "run"
                        and state.get("start_line") != line_number
                    )
                )
            ):
                embedded_end = line.find(">>", position + 2)
                if embedded_end != -1:
                    position = embedded_end + 2
                    continue
            if state["passage_link"]:
                if line.startswith("]]", position):
                    state["passage_link"] = False
                    position += 2
                else:
                    position += 1
                continue
            if (
                not quote
                and state["name"].lower() in ("link", "linkappend", "linkprepend", "linkreplace")
                and line.startswith("[[", position)
            ):
                state["passage_link"] = True
                position += 2
                continue
            if line.startswith(">>", position):
                # Treat an empty, unterminated quote immediately before the
                # macro terminator as part of the macro text. This keeps a
                # stray quote from hiding subsequent closing macros.
                if quote and state["quote_start"] == position - 1 and line[position - 1] == quote:
                    state["quote"] = None
                    quote = None
                if quote:
                    position += 2
                    continue
                yield state["closing"], state["name"], state["start_line"]
                state.clear()
                position += 2
                break
            if state["escaped"]:
                state["escaped"] = False
            elif character == "\\" and quote:
                state["escaped"] = True
            elif quote:
                if character == quote:
                    state["quote"] = None
            elif character in ("'", '"', "`"):
                state["quote"] = character
                state["quote_start"] = position
            position += 1
        else:
            return

def mask_html_comments(line: str, in_comment: bool) -> tuple[str, bool]:
    """Replace HTML comment contents with spaces without changing line text."""
    output = []
    position = 0

    while position < len(line):
        if in_comment:
            end = line.find("-->", position)
            if end == -1:
                output.append(" " * (len(line) - position))
                return "".join(output), True
            output.append(" " * (end + 3 - position))
            position = end + 3
            in_comment = False
            continue

        start = line.find("<!--", position)
        if start == -1:
            output.append(line[position:])
            break

        output.append(line[position:start])
        end = line.find("-->", start + 4)
        if end == -1:
            output.append(" " * (len(line) - start))
            return "".join(output), True
        output.append(" " * (end + 3 - start))
        position = end + 3

    return "".join(output), in_comment


def mask_block_comments(line: str, in_comment: bool) -> tuple[str, bool]:
    """Replace C-style block comment contents with spaces."""
    output = []
    position = 0

    while position < len(line):
        if in_comment:
            end = line.find("*/", position)
            if end == -1:
                output.append(" " * (len(line) - position))
                return "".join(output), True
            output.append(" " * (end + 2 - position))
            position = end + 2
            in_comment = False
            continue

        start = line.find("/*", position)
        if start == -1:
            output.append(line[position:])
            break

        output.append(line[position:start])
        end = line.find("*/", start + 2)
        if end == -1:
            output.append(" " * (len(line) - start))
            return "".join(output), True
        output.append(" " * (end + 2 - start))
        position = end + 2

    return "".join(output), in_comment


def scan(path: Path) -> list[str]:
    findings, stack = [], []
    in_html_comment = False
    in_block_comment = False
    macro_state = {}
    for number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line, in_html_comment = mask_html_comments(raw_line, in_html_comment)
        line, in_block_comment = mask_block_comments(line, in_block_comment)
        if line.startswith(":: "):
            if stack:
                findings.append(f"{path}:{number}: passage boundary with unclosed {stack[-1][0]} from line {stack[-1][1]}")
                stack.clear()
        if MALFORMED_CLOSE.search(line):
            findings.append(f"{path}:{number}: malformed closing macro")
        for closing, name, token_line in iter_tokens(line, number, macro_state):
            name = name.lower()
            if name in BRANCHES:
                if not stack or stack[-1][0] != BRANCHES[name]:
                    findings.append(f"{path}:{token_line}: {name} does not match current structure")
            elif name in OPENERS and not closing:
                stack.append((name, token_line))
            elif name in OPENERS and closing:
                if not stack:
                    findings.append(f"{path}:{token_line}: closing {name} has no opener")
                elif stack[-1][0] != name:
                    findings.append(f"{path}:{token_line}: closing {name} mismatches {stack[-1][0]} from line {stack[-1][1]}")
                else:
                    stack.pop()
    for name, number in stack:
        findings.append(f"{path}:EOF: unclosed {name} from line {number}")
    return findings

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path)
    args = parser.parse_args()
    files = [p for root in args.paths for p in (root.rglob("*.twee") if root.is_dir() else [root])]
    findings = [finding for path in files for finding in scan(path)]
    print("\n".join(findings))
    return 1 if findings else 0

if __name__ == "__main__":
    sys.exit(main())
