<p align="center">
  <a href="README.md">Русский</a> · <strong>English</strong>
</p>

# prose-polish-ru

Russian editorial skill and hard humanizer. Input — theses, a generated draft,
or finished author text. A number in a draft is not a fact until checked. On
articles and posts, Pass H is mandatory: author voice, light typos, roughness,
awkwardness, emotion, and decisiveness.

Contract: [`SKILL.md`](SKILL.md). Procedure:
[`references/editorial-procedure.md`](references/editorial-procedure.md).
Marker catalog: [`references/ai-markers.md`](references/ai-markers.md).

> This skill works on **Russian-language** text. The README is maintained in
> Russian; this page is a summary for English-speaking users.

## Quick start

```bash
npx skills add letya999/prose-polish-ru -g -y --skill prose-polish-ru --copy -a "*"
```

Invoke the skill by name in your agent and paste theses or a draft:

```text
$prose-polish-ru polish this post:

[text]
```

Called without a verb, the skill returns a `score` card and a menu — it does not
start editing. A plain "rewrite this" without the skill name does not trigger it.

From a local clone:

```bash
git clone https://github.com/letya999/prose-polish-ru.git
cd prose-polish-ru
npx skills add . -g -y --skill prose-polish-ru --copy -a "*"
python scripts/lint_text.py --self-test
```

## One pipeline, four steps

Accuracy before usefulness, usefulness before structure, structure before
voice. A confident sentence that outruns its evidence is a failure. The
P(neuroslop) estimate reads the stuffing, not "was this model-written".

## Routed by request, not by session counter

Depth (`light` · `standard` · `deep`) and output format (`clean` · table ·
`audit` · `score`) are separate axes. `clean` is a format without the marker
table — it does not disable fact-checking.

## License

[MIT](LICENSE)
