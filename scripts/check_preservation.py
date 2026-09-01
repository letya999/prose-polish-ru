#!/usr/bin/env python3
"""Compare protected Markdown artifacts before and after prose polishing."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path


URL_RE = re.compile(r"https?://[^\s)>\]]+")
MD_LINK_RE = re.compile(r"(!?)\[([^\]]*)\]\(([^)]+)\)")
INLINE_CODE_RE = re.compile(r"(?<!`)`([^`\n]+)`(?!`)")
FENCE_RE = re.compile(r"^\s*(```|~~~)([^\n]*)\n(.*?)^\s*\1\s*$", re.M | re.S)
NUMBER_RE = re.compile(
    r"(?<![\w])(?:\d{1,3}(?:[ .\u00a0]\d{3})+|\d+)(?:[,.]\d+)?"
    r"(?:\s*[–—-]\s*(?:\d{1,3}(?:[ .\u00a0]\d{3})+|\d+)(?:[,.]\d+)?)?"
    r"\s*(?:%|‰|×|x|мс|с|сек|мин|ч|дн(?:я|ей)?|байт|КБ|МБ|ГБ|ТБ|k|K|M|B|"
    r"руб\.?|₽|\$|€|USD|EUR|токен(?:ов|а)?|символ(?:ов|а)?|раз(?:а)?)?"
)
HEADING_RE = re.compile(r"^\s{0,3}(#{1,6})\s+(.+?)\s*#*\s*$", re.M)
QUOTE_RE = re.compile(r"(?:«[^»]{2,}»|“[^”]{2,}”|\"[^\"\n]{2,}\")")


@dataclass(frozen=True)
class Difference:
    category: str
    severity: str
    kind: str
    value: str
    before_count: int
    after_count: int


def normalize_number(value: str) -> str:
    return re.sub(r"[ \u00a0]", "", value.strip()).lower()


def digest(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:16]


def extract(text: str, strict_headings: bool = False) -> dict[str, Counter[str]]:
    links = Counter(target.strip() for _, _, target in MD_LINK_RE.findall(text))
    images = Counter(target.strip() for image, _, target in MD_LINK_RE.findall(text) if image)
    fenced = Counter(
        f"{lang.strip()}:{digest(body)}" for _, lang, body in FENCE_RE.findall(text)
    )
    data: dict[str, Counter[str]] = {
        "urls": Counter(URL_RE.findall(text)),
        "link_destinations": links,
        "image_destinations": images,
        "inline_code": Counter(INLINE_CODE_RE.findall(text)),
        "fenced_code": fenced,
        "numbers": Counter(normalize_number(v) for v in NUMBER_RE.findall(text) if v.strip()),
        "quotations": Counter(QUOTE_RE.findall(text)),
    }
    if strict_headings:
        data["headings"] = Counter(f"{len(level)}:{title.strip()}" for level, title in HEADING_RE.findall(text))
    return data


def compare(before: str, after: str, strict_headings: bool = False) -> list[Difference]:
    left = extract(before, strict_headings)
    right = extract(after, strict_headings)
    differences: list[Difference] = []
    for category in left.keys() | right.keys():
        before_values = left.get(category, Counter())
        after_values = right.get(category, Counter())
        for value in before_values.keys() | after_values.keys():
            old = before_values[value]
            new = after_values[value]
            if old == new:
                continue
            kind = "removed_or_changed" if old > new else "added"
            severity = "critical" if category in {
                "urls", "link_destinations", "image_destinations", "inline_code",
                "fenced_code", "numbers"
            } else "high"
            differences.append(Difference(category, severity, kind, value, old, new))
    return sorted(differences, key=lambda d: (d.category, d.value, d.kind))


def render(differences: list[Difference]) -> str:
    if not differences:
        return "Protected artifacts preserved. Semantic equivalence still requires editorial review."
    lines = []
    for diff in differences:
        lines.append(
            f"{diff.severity.upper():8} [{diff.category}] {diff.kind}: "
            f"{diff.value!r} ({diff.before_count} -> {diff.after_count})"
        )
    lines.append(f"\n{len(differences)} protected-artifact difference(s).")
    return "\n".join(lines)


def self_test() -> None:
    before = """# Заголовок

Цена 3–10× и 2.6 раза. [Документация](https://example.com/a).
Запусти `tool --flag`.

```bash
tool --flag
```
"""
    same = before.replace("Цена", "Стоимость")
    assert not compare(before, same)
    changed = same.replace("3–10×", "3-10x").replace("https://example.com/a", "https://example.com/b")
    differences = compare(before, changed)
    categories = {item.category for item in differences}
    assert "numbers" in categories, categories
    assert "urls" in categories, categories
    assert "link_destinations" in categories, categories
    print("self-test: ok")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("before", nargs="?", type=Path)
    parser.add_argument("after", nargs="?", type=Path)
    parser.add_argument("--strict-headings", action="store_true")
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
    differences = compare(before, after, args.strict_headings)
    if args.as_json:
        print(json.dumps([asdict(item) for item in differences], ensure_ascii=False, indent=2))
    else:
        print(render(differences))
    return 1 if differences else 0


if __name__ == "__main__":
    raise SystemExit(main())
