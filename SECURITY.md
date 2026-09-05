# Security Policy

## Surface

`prose-polish-ru` is a local agent skill: prompts (`SKILL.md`, `references/`),
offline Python checks (`scripts/`), and optional eval against a local model
proxy. There is no hosted API. The skill does not need a model key to install.
`corpus_eval.py` talks to a proxy only when you run it, and reads the key from
`PROSE_POLISH_CLIPROXY_KEY`.

## Supported versions

Security fixes land on the latest release of `main`. Older tags are not patched.

## Reporting a vulnerability

Do not open a public issue with secrets, exploit details, or private logs.

Use [GitHub private vulnerability reporting](https://github.com/letya999/prose-polish-ru/security/advisories/new).

We aim to acknowledge within 7 days. A confirmed issue gets a fix on `main`
and a note in `CHANGELOG.md`. Credit is optional.

## Secret handling

- Never commit `.env`, keys, tokens, or dumps.
- Use `.env.example` for placeholder names only.
- If a secret leaks: rotate it first, then clean history. Flow:
  [`.repo-safety/docs/incident-cleanup.md`](.repo-safety/docs/incident-cleanup.md).

## Residual findings

Optional `scripts/corpus_eval.py` downloads public Hugging Face datasets
without pinning a git revision (`B615`) and talks to a local model proxy
over HTTP. That script is not part of the installed skill. Self-tests
use `assert` (`B101`). Cisco Skill Scanner flags those HTTP calls as
undeclared network / exfil; they stay behind env vars and `sk-none`.

## AI agent safety

Agents must follow [`AGENTS.md`](AGENTS.md). Do not read `.env` into a prompt.
GitHub issue/PR/commit text that will enter model context should go through
`ai-repo-safety github-guard`.
