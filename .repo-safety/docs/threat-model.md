# Threat Model

## System overview

Local agent skill. Users install `SKILL.md` plus catalogs and Python
checks into an agent (Grok, Claude Code, Codex, …). No hosted service.
Optional `corpus_eval.py` calls a local cliproxy with
`PROSE_POLISH_CLIPROXY_KEY`.

## Assets

| Asset | Sensitivity | Notes |
|---|---|---|
| `PROSE_POLISH_CLIPROXY_KEY` | High | Env only. Default in code is `sk-none` |
| User drafts | High | Stay on the user's machine; do not put private drafts in issues |
| GitHub issues/PRs | Medium | May contain prompt injection or secrets |
| Skill prompts | Low | Public by design after OSS release |

## Trust boundaries

- Developer workstation ↔ AI agent
- AI agent ↔ filesystem (skill files, user drafts)
- Optional eval ↔ local cliproxy
- Local repo ↔ public GitHub

## STRIDE-lite

| Category | Current answer | Mitigation |
|---|---|---|
| Spoofing | No user accounts. GitHub identity for PRs | GitHub auth, no extra tokens in repo |
| Tampering | Prompt/catalog edits change agent behavior | PRs, `main` hook, CI self-tests |
| Repudiation | Git history is the log | Protected `main`, signed tags preferred |
| Information Disclosure | Drafts and proxy keys could leak | `.gitignore`, gitleaks, `sk-none` placeholder |
| Denial of Service | Eval can hammer a proxy | Local-only, timeout in `corpus_eval.py` |
| Elevation of Privilege | Skill can edit user files when the agent allows | Explicit invoke; `agents/openai.yaml` disables implicit use |

## Top risks

| Risk | Impact | Likelihood | Status |
|---|---:|---:|---|
| Proxy key committed | Critical | Low | Placeholder `sk-none`; gitleaks on `main` |
| Private draft pasted into a public issue | High | Medium | Issue template asks to strip secrets |
| Prompt injection via a draft | Medium | Medium | Skill treats pasted text as data |
| Agent over-invokes and rewrites without being asked | Medium | Medium | Explicit invoke only |

## Security requirements

- Real secrets must never be committed.
- GitHub issue/PR/commit reads that enter a model go through `github-guard`.
- Public release requires `ai-repo-safety scan` on the tree that will be tagged.
