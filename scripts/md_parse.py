#!/usr/bin/env python3
"""Shared Markdown parse for prose-polish-ru checkers.

Mechanical parse only: blocks, links, numbers, code. Does not claim
semantic equivalence. Callers must still review hedges, causation, and
claim strength by hand.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field


FENCE_OPEN_RE = re.compile(r"^(\s{0,3})(```|~~~)([^\n]*)\s*$")
HEADING_RE = re.compile(r"^(\s{0,3})(#{1,6})\s+(.+?)\s*#*\s*$")
HTML_HEADING_RE = re.compile(r"^(\s*)<h([1-6])\b[^>]*>(.*?)</h\2>\s*$", re.I)
HTML_U_RE = re.compile(r"<u>(.*?)</u>", re.I)
ESCAPED_HEADING_RE = re.compile(r"^(\s{0,3})\\(#{1,6})\s+(.+?)\s*$")
BOLD_HEADING_RE = re.compile(r"^(\s{0,3})\*\*(#{1,6}\s+.+?)\*\*\s*$")
LIST_RE = re.compile(r"^(\s*)([-*+]|\d+[.)])\s+")
TABLE_ROW_RE = re.compile(r"^\s*\|.*\|?\s*$")
TABLE_SEP_RE = re.compile(r"^\s*\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)+\|?\s*$")
HR_RE = re.compile(r"^\s{0,3}(?:-{3,}|\*{3,}|_{3,})\s*$")
REF_DEF_RE = re.compile(r"^(\s{0,3})\[([^\]]+)\]:\s+(\S+)(?:\s+(?:\"[^\"]*\"|'[^']*'))?\s*$")
INLINE_CODE_RE = re.compile(r"(?<!`)(`+)([^`\n]+?)\1(?!`)")
HTML_BLOCK_RE = re.compile(r"^\s*</?[a-zA-Z][\w:-]*\b")

WORD_RE = re.compile(r"[A-Za-zА-Яа-яЁё0-9-]+")
CONTENT_WORD_RE = re.compile(r"[A-Za-zА-Яа-яЁё]{2,}")

VERSION_RE = re.compile(
    r"(?<![\w./])v?(\d+(?:\.\d+){2,})(?![\w.])",
    re.I,
)
NUMBER_RE = re.compile(
    r"(?<![\w./])"
    r"(?P<sign>[+-])?"
    r"(?P<value>\d{1,3}(?:[ .\u00a0]\d{3})+|\d+)"
    r"(?:(?P<dec>[,.])(?P<frac>\d+))?"
    r"(?:\s*(?P<dash>[–—-])\s*"
    r"(?P<value2>\d{1,3}(?:[ .\u00a0]\d{3})+|\d+)"
    r"(?:(?P<dec2>[,.])(?P<frac2>\d+))?)?"
    r"(?:\s*(?P<unit>%|‰|×|x|мс|с|сек|мин|ч|дн(?:я|ей)?|байт|КБ|МБ|ГБ|ТБ|"
    r"k|K|M|B|руб\.?|₽|\$|€|USD|EUR|токен(?:ов|а)?|символ(?:ов|а)?|раз(?:а)?))?"
    r"(?![\w/])"
)

UNITS = (
    "%", "‰", "×", "x", "мс", "с", "сек", "мин", "ч",
    "байт", "КБ", "МБ", "ГБ", "ТБ", "k", "K", "M", "B",
    "руб", "₽", "$", "€", "USD", "EUR",
)


@dataclass(frozen=True)
class Block:
    kind: str
    start: int
    end: int
    text: str
    meta: dict = field(default_factory=dict)


@dataclass(frozen=True)
class NumberHit:
    raw: str
    sign: str
    value: str
    unit: str
    kind: str
    left: str
    right: str
    start: int
    end: int


@dataclass(frozen=True)
class LinkHit:
    kind: str
    label: str
    dest: str
    start: int
    end: int
    image: bool = False


@dataclass
class Parsed:
    text: str
    blocks: list[Block]
    fences: list[Block]
    tables: list[Block]
    headings: list[Block]
    lists: list[Block]
    html_blocks: list[Block]
    numbers: list[NumberHit]
    links: list[LinkHit]
    inline_code: list[tuple[int, int, str]]
    completeness: float
    notes: list[str]


def _line_offsets(text: str) -> list[tuple[int, int, str]]:
    lines: list[tuple[int, int, str]] = []
    pos = 0
    for raw in text.splitlines(keepends=True):
        lines.append((pos, pos + len(raw), raw))
        pos += len(raw)
    if not lines:
        lines.append((0, 0, ""))
    return lines


def split_table_row(line: str) -> list[str]:
    """Split a GFM table row, honoring escaped pipes."""
    stripped = line.strip()
    if stripped.startswith("|"):
        stripped = stripped[1:]
    if stripped.endswith("|") and not stripped.endswith("\\|"):
        stripped = stripped[:-1]
    cells: list[str] = []
    buf: list[str] = []
    i = 0
    while i < len(stripped):
        ch = stripped[i]
        if ch == "\\" and i + 1 < len(stripped):
            buf.append(stripped[i + 1])
            i += 2
            continue
        if ch == "|":
            cells.append("".join(buf).strip())
            buf = []
            i += 1
            continue
        buf.append(ch)
        i += 1
    cells.append("".join(buf).strip())
    return cells


def find_urls(text: str) -> list[tuple[int, int, str]]:
    """Find http(s) URLs, including nested parentheses in the path."""
    out: list[tuple[int, int, str]] = []
    i = 0
    lower = text.lower()
    while True:
        http = lower.find("http://", i)
        https = lower.find("https://", i)
        candidates = [p for p in (http, https) if p >= 0]
        if not candidates:
            break
        start = min(candidates)
        j = start
        depth = 0
        while j < len(text):
            ch = text[j]
            if ch.isspace() or ch in "<>\"'":
                break
            if ch == "(":
                depth += 1
            elif ch == ")":
                if depth == 0:
                    break
                depth -= 1
            elif ch == "]" and depth == 0:
                break
            j += 1
        url = text[start:j].rstrip(".,;:!?")
        out.append((start, start + len(url), url))
        i = start + len(url)
    return out


def _inline_links(text: str) -> list[LinkHit]:
    hits: list[LinkHit] = []
    i = 0
    n = len(text)
    while i < n:
        image = False
        if text[i] == "!" and i + 1 < n and text[i + 1] == "[":
            image = True
            lb = i + 1
        elif text[i] == "[":
            lb = i
        else:
            i += 1
            continue
        rb = text.find("]", lb + 1)
        if rb < 0:
            i += 1
            continue
        label = text[lb + 1 : rb]
        j = rb + 1
        if j < n and text[j] == "(":
            dest, end = _balanced_paren(text, j)
            if dest is not None:
                hits.append(LinkHit("inline", label, dest.strip(), i, end, image))
                i = end
                continue
        if j < n and text[j] == "[":
            rb2 = text.find("]", j + 1)
            if rb2 >= 0:
                ref = text[j + 1 : rb2].strip() or label
                hits.append(LinkHit("reference", label, ref, i, rb2 + 1, image))
                i = rb2 + 1
                continue
        i += 1
    return hits


def _balanced_paren(text: str, open_idx: int) -> tuple[str | None, int]:
    if open_idx >= len(text) or text[open_idx] != "(":
        return None, open_idx
    depth = 0
    i = open_idx
    while i < len(text):
        ch = text[i]
        if ch == "\\":
            i += 2
            continue
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                return text[open_idx + 1 : i], i + 1
        i += 1
    return None, open_idx


def _context_words(text: str, start: int, end: int, k: int = 2) -> tuple[str, str]:
    left_blob = text[max(0, start - 80) : start]
    right_blob = text[end : end + 80]
    left = CONTENT_WORD_RE.findall(left_blob)
    right = CONTENT_WORD_RE.findall(right_blob)
    return " ".join(left[-k:]), " ".join(right[:k])


def _norm_value(value: str, frac: str | None, dec: str | None) -> str:
    whole = re.sub(r"[ \u00a0]", "", value)
    if frac:
        return f"{whole}.{frac}"
    return whole


def extract_numbers(text: str, skip: list[tuple[int, int]] | None = None) -> list[NumberHit]:
    skip = skip or []

    def covered(a: int, b: int) -> bool:
        return any(a < e and b > s for s, e in skip)

    hits: list[NumberHit] = []
    occupied: list[tuple[int, int]] = []

    for m in VERSION_RE.finditer(text):
        if covered(m.start(), m.end()):
            continue
        left, right = _context_words(text, m.start(), m.end())
        hits.append(
            NumberHit(
                raw=m.group(0),
                sign="",
                value=m.group(1),
                unit="",
                kind="version",
                left=left,
                right=right,
                start=m.start(),
                end=m.end(),
            )
        )
        occupied.append((m.start(), m.end()))

    for m in NUMBER_RE.finditer(text):
        if covered(m.start(), m.end()):
            continue
        if any(m.start() < e and m.end() > s for s, e in occupied):
            continue
        sign = m.group("sign") or ""
        value = _norm_value(m.group("value"), m.group("frac"), m.group("dec"))
        unit = (m.group("unit") or "").lower().rstrip(".")
        kind = "range" if m.group("value2") else "number"
        if m.group("value2"):
            value2 = _norm_value(m.group("value2"), m.group("frac2"), m.group("dec2"))
            value = f"{value}-{value2}"
        left, right = _context_words(text, m.start(), m.end())
        hits.append(
            NumberHit(
                raw=m.group(0),
                sign=sign,
                value=value,
                unit=unit,
                kind=kind,
                left=left.lower(),
                right=right.lower(),
                start=m.start(),
                end=m.end(),
            )
        )
    return hits


def parse(text: str) -> Parsed:
    lines = _line_offsets(text)
    blocks: list[Block] = []
    notes: list[str] = []
    i = 0
    recognized = 0

    while i < len(lines):
        start, end, raw = lines[i]
        stripped = raw.strip("\n")
        fence = FENCE_OPEN_RE.match(stripped)
        if fence:
            marker = fence.group(2)
            lang = fence.group(3).strip()
            j = i + 1
            body_parts: list[str] = []
            while j < len(lines):
                if lines[j][2].lstrip().startswith(marker):
                    close_end = lines[j][1]
                    body = "".join(body_parts)
                    blocks.append(
                        Block(
                            "fence",
                            start,
                            close_end,
                            body,
                            {"lang": lang, "marker": marker},
                        )
                    )
                    recognized += close_end - start
                    i = j + 1
                    break
                body_parts.append(lines[j][2])
                j += 1
            else:
                notes.append("unclosed fence")
                blocks.append(Block("fence", start, lines[-1][1], "".join(body_parts), {"lang": lang, "unclosed": True}))
                recognized += lines[-1][1] - start
                i = len(lines)
            continue

        if TABLE_ROW_RE.match(stripped) and "|" in stripped:
            j = i
            rows: list[str] = []
            while j < len(lines) and TABLE_ROW_RE.match(lines[j][2].strip("\n")):
                rows.append(lines[j][2])
                j += 1
            table_end = lines[j - 1][1]
            cells = [split_table_row(r) for r in rows if not TABLE_SEP_RE.match(r.strip())]
            blocks.append(
                Block(
                    "table",
                    start,
                    table_end,
                    "".join(rows),
                    {"rows": len(cells), "cols": len(cells[0]) if cells else 0},
                )
            )
            recognized += table_end - start
            i = j
            continue

        heading = HEADING_RE.match(stripped)
        html_h = HTML_HEADING_RE.match(stripped)
        bold_h = BOLD_HEADING_RE.match(stripped)
        escaped_h = ESCAPED_HEADING_RE.match(stripped)
        if heading:
            blocks.append(
                Block(
                    "heading",
                    start,
                    end,
                    heading.group(3).strip(),
                    {"level": len(heading.group(2)), "raw": True},
                )
            )
            recognized += end - start
            i += 1
            continue
        if html_h:
            inner = re.sub(r"<[^>]+>", "", html_h.group(3)).strip()
            blocks.append(
                Block(
                    "heading",
                    start,
                    end,
                    inner,
                    {"level": int(html_h.group(2)), "html": True},
                )
            )
            recognized += end - start
            i += 1
            continue
        if bold_h:
            inner = bold_h.group(2).lstrip("#").strip()
            level = len(re.match(r"#+", bold_h.group(2)).group(0)) if re.match(r"#+", bold_h.group(2)) else 2
            blocks.append(Block("heading", start, end, inner, {"level": level, "bold_wrapped": True}))
            notes.append("bold-wrapped heading")
            recognized += end - start
            i += 1
            continue
        if escaped_h:
            notes.append("escaped heading")
            blocks.append(
                Block(
                    "paragraph",
                    start,
                    end,
                    stripped,
                    {"escaped_heading": True},
                )
            )
            recognized += end - start
            i += 1
            continue

        if LIST_RE.match(stripped):
            j = i
            items: list[str] = []
            while j < len(lines) and (
                LIST_RE.match(lines[j][2].strip("\n"))
                or (items and lines[j][2].startswith("  ") and lines[j][2].strip())
            ):
                items.append(lines[j][2])
                j += 1
            list_end = lines[j - 1][1]
            blocks.append(Block("list", start, list_end, "".join(items), {"items": len(items)}))
            recognized += list_end - start
            i = j
            continue

        if stripped.lstrip().startswith(">"):
            j = i
            while j < len(lines) and lines[j][2].lstrip().startswith(">"):
                j += 1
            q_end = lines[j - 1][1]
            blocks.append(Block("quote", start, q_end, "".join(x[2] for x in lines[i:j]), {}))
            recognized += q_end - start
            i = j
            continue

        ref = REF_DEF_RE.match(stripped)
        if ref:
            blocks.append(
                Block(
                    "ref_def",
                    start,
                    end,
                    ref.group(3),
                    {"id": ref.group(2).strip().lower(), "dest": ref.group(3)},
                )
            )
            recognized += end - start
            i += 1
            continue

        if HR_RE.match(stripped):
            blocks.append(Block("hr", start, end, stripped, {}))
            recognized += end - start
            i += 1
            continue

        if HTML_BLOCK_RE.match(stripped) or stripped.startswith("<u>"):
            blocks.append(Block("html", start, end, stripped, {}))
            recognized += end - start
            i += 1
            continue

        if not stripped.strip():
            blocks.append(Block("blank", start, end, raw, {}))
            recognized += end - start
            i += 1
            continue

        j = i + 1
        while j < len(lines):
            nxt = lines[j][2]
            if not nxt.strip():
                break
            if (
                FENCE_OPEN_RE.match(nxt.strip("\n"))
                or HEADING_RE.match(nxt.strip("\n"))
                or TABLE_ROW_RE.match(nxt.strip("\n"))
                or LIST_RE.match(nxt.strip("\n"))
                or nxt.lstrip().startswith(">")
            ):
                break
            j += 1
        p_end = lines[j - 1][1]
        para = "".join(x[2] for x in lines[i:j])
        italic_caption = bool(re.match(r"^\*(?!\*)(.+?)\*\s*$", para.strip()))
        bold_caption = bool(re.match(r"^\*\*(.+?)\*\*\s*$", para.strip()))
        blocks.append(
            Block(
                "caption" if italic_caption or bold_caption else "paragraph",
                start,
                p_end,
                para,
                {"italic": italic_caption, "bold": bold_caption},
            )
        )
        recognized += p_end - start
        i = j

    fences = [b for b in blocks if b.kind == "fence"]
    tables = [b for b in blocks if b.kind == "table"]
    headings = [b for b in blocks if b.kind == "heading"]
    lists = [b for b in blocks if b.kind == "list"]
    html_blocks = [b for b in blocks if b.kind == "html"]

    skip_spans = [(b.start, b.end) for b in fences]
    inline_code = [(m.start(), m.end(), m.group(2)) for m in INLINE_CODE_RE.finditer(text)]
    skip_spans.extend((a, b) for a, b, _ in inline_code)
    skip_spans.extend((a, b) for a, b, _ in find_urls(text))

    numbers = extract_numbers(text, skip_spans)
    links = _inline_links(text)
    for b in blocks:
        if b.kind == "ref_def":
            links.append(
                LinkHit("definition", b.meta.get("id", ""), b.meta.get("dest", ""), b.start, b.end)
            )

    n = max(len(text), 1)
    completeness = min(1.0, recognized / n)
    if any(b.meta.get("unclosed") for b in fences):
        notes.append("parse incomplete: unclosed fence")
    if any(b.kind == "html" for b in blocks):
        notes.append("html present")
    if any(b.meta.get("escaped_heading") for b in blocks):
        notes.append("escaped heading treated as paragraph")

    return Parsed(
        text=text,
        blocks=blocks,
        fences=fences,
        tables=tables,
        headings=headings,
        lists=lists,
        html_blocks=html_blocks,
        numbers=numbers,
        links=links,
        inline_code=inline_code,
        completeness=round(completeness, 3),
        notes=notes,
    )


def prose_spans(parsed: Parsed) -> list[tuple[int, int, str]]:
    """Paragraph running prose only: no lists, tables, captions, code, URLs."""
    skip = {(b.start, b.end) for b in parsed.fences}
    out: list[tuple[int, int, str]] = []
    for b in parsed.blocks:
        if b.kind != "paragraph":
            continue
        if (b.start, b.end) in skip:
            continue
        out.append((b.start, b.end, b.text))
    return out


def self_test() -> None:
    table = "| a \\| b | c |\n|---|---|\n| 1 | 2 |\n"
    assert split_table_row("| a \\| b | c |") == ["a | b", "c"]
    parsed = parse("# Title\n\nText 2.1.198 and -5% vs 5%.\n\n" + table)
    kinds = [b.kind for b in parsed.blocks]
    assert "heading" in kinds
    assert parsed.tables and parsed.tables[0].meta["rows"] == 2
    versions = [n for n in parsed.numbers if n.kind == "version"]
    assert versions and versions[0].value == "2.1.198"
    signed = [n for n in parsed.numbers if n.unit == "%" ]
    assert any(n.sign == "-" and n.value == "5" for n in signed)
    assert any(n.sign == "" and n.value == "5" for n in signed)
    nested = parse("[x](https://ex.com/a(b)/c)")
    assert any("a(b)" in hit.dest for hit in nested.links)
    ref = parse("[x][id]\n\n[id]: https://ex.com/ref\n")
    assert any(hit.kind == "reference" for hit in ref.links)
    assert any(hit.kind == "definition" and "ref" in hit.dest for hit in ref.links)
    html = parse("<h2>Раздел</h2>\n\n<u>1. пункт</u>\n")
    assert any(b.kind == "heading" and b.text == "Раздел" for b in html.headings)
    print("md_parse self-test: ok")


if __name__ == "__main__":
    self_test()
