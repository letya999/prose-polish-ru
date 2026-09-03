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
    r"\bдавайте (?:разберёмся|посмотрим|нырнём|погрузимся)\b": ("W08", "water", "Chatbot announcement"),
    r"\bподводя итог\b": ("W09", "water", "Formulaic closer"),
    r"\bв заключение можно сказать\b": ("W10", "water", "Formulaic closer"),
    r"\bадресовать проблем": ("K01", "calque", "Translated collocation"),
    r"\bдоставить ценность\b": ("K02", "calque", "Translated collocation"),
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
    r"\bв эпоху цифровизации\b": ("W11", "water", "Epoch framing"),
    r"\bлюбопытно, что\b": ("W12", "water", "Duty evaluation"),
    r"\bпримечательно, что\b": ("W13", "water", "Duty evaluation"),
    r"\bявляется неотъемлемой\b": ("S05", "significance", "Inalienable-part cliché"),
    r"\bкраеугольн(?:ый|ым) камн": ("S06", "significance", "Cornerstone metaphor"),
    r"\bглубокое погружение\b": ("K03", "calque", "Delve calque"),
    r"\bраскрыть потенциал\b": ("S07", "significance", "Unlock-potential calque"),
    r"\bвывести на новый уровень\b": ("S08", "significance", "Next-level calque"),
    r"\b(?:правда|реальность) (?:в том|такова)\b": ("M01", "metadiscourse", "Truth-is announcement"),
    r"\bбуду(?: с вами)? честен\b": ("M02", "metadiscourse", "Performative honesty"),
    r"\bподч[её]ркивая важность\b": ("S09", "significance", "Participle significance tail"),
    r"\bот новичков до\b": ("C04", "contrast", "Fake-coverage merism"),
    r"\bв высшей степени\b": ("L05", "diction", "GPT-Russian booster"),
    r"\bне секрет, что\b": ("W14", "water", "Secret-is-not throat-clearing"),
    r"\bодним из ключевых аспектов\b": ("S12", "significance", "Key-aspect framing"),
    r"\bсуществует множество (?:способов|подходов|вариантов)\b": (
        "A04", "abstraction", "Fake completeness",
    ),
    r"\bоднозначного ответа не существует\b": (
        "A05", "abstraction", "Fake nuance",
    ),
    r"\bнельзя не отметить\b": ("W15", "water", "Litotes emphasis"),
    r"\bзадумывались ли вы\b": ("W16", "water", "Rhetorical opener"),
    r"\bмало кто знает\b": ("M03", "metadiscourse", "Faux-insight drumroll"),
    r"\bнесмотря на (?:эти |существующие )?вызовы\b": (
        "S13", "significance", "Challenge-redemption coda",
    ),
    r"\bтем самым способствуя\b": ("S14", "significance", "Participle significance tail"),
    r"\bкак показывает практика\b": ("E03", "evidence", "Practice-without-practice"),
    r"\bв заключение хочется\b": ("W17", "water", "Formulaic closer"),
    r"\bначните уже сегодня\b": ("W18", "water", "CTA closer"),
    r"\bимеет богатую историю\b": ("S15", "significance", "Gazetteer history padding"),
    r"\bоказывает существенное влияние\b": (
        "S16", "significance", "AINL-style influence claim",
    ),
    r"\bперспективн(?:ый|ого|ым) (?:подход|метод|направление)\b": (
        "S17", "significance", "Prospect-without-result",
    ),
    r"\bсцена разворачивается\b": ("A06", "abstraction", "Vision-captionese"),
    r"\bэтот опыт сделает\b": ("M04", "metadiscourse", "Expand-task moral closer"),
    r"\bне оправдал(?:и|а|о)?(?: моих)? ожиданий\b": (
        "S19", "significance", "AI-review expectation template",
    ),
    r"\bв условиях нынешней экономики\b": (
        "S20", "significance", "Epoch tail on a local note",
    ),
    r"\bмогут быть использованы для\b": (
        "S21", "significance", "AINL utility tail without a parameter",
    ),
    r"\bвостребована во множестве\b": (
        "S22", "significance", "Textbook demand padding",
    ),
    r"\bне стал исключением\b": ("W19", "water", "News-exception opener"),
    r"\bпервое, что меня (?:удивило|поразило)\b": (
        "W20", "water", "Review atmosphere opener",
    ),
    r"\bв целом, посещение\b": ("W21", "water", "Review recap closer"),
    r"\bсчитает себя эксклюзив": (
        "S23", "significance", "Exclusive-claim without a price",
    ),
    r"\bвеликолепн(?:ый|ого|ым) сервис": (
        "S24", "significance", "Praise-brochure service with no episode",
    ),
    r"\bпревзош[её]л(?:и|а)? (?:все )?(?:мои|наши) ожидания\b": (
        "S25", "significance", "Praise expectation template",
    ),
    r"\bвсегда готов(?:ы|а|о)? помочь\b": (
        "S26", "significance", "Staff merism without an episode",
    ),
    r"\bкаждое блюдо было шедевром\b": (
        "S27", "significance", "Praise merism with no dish",
    ),
    r"\bхочется отметить\b": ("W22", "water", "Praise metadiscourse opener"),
    r"\bтранспортн(?:ой|ая) доступност": (
        "S28", "significance", "Hotel-brochure accessibility closer",
    ),
}

# High-precision fills: fire on the first hit. Common канцелярит still
# needs density (count >= 2) so a single `таким образом` is not a finding.
ONCE_CODES = {
    "S02", "S03", "S15", "S16", "S17", "S18", "S19", "S20", "S21", "S22",
    "S23", "S24", "S25", "S26", "S27", "S28",
    "M03", "M04",
    "A04", "A05", "A06",
    "C01",
    "W06", "W08", "W14", "W16", "W18", "W19", "W20", "W21", "W22",
}

PLACEHOLDERS = re.compile(
    r"(?:\[(?:ссылка|источник|вставить[^\]]*|cta|пример)\]|"
    r"\{\{[^}]+\}\}|<(?:NAME|URL|TODO|PLACEHOLDER)>)",
    re.IGNORECASE,
)
LEAKS = re.compile(
    r"(?:"
    r"\b(?:turn\d+(?:search|view|fetch|file|image|news|video|ref)\d+|oaicite|oai_citation|citeturn)\b|"
    r":contentReference\[oaicite:\d+\]|"
    r"grok_card://|grok_render_citation_card_json|"
    r"utm_source=(?:chatgpt|copilot|openai)\.com|"
    r"\[cite_start\]|\[cite:\s*\d+|"
    r"</?think>|"
    r"по состоянию на момент (?:моего|последнего)|"
    r"as of my last knowledge"
    r")",
    re.I,
)
URL_RE = re.compile(r"https?://[^\s)>\]]+")
MD_LINK_RE = re.compile(r"(!?)\[([^\]]*)\]\(([^)]+)\)")
INLINE_CODE_RE = re.compile(r"`[^`\n]+`")
SENTENCE_RE = re.compile(r"(?<=[.!?…])\s+(?=[А-ЯA-ZЁ])")
WORD_RE = re.compile(r"[A-Za-zА-Яа-яЁё0-9-]+")
GENERIC_HEADINGS = {
    "введение", "основная часть", "заключение", "вывод", "итоги",
    "практический вывод",
}
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


def content_tokens(text: str) -> set[str]:
    return {w.lower() for w in WORD_RE.findall(text) if len(w) >= 4}


def scan_markdown(lines: list[str], findings: list[Finding]) -> None:
    heading_texts: Counter[str] = Counter()
    headings_by_level: dict[int, list[tuple[str, int]]] = {}
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

        heading = re.match(r"^\s{0,3}(#{1,6})\s+(.+?)\s*#*\s*$", line)
        if heading:
            level = len(heading.group(1))
            title = re.sub(r"[*_`]+", "", heading.group(2)).strip().lower()
            heading_texts[title] += 1
            headings_by_level.setdefault(level, []).append((title, line_no))
            if title in GENERIC_HEADINGS:
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
    for level, items in headings_by_level.items():
        if len(items) >= 4:
            generic = sum(1 for title, _ in items if title in GENERIC_HEADINGS)
            if generic >= 2:
                add(findings, "S11", "medium", "structure", items[0][1],
                    "Brochure heading grid: several same-level generic sections",
                    ", ".join(title for title, _ in items))
                break
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

    prose_lines: list[tuple[int, str, bool]] = []
    phrase_hits: Counter[str] = Counter()
    phrase_first_line: dict[str, int] = {}

    for line_no, raw in enumerate(masked, start=1):
        if line_no in fenced or is_table_line(raw):
            continue
        text = prose_only(raw)
        if not text.strip():
            continue
        prose_lines.append((line_no, text, bool(re.match(r"^\s{0,3}#{1,6}\s+", raw))))

        for pattern, (code, category, message) in PHRASES.items():
            matches = list(re.finditer(pattern, text, re.I | re.S))
            if matches:
                phrase_hits[code] += len(matches)
                phrase_first_line.setdefault(code, line_no)
                if category in {"evidence", "voice"} or code in ONCE_CODES:
                    add(findings, code, "medium", category, line_no, message, raw)

        placeholder = PLACEHOLDERS.search(raw)
        if placeholder:
            add(findings, "A01", "critical", "artifact", line_no,
                "Unresolved placeholder", raw)
        leak = LEAKS.search(raw)
        if leak:
            add(findings, "A02", "critical", "artifact", line_no,
                "Leaked chatbot or citation artifact", raw)
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
        if re.search(r"(?:^|[\s.,;:!?])n[А-ЯЁ]", text):
            add(findings, "A07", "high", "artifact", line_no,
                "Glued join letter: Latin n before a capital Cyrillic word", raw)
        if re.search(
            r"обеспечить прозрачность|вернуть доверие населения|будет усилен контроль",
            text,
            re.I,
        ):
            add(findings, "S18", "medium", "significance", line_no,
                "News-governance ritual without a new fact", raw)

    for pattern, (code, category, message) in PHRASES.items():
        count = phrase_hits[code]
        if code in ONCE_CODES or category in {"evidence", "voice"}:
            continue
        if count >= 2:
            severity = "medium" if count >= 3 else "low"
            add(findings, code, severity, category, phrase_first_line[code],
                f"{message}; occurs {count} times", pattern)

    full_prose = "\n".join(text for _, text, is_heading in prose_lines if not is_heading)
    stutter = re.search(r"(.{12,80}?)\s+\1", full_prose)
    if stutter:
        add(findings, "A08", "high", "artifact", 1,
            "Immediate stutter: the same clause or numeral phrase twice",
            stutter.group(1))
    sentences = [s.strip() for s in SENTENCE_RE.split(full_prose) if len(WORD_RE.findall(s)) >= 3]
    for idx in range(len(sentences) - 1):
        left = content_tokens(sentences[idx])
        right = content_tokens(sentences[idx + 1])
        shared = left & right
        smaller = min(len(left), len(right))
        if len(left) >= 3 and len(right) >= 3 and smaller and len(shared) / smaller >= 0.5:
            add(findings, "S10", "medium", "structure", 1,
                "Adjacent sentences restate the same thesis; inspect for brochure echo",
                f"{sentences[idx][:80]} | {sentences[idx + 1][:80]}")
            break
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
    dash_heavy = (
        (mode == "article" and em_dashes >= 4)
        or (word_count >= 100 and em_dashes / max(word_count, 1) * 1000 > 12)
    )
    if dash_heavy:
        add(findings, "R04", "low", "punctuation", 1,
            "High em-dash density; in article/post inspect decorative apposition",
            f"{em_dashes} em dashes / {word_count} words")

    if len(lengths) >= 4:
        for start in range(len(lengths) - 3):
            window = lengths[start : start + 4]
            if all(n <= 8 for n in window):
                add(findings, "R05", "medium", "rhythm", 1,
                    "Four consecutive short sentences; join unless each is a real hit",
                    ", ".join(map(str, window)))
                break

    guillemets = min(full_prose.count("«"), full_prose.count("»"))
    if mode == "article" and guillemets >= 3:
        add(findings, "R07", "medium", "punctuation", 1,
            "Guillemet density is high for article/post; drop emphasis quotes",
            f"{guillemets} «» pairs")

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
`важно отметить` не считается. Сабагент == холодный старт, путь => разбор.
oaicite leftover.

```python
print("важно отметить")
```
"""
    findings = scan_prose(sample.splitlines(), "article")
    codes = {item.code for item in findings}
    assert "W01" in codes, codes
    assert "F11" in codes, codes
    assert "F32" in codes, codes
    assert "A02" in codes, codes
    assert "S10" in codes, codes
    assert all("print" not in item.evidence for item in findings)
    assert all("==" not in item.evidence and "=>" not in item.evidence for item in findings)
    brochure = """## Введение
Пайплайн падает из-за кэша. Пайплайн действительно падает именно из-за кэша npm.

## Основная часть
Кэш влияет на сборку.

## Практический вывод
Команда должна проверить кэш.

## Заключение
Кэш имеет значение.
"""
    brochure_codes = {item.code for item in scan_prose(brochure.splitlines(), "article")}
    assert "S10" in brochure_codes, brochure_codes
    assert "S11" in brochure_codes, brochure_codes
    assert "F01" in brochure_codes, brochure_codes
    surface = """Кэш — «тихая» проблема. Это «дорого». Это «важно». Пайплайн — «зелёный».
Кэш это тихая проблема. Это очень дорого выходит. Это снова падает ночью. Это уже всех достало.
"""
    surface_codes = {item.code for item in scan_prose(surface.splitlines(), "article")}
    assert "R05" in surface_codes, surface_codes
    assert "R07" in surface_codes, surface_codes
    cluster = """Не секрет, что существует множество подходов.
Не секрет, что эксперты считают иначе.
По состоянию на момент моего обучения данных мало.
"""
    cluster_codes = {item.code for item in scan_prose(cluster.splitlines(), "generic")}
    assert "W14" in cluster_codes, cluster_codes
    assert "A02" in cluster_codes, cluster_codes
    ds = """Село имеет богатую историю. Исследование оказывает существенное влияние.
Село имеет богатую историю и оказывает существенное влияние.
"""
    ds_codes = {item.code for item in scan_prose(ds.splitlines(), "generic")}
    assert "S15" in ds_codes, ds_codes
    assert "S16" in ds_codes, ds_codes
    news = (
        "Около 7 тыс. Около 7 тыс. покупателей ждут квартиры. "
        "nМинистр подчеркнул контроль. "
        "Власти намерены обеспечить прозрачность и вернуть доверие населения."
    )
    news_codes = {item.code for item in scan_prose(news.splitlines(), "generic")}
    assert "A07" in news_codes, news_codes
    assert "A08" in news_codes, news_codes
    assert "S18" in news_codes, news_codes
    once = (
        "Село имеет богатую историю. Блюда не оправдали ожиданий. "
        "Сайт nbc.com не стал исключением. Первое, что меня удивило, это атмосфера. "
        "В целом, посещение ресторана было пустым. Клиника считает себя эксклюзивной. "
        "Раздел востребована во множестве областях. Результаты могут быть использованы для оптимизации."
    )
    once_codes = {item.code for item in scan_prose(once.splitlines(), "generic")}
    assert "S15" in once_codes, once_codes
    assert "S19" in once_codes, once_codes
    assert "W19" in once_codes, once_codes
    assert "W20" in once_codes, once_codes
    assert "W21" in once_codes, once_codes
    assert "S23" in once_codes, once_codes
    assert "S22" in once_codes, once_codes
    assert "S21" in once_codes, once_codes
    praise = (
        "Хочется отметить заботу. Великолепный сервис и персонал всегда готов помочь. "
        "Каждое блюдо было шедевром. Уровень превзошёл все наши ожидания. "
        "Отель благодаря удобной транспортной доступности."
    )
    praise_codes = {item.code for item in scan_prose(praise.splitlines(), "generic")}
    assert "W22" in praise_codes, praise_codes
    assert "S24" in praise_codes, praise_codes
    assert "S26" in praise_codes, praise_codes
    assert "S27" in praise_codes, praise_codes
    assert "S25" in praise_codes, praise_codes
    assert "S28" in praise_codes, praise_codes
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
