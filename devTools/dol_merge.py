#!/usr/bin/env python3
"""Merge Twee and consolidated JS/CSS deltas into the raw DoL source tree.

Usage:
    python dol_merge.py delta.twee game_root \
        [--js-dump dol_diff_modules.js] [--css-dump dol_diff_modules.css] \
        [--source-root project_root] [--checkpoint DIR] [--compile]

Existing passages are replaced in the source file that owns their unique
header. New passages are written to a separate .twee patch file. Consolidated
script/style dumps are routed to their raw .js/.css files using block IDs and
source hints embedded by dol_diff.py. Removed content is reported, never
silently deleted.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


HEADER_RE = re.compile(r"(?m)^(?P<header>::[^\r\n]*)(?P<newline>\r\n|\n|$)")
TAGGED_HEADER_RE = re.compile(r"^(?P<name>.*?)(?:\s+\[(?P<tags>[^\]]*)\])?$")
DUMP_BLOCK_RE = re.compile(
    r"(?ms)^/\* BEGIN EXTRACTED (?P<key>[^*]+) \*/\r?\n"
    r"(?P<body>.*?)"
    r"^/\* END EXTRACTED (?P=key) \*/\r?\n?"
)
SOURCE_HINT_RE = re.compile(
    r"/\*\s*[^\r\n]*?:\s*\"(?P<path>[^\"]+)\"\s*\*/"
)


@dataclass(frozen=True)
class Passage:
    name: str
    tags: str
    body: str


@dataclass(frozen=True)
class SourcePassage:
    name: str
    tags: str
    path: Path
    body_start: int
    body_end: int
    newline: str


@dataclass(frozen=True)
class DumpBlock:
    key: str
    body: str


def split_header(header: str) -> tuple[str, str]:
    match = TAGGED_HEADER_RE.match(header[2:].strip())
    if not match:
        raise ValueError(f"Invalid Twee passage header: {header!r}")
    return match.group("name").strip(), (match.group("tags") or "").strip()


def parse_delta(path: Path) -> tuple[list[Passage], list[str]]:
    text = path.read_text(encoding="utf-8")
    matches = list(HEADER_RE.finditer(text))
    passages: list[Passage] = []
    removed: list[str] = []
    for index, match in enumerate(matches):
        name, tags = split_header(match.group("header"))
        body_start = match.end()
        body_end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        body = text[body_start:body_end].strip("\r\n")
        if name == "__REMOVED_PASSAGES__":
            removed.extend(line[2:].strip() for line in body.splitlines() if line.startswith("- "))
        elif not name.startswith("__HTML_"):
            passages.append(Passage(name=name, tags=tags, body=body))
    if not passages and not removed:
        raise ValueError(f"No Twee passages found in {path}")
    return passages, removed


def parse_dump(path: Path) -> list[DumpBlock]:
    text = path.read_text(encoding="utf-8")
    blocks = [DumpBlock(key=m.group("key").strip(), body=m.group("body")) for m in DUMP_BLOCK_RE.finditer(text)]
    if not blocks:
        raise ValueError(f"No extracted blocks found in {path}")
    keys = [block.key for block in blocks]
    if len(keys) != len(set(keys)):
        raise ValueError(f"Duplicate extracted block in {path}")
    return blocks


def index_source(game_root: Path) -> tuple[dict[str, SourcePassage], dict[Path, str]]:
    passages: dict[str, SourcePassage] = {}
    texts: dict[Path, str] = {}
    for path in sorted(game_root.rglob("*.twee")):
        text = path.read_text(encoding="utf-8")
        texts[path] = text
        matches = list(HEADER_RE.finditer(text))
        for index, match in enumerate(matches):
            name, tags = split_header(match.group("header"))
            if not name:
                raise ValueError(f"Blank passage name in {path}")
            if name in passages:
                raise ValueError(f"Duplicate passage {name!r}: {passages[name].path} and {path}")
            body_start = match.end()
            body_end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
            passages[name] = SourcePassage(
                name=name, tags=tags, path=path, body_start=body_start,
                body_end=body_end, newline=match.group("newline") or "\n",
            )
    return passages, texts


def replace_passages(
    delta: list[Passage], index: dict[str, SourcePassage], texts: dict[Path, str]
) -> tuple[dict[Path, str], list[Passage]]:
    replacements: dict[Path, list[tuple[int, int, str]]] = {}
    additions: list[Passage] = []
    for passage in delta:
        source = index.get(passage.name)
        if source is None:
            additions.append(passage)
            continue
        body = passage.body.replace("\r\n", "\n").replace("\n", source.newline)
        replacements.setdefault(source.path, []).append((source.body_start, source.body_end, body + source.newline))
    updated = dict(texts)
    for path, edits in replacements.items():
        text = texts[path]
        for start, end, replacement in sorted(edits, reverse=True):
            text = text[:start] + replacement + text[end:]
        updated[path] = text
    return updated, additions


def resolve_dump_target(key: str, body: str, source_root: Path) -> Path:
    try:
        kind, block_id = key.split(":", 1)
    except ValueError as error:
        raise ValueError(f"Invalid extracted block key: {key!r}") from error

    hint = SOURCE_HINT_RE.search(body)
    if kind == "script" and hint:
        hinted = hint.group("path").replace("\\\\", "\\")
        target = (source_root / Path(hinted)).resolve()
        if target.suffix.lower() != ".js":
            raise ValueError(f"Script hint does not point to .js: {key!r}")
    elif kind == "script":
        stem = block_id.split("#", 1)[0].removeprefix("script-module-")
        target = (source_root / "modules" / f"{stem}.js").resolve()
    elif kind == "style":
        stem = block_id.split("#", 1)[0]
        if stem.startswith("style-module-"):
            stem = stem.removeprefix("style-module-")
        elif stem == "style-named-npc-portrait":
            stem = "named-npc-portrait"
        else:
            raise ValueError(f"No raw CSS mapping for extracted block {key!r}")
        occurrence = ""
        if "#" in block_id:
            occurrence = "-" + block_id.rsplit("#", 1)[1]
        target = (source_root / "modules" / "css" / f"{stem}{occurrence}.css").resolve()
    else:
        raise ValueError(f"Unsupported extracted block type: {kind!r}")

    root = source_root.resolve()
    if target != root and root not in target.parents:
        raise ValueError(f"Resolved dump target escapes source root: {target}")
    return target


def split_user_script(block: DumpBlock) -> list[tuple[str, str]]:
    hints = list(SOURCE_HINT_RE.finditer(block.body))
    if not hints:
        raise ValueError("twine-user-script dump has no source hints")
    parts: list[tuple[str, str]] = []
    for index, hint in enumerate(hints):
        end = hints[index + 1].start() if index + 1 < len(hints) else len(block.body)
        source_path = hint.group("path").replace("\\\\", "\\")
        body = block.body[hint.end():end].strip("\r\n")
        parts.append((source_path, body))
    return parts


def replace_dump_blocks(
    dumps: list[tuple[Path, list[DumpBlock]]], source_root: Path
) -> tuple[dict[Path, str], list[Path], dict[str, str]]:
    updates: dict[Path, str] = {}
    special_styles: dict[str, str] = {}
    for dump_path, blocks in dumps:
        for block in blocks:
            if block.key == "script:twine-user-script":
                for hinted_path, body in split_user_script(block):
                    target = (source_root / Path(hinted_path)).resolve()
                    if target.suffix.lower() != ".js":
                        raise ValueError(f"Script hint does not point to .js: {hinted_path!r}")
                    updates[target] = body + "\n"
                continue
            if block.key == "style:style-named-npc-portrait":
                special_styles["named-npc-portrait"] = block.body.rstrip("\r\n")
                continue
            target = resolve_dump_target(block.key, block.body, source_root)
            existing = target.read_text(encoding="utf-8") if target.exists() else ""
            body = block.body.rstrip("\r\n")
            if target.exists() and existing.rstrip("\r\n") == body:
                continue
            updates[target] = body + "\n"
    return updates, list(updates), special_styles


def merge_special_styles(
    styles: dict[str, str], game_root: Path, source_root: Path
) -> tuple[dict[Path, str], list[Path]]:
    if not styles:
        return {}, []
    head_file = source_root / "devTools" / "head.html"
    original = head_file.read_text(encoding="utf-8")
    head = original
    for name, body in styles.items():
        tag = f'<style id="style-{name}" type="text/css">{body}</style>'
        pattern = re.compile(rf'(?is)<style id="style-{re.escape(name)}"[^>]*>.*?</style>')
        head = pattern.sub(tag, head) if pattern.search(head) else head + "\n" + tag + "\n"
    if head == original:
        return {}, []
    return {head_file: head}, [head_file]


def write_checkpoint(paths: list[Path], source_root: Path, checkpoint: Path) -> None:
    checkpoint.mkdir(parents=True, exist_ok=False)
    for path in paths:
        target = checkpoint / path.resolve().relative_to(source_root.resolve())
        target.parent.mkdir(parents=True, exist_ok=True)
        if path.exists():
            shutil.copy2(path, target)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("delta", type=Path)
    parser.add_argument("game_root", type=Path)
    parser.add_argument("--js-dump", type=Path)
    parser.add_argument("--css-dump", type=Path)
    parser.add_argument("--source-root", type=Path, help="project root containing game/ and modules/")
    parser.add_argument("--checkpoint", type=Path)
    parser.add_argument("--new-file", type=Path)
    parser.add_argument("--compile", action="store_true", help="run compile.bat after merging")
    args = parser.parse_args()
    source_root = (args.source_root or args.game_root.parent).resolve()

    try:
        delta, removed = parse_delta(args.delta)
        index, texts = index_source(args.game_root)
        updated, additions = replace_passages(delta, index, texts)
        dump_inputs = []
        if args.js_dump:
            dump_inputs.append((args.js_dump, parse_dump(args.js_dump)))
        if args.css_dump:
            dump_inputs.append((args.css_dump, parse_dump(args.css_dump)))
        dump_updates, dump_paths, special_styles = replace_dump_blocks(dump_inputs, source_root)
        special_updates, special_paths = merge_special_styles(special_styles, args.game_root, source_root)
        all_dump_updates = {**dump_updates, **special_updates}
        affected = [path for path in updated if updated[path] != texts[path]] + dump_paths + special_paths
        new_file = args.new_file or args.game_root / "zz-merged-delta.twee"
        if additions and new_file.exists():
            raise ValueError(f"New passage file already exists: {new_file}")
        if args.checkpoint:
            write_checkpoint(affected, source_root, args.checkpoint)
        for path in [path for path in updated if updated[path] != texts[path]]:
            path.write_text(updated[path], encoding="utf-8", newline="")
        for path, content in all_dump_updates.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8", newline="")
        if additions:
            content = "\n\n".join(
                f"::{p.name}{f' [{p.tags}]' if p.tags else ''}\n{p.body.rstrip()}" for p in additions
            ) + "\n"
            new_file.write_text(content, encoding="utf-8", newline="")
        for path, content in all_dump_updates.items():
            if path.read_text(encoding="utf-8").rstrip("\r\n") != content.rstrip("\r\n"):
                raise ValueError(f"Post-write validation failed: {path}")
        if args.compile:
            subprocess.run(["cmd", "/c", "compile.bat"], cwd=source_root, check=True)
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    print(
        f"updated_passages={len(delta) - len(additions)} added_passages={len(additions)} "
        f"updated_raw_blocks={len(all_dump_updates)} removed_reported={len(removed)} files={len(affected)}"
    )
    if removed:
        print("removed passages were reported only: " + ", ".join(removed))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())