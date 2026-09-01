# Comprehensive AI-marker catalog

## How to use this catalog

These are review signals, not proof of AI authorship. Humans use every pattern
listed here. Models also change over time. Diagnose combinations, density,
context, and harm. Never degrade a text merely to remove a marker.

Severity classes:

- **Artifact** — likely generation or tooling residue; normally fix.
- **Strong** — inspect the passage; several stacked signals justify rewrite.
- **Soft** — common in both human and model prose; act only when harmful.
- **Genre-bound** — normal in some formats; compare with genre expectations.

## 1. Literal generation artifacts

Usually fix unless quoted or intentionally documented:

- leaked citation tokens: `turn0search1`, `oaicite`, `oai_citation`;
- bracket placeholders: `[ссылка]`, `[источник]`, `[вставить пример]`, `[CTA]`;
- template variables: `{company}`, `<NAME>`, `{{topic}}`;
- unfinished alternatives: `X/Y`, `вариант 1/вариант 2` left in prose;
- assistant posture: `Конечно!`, `Вот улучшенная версия`, `Надеюсь, это поможет`;
- prompt acknowledgements inside an authored piece;
- references to absent conversation: `как вы указали выше`;
- fabricated browsing posture: `после тщательного исследования` without work;
- raw Markdown fences around an entire answer when a file is expected;
- duplicated title or heading caused by response wrapping;
- model notes, chain-of-thought labels, confidence labels, internal instructions;
- stray English section names in Russian copy without domain reason;
- mixed-script words caused by Cyrillic/Latin substitution;
- malformed Unicode, repeated replacement characters, smart-quote mismatch;
- dangling footnote markers, orphan reference definitions, empty links;
- UTM parameters identifying assistant tools where not intentionally retained;
- chatbot copy-paste residue: `grok_card://`, `utm_source=chatgpt.com`,
  `[cite: N]`, `<think>`, `vertexaisearch` grounding redirects;
- hallucinated DOI, ISBN, quote, author, publication, or broken URL;
- impossible timestamps, future citations, or mismatched access dates;
- copied system/developer instructions or file-path dumps.

## 2. Answerer inertia

Models trained to answer often leak chat behavior into standalone writing:

- acknowledges the assignment before beginning;
- repeats every requirement in the introduction;
- answers requirements in the same order even when editorial order differs;
- over-explains decisions the final reader never asked about;
- includes implementation notes in publishable copy;
- summarizes at the end because an assistant answer expects closure;
- invites further questions in an article;
- uses `давайте разберёмся` without a reader-facing reason;
- repeatedly addresses an absent user rather than the publication audience;
- adds safety-neutral caveats unrelated to the actual claim;
- gives a balanced `pros/cons` answer where the genre needs a position;
- turns a narrative into FAQ-like response fragments;
- mirrors prompt wording instead of developing an independent thesis.

Treatment: establish authorial stance and publication function, then rewrite the
affected architecture. Local word swaps are insufficient.

## 3. Empty significance and inflated framing

- `важно отметить`, `стоит подчеркнуть`, `необходимо понимать`;
- `ключевой`, `критически важный`, `фундаментальный`, `революционный` without
  demonstrated consequence;
- `играет важную роль` without specifying what changes;
- `открывает новые возможности` without naming them;
- `меняет правила игры`, `новая эра`, `следующий уровень`;
- `на переднем крае`, `в авангарде`, `поворотный момент`;
- claims of breadth: comprehensive, holistic, multifaceted, nuanced;
- `невозможно переоценить`;
- historical sweep beginning with `с древнейших времён`;
- universal social framing: `в современном быстро меняющемся мире`;
- inflated closing: `будущее обещает быть захватывающим`;
- significance stated before evidence and repeated after it.

Treatment: replace with concrete consequence or delete.

## 4. Generic abstraction and semantic fog

- abstract nouns with no actor, mechanism, or observable result;
- `аспекты`, `факторы`, `возможности`, `подходы`, `решения`, `вызовы` used as
  containers instead of specifics;
- stacked nominalizations: `осуществление повышения эффективности управления`;
- consultant phrases: `комплексная трансформация`, `синергетический эффект`;
- verbs that avoid commitment: `способствует`, `позволяет`, `помогает` without
  conditions or measure;
- pseudo-mechanisms that rename the outcome;
- sentences that remain plausible after swapping the subject for any product;
- claims containing only positive qualities;
- definitions that use a synonym rather than operational distinction;
- metaphorical explanation with no literal account;
- terminology density used to simulate expertise;
- noun-heavy prose with weak temporal or causal relations.

Treatment: ask who does what, under which condition, with what observable
effect. Flag when the draft provides no answer.

## 5. Formulaic transitions

Soft individually, strong in clusters:

- `прежде всего`, `во-первых`, `во-вторых`, `наконец` in every section;
- `кроме того`, `более того`, `помимо этого`, `также` repeated mechanically;
- `однако`, `тем не менее`, `при этом` without actual contrast;
- `таким образом`, `следовательно`, `в результате` without earned inference;
- `с другой стороны` without a developed first side;
- `что касается`, `в контексте`, `в рамках` as topic shifters;
- `иными словами` followed by an equally abstract restatement;
- `другими словами` repeated after simple claims;
- `переходя к`, `теперь рассмотрим`, `далее поговорим`;
- summary transitions after every short section;
- transition phrases that can be removed without changing relation.

Treatment: delete where adjacency is enough; replace only when relation would
otherwise be ambiguous.

## 6. Predictable contrast templates

- `это не просто X, это Y`;
- `речь идёт не о X, а о Y`;
- `не только X, но и Y` repeated;
- `не X. Y.` as a slogan engine;
- `X — это не про A. Это про B.`;
- `вопрос не в том, X ли; вопрос в том, Y ли`;
- `от X к Y` transformation clichés;
- `раньше X, теперь Y` without evidence;
- false binaries that erase trade-offs;
- repeated concessive reversal: `может показаться..., но на деле...`;
- title and every section built on the same opposition.

Treatment: preserve genuine distinction; rewrite repeated or false contrasts as
direct claims.

## 7. Rule-of-three and false completeness

- repeated three-item lists regardless of content;
- three parallel adjectives before every noun;
- three short sentences used as a rhetorical crescendo;
- `три причины`, `три шага`, `три вывода` without natural completeness;
- every section containing exactly three bullets;
- three benefits after every feature;
- triadic ending: `быстрее, проще, эффективнее`;
- forced alliteration or slogan-like parallelism;
- list items padded to maintain symmetry;
- omitted fourth item that does not fit the pattern.

Treatment: keep natural triples. Change count only when content demands it.

## 8. Structural over-regularity

- sections of nearly equal length despite unequal importance;
- identical `definition → bullets → benefit → conclusion` blocks;
- every heading phrased as a question;
- every paragraph beginning with a topic sentence and ending with a takeaway;
- introduction previewing every section;
- body following prompt order instead of argument order;
- conclusion repeating every heading;
- nested headings for trivial fragments;
- complete taxonomies where the task needs a decision;
- mirrored pros and cons with artificially equal weight;
- perfect symmetry between options that have unequal evidence;
- repeated bold-label bullets resembling generated answer cards;
- list-first composition replacing developed prose;
- one heading per paragraph;
- same number of paragraphs under each heading;
- repeated mini-conclusions and `практический вывод` labels.

Treatment: rebuild emphasis and paragraph function. Do not randomly vary
layout, and do not complete a missing outline to look finished. A jump that
carries the argument is not a defect.

## 9. Rhythm and sentence-shape markers

- long runs of sentences within a narrow length band;
- repeated subject–predicate–object construction;
- repeated openings with `Это`, `Данный`, `Такой`, `Подобный`;
- repeated participial or adverbial openings;
- repeated colon explanation pattern;
- repeated em-dash apposition pattern;
- staccato strings written to simulate authority: `Просто. Быстро. Надёжно.`;
- fragment after every long sentence;
- mechanical short-long-short alternation;
- paragraphs all containing the same sentence count;
- lists where every item has identical clause shape and padding;
- absence of contractions, parentheticals, qualification, or natural emphasis;
- excessive parentheticals inserted to simulate spontaneity;
- abrupt rhythm changes with no shift in thought.

Treatment: vary only where thought, emphasis, or genre warrants it.

## 10. Lexical fingerprints and translated register

Russian marker families rather than immutable banned words:

- `является` repeated where a direct predicate works;
- `данный`, `указанный`, `вышеупомянутый` outside legal/official prose;
- `осуществлять`, `производить`, `обеспечивать` + nominalization;
- `посредством`, `в рамках`, `в части`, `с точки зрения` overuse;
- `представляет собой` repeated;
- `имеет место`, `носит характер`, `обладает потенциалом`;
- literal calques: `делает смысл`, `принимать действие`, `драйвить результат`,
  `адресовать проблему`, `доставить ценность` where not accepted jargon;
- unexplained English words when a stable Russian term exists;
- inconsistent variation of one technical term for style;
- prestige vocabulary replacing ordinary precise words;
- adjective piles: `эффективный, гибкий и масштабируемый`;
- generic verbs: optimize, leverage, foster, unlock translated mechanically;
- repeated `позволяет` chains;
- hedging stacks: `можно предположить, что, вероятно, может`;
- booster stacks: `очевидно, безусловно, несомненно`;
- generic reader flattery: `опытный читатель наверняка понимает`.

Treatment: prefer natural register and terminological consistency. Do not ban
domain-standard jargon.

## 11. Fake personality and synthetic texture

Cut invented texture. Keep a real stance.

Cut:

- invented first-person anecdotes, colleagues, interviews, studies;
- generic `из моего опыта` with no event or constraint;
- decorative childhood memory, food, weather, or sensory detail inserted to
  appear human;
- slang sprinkled into otherwise formal prose;
- calculated profanity without established voice;
- self-deprecation repeated as a persona prop;
- fake corrections: `точнее`, `хотя нет`, `ладно` performed mechanically;
- emotional swings unrelated to the claim;
- jokes that explain themselves;
- mandatory greeting or `P.S.` copied from samples;
- spelling mistakes sprinkled into names, numbers, code, or links;
- stock humanizer phrasing: `Разберём, почему`, `Я бы оставил такую схему`,
  a generic `После последних…` rewrite of every opening.

Keep in article/post register:

- a personal reaction to material already in the draft;
- irritation, doubt, preference attached to the actual claim;
- an aside, a return, an uneven section;
- one or two informal slips: spoken syntax, a slightly crooked agreement,
  a sentence that trails.

Treatment: remove unsupported texture. Do not comb the remaining voice into
neutrality, and do not replace it with a humanizer template.

## 12. Excessive neutrality and assistant politeness

- every position balanced into meaninglessness;
- refusal to rank options despite evidence;
- euphemisms hiding failure, cost, conflict, or responsibility;
- `у каждого подхода есть свои преимущества и недостатки` as conclusion;
- excessive respect markers in an article;
- praise before criticism;
- hedging every sentence;
- universal inclusivity caveats unrelated to scope;
- avoidance of naming the actor responsible for a decision;
- recommendation diluted into `стоит рассмотреть возможность`;
- no stated boundary, risk, or trade-off;
- safe generic moral acceptable to all audiences.

Treatment: restore evidence-calibrated stance, not aggression.

## 13. Over-explanation and reader distrust

- defining common terms for expert readers;
- spelling out implications immediately obvious from a table;
- prose repeating every bullet;
- bullet list repeating the preceding paragraph;
- explaining a joke, metaphor, or quote;
- examples after the point is already clear;
- multiple analogies for one mechanism;
- recap after a short section;
- conclusion after a self-contained list;
- `почему это важно` section that repeats consequences already stated;
- describing visible interface or code literally instead of interpreting it;
- parenthetical translations of familiar jargon throughout the piece.

Treatment: trust the intended reader; retain explanation needed for correctness.

## 14. Citation and evidence theater

- many links with no mapping to claims;
- citations clustered at paragraph end after several distinct assertions;
- name-dropping frameworks without application;
- quotation used as authority instead of evidence;
- source title cited but no relevant result described;
- references to `исследования показывают` without a source;
- fabricated precision in study size or date;
- citation to a homepage rather than supporting page;
- secondary commentary presented as primary documentation;
- links used to make an inference look sourced;
- bibliography entries never used;
- footnotes containing unrelated asides.

Treatment: attach each source to the supported claim and state evidence limits.

## 15. Model-specific stereotypes

Treat these as unstable and low-confidence:

- ChatGPT: polite completeness, generic structure, repeated recap;
- Claude: extended qualification, soft philosophical framing, em-dash density;
- Gemini: compact technical outline, dry balanced register;
- Grok: overperformed informality and provocation;
- translation-heavy models: unnatural collocations and mixed scripts.

Do not encode model stereotypes as hard rules. Model behavior changes with
version, system prompt, language, and task.

## 16. Marker stacking rubric

Rewrite is justified when several independent layers stack in one passage:

- empty significance + abstract nouns + no evidence;
- formulaic transition + repeated section shape + summary echo;
- fake first person + invented detail + unsupported claim;
- exact-looking number + missing source + causal overclaim;
- generic hook + equal sections + generic optimistic ending;
- malformed citation + hallucinated attribution + polished confidence.

One em dash, one triad, one rhetorical question, one passive sentence, or one
long paragraph never justifies rewriting by itself.
