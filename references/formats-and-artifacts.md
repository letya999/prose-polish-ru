# Formats and artifacts

AI slop is not limited to sentences. Models often damage information design:
they invent rows, duplicate prose in tables, turn everything into bullets,
fabricate links, over-format headings, and alter code while polishing. Review
each artifact by its function.

## 1. Headings

Check:

- hierarchy increments logically (`#` → `##` → `###`);
- no level is used merely for visual size;
- heading describes the section's actual job;
- neighboring headings use compatible grammar when they are peers;
- compatibility does not become forced identical phrasing;
- one short paragraph is not buried under an unnecessary heading;
- headings do not repeat title, introduction, or each other;
- heading is not generic: `Введение`, `Основная часть`, `Заключение` unless the
  genre expects it;
- question headings ask real questions;
- title does not overpromise comprehensiveness, novelty, or certainty;
- heading anchors and internal links remain valid after renaming;
- explicit user headings remain unchanged under strict structure.

Common AI artifacts:

- emoji before every heading;
- title case copied from English into Russian;
- every heading built as `Как X меняет Y`;
- colon subtitles everywhere;
- one heading per paragraph;
- equal numbers of subsections in every section;
- headings that summarize the paragraph instead of aiding navigation;
- generic provocative hooks unsupported by the body.

## 2. Lists

Use a list when readers need scanning, comparison, sequence, inventory, options,
or independent conditions. Use prose when items form one developing argument.

Check:

- all items answer the same implied question;
- order is meaningful or explicitly arbitrary;
- numbered lists represent sequence, rank, or later reference;
- bullets represent unordered peers;
- grammatical parallelism aids comprehension;
- parallelism has not padded weak items to match strong ones;
- item count reflects content, not rule-of-three preference;
- each item adds a distinct fact or action;
- lead-in agrees grammatically with each item;
- punctuation and capitalization are consistent with item length;
- nested lists are necessary and no deeper than comprehension allows;
- prose before/after does not repeat every item;
- one-item lists are converted to prose unless format requires them;
- list labels are informative, not bold decoration;
- checklist boxes represent actionable verification;
- items are not fake categories with overlapping boundaries.

Common AI artifacts:

- converting every paragraph into bullets;
- exactly three bullets in every section;
- bold label + colon + generic explanation repeated mechanically;
- benefits list after every feature;
- steps that are not ordered actions;
- `Преимущества`, `Недостатки`, `Выводы` lists saying the same thing;
- final bullet that merely summarizes prior bullets;
- padding items with examples of unequal scope;
- duplicated verbs and sentence endings;
- invented completeness: `Вот полный список`.

Do not remove useful list parallelism merely to create irregularity. Do not
add a missing item or complete a tidy outline just to look finished.

## 3. Tables

Use a table for repeated fields or exact comparison across shared dimensions.
Do not use it for paragraphs that happen to have labels.

Check structure:

- columns express stable dimensions;
- rows represent comparable entities;
- every cell belongs to its row and column intersection;
- headers are specific and non-overlapping;
- units appear in headers or every relevant cell consistently;
- empty, unknown, not applicable, and zero are distinguished;
- sorting has a reason;
- row/column count remains readable on target platform;
- Markdown pipes are escaped inside cell content;
- multiline content does not break table syntax;
- alignment markers are valid;
- links and inline code remain valid in cells;
- table has prose interpretation only for non-obvious patterns.

Check content:

- values match source material;
- no invented cells complete a pattern;
- qualitative labels use consistent criteria;
- comparisons share baseline, time period, and conditions;
- ranges, multipliers, decimal separators, currencies, and units are preserved;
- percentages include denominator context where needed;
- `Да/Нет`, `Высокий/Средний/Низкий` are defined when judgment matters;
- table does not claim precision unavailable in sources;
- prose does not restate every cell;
- caveats are attached to relevant rows or introduced before interpretation.

Common AI artifacts:

- fabricated feature matrices;
- all options receiving balanced pros and cons;
- generic `Описание / Преимущества / Недостатки` columns;
- subjective scores without rubric;
- invented dates, prices, availability, or versions;
- redundant summary column;
- cells filled with `эффективный`, `гибкий`, `масштабируемый`;
- converting symbols such as `3–10×` into `3-10x`;
- deleting `+`, `/`, parentheses, or code identifiers to satisfy a prose lint;
- equal-length cell prose that obscures actual differences.

Never polish cell values as ordinary prose without checking their semantic role.

## 4. Links

Check:

- destination is preserved exactly unless link repair was requested;
- link label describes the destination or evidentiary role;
- label does not overstate what the destination proves;
- no bare `click here` / `здесь` when meaningful text fits;
- repeated destination is not linked in every mention without reason;
- link is placed at the supporting claim;
- closing punctuation is outside the URL when appropriate;
- parentheses in URLs are balanced;
- relative paths resolve from the document location;
- anchors still exist after heading edits;
- reference-style link definitions are present and unique;
- tracking parameters are preserved or removed only intentionally;
- local file links and web links use the target platform's expected syntax;
- HTTPS is not invented for a source known only as HTTP;
- access restrictions or login requirements are not concealed.

Common AI artifacts:

- hallucinated URLs;
- links to search results instead of primary pages;
- homepage links used as citations;
- a link attached to several unsupported claims;
- fabricated anchor text such as an exact report title;
- assistant/tool tracking parameters;
- empty destinations: `[]()`;
- placeholder links;
- link-label mismatch;
- converting a valid raw URL needed by a platform into unsupported Markdown.

## 5. Citations and quotations

Check:

- quotation text remains verbatim;
- omissions and brackets are explicit;
- author and source are correct;
- quotation marks match nesting conventions;
- source supports the nearby claim;
- direct quotation is not silently converted into paraphrase or vice versa;
- citation key and bibliography entry correspond;
- footnote numbering remains valid;
- a paragraph with multiple claims has citations placed precisely;
- secondary sources are not presented as original research;
- cited publication date and event date are not confused;
- source limitations survive compression;
- quotes are not rewritten to match surrounding voice.

Common AI artifacts:

- invented quote wording;
- plausible but nonexistent paper titles;
- fake DOI/ISBN;
- author-year mismatch;
- citation tokens leaked from tools;
- quote used as decoration;
- `исследования показывают` without citation;
- long bibliography unrelated to body;
- citations added to facts they do not support.

## 6. Images and captions

Check:

- image path or URL remains unchanged;
- alt text describes the image's information, not `image` or marketing copy;
- alt text does not rewrite technical notation to appease lint;
- caption adds interpretation, provenance, or caveat rather than repeating alt;
- figure numbering remains consistent;
- body references the correct figure;
- claims derived from a chart state what is actually visible;
- axes, units, legends, scale, and date range are considered;
- decorative images are not treated as evidence;
- generated image descriptions do not invent unseen details;
- localized assets remain localized;
- copyright/source credit is preserved.

Common AI artifacts:

- generic `Схема процесса` alt text;
- overlong captions that restate the section;
- invented interpretation of an uninspected image;
- renaming image files or paths during prose cleanup;
- changing `spawn vs peering` to unnatural wording solely to remove `vs`;
- treating image filename as proof of content.

## 7. Code, commands, and technical identifiers

Treat as protected by default.

Check:

- fenced code content is byte-preserved unless code editing was requested;
- language tag remains correct;
- inline code remains inline code;
- CLI flags retain hyphens, case, quotes, and spacing;
- paths retain separators and case where relevant;
- function, class, API, model, config, and environment names remain exact;
- placeholder syntax remains valid;
- commands are not combined, reordered, or made destructive;
- comments inside code are not polished unless requested;
- output examples are not confused with executable commands;
- code line wrapping does not change semantics;
- Markdown fencing remains balanced.

Common AI artifacts:

- typographic quotes inside executable commands;
- em dashes replacing double hyphens;
- translated identifiers;
- corrected spelling inside code;
- invented flags;
- removed escapes;
- command prompts copied into the command;
- prose lint firing on code tokens;
- changing version numbers or package names to plausible alternatives.

## 8. Markdown emphasis

Check:

- bold marks a small number of genuinely scannable concepts;
- italics distinguish emphasis, terminology, titles, or captions consistently;
- underline/HTML is supported by target platform;
- emphasis markers are balanced;
- punctuation around emphasis renders correctly;
- adjacent bold fragments do not turn the page into a generated slide deck;
- labels do not replace proper prose or headings;
- emphasis is not repeated on every key noun;
- ALL CAPS is purposeful;
- blockquotes contain quoted or intentionally offset material.

Common AI artifacts:

- bold lead-in on every bullet;
- bolding the answer to every paragraph;
- emoji + bold + colon templates;
- decorative horizontal rule after every section;
- excessive callouts and pseudo-UI cards;
- `**Важно:**` repeated throughout;
- emphasis that survives after its emphasized claim was deleted.

## 9. Horizontal rules and spacing

Check:

- rules mark a meaningful large transition;
- blank lines follow target Markdown conventions;
- no repeated separators create slide-like segmentation;
- lists and headings render with required blank lines;
- trailing spaces are intentional only for hard line breaks;
- paragraphs are not split every sentence for fake airiness;
- Telegram line breaks remain readable on mobile;
- Habr Markdown/HTML combinations are supported.

Common AI artifacts:

- `---` between every short section;
- excessive one-line paragraphs;
- invisible non-breaking spaces;
- blank headings;
- extra code fences around output.

## 10. Equations, symbols, and notation

Check:

- mathematical operators remain exact;
- hyphen, minus, en dash, em dash, and range dash retain their roles;
- multiplication sign `×` is not rewritten as letter `x`;
- inequalities remain correct;
- decimal separators match locale and source;
- units retain spacing and capitalization;
- slash, plus, ampersand, arrows, and equality signs remain when meaningful;
- notation such as `==`, `=>`, `->`, `vs` is protected author operator when it
  marks identity, implication, or comparison in technical prose; do not rewrite
  it into a hyphen, `это`, or a literary dash;
- Unicode normalization does not alter identifiers;
- percentages and basis points are not confused.

AI-marker scanners frequently overreach here. Never trade correctness for a
clean lint report.

## 11. Platform calibration

### Expert article / Habr

- prioritize evidence, mechanism, limitations, and a visible personal stance;
- allow technical notation, author operators, tables, figures, and longer
  explanations;
- allow unequal sections, an aside, and a slightly crooked sentence;
- avoid Telegram-style line fragmentation and engagement bait;
- keep sources close to claims;
- inspect title strength without manufacturing controversy;
- conclusion should state implication or boundary, not generic future promise
  and not a stock `Я бы оставил такую схему`.

### Telegram expert post

- optimize for mobile scan without turning every sentence into a paragraph;
- keep one central thought and selective supporting detail;
- use lists only when they outperform compact prose;
- links may need visible URLs depending on publishing workflow;
- hashtags, greeting, question, emoji, and `P.S.` are optional conventions;
- do not force a hook or CTA when the message already lands.

### Tutorial

- preserve sequence, prerequisites, commands, expected results, and failure
  recovery;
- do not remove repetition that prevents operational mistakes;
- distinguish explanation from instruction;
- numbered steps must be executable in order.

### Opinion piece

- preserve stance and evidence boundaries;
- avoid balancing away the opinion;
- include material counterarguments, not ceremonial `с другой стороны`;
- distinguish provocation from unsupported certainty.

### Formal or policy text

- do not apply conversationality by default;
- preserve defined terms and deliberate repetition;
- passive voice and symmetry may be functional;
- use this skill cautiously and only under explicit invocation.

## 12. Artifact acceptance check

Before delivery ask:

1. Does each artifact do a job prose cannot do as well?
2. Is its content preserved and supported?
3. Does surrounding prose interpret rather than duplicate it?
4. Does it render on the target platform?
5. Did polishing alter data, destinations, notation, code, or attribution?
6. Did the lint tool inspect only prose and ignore protected content?
