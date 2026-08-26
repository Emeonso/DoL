#!/usr/bin/env python3
"""Compare exported DoL HTML files and emit a Twee delta.

Usage:
    python dol_diff.py baseline.html current.html output_delta.twee
    python dol_diff.py baseline.html current.html output_delta.twee --include-nonpassage

Passages are matched by name because Twine pids can drift between versions.
With --include-nonpassage, changed embedded script/style blocks are emitted as
Twee metadata passages so their source can be reviewed or routed to .js/.css
modules by a merge step.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import re
import sys
from dataclasses import dataclass
from pathlib import Path


PASSAGE_RE = re.compile(
    r"<tw-passagedata\b(?P<attrs>[^>]*)>(?P<body>.*?)</tw-passagedata\s*>",
    re.IGNORECASE | re.DOTALL,
)
BLOCK_RE = re.compile(
    r"<(?P<kind>script|style)\b(?P<attrs>[^>]*)>(?P<body>.*?)</(?P=kind)\s*>",
    re.IGNORECASE | re.DOTALL,
)
ATTR_RE = re.compile(
    r"(?P<name>[A-Za-z_:][\w:.-]*)"
    r"(?:\s*=\s*(?:\"(?P<dq>[^\"]*)\"|'(?P<sq>[^']*)'|(?P<bare>[^\s>]+)))?"
)


@dataclass(frozen=True)
class Passage:
    name: str
    tags: str
    body: str

    @property
    def digest(self) -> str:
        return hashlib.sha256(self.body.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class HtmlBlock:
    kind: str
    block_id: str
    body: str

    @property
    def key(self) -> str:
        return f"{self.kind}:{self.block_id}"

    @property
    def digest(self) -> str:
        return hashlib.sha256(self.body.encode("utf-8")).hexdigest()


def parse_attributes(raw: str) -> dict[str, str | bool]:
    attributes: dict[str, str | bool] = {}
    for match in ATTR_RE.finditer(raw):
        if match.group("dq") is not None:
            value = match.group("dq")
        elif match.group("sq") is not None:
            value = match.group("sq")
        elif match.group("bare") is not None:
            value = match.group("bare")
        else:
            value = True
        attributes[match.group("name").lower()] = value
    return attributes


def parse_passages(path: Path) -> dict[str, Passage]:
    text = path.read_text(encoding="utf-8")
    passages: dict[str, Passage] = {}
    for match in PASSAGE_RE.finditer(text):
        attrs = parse_attributes(match.group("attrs"))
        name = html.unescape(str(attrs.get("name", "")))
        tags = html.unescape(str(attrs.get("tags", "")))
        body = html.unescape(match.group("body"))
        if not name:
            raise ValueError(f"Passage without a name in {path}")
        if name in passages:
            raise ValueError(f"Duplicate passage name {name!r} in {path}")
        passages[name] = Passage(name=name, tags=tags, body=body)
    if not passages:
        raise ValueError(f"No <tw-passagedata> elements found in {path}")
    return passages


def parse_html_blocks(path: Path) -> dict[str, HtmlBlock]:
    text = path.read_text(encoding="utf-8")
    blocks: dict[str, HtmlBlock] = {}
    occurrences: dict[tuple[str, str], int] = {}
    for index, match in enumerate(BLOCK_RE.finditer(text), start=1):
        kind = match.group("kind").lower()
        attrs = parse_attributes(match.group("attrs"))
        base_id = str(attrs.get("id", f"{kind}-{index}"))
        occurrence_key = (kind, base_id)
        occurrences[occurrence_key] = occurrences.get(occurrence_key, 0) + 1
        occurrence = occurrences[occurrence_key]
        block_id = base_id if occurrence == 1 else f"{base_id}#{occurrence}"
        block = HtmlBlock(kind=kind, block_id=block_id, body=match.group("body"))
        blocks[block.key] = block
    return blocks


def twee_header(name: str, tags: str = "") -> str:
    name = name.replace("\r", " ").replace("\n", " ")
    return f"::{name}{f' [{tags}]' if tags else ''}"


def emit_passage(passage: Passage) -> str:
    return f"{twee_header(passage.name, passage.tags)}\n{passage.body.rstrip(chr(13) + chr(10))}\n"


def emit_html_block(block: HtmlBlock) -> str:
    prefix = "__HTML_SCRIPT__" if block.kind == "script" else "__HTML_STYLE__"
    tag = "meta script" if block.kind == "script" else "meta stylesheet"
    return f"{twee_header(prefix + block.block_id, tag)}\n{block.body.rstrip(chr(13) + chr(10))}\n"


def module_dump_kind(block: HtmlBlock) -> str | None:
    """Return the consolidated dump type for an application-owned HTML block."""
    block_id = block.block_id.split("#", 1)[0]
    if block.kind == "script" and block_id not in {"script-libraries", "script-sugarcube"}:
        return "js"
    if block.kind == "style" and (
        block_id.startswith("style-module-")
        or block_id == "style-named-npc-portrait"
    ):
        # These are generated from font assets rather than CSS source modules.
        if block_id in {
            "style-module-Lexend-VariableFont_wght",
            "style-module-OpenDyslexicMono-Regular",
        }:
            return None
        return "css"
    return None


def extract_raw_module_delta(
    baseline_path: Path, current_path: Path, dump_root: Path
) -> tuple[int, int, list[str]]:
    """Write changed application blocks to consolidated root-level JS/CSS dumps."""
    baseline = parse_html_blocks(baseline_path)
    current = parse_html_blocks(current_path)
    changed = [
        current[key]
        for key in sorted(current)
        if key not in baseline or baseline[key].digest != current[key].digest
    ]
    dumps: dict[str, list[str]] = {"js": [], "css": []}
    skipped: list[str] = []
    for block in changed:
        dump_kind = module_dump_kind(block)
        if dump_kind is None:
            skipped.append(block.key)
            continue
        extension = "js" if dump_kind == "js" else "css"
        dumps[dump_kind].append(
            f"/* BEGIN EXTRACTED {block.key} */\n"
            f"{block.body.rstrip(chr(13) + chr(10))}\n"
            f"/* END EXTRACTED {block.key} */\n"
        )
    dump_root.mkdir(parents=True, exist_ok=True)
    written = 0
    for dump_kind, sections in dumps.items():
        if not sections:
            continue
        path = dump_root / f"dol_diff_modules.{dump_kind}"
        path.write_text("\n".join(sections), encoding="utf-8", newline="")
        written += 1
    return written, len(changed), skipped


def diff_and_emit(
    baseline_path: Path,
    current_path: Path,
    output_path: Path,
    include_nonpassage: bool = False,
) -> tuple[int, int, int, int, int, int]:
    baseline = parse_passages(baseline_path)
    current = parse_passages(current_path)
    added = [current[name] for name in sorted(current) if name not in baseline]
    changed = [
        current[name]
        for name in sorted(current)
        if name in baseline and baseline[name].digest != current[name].digest
    ]
    removed = [baseline[name] for name in sorted(baseline) if name not in current]

    sections = [emit_passage(passage) for passage in added + changed]
    html_added = html_changed = html_removed = 0
    if include_nonpassage:
        baseline_blocks = parse_html_blocks(baseline_path)
        current_blocks = parse_html_blocks(current_path)
        html_added_blocks = [
            current_blocks[key] for key in sorted(current_blocks) if key not in baseline_blocks
        ]
        html_changed_blocks = [
            current_blocks[key]
            for key in sorted(current_blocks)
            if key in baseline_blocks and baseline_blocks[key].digest != current_blocks[key].digest
        ]
        html_removed_blocks = [
            baseline_blocks[key] for key in sorted(baseline_blocks) if key not in current_blocks
        ]
        sections.extend(emit_html_block(block) for block in html_added_blocks + html_changed_blocks)
        html_added, html_changed, html_removed = (
            len(html_added_blocks), len(html_changed_blocks), len(html_removed_blocks)
        )
        if html_removed_blocks:
            sections.append(
                ":: __REMOVED_HTML_BLOCKS__ [meta]\n"
                + "\n".join(f"- {block.key}" for block in html_removed_blocks)
                + "\n"
            )

    if removed:
        sections.append(
            ":: __REMOVED_PASSAGES__ [meta]\n"
            + "\n".join(f"- {passage.name}" for passage in removed)
            + "\n"
        )
    output_path.write_text("\n".join(sections), encoding="utf-8")
    return (
        len(added), len(changed), len(removed),
        html_added, html_changed, html_removed,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("baseline", type=Path, help="older exported HTML file")
    parser.add_argument("current", type=Path, help="newer exported HTML file")
    parser.add_argument("output", type=Path, help="destination .twee delta file")
    parser.add_argument(
        "--extract-modules",
        type=Path,
        metavar="MODULES_ROOT",
        help="write changed application blocks to root-level dol_diff_modules.js/.css dumps",
    )
    parser.add_argument(
        "--include-nonpassage",
        action="store_true",
        help="also emit changed embedded script/style blocks as Twee metadata passages",
    )
    args = parser.parse_args()
    try:
        result = diff_and_emit(
            args.baseline, args.current, args.output, args.include_nonpassage
        )
    except (OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    added, changed, removed, html_added, html_changed, html_removed = result
    if args.extract_modules:
        written, considered, skipped = extract_raw_module_delta(
            args.baseline, args.current, args.extract_modules
        )
        print(f"raw_modules_written={written} considered={considered} skipped={len(skipped)}")
        if skipped:
            print("skipped_blocks=" + ", ".join(skipped))
    print(
        f"added={added} changed={changed} removed={removed}"
        + (
            f" html_added={html_added} html_changed={html_changed}"
            f" html_removed={html_removed}"
            if args.include_nonpassage else ""
        )
        + f" -> {args.output}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())