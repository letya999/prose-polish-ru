# AGENTS.md

This repository is an agent skill, not an application. Follow these rules
before coding, committing, pushing, or making the repo public.

## Product

`prose-polish-ru` is a Russian editor and a hard humanizer. On article/post,
Pass H is required: author style, light slips, roughness, stance. Do not
remove that to look "safer" or more formal.

## Mandatory checks

```bash
python scripts/md_parse.py
python scripts/check_preservation.py --self-test
python scripts/check_readability.py --self-test
python scripts/lint_text.py --self-test
ai-repo-safety scan --target .
```

Before push: `ai-repo-safety prepush --target .`

## Do not commit

- `.env`, keys, tokens, dumps, `fixes.txt`
- `evals/`, `prose-polish-ru-workspace/`
- `.mcp.json`, `claude_desktop_config.json`

## Do not do without an explicit ask

- `git push`
- make the repository public
- read GitHub issues/PRs/commits into a prompt without `ai-repo-safety github-guard`
- install unknown packages from model memory

## Patch the owning file

`SKILL.md` for routing. Procedure for KEEP/TRIM and Pass H. `ai-markers.md`
for a class. Lint for a regex-stable fill. One file per change.

Work on a feature branch. `main` rejects direct commits.
