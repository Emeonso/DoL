#!/usr/bin/env python3
"""Statically audit SugarCube widget definitions and calls in Twee source."""
from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path


PASSAGE_HEADER = re.compile(r"^::\s+([^\[]*?)(?:\s*\[([^]]*)\])?\s*$")
MACRO = re.compile(r"<<\s*(/?)\s*([A-Za-z][\w-]*)(.*?)>>", re.DOTALL)
WIDGET_NAME = re.compile(r"^\s*(?:(['\"])([A-Za-z][\w-]*)\1|([A-Za-z][\w-]*))")
HTML_COMMENT = re.compile(r"<!--[\s\S]*?-->")
BLOCK_COMMENT = re.compile(r"/\*[\s\S]*?\*/")
JS_MACRO_ADD = re.compile(r"\bMacro\.add\(\s*([\"'])([A-Za-z][\w-]*)\1")
JS_MACRO_ADD_ARRAY = re.compile(r"\bMacro\.add\(\s*\[([^]]*)\]")
JS_DEFINE_MACRO = re.compile(r"\bDefineMacroS?\(\s*([\"'])([A-Za-z][\w-]*)\1")
JS_STRING_LITERAL = re.compile(r"([\"'])([A-Za-z][\w-]*)\1")
STAT_DISPLAY_CREATE = re.compile(r"\bstatDisplay\.create\(\s*([\"'])([A-Za-z][\w-]*)\1")

EXAMPLE_PASSAGE_MARKERS = ("example", "sample", "template")

BUILT_INS = {
    "widget", "if", "elseif", "else", "for", "switch", "case", "default",
    "set", "unset", "run", "script", "print", "include", "display", "link",
    "linkappend", "linkprepend", "linkreplace", "button", "replace", "append",
    "prepend", "capture", "silently", "nobr", "break", "continue", "return",
    "goto", "exit", "exitall", "choice", "checkbox", "radiobutton", "textbox", "textarea", "listbox",
    "option", "optionsfrom", "cycle", "numberbox", "remove", "addclass",
    "removeclass", "toggleclass", "timed", "repeat", "stop", "done", "type",
    "audio", "cacheaudio", "createaudiogroup", "createplaylist", "masteraudio",
    "playlist", "onchange", "actions", "back", "compute", "dynamicblock",
    "safereplace", "twinescript",
}


@dataclass(frozen=True)
class Passage:
    name: str
    tags: frozenset[str]
    start: int
    end: int


@dataclass(frozen=True)
class Definition:
    name: str
    path: Path
    line: int
    passage: str
    passage_is_widget: bool
    passage_is_example: bool
    ordinal: int


@dataclass(frozen=True)
class Call:
    name: str
    path: Path
    line: int
    passage: str
    owner: str | None


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def mask_comments(text: str) -> str:
    def spaces(match: re.Match[str]) -> str:
        value = match.group(0)
        return "".join("\n" if char == "\n" else " " for char in value)

    return BLOCK_COMMENT.sub(spaces, HTML_COMMENT.sub(spaces, text))


def is_example_passage(passage: Passage) -> bool:
    name = passage.name.casefold()
    return any(marker in name for marker in EXAMPLE_PASSAGE_MARKERS) or "template" in passage.tags


def passages(text: str) -> list[Passage]:
    headers: list[tuple[int, int, str, frozenset[str]]] = []
    offset = 0
    for raw in text.splitlines(keepends=True):
        match = PASSAGE_HEADER.match(raw.rstrip("\r\n"))
        if match:
            tags = frozenset((match.group(2) or "").split())
            headers.append((offset, offset + len(raw), match.group(1).strip(), tags))
        offset += len(raw)
    result = []
    for index, (_, body_start, name, tags) in enumerate(headers):
        body_end = headers[index + 1][0] if index + 1 < len(headers) else len(text)
        result.append(Passage(name, tags, body_start, body_end))
    return result


def scan_file(path: Path) -> tuple[list[Definition], list[Call], list[str]]:
    original = path.read_text(encoding="utf-8-sig")
    text = mask_comments(original)
    definitions: list[Definition] = []
    calls: list[Call] = []
    findings: list[str] = []
    ordinal = 0

    for passage in passages(text):
        stack: list[tuple[str, int]] = []
        body = text[passage.start:passage.end]
        for token in MACRO.finditer(body):
            closing, raw_name, arguments = token.groups()
            name = raw_name.lower()
            absolute = passage.start + token.start()
            number = line_number(text, absolute)
            owner = stack[-1][0] if stack else None

            if name == "widget":
                if closing:
                    if not stack:
                        findings.append(f"{path}:{number}: closing widget has no opener")
                    else:
                        stack.pop()
                    continue

                match = WIDGET_NAME.match(arguments)
                if not match:
                    findings.append(f"{path}:{number}: widget name must be a quoted literal or bare identifier")
                    widget_name = f"<invalid@{number}>"
                else:
                    widget_name = match.group(2) or match.group(3)
                if stack:
                    findings.append(
                        f"{path}:{number}: nested widget {widget_name!r} is inside "
                        f"{stack[-1][0]!r} opened at line {stack[-1][1]}"
                    )
                ordinal += 1
                definitions.append(
                    Definition(
                        widget_name,
                        path,
                        number,
                        passage.name,
                        "widget" in passage.tags,
                        is_example_passage(passage),
                        ordinal,
                    )
                )
                stack.append((widget_name, number))
                continue

            if not closing:
                calls.append(Call(raw_name, path, number, passage.name, owner))

        for widget_name, number in stack:
            findings.append(f"{path}:{number}: widget {widget_name!r} is not closed before passage end")

    return definitions, calls, findings


def source_files(paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    for path in paths:
        if path.is_dir():
            files.extend(path.rglob("*.twee"))
            files.extend(path.rglob("*.tw"))
            files.extend(path.rglob("*.js"))
            files.extend(path.rglob("*.cjs"))
        elif path.suffix.lower() in {".twee", ".tw", ".js", ".cjs"}:
            files.append(path)
    return sorted(set(files))


def javascript_macro_names(paths: list[Path]) -> set[str]:
    names: set[str] = set()
    for path in paths:
        if path.suffix.lower() not in {".js", ".cjs"}:
            continue
        text = mask_comments(path.read_text(encoding="utf-8-sig"))
        names.update(match.group(2) for match in JS_MACRO_ADD.finditer(text))
        for match in JS_MACRO_ADD_ARRAY.finditer(text):
            names.update(item.group(2) for item in JS_STRING_LITERAL.finditer(match.group(1)))
        names.update(match.group(2) for match in JS_DEFINE_MACRO.finditer(text))
        names.update(match.group(2) for match in STAT_DISPLAY_CREATE.finditer(text))
    return names


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path, help="Twee files or source directories")
    parser.add_argument("--list", action="store_true", help="print widget registration order")
    parser.add_argument(
        "--calls", action="store_true", help="print calls grouped beneath their owning widget"
    )
    parser.add_argument(
        "--allow-unresolved", action="store_true", help="do not fail on calls absent from the supplied paths"
    )
    args = parser.parse_args()

    files = source_files(args.paths)
    if not files:
        print("No Twee source files found", file=sys.stderr)
        return 2

    twee_files = [path for path in files if path.suffix.lower() in {".twee", ".tw"}]
    definitions: list[Definition] = []
    calls: list[Call] = []
    findings: list[str] = []
    for path in twee_files:
        file_definitions, file_calls, file_findings = scan_file(path)
        definitions.extend(file_definitions)
        calls.extend(file_calls)
        findings.extend(file_findings)

    by_name: dict[str, list[Definition]] = defaultdict(list)
    for definition in definitions:
        by_name[definition.name].append(definition)

    for name, matches in sorted(by_name.items()):
        if len(matches) > 1:
            locations = ", ".join(f"{item.path}:{item.line}" for item in matches)
            findings.append(f"duplicate widget {name!r}: {locations}")
        for item in matches:
            if not item.passage_is_widget and not item.passage_is_example:
                findings.append(
                    f"{item.path}:{item.line}: widget {item.name!r} is in passage "
                    f"{item.passage!r}, which lacks the [widget] tag"
                )

    known = set(by_name) | javascript_macro_names(files)
    unresolved: dict[str, list[Call]] = defaultdict(list)
    for call in calls:
        if call.name not in known and call.name.lower() not in BUILT_INS and not call.name.startswith("-"):
            unresolved[call.name].append(call)
    if not args.allow_unresolved:
        for name, matches in sorted(unresolved.items()):
            sample = matches[0]
            suffix = f" ({len(matches)} calls)" if len(matches) > 1 else ""
            findings.append(f"{sample.path}:{sample.line}: unresolved macro {name!r}{suffix}")

    if args.list:
        for definition in definitions:
            print(
                f"{definition.path}:{definition.line}: #{definition.ordinal:03d} "
                f"{definition.name} [{definition.passage}]"
            )

    if args.calls:
        grouped: dict[tuple[Path, str | None], list[Call]] = defaultdict(list)
        for call in calls:
            grouped[(call.path, call.owner)].append(call)
        for (path, owner), owned_calls in grouped.items():
            if owner is None:
                continue
            names = ", ".join(sorted({call.name for call in owned_calls}, key=lambda value: (value.casefold(), value)))
            print(f"{path}: widget {owner} calls: {names}")

    for finding in findings:
        print(finding)

    if findings:
        print(f"\n{len(findings)} finding(s); {len(definitions)} widget definition(s) scanned.")
        return 1
    print(f"OK: {len(definitions)} widget definition(s) scanned across {len(files)} file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
