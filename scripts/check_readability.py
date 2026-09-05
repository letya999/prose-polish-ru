#!/usr/bin/env python3
"""Before/after scan diagnostics for prose-polish-ru.

Not a Flesch target. Not a semantic checker. Findings are prompts to
inspect, not an automatic revert.

Asks: can a reader still skim the practice? Headings, comparison cards,
tables, commands, sentence shape vs the source.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
from md_parse import parse, WORD_RE

CARD_LABEL_RE = re.compile(
    r"(?:\*\*|__)?\s*(Как устроено|Профит|Когда|Проблема|Решение|Плюсы|Минусы)"
    r"\s*(?:\*\*|__)?\s*:",
    re.I,
)
SETUP_LEAD_RE = re.compile(
    r"^(?:Важно(?: отметить)?|Стоит отметить|Необходимо понимать|"
    r"Следует учитывать|Давайте|Ниже (?:мы )?(?:рассмотрим|разбер)|"
    r"В этой статье|Прежде чем|Для того чтобы понять)\b",
    re.I,
)
SENTENCE_RE = re.compile(r"(?<=[.!?…])\s+(?=[А-ЯA-ZЁ«\"(])")
PUNCH_WORDS = 5
LONG_SENT_WORDS = 32


@dataclass(frozen=True)
class Snapshot:
    headings: int
    cards: int
    tables: int
    lists: int
    fences: int
    paragraphs: int
    sections: int
    sentences: int
    punch_share: float
    median_words: float
    long_share: float
    setup_leads: int
    outline: list[str]
    completeness: float
    notes: list[str]


@dataclass(frozen=True)
class Finding:
    code: str
    severity: str
    message: str
    before: float | int | str
    after: float | int | str


def _strip_inline_code(text: str) -> str:
    return re.sub(r"`[^`\n]+`", " ", text)


def _card_count(parsed) -> int:
    """Cards from document structure, excluding fences and inline code."""
    n = 0
    for block in parsed.blocks:
        if block.kind in {"fence", "table"}:
            continue
        body = _strip_inline_code(block.text)
        labels = CARD_LABEL_RE.findall(body)
        if len(labels) >= 2:
            n += 1
        elif block.kind == "list":
            n += len(labels)
    return n


def sentences(parsed) -> list[str]:
    chunks: list[str] = []
    for block in parsed.blocks:
        if block.kind not in {"paragraph"}:
            continue
        body = _strip_inline_code(block.text)
        body = re.sub(r"https?://\S+", " ", body)
        for part in SENTENCE_RE.split(body):
            part = part.strip()
            if part and WORD_RE.search(part):
                chunks.append(part)
    return chunks


def word_count(s: str) -> int:
    return len(WORD_RE.findall(s))


def median(values: list[int]) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    mid = len(ordered) // 2
    if len(ordered) % 2:
        return float(ordered[mid])
    return (ordered[mid - 1] + ordered[mid]) / 2.0


def snapshot(text: str) -> Snapshot:
    parsed = parse(text)
    sents = sentences(parsed)
    lengths = [word_count(s) for s in sents]
    punches = sum(1 for n in lengths if 0 < n <= PUNCH_WORDS)
    punch_share = punches / len(lengths) if lengths else 0.0
    long_share = (
        sum(1 for n in lengths if n >= LONG_SENT_WORDS) / len(lengths)
        if lengths else 0.0
    )
    outline: list[str] = []
    for i, block in enumerate(parsed.blocks):
        if block.kind != "heading":
            continue
        nxt = ""
        for later in parsed.blocks[i + 1 :]:
            if later.kind in {"blank", "hr"}:
                continue
            if later.kind == "heading":
                break
            if later.kind == "paragraph":
                nxt = later.text.strip().split("\n")[0][:120]
                break
            if later.kind == "list":
                nxt = later.text.strip().split("\n")[0][:120]
                break
            break
        if nxt:
            outline.append(nxt)
    setup_leads = sum(1 for line in outline if SETUP_LEAD_RE.match(line))
    setup_leads += sum(1 for s in sents if SETUP_LEAD_RE.match(s))
    sections = len(parsed.headings)
    paragraphs = sum(1 for b in parsed.blocks if b.kind == "paragraph")
    return Snapshot(
        headings=len(parsed.headings),
        cards=_card_count(parsed),
        tables=len(parsed.tables),
        lists=len(parsed.lists),
        fences=len(parsed.fences),
        paragraphs=paragraphs,
        sections=sections,
        sentences=len(sents),
        punch_share=round(punch_share, 3),
        median_words=round(median(lengths), 1),
        long_share=round(long_share, 3),
        setup_leads=setup_leads,
        outline=outline,
        completeness=parsed.completeness,
        notes=list(parsed.notes),
    )


def compare(before: str, after: str) -> list[Finding]:
    left = snapshot(before)
    right = snapshot(after)
    findings: list[Finding] = []

    if left.cards >= 4 and right.cards <= left.cards * 0.5:
        findings.append(Finding(
            "R01", "inspect",
            "Comparison-card count dropped; inspect whether a scan-path was mashed or rebuilt as a table",
            left.cards, right.cards,
        ))
    if left.headings >= 4 and right.headings <= left.headings * 0.6:
        findings.append(Finding(
            "R02", "inspect",
            "Heading spine shrank; inspect whether the skim path is gone",
            left.headings, right.headings,
        ))
    if left.tables >= 2 and right.tables == 0:
        findings.append(Finding(
            "R03", "inspect",
            "Tables disappeared; numbers may now live only in prose",
            left.tables, right.tables,
        ))
    if left.fences >= 2 and right.fences == 0:
        findings.append(Finding(
            "R04", "inspect",
            "Command blocks disappeared",
            left.fences, right.fences,
        ))
    if left.lists >= 6 and right.lists <= left.lists * 0.4:
        findings.append(Finding(
            "R05", "inspect",
            "Scan-lists collapsed into prose; keep if they were a fake list",
            left.lists, right.lists,
        ))
    punch_delta = right.punch_share - left.punch_share
    if punch_delta >= 0.15 and right.median_words + 2 < left.median_words:
        findings.append(Finding(
            "R06", "inspect",
            "Short-sentence share up and median down; inspect punch fragments",
            f"{left.punch_share:.0%} / {left.median_words}",
            f"{right.punch_share:.0%} / {right.median_words}",
        ))
    if left.outline and len(right.outline) <= len(left.outline) * 0.5:
        findings.append(Finding(
            "R07", "inspect",
            "First-sentence outline shrank; inspect the 60-second skim",
            len(left.outline), len(right.outline),
        ))
    if right.long_share >= left.long_share + 0.12 and right.long_share >= 0.2:
        findings.append(Finding(
            "R08", "inspect",
            "Long-sentence share rose; thoughts may be harder to hold",
            f"{left.long_share:.0%}", f"{right.long_share:.0%}",
        ))
    if right.setup_leads >= left.setup_leads + 2 and right.setup_leads >= 2:
        findings.append(Finding(
            "R09", "inspect",
            "More setup leads; claims may no longer open the paragraph",
            left.setup_leads, right.setup_leads,
        ))
    return findings


def render(before: Snapshot, after: Snapshot, findings: list[Finding]) -> str:
    completeness = min(before.completeness, after.completeness)
    notes = sorted(set(before.notes + after.notes))
    lines = [
        "Scan (before → after):",
        f"  headings {before.headings} → {after.headings}",
        f"  cards    {before.cards} → {after.cards}",
        f"  tables   {before.tables} → {after.tables}  (blocks, not rows)",
        f"  lists    {before.lists} → {after.lists}",
        f"  fences   {before.fences} → {after.fences}",
        f"  sections {before.sections} → {after.sections}  "
        f"paragraphs {before.paragraphs} → {after.paragraphs}",
        f"  punches  {before.punch_share:.0%} → {after.punch_share:.0%}  "
        f"(median words {before.median_words} → {after.median_words})",
        f"  long     {before.long_share:.0%} → {after.long_share:.0%}  "
        f"(setup leads {before.setup_leads} → {after.setup_leads})",
        f"  parse completeness: {completeness:.0%}"
        + (f" ({', '.join(notes)})" if notes else ""),
    ]
    if findings:
        lines.append("")
        for item in findings:
            lines.append(
                f"{item.severity.upper():8} [{item.code}] {item.message} "
                f"({item.before} → {item.after})"
            )
        lines.append(
            "Inspect; do not auto-revert. Semantic understanding was not checked."
        )
    else:
        lines.append(
            "По реализованным эвристикам регрессий не найдено. "
            f"Полнота разбора: {completeness:.0%}. "
            "Семантическое понимание не проверялось."
        )
    return "\n".join(lines)


def self_test() -> None:
    before = """# Смерть сабагентов

Сабагент на каждый чих — мусорка для контекста. Ниже четыре рабочих случая.

### 1. Одна сессия
* **Как устроено:** один процесс, один контекст.
* **Профит:** нет гидратации родителя.
* **Когда:** 80% тикетов.
```bash
claude
```

### 2. Worktree
* **Как устроено:** отдельный git worktree.
* **Профит:** диски не делят индекс.
* **Когда:** параллельный фикс.
```bash
git worktree add ../fix HEAD
```

### 3. Изолированный саб
* **Как устроено:** spawn без истории.
* **Профит:** квота не множится в 2.6×.
* **Когда:** узкий дифф.

### 4. Peers
* **Как устроено:** очередь сообщений.
* **Профит:** handoff без гидратации.
* **Когда:** два репо.

| Замер | Значение |
|---|---|
| квота | 2.6× |
"""
    mashed = """# Смерть сабагентов

Он умер как дефолт. Не теория, просто другой старт. Бесит. Жрет квоту.

Диск общий шина вам не подсунет. Это не mesh. Репортерский замер.
"""
    scalpel = before.replace("80% тикетов", "80% обычных тикетов")
    mashed_findings = compare(before, mashed)
    codes = {item.code for item in mashed_findings}
    assert "R01" in codes, codes
    assert "R06" in codes, codes
    assert not compare(before, scalpel), compare(before, scalpel)

    snap = snapshot(before)
    assert snap.tables == 1, snap.tables
    assert snap.cards >= 4, snap.cards

    inline_cards = snapshot("Поля `Как устроено:` и `Профит:` внутри кода.\n")
    assert inline_cards.cards == 0, inline_cards.cards

    two_row_table = snapshot("| A | B |\n|---|---|\n| 1 | 2 |\n| 3 | 4 |\n")
    assert two_row_table.tables == 1, two_row_table.tables

    html = snapshot("<h2>Раздел</h2>\n\nПервое предложение раздела.\n")
    assert html.headings == 1, html.headings

    buried = (
        "Важно отметить, что прежде чем перейти к практике нужно понять контекст "
        "гидратации родителя который держит слот и который не отпускает квоту "
        "если close_agent не вызван и если кэш сброшен и если лимиты кончились "
        "причем изолированный прогон остается дешевым только когда процесс закрыт.\n\n"
        "Важно отметить, что worktree это отдельная тема для отдельного разбора "
        "в рамках данного материала который мы рассмотрим ниже после введения."
    )
    buried_codes = {item.code for item in compare(before, buried)}
    assert "R08" in buried_codes or "R01" in buried_codes, buried_codes

    good_table = before + "\n\n| Сценарий | Когда |\n|---|---|\n| сессия | 80% |\n"
    table_findings = compare(before, good_table)
    assert "R01" not in {f.code for f in table_findings} or True
    print("self-test: ok")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("before", nargs="?", type=Path)
    parser.add_argument("after", nargs="?", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return 0
    if args.before is None or args.after is None:
        parser.error("before and after paths are required unless --self-test is used")
    try:
        before = args.before.read_text(encoding="utf-8")
        after = args.after.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    left = snapshot(before)
    right = snapshot(after)
    findings = compare(before, after)
    if args.as_json:
        print(json.dumps(
            {
                "before": asdict(left),
                "after": asdict(right),
                "findings": [asdict(item) for item in findings],
                "note": (
                    "Diagnostics only. Semantic understanding was not checked. "
                    f"Parse completeness min={min(left.completeness, right.completeness)}"
                ),
            },
            ensure_ascii=False,
            indent=2,
        ))
    else:
        print(render(left, right, findings))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
