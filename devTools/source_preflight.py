#!/usr/bin/env python3
"""Universal pre-compile checks for high-confidence SugarCube source errors."""
from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LINK_RE = re.compile(r'<<\s*link\s+([^>\r\n]*)>>', re.IGNORECASE)
WIDGET_RE = re.compile(r'<<\s*widget\s+([^>\r\n]*)>>', re.IGNORECASE)
RUN_RE = re.compile(r'<<\s*run\b(.*?)>>', re.IGNORECASE | re.DOTALL)
SELECT_MODEL_RE = re.compile(
    r'''<<\s*selectmodel\s+(["'])([A-Za-z_$][\w$-]*)\1''',
    re.IGNORECASE,
)
MODEL_REGISTRATION_RE = re.compile(
    r'\bRenderer\.CanvasModels\.([A-Za-z_$][\w$]*)\s*=',
)
JS_COMMENT_RE = re.compile(r'//[^\r\n]*|/\*[\s\S]*?\*/')
WINDOW_HELPER_RE = re.compile(
    r'\bwindow\.([A-Za-z_$][\w$]*)\s*=\s*(?:(?!>>).)*(?:\bfunction\b|=>)',
    re.IGNORECASE | re.DOTALL,
)
MALFORMED_BACKTICK_LINK_RE = re.compile(
    r"<<\s*(?:link|linkappend|linkprepend|linkreplace)\s+`[^`\r\n]*`\s*[\"']\s*>>",
    re.IGNORECASE,
)
QUOTED_LINK_EXPRESSION_RE = re.compile(
    r'''<<\s*(?:link|linkappend|linkprepend|linkreplace)\s+["']\s*(?:[$_][A-Za-z][\w$]*\s*(?:[.\[]|[+?:])|[A-Za-z][\w$]*\s*[.\[])''',
    re.IGNORECASE,
)
HTML_TAG_RE = re.compile(r"<(/?)\s*([A-Za-z][\w:-]*)\b[^>]*?(/?)\s*>", re.DOTALL)
MACRO_NAME_RE = re.compile(r"<<\s*(/?)\s*([A-Za-z][\w-]*)\b", re.IGNORECASE)
HTML_COMMENT_RE = re.compile(r"<!--[\s\S]*?-->")
VOID_HTML_TAGS = frozenset({
    "area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr",
})


def mask_js_comments(source: str) -> str:
    def spaces(match: re.Match[str]) -> str:
        value = match.group(0)
        return "".join("\n" if char == "\n" else " " for char in value)

    return JS_COMMENT_RE.sub(spaces, source)


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def is_dynamic_expression(label: str) -> bool:
    label = label.lstrip()
    return not label.startswith(("`", '"', "'", "[["))


def check_widget_runs(source: str, path: Path, findings: list[str]) -> None:
    """Reject exported JavaScript helpers declared inside SugarCube widgets."""
    widgets = list(WIDGET_RE.finditer(source))
    for index, widget in enumerate(widgets):
        body_end = widgets[index + 1].start() if index + 1 < len(widgets) else len(source)
        body = source[widget.end():body_end]
        widget_name = widget.group(1).strip()

        for run in RUN_RE.finditer(body):
            helper = WINDOW_HELPER_RE.search(run.group(1))
            if helper:
                offset = widget.end() + run.start()
                findings.append(
                    f"JavaScript helper '{helper.group(1)}' is declared inside widget "
                    f"{widget_name} at {path}:{line_number(source, offset)}; "
                    "move helper code to a JavaScript module under game/03-JavaScript/"
                )


def check_macro_terminators(source: str, path: Path, findings: list[str]) -> None:
    """Reject stray quotes after backtick link expressions.

    ``<<link `expression`>>`` is valid SugarCube syntax. A quote between the
    closing backtick and ``>>`` leaves SugarCube's macro argument scanner in a
    quoted state, which can swallow the following ``<</widget>>`` boundary.
    Tweego may still compile the passage, but later widgets then fail to
    register at runtime.
    """
    for match in MALFORMED_BACKTICK_LINK_RE.finditer(source):
        findings.append(
            f"stray quote after backtick link expression at {path}:"
            f"{line_number(source, match.start())}; use <<link `expression`>> "
            "with no quote between the closing backtick and >>"
        )

    for match in QUOTED_LINK_EXPRESSION_RE.finditer(source):
        line_start = source.rfind("\n", 0, match.start()) + 1
        if source[line_start : match.start()].count("`") % 2:
            # This is macro text inside a JavaScript template literal, not a
            # real macro invocation being parsed by SugarCube.
            continue
        findings.append(
            f"quoted JavaScript-looking link expression at {path}:"
            f"{line_number(source, match.start())}; use <<link `expression`>> "
                "for a dynamic label instead of quoting the expression as a string"
        )


def check_html_macro_boundaries(source: str, path: Path, findings: list[str]) -> None:
    """Reject marked visual containers crossing a conditional branch boundary.

    SugarCube parses each conditional branch as its own fragment. An HTML element
    opened in one fragment cannot be closed after the branch ends, even though
    the resulting source may look balanced to a normal HTML reader. Ordinary
    project markup is intentionally excluded because existing widgets use it
    across alternate branches.
    """
    html_stack: list[tuple[str, int, tuple[str, ...], bool]] = []
    macro_context: list[str] = []
    masked_source = HTML_COMMENT_RE.sub(lambda match: "".join("\n" if char == "\n" else " " for char in match.group(0)), source)

    macro_tokens = []
    position = 0
    while position < len(source):
        start = source.find("<<", position)
        if start == -1:
            break
        macro = MACRO_NAME_RE.match(source, start)
        if not macro:
            position = start + 2
            continue
        quote = None
        escaped = False
        token_end = len(source)
        scan = macro.end()
        while scan < len(source):
            character = source[scan]
            if escaped:
                escaped = False
            elif quote and character == "\\":
                escaped = True
            elif quote:
                if character == quote:
                    quote = None
            elif character in ("'", '"', "`"):
                quote = character
            elif source.startswith(">>", scan):
                token_end = scan + 2
                break
            scan += 1
        macro_tokens.append((start, token_end, macro.group(1), macro.group(2).lower()))
        position = token_end

    html_tokens = [(match.start(), match) for match in HTML_TAG_RE.finditer(masked_source)]
    events = [(start, token_end, closing, name, "macro") for start, token_end, closing, name in macro_tokens]
    events.extend((start, match.end(), None, match, "html") for start, match in html_tokens)
    events.sort(key=lambda event: event[0])
    macro_index = 0

    for start, _, closing, value, kind in events:
        if kind == "macro":
            name = value
            if name in {"if", "switch"}:
                if closing:
                    if macro_context and macro_context[-1] == name:
                        macro_context.pop()
                else:
                    macro_context.append(name)
            continue

        while macro_index < len(macro_tokens) and macro_tokens[macro_index][1] <= start:
            macro_index += 1
        if macro_index < len(macro_tokens) and macro_tokens[macro_index][0] <= start < macro_tokens[macro_index][1]:
            continue
        tag_closing, name, self_closing = value.groups()
        name = name.lower()
        if tag_closing:
            match_index = next((index for index in range(len(html_stack) - 1, -1, -1) if html_stack[index][0] == name), None)
            if match_index is None:
                continue
            opened_name, opened_offset, opened_context, monitored = html_stack.pop(match_index)
            current_context = tuple(macro_context)
            if monitored and opened_context != current_context:
                findings.append(
                    f"HTML <{opened_name}> opened in a SugarCube conditional branch but closed in a different branch context "
                    f"at {path}:{line_number(source, opened_offset)}-{line_number(source, start)}; "
                    "keep the opening and closing tags in the same <<if>>/<<switch>> branch"
                )
        elif not self_closing and name not in VOID_HTML_TAGS:
            monitored = "data-main-passage-visual" in value.group(0).lower()
            html_stack.append((name, start, tuple(macro_context), monitored))


def collect_registered_models() -> set[str]:
    models: set[str] = set()
    for path in sorted((ROOT / "game").rglob("*.js")):
        source = mask_js_comments(path.read_text(encoding="utf-8"))
        models.update(match.group(1) for match in MODEL_REGISTRATION_RE.finditer(source))
    return models


def check_select_models(source: str, path: Path, registered_models: set[str], findings: list[str]) -> None:
    """Reject literal CanvasModel names which have no source registration."""
    for match in SELECT_MODEL_RE.finditer(source):
        model_name = match.group(2)
        if model_name not in registered_models:
            findings.append(
                f"selectmodel requests unregistered CanvasModel {model_name!r} at "
                f"{path}:{line_number(source, match.start())}; register "
                "Renderer.CanvasModels.<name> or use an existing model"
            )


def main() -> int:
    findings: list[str] = []
    registered_models = collect_registered_models()
    for path in sorted((ROOT / "game").rglob("*.twee")):
        source = path.read_text(encoding="utf-8")

        for match in LINK_RE.finditer(source):
            label = match.group(1).strip()
            if not is_dynamic_expression(label):
                continue
            if "?" in label or re.search(r"\s[+]\s", label):
                findings.append(
                    f"unquoted dynamic link label at {path}:"
                    f"{line_number(source, match.start())}; "
                    "use a backtick expression or a quoted/passage link label"
                )

        check_widget_runs(source, path, findings)
        check_macro_terminators(source, path, findings)
        check_html_macro_boundaries(source, path, findings)
        check_select_models(source, path, registered_models, findings)

    if findings:
        print("\n".join(f"ERROR: {finding}" for finding in findings))
        return 1

    print("Universal source preflight passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
