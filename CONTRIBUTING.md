# Contributing

Thanks for helping. Issues and PRs in Russian or English are fine.
The most useful patches are: a new *class* of Russian neuroslop with a
false-slop boundary, a KEEP/TRIM miss, or a lint that is regex-stable.

## Setup

```bash
git clone https://github.com/letya999/prose-polish-ru.git
cd prose-polish-ru
git config core.hooksPath .githooks
python -m pip install --upgrade pip
```

Scripts use the standard library only. No extra packages for the linters.

## Checks before a PR

```bash
python scripts/md_parse.py
python scripts/check_preservation.py --self-test
python scripts/check_readability.py --self-test
python scripts/lint_text.py --self-test
```

Optional, needs a local model proxy:

```bash
python scripts/corpus_eval.py run --pack audit --limit 2
```

## Where to patch

| File | When |
|---|---|
| `SKILL.md` | routing, invocation, output contract |
| `references/editorial-procedure.md` | KEEP/TRIM, Pass H, fact check |
| `references/ai-markers.md` | a new *class* or False slop, not a banned word |
| `references/heuristics.md` | argument, rhythm, diction, voice |
| `references/formats-and-artifacts.md` | Markdown, tables, lists, links, code |
| `scripts/lint_text.py` | regex-stable fill |
| `assets/simple-language.md` | one thought, first sentence does the work |

One owning file per change. Do not dump KEEP examples into `SKILL.md` to
raise precision.

## Rules

- Pass H on article/post is the product: light slips, roughness, stance.
  Do not "fix" that away.
- Do not invent facts in before/after examples.
- Do not commit `evals/`, `prose-polish-ru-workspace/`, `.env`, or `fixes.txt`.
- Default branch is `dev`. Work on a feature branch, then merge to `dev`.
- `main` is protected: only pull requests from `dev`.
