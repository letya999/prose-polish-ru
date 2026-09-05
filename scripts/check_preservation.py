#!/usr/bin/env python3
"""Compare protected Markdown artifacts before and after prose polishing.

Successful result means: mechanical invariants held (or were authorized).
It does not mean hedges, causation, or claim strength survived.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
from md_parse import NumberHit, parse, self_test as md_self_test


@dataclass(frozen=True)
class Difference:
    category: str
    severity: str
    kind: str
    value: str
    before_count: int
    after_count: int


def number_key(hit: NumberHit) -> str:
    return f"{hit.sign}|{hit.value}|{hit.unit}|{hit.kind}"


def extract(text: str) -> dict[str, Counter[str]]:
    parsed = parse(text)
    urls = Counter()
    link_dests = Counter()
    image_dests = Counter()
    ref_ids = {}
    for hit in parsed.links:
        if hit.kind == "definition":
            ref_ids[hit.label] = hit.dest
            urls[hit.dest] += 1
            continue
        dest = hit.dest
        if hit.kind == "reference":
            dest = ref_ids.get(hit.dest.lower(), f"ref:{hit.dest.lower()}")
        link_dests[dest] += 1
        urls[dest] += 1
        if hit.image:
            image_dests[dest] += 1
    fenced = Counter(
        f"{b.meta.get('lang', '')}:{len(b.text)}:{b.text[:40]}"
        for b in parsed.fences
    )
    return {
        "urls": urls,
        "link_destinations": link_dests,
        "image_destinations": image_dests,
        "inline_code": Counter(code for _, _, code in parsed.inline_code),
        "fenced_code": fenced,
        "numbers": Counter(number_key(n) for n in parsed.numbers),
        "number_order": Counter(
            f"{i}:{number_key(n)}" for i, n in enumerate(parsed.numbers)
        ),
        "headings": Counter(
            f"{b.meta.get('level', 0)}:{b.text.strip()}" for b in parsed.headings
        ),
    }


def load_allow(path: Path | None) -> list[dict]:
    if path is None:
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("allow-json must be a list of {category,value,reason}")
    return data


_URL_CATS = {"urls", "link_destinations", "image_destinations"}


def allowed(diff: Difference, allow: list[dict]) -> bool:
    for item in allow:
        cat = item.get("category") or item.get("cat")
        value = item.get("value") or item.get("after") or item.get("before")
        if cat and cat != diff.category:
            if not (cat in _URL_CATS and diff.category in _URL_CATS):
                continue
        if value and str(value) not in diff.value:
            continue
        if cat or value:
            return True
    return False


def compare(
    before: str,
    after: str,
    strict_headings: bool = False,
    allow: list[dict] | None = None,
) -> list[Difference]:
    left = extract(before)
    right = extract(after)
    allow = allow or []
    if not strict_headings:
        left.pop("headings", None)
        right.pop("headings", None)
    differences: list[Difference] = []
    # If the bag of numbers matches but the order changed, values were swapped
    # across objects. Synonym edits around the same sequence must not fire.
    if left.get("numbers") == right.get("numbers") and left.get("number_order") != right.get(
        "number_order"
    ):
        differences.append(
            Difference(
                "numbers",
                "critical",
                "removed_or_changed",
                "order/binding changed",
                1,
                0,
            )
        )
    left.pop("number_order", None)
    right.pop("number_order", None)
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
                "urls", "link_destinations", "image_destinations",
                "inline_code", "fenced_code", "numbers",
            } else "high"
            item = Difference(category, severity, kind, value, old, new)
            if allowed(item, allow):
                continue
            differences.append(item)
    return sorted(differences, key=lambda d: (d.category, d.value, d.kind))


def render(differences: list[Difference]) -> str:
    if not differences:
        return (
            "Protected artifacts preserved. This is a mechanical check only: "
            "hedges, causation, and claim strength were not verified."
        )
    lines = []
    for diff in differences:
        lines.append(
            f"{diff.severity.upper():8} [{diff.category}] {diff.kind}: "
            f"{diff.value!r} ({diff.before_count} -> {diff.after_count})"
        )
    lines.append(f"\n{len(differences)} protected-artifact difference(s).")
    return "\n".join(lines)


def self_test() -> None:
    md_self_test()
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
    assert "urls" in categories or "link_destinations" in categories, categories

    hedge = "Процессы иногда зависают."
    hedge_cut = "Процессы зависают."
    assert not compare(hedge, hedge_cut), "hedge-only change is semantic, not this script"

    remaining = "Завершил оставшуюся работу за 18 минут."
    remaining_cut = "Завершил работу за 18 минут."
    assert not compare(remaining, remaining_cut)

    swap_before = "У A было 4, у B — 15."
    swap_after = "У A было 15, у B — 4."
    swap_diffs = compare(swap_before, swap_after)
    assert any(d.category == "numbers" for d in swap_diffs), swap_diffs

    ref_before = "[док][id]\n\n[id]: https://example.com/old\n"
    ref_after = "[док][id]\n\n[id]: https://example.com/new\n"
    ref_diffs = compare(ref_before, ref_after)
    assert any("old" in d.value or "new" in d.value for d in ref_diffs), ref_diffs

    nested_before = "[x](https://ex.com/a(b)/end)\n"
    nested_after = "[x](https://ex.com/a(b)/other)\n"
    nested_diffs = compare(nested_before, nested_after)
    assert nested_diffs, nested_diffs

    signed_before = "падение -5% и рост 5%."
    signed_after = "падение 5% и рост -5%."
    signed_diffs = compare(signed_before, signed_after)
    assert any(d.category == "numbers" for d in signed_diffs), signed_diffs

    version_before = "релиз 2.1.198 вышел."
    version_after = "релиз 2.1.198 вышел без шума."
    assert not compare(version_before, version_after)

    allow = [{"category": "link_destinations", "value": "https://example.com/b"}]
    allowed_diffs = compare(before, changed, allow=allow)
    assert not any("example.com/b" in d.value for d in allowed_diffs)
    print("self-test: ok")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("before", nargs="?", type=Path)
    parser.add_argument("after", nargs="?", type=Path)
    parser.add_argument("--strict-headings", action="store_true")
    parser.add_argument("--allow-json", type=Path, help="authorized fact-check replacements")
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
        allow = load_allow(args.allow_json)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    differences = compare(before, after, args.strict_headings, allow)
    if args.as_json:
        print(json.dumps([asdict(item) for item in differences], ensure_ascii=False, indent=2))
    else:
        print(render(differences))
    return 1 if differences else 0


if __name__ == "__main__":
    raise SystemExit(main())
