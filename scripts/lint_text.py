#!/usr/bin/env python3
"""Conservative Russian prose linter for prose-polish-ru.

Findings are review prompts, not proof of AI authorship. The scanner masks code,
URLs, formulas, tables, and Markdown destinations before prose checks.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class Finding:
    code: str
    severity: str
    category: str
    line: int
    message: str
    evidence: str


PHRASES: dict[str, tuple[str, str, str]] = {
    r"\bважно отметить\b": ("W01", "water", "Empty importance marker"),
    r"\bстоит (?:отметить|подчеркнуть)\b": ("W02", "water", "Meta-emphasis"),
    r"\bнеобходимо понимать\b": ("W03", "water", "Reader instruction instead of content"),
    r"\bследует учитывать\b": ("W04", "water", "Generic caution"),
    r"\bна сегодняшний день\b": ("W05", "water", "Disposable time framing"),
    r"\bв современном (?:мире|обществе)\b": ("W06", "water", "Generic opening"),
    r"\bниже (?:мы )?(?:рассмотрим|разбер[её]м)\b": ("W07", "water", "Prose table of contents"),
    r"\bтаким образом\b": ("T01", "transition", "Check whether inference is earned"),
    r"\bболее того\b": ("T02", "transition", "Check whether escalation is real"),
    r"\bпомимо этого\b": ("T03", "transition", "Formulaic additive transition"),
    r"\bиными словами\b": ("T04", "transition", "Check for redundant restatement"),
    r"\bдругими словами\b": ("T05", "transition", "Check for redundant restatement"),
    r"\bэто не просто\b": ("C01", "contrast", "Formulaic contrast"),
    r"\bречь (?:ид[её]т|не ид[её]т) (?:не )?о\b": ("C02", "contrast", "Formulaic reframing"),
    r"\bне только\b.{0,100}\bно и\b": ("C03", "contrast", "Not-only-but-also template"),
    r"\bпредставляет собой\b": ("L01", "diction", "Bureaucratic predicate"),
    r"\bданн(?:ый|ая|ое|ые|ого|ому|ым|ых)\b": ("L02", "diction", "Demonstrative bureaucracy"),
    r"\bосуществл(?:ять|ение|яется)\b": ("L03", "diction", "Nominal bureaucratic verb"),
    r"\bв рамках\b": ("L04", "diction", "Bureaucratic preposition"),
    r"\bиграет (?:важную|ключевую) роль\b": ("S01", "significance", "Unspecified significance"),
    r"\bоткрывает новые возможности\b": ("S02", "significance", "Generic benefit"),
    r"\bменяет правила игры\b": ("S03", "significance", "Inflated framing"),
    r"\bневозможно переоценить\b": ("S04", "significance", "Inflated framing"),
    r"\bкомплексн(?:ый|ая|ое) подход\b": ("A01", "abstraction", "Generic abstraction"),
    r"\bповышени[ея] эффективности\b": ("A02", "abstraction", "Name the measurable effect"),
    r"\bоптимизаци[яи] процессов\b": ("A03", "abstraction", "Name the changed process"),
    r"\b[пП]о моему опыту\b": ("V01", "voice", "Verify that concrete experience follows"),
    r"\bисследования показывают\b": ("E01", "evidence", "Citation may be required"),
    r"\bэксперты (?:считают|отмечают|говорят)\b": ("E02", "evidence", "Unnamed authority"),
}

PLACEHOLDERS = re.compile(
    r"(?:\[(?:ссылка|источник|вставить[^\]]*|cta|пример)\]|"
    r"\{\{[^}]+\}\}|<(?:NAME|URL|TODO|PLACEHOLDER)>)",
    re.IGNORECASE,
)
LEAKS = re.compile(r"\b(?:turn\d+(?:search|view|fetch)\d+|oaicite|oai_citation)\b", re.I)
URL_RE = re.compile(r"https?://[^\s)>\]]+")
MD_LINK_RE = re.compile(r"(!?)\[([^\]]*)\]\(([^)]+)\)")
INLINE_CODE_RE = re.compile(r"`[^`\n]+`")
SENTENCE_RE = re.compile(r"(?<=[.!?…])\s+(?=[А-ЯA-ZЁ])")
WORD_RE = re.compile(r"[A-Za-zА-Яа-яЁё0-9-]+")
MIXED_SCRIPT_RE = re.compile(
    r"\b(?=[A-Za-zА-Яа-яЁё]*[A-Za-z])(?=[A-Za-zА-Яа-яЁё]*[А-Яа-яЁё])[A-Za-zА-Яа-яЁё]+\b"
)


def mask_fences(lines: list[str]) -> tuple[list[str], set[int]]:
    masked: list[str] = []
    protected: set[int] = set()
    in_fence = False
    marker = ""
    for idx, line in enumerate(lines, start=1):
        stripped = line.lstrip()
        if not in_fence and (stripped.startswith("```") or stripped.startswith("~~~")):
            in_fence = True
            marker = stripped[:3]
            protected.add(idx)
            masked.append("")
            continue
        if in_fence:
            protected.add(idx)
            masked.append("")
            if stripped.startswith(marker):
                in_fence = False
            continue
        masked.append(line)
    return masked, protected


def is_table_line(line: str) -> bool:
    stripped = line.strip()
    return stripped.startswith("|") and stripped.endswith("|") and stripped.count("|") >= 2


def prose_only(line: str) -> str:
    line = MD_LINK_RE.sub(lambda m: m.group(2) if not m.group(1) else "", line)
    line = URL_RE.sub("", line)
    line = INLINE_CODE_RE.sub("", line)
    line = re.sub(r"^\s{0,3}(?:#{1,6}|[-*+] |\d+[.)] |> )", "", line)
    return line


def evidence(text: str, limit: int = 140) -> str:
    clean = re.sub(r"\s+", " ", text).strip()
    return clean if len(clean) <= limit else clean[: limit - 1] + "…"


def add(findings: list[Finding], code: str, severity: str, category: str,
        line: int, message: str, text: str) -> None:
    findings.append(Finding(code, severity, category, line, message, evidence(text)))


def scan_markdown(lines: list[str], findings: list[Finding]) -> None:
    heading_texts: Counter[str] = Counter()
    url_counts: Counter[str] = Counter()
    list_run: list[tuple[int, str]] = []
    table_rows: list[tuple[int, str]] = []

    def flush_list() -> None:
        nonlocal list_run
        if len(list_run) == 3:
            labels = [bool(re.match(r"^\s*[-*+]\s+\*\*[^*]+\*\*\s*[:—-]", x[1])) for x in list_run]
            if all(labels):
                add(findings, "F11", "low", "list", list_run[0][0],
                    "Exactly three bold-label bullets; inspect for a generated card pattern",
                    " | ".join(x[1].strip() for x in list_run))
        list_run = []

    def flush_table() -> None:
        nonlocal table_rows
        if len(table_rows) >= 2:
            counts = [row.count("|") for _, row in table_rows]
            if len(set(counts)) > 1:
                add(findings, "F21", "high", "table", table_rows[0][0],
                    "Markdown table rows have inconsistent column counts",
                    " | ".join(row.strip() for _, row in table_rows[:3]))
            seen = Counter(re.sub(r"\s+", " ", row.strip().lower()) for _, row in table_rows)
            for normalized, count in seen.items():
                if count > 1 and not re.fullmatch(r"\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)+\|?", normalized):
                    add(findings, "F22", "medium", "table", table_rows[0][0],
                        "Duplicate table row", normalized)
                    break
        table_rows = []

    for line_no, line in enumerate(lines, start=1):
        stripped = line.strip()
        if is_table_line(line):
            table_rows.append((line_no, line))
        else:
            flush_table()

        if re.match(r"^\s*(?:[-*+] |\d+[.)] )", line):
            list_run.append((line_no, line))
        else:
            flush_list()

        heading = re.match(r"^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$", line)
        if heading:
            title = re.sub(r"[*_`]+", "", heading.group(1)).strip().lower()
            heading_texts[title] += 1
            if title in {"введение", "основная часть", "заключение", "вывод", "итоги"}:
                add(findings, "F01", "low", "heading", line_no,
                    "Generic heading; keep only if the genre requires it", line)

        for image, label, target in MD_LINK_RE.findall(line):
            url_counts[target] += 1
            if not target.strip() or target.strip().lower() in {"url", "link", "ссылка"}:
                add(findings, "F31", "critical", "link", line_no,
                    "Empty or placeholder link destination", line)
            if not image and label.strip().lower() in {"здесь", "тут", "ссылка", "подробнее", "click here"}:
                add(findings, "F32", "low", "link", line_no,
                    "Non-descriptive link label", line)
            if image and label.strip().lower() in {"", "image", "изображение", "картинка", "схема"}:
                add(findings, "F41", "medium", "image", line_no,
                    "Generic image alt text", line)
            if re.search(r"utm_source=(?:openai|chatgpt|copilot|claude)", target, re.I):
                add(findings, "F33", "medium", "link", line_no,
                    "Assistant-identifying tracking parameter", line)

        if stripped.startswith("```") and stripped.count("```") > 1:
            add(findings, "F51", "high", "code", line_no,
                "Multiple fence markers on one line; inspect Markdown", line)

    flush_list()
    flush_table()
    for title, count in heading_texts.items():
        if title and count > 1:
            add(findings, "F02", "medium", "heading", 1,
                f"Duplicate heading appears {count} times", title)
    for url, count in url_counts.items():
        if count >= 4:
            add(findings, "F34", "low", "link", 1,
                f"Same link destination appears {count} times", url)


def scan_prose(lines: list[str], mode: str) -> list[Finding]:
    findings: list[Finding] = []
    masked, fenced = mask_fences(lines)
    scan_markdown(masked, findings)

    prose_lines: list[tuple[int, str]] = []
    phrase_hits: Counter[str] = Counter()
    phrase_first_line: dict[str, int] = {}

    for line_no, raw in enumerate(masked, start=1):
        if line_no in fenced or is_table_line(raw):
            continue
        text = prose_only(raw)
        if not text.strip():
            continue
        prose_lines.append((line_no, text))

        for pattern, (code, category, message) in PHRASES.items():
            matches = list(re.finditer(pattern, text, re.I | re.S))
            if matches:
                phrase_hits[code] += len(matches)
                phrase_first_line.setdefault(code, line_no)
                if category in {"evidence", "voice"}:
                    add(findings, code, "medium", category, line_no, message, raw)

        placeholder = PLACEHOLDERS.search(raw)
        if placeholder:
            add(findings, "A01", "critical", "artifact", line_no,
                "Unresolved placeholder", raw)
        leak = LEAKS.search(raw)
        if leak:
            add(findings, "A02", "critical", "artifact", line_no,
                "Leaked generation or citation token", raw)
        mixed = MIXED_SCRIPT_RE.findall(text)
        for token in mixed:
            # Common technical hybrids are allowed when separated by punctuation;
            # this catches only one contiguous alphabetic token.
            add(findings, "A03", "high", "artifact", line_no,
                "Mixed Latin and Cyrillic letters inside one word", token)
        if re.search(r"\b(?:всегда|никогда|единственн\w*|все без исключения)\b", text, re.I):
            add(findings, "L11", "medium", "logic", line_no,
                "Absolute claim; verify scope and evidence", raw)
        if re.search(r"\b(?:поэтому|следовательно|это доказывает)\b", text, re.I):
            add(findings, "L12", "low", "logic", line_no,
                "Inspect causal or inferential step", raw)

    for pattern, (code, category, message) in PHRASES.items():
        count = phrase_hits[code]
        if count >= 2 and category not in {"evidence", "voice"}:
            severity = "medium" if count >= 3 else "low"
            add(findings, code, severity, category, phrase_first_line[code],
                f"{message}; occurs {count} times", pattern)

    full_prose = "\n".join(text for _, text in prose_lines)
    sentences = [s.strip() for s in SENTENCE_RE.split(full_prose) if len(WORD_RE.findall(s)) >= 3]
    lengths = [len(WORD_RE.findall(s)) for s in sentences]
    if len(lengths) >= 6:
        for start in range(len(lengths) - 5):
            window = lengths[start : start + 6]
            mean = sum(window) / len(window)
            if mean >= 6 and max(window) - min(window) <= max(3, int(mean * 0.22)):
                add(findings, "R01", "low", "rhythm", 1,
                    "Six consecutive sentences have unusually similar length",
                    ", ".join(map(str, window)))
                break

    starters: Counter[str] = Counter()
    for sentence in sentences:
        words = [w.lower() for w in WORD_RE.findall(sentence)]
        if len(words) >= 2:
            starters[" ".join(words[:2])] += 1
    for starter, count in starters.most_common(5):
        threshold = 4 if len(sentences) >= 20 else 3
        if count >= threshold:
            add(findings, "R02", "medium", "rhythm", 1,
                f"Repeated sentence opening appears {count} times", starter)

    question_count = full_prose.count("?")
    word_count = len(WORD_RE.findall(full_prose))
    question_limit = 5 if mode == "telegram" else 4
    if word_count and question_count >= question_limit and question_count / word_count * 1000 > 5:
        add(findings, "R03", "low", "rhetoric", 1,
            "High rhetorical-question density; verify each question earns its place",
            f"{question_count} questions / {word_count} words")

    em_dashes = full_prose.count("—")
    if word_count >= 100 and em_dashes / word_count * 1000 > 12:
        add(findings, "R04", "low", "punctuation", 1,
            "High em-dash density; inspect repetition, do not replace mechanically",
            f"{em_dashes} em dashes / {word_count} words")

    bold_labels = sum(
        1 for _, raw in enumerate(masked, start=1)
        if re.match(r"^\s*[-*+]\s+\*\*[^*]+\*\*\s*[:—-]", raw)
    )
    if bold_labels >= 5:
        add(findings, "F12", "medium", "list", 1,
            "Repeated bold-label list pattern", f"{bold_labels} items")

    return sorted(findings, key=lambda f: (f.line, f.code, f.evidence))


def render_text(findings: list[Finding]) -> str:
    if not findings:
        return "No review signals found. This is not proof of human authorship."
    rows = []
    for item in findings:
        rows.append(
            f"{item.severity.upper():8} {item.code:4} line {item.line:<4} "
            f"[{item.category}] {item.message}\n  {item.evidence}"
        )
    rows.append(f"\n{len(findings)} review signal(s). Inspect in context; do not optimize for zero.")
    return "\n".join(rows)


def self_test() -> None:
    sample = """# Введение

Важно отметить, что данный подход играет важную роль.
Важно отметить, что данный подход открывает новые возможности.

- **Первое**: быстро.
- **Второе**: гибко.
- **Третье**: эффективно.

[здесь](https://example.com)
`важно отметить` не считается.

```python
print("важно отметить")
```
"""
    findings = scan_prose(sample.splitlines(), "article")
    codes = {item.code for item in findings}
    assert "W01" in codes, codes
    assert "F11" in codes, codes
    assert "F32" in codes, codes
    assert all("print" not in item.evidence for item in findings)
    print("self-test: ok")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", type=Path)
    parser.add_argument("--mode", choices=("generic", "article", "telegram"), default="generic")
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return 0
    if args.path is None:
        parser.error("path is required unless --self-test is used")
    try:
        text = args.path.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    findings = scan_prose(text.splitlines(), args.mode)
    if args.as_json:
        print(json.dumps([asdict(item) for item in findings], ensure_ascii=False, indent=2))
    else:
        print(render_text(findings))
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
