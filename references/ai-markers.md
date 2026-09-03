# Comprehensive AI-marker catalog

## How to use this catalog

These are review signals, not proof of AI authorship. Humans use every pattern
listed here. Models also change over time. Diagnose combinations, density,
context, and harm. Never degrade a text merely to remove a marker. In `audit`,
name stacked signals нейрослоп (quality), then table the harm. The Category
column cites this catalog as `§N short-name` (section number below). Do not
write a free-text bucket instead of `§N`. Do not write an authorship verdict,
a probability table, or "how I detected this". Claim strength →
[Editorial procedure](editorial-procedure.md) Pass 4.

Cite `§N`: 1 artifacts · 2 inertia · 3 empty significance · 4 fog ·
5 transitions · 6 contrast · 7 rule-of-three · 8 over-regularity · 9 rhythm ·
10 lexical · 11 fake personality · 12 neutrality · 13 over-explanation ·
14 citation theater · 15 model stereotypes · 16 stacking · 17 agnostic corpus ·
18 EN style-words · 19 sentence DNA · 20 RU neuroslop · 21 promo ·
22 sincerity · 23 guessing the gap · 24 stacking expanded · 25 formatting ·
26 humanizer · 27 calque lexicon · 28 openers · 29 closers ·
30 weasel attribution · 31 faux-insight · 32 empty completeness ·
33 notability · 34 inanimate subject · 35 translationese · 36 cutoff disclaimer ·
37 engagement · 38 citation laundering · 39 dataset fills / false slop ·
40 pseudo-nuance · 41 reasoning scaffolding · 42 sterile archetypes ·
43 prestige inflation · 44 hyper-cohesion · 45 therapeutic tone ·
46 compulsive hedging · 47 purple tech · 48 genitive chains ·
49 paragraph echo · 50 particle deficit · 51 trivial definitions ·
52 call-and-response · 53 theme-rheme dislocation · 54 flat surprisal ·
55 agent deletion · 56 epistemic cowardice · 57 negative parallelism ·
58 connective inflation.

The lists mix three layers. Do not collapse them:

- **Language-agnostic:** composition, evidence theater, homogenization,
  cheerfulness, answerer inertia. These travel across languages.
- **English-measured:** Kobak PubMed style-verbs, Pew negative parallelism,
  2026 hedging shapes (`ensuring`, `plays a crucial role in shaping`).
  Frequencies are English. In Russian look for the calque, not the English
  token, unless the draft is English.
- **Russian practitioner:** канцелярит, `является`, missing `же`/`ведь`/`вот`,
  Latin quotes, possessive calques, `весьма`/`крайне`. Few of these have a
  published human-baseline frequency; treat density, not a single hit.

House format (channel hashtag, author greeting, author `P.S.`, operators)
is KEEP. An isolated dash, ё, or long sentence is Soft. Stacked канцелярит,
formulaic contrast, and a brochure-regular outline are Strong. One span with
several markers is one finding, not several rewrites.

Sections 1–16 are the working core. 17–27 add measured English, Russian
practitioner, and stacking. 28–38 add 2026 classes that those lists still
missed: openers/closers, weasel attribution, faux-insight, empty
completeness, notability padding, inanimate-subject analysis,
translationese, knowledge-cutoff disclaimers, engagement fingerprints,
and citation laundering. 39 is tuned on public corpora (LLMTrace RU,
AINL-Eval abstracts, Reddit cited ranking). 40–47 target frontier reasoning
and RL-aligned LLMs (pseudo-nuance, reasoning scaffolding leak, sterile
archetypes, prestige micro-jargon, hyper-cohesion, therapeutic tone,
compulsive hedging, purple tech). 48–52 target Russian-specific structural
and syntax distortions (genitive chains, paragraph echo, particle deficit,
trivial definitions, call-and-response). 53–58 target academic stylometric
and discourse anomalies (RuATD, AINL-Eval, arXiv:2606.04177 284-feature analysis):
theme-rheme dislocation, flat surprisal, agent deletion, epistemic cowardice,
negative parallelism, and discourse connective inflation. Corpora links →
[README](../README.md). Do not treat the extra sections as a second
banned-word dump. Do not train a detector on these sets.

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
- copied system/developer instructions or file-path dumps;
- knowledge-cutoff disclaimers: `по состоянию на момент моего обучения`,
  `as of my last knowledge update`, `на основе имеющейся информации`;
- leftover UI chrome: `:::writing{variant=...}`, `[span_N]`, footnote `↩`,
  `utm_source=openai`;
- vision-captionese dumped into prose: `Сцена разворачивается на…`,
  `The image depicts…`, `На снимке можно увидеть…` with a census of
  objects and no claim;
- generation-task residue left in the piece: `Я попробовала написать
  поэму, и вот что у меня получилось`;
- glued join letter from a swallowed newline: `nМинистр`, `nВласти`
  (Latin `n` + capital Cyrillic mid-prose);
- immediate stutter: the same clause or numeral phrase twice in a row
  (`Около 7 тыс. Около 7 тыс.`);
- orphan quote fence: a closing `"` / `»` with no opener, or a quote
  that starts mid-paragraph after a join.

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
- chat cheers: `Отличный вопрос!`, `Безусловно!`, `Конечно! Давайте`;
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
- historical sweep beginning with `с древнейших времён`,
  `на протяжении всей истории человечества`;
- universal social framing: `в современном быстро меняющемся мире`,
  `в эпоху цифровизации`, `на сегодняшний день`;
- inflated closing: `будущее обещает быть захватывающим`;
- significance stated before evidence and repeated after it;
- English puffery (Wikipedia AISIGNS / Pew): `stands as`, `serves as`,
  `is a testament`, `indelible mark`, `evolving landscape`, `key turning
  point`, `reflects broader`, `setting the stage`, `underscores its
  importance`;
- Russian twins: `служит напоминанием`, `является неотъемлемой частью`,
  `краеугольный камень`, `культурный код`, `в ДНК компании`;
- name-dropping a media list with no thesis: `писали РБК, Ведомости и
  Коммерсантъ`;
- hedge-then-puff: `хотя он малоизвестен, он символизирует…`;
- ecosystem/conservation padding on a mundane fact (AISIGNS biology
  pattern; same shape in product copy: `вклад в экосистему отрасли`).

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
- title and every section built on the same opposition;
- English `rather than` as a hedge instead of a comparison;
- merisms of fake coverage: `от новичков до профессионалов`,
  `будь то X или Y`, `независимо от того`;
- rejecting a fake alternative nobody offered: `казалось бы, достаточно
  просто…, однако`;
- negative listing: `Не инструмент. Не платформа. Движение.`;
  English `Not a tool. Not a platform. A movement.`;
- `it's less about X and more about Y` / `меньше про X, больше про Y`.

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
- adjacent sentences restating the same thesis in new wrappers;
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
- a thought chopped into a run of 4–8-word sentences;
- `«ёлочки»` around ordinary words for emphasis, or upgrading `"..."` to `«...»`;
- decorative em-dash apposition installed during polish (`кэш — это...` on
  every sentence);
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
- generic reader flattery: `опытный читатель наверняка понимает`;
- GPT-Russian boosters: `весьма`, `крайне`, `в высшей степени` stacked;
- delve-calques: `погрузиться в тему`, `глубокое погружение`,
  `раскрыть потенциал`, `вывести на новый уровень` with no scene;
- synonym carousel for one entity: `компания` → `организация` →
  `предприятие` with no shift in meaning;
- English-trained subject insertion: possessive `наш продукт`, `свою работу`
  where Russian drops the possessive;
- missing spoken particles `же`, `ведь`, `вот`, `уж` across a long
  article/post (Soft alone; Strong with канцелярит).

Treatment: prefer natural register and terminological consistency. Do not ban
domain-standard jargon. Do not sprinkle particles as a humanizer trick.

## 11. Fake personality and synthetic texture

Cut invented texture. Keep a real stance.

Cut:

- invented first-person anecdotes, colleagues, interviews, studies;
- generic `из моего опыта` with no event or constraint;
- decorative childhood memory, food, weather, or sensory detail inserted to
  appear human;
- `Короче` / `если честно` once per paragraph as a persona prop;
- costume slang as residue only when it is a mechanical dump that fights
  the rest of the page. Pass H may use colloquial / slang to unstiffen a
  brochure; KEEP a forum register that is the piece's voice throughout;
- calculated profanity without established voice;
- self-deprecation repeated as a persona prop;
- fake corrections: `точнее`, `хотя нет`, `ладно` performed mechanically;
- emotional swings unrelated to the claim;
- jokes that explain themselves;
- greeting or `P.S.` *installed* onto a draft that did not use them
  (KEEP the author's house greeting/`P.S.`);
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
- metadiscourse the source did not use: `следует отметить`, `в данной работе`,
  relationship-marker stacks added by an LLM-as-editor pass;
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
- footnotes containing unrelated asides;
- citation laundering: a real URL or brand that does not support *this*
  claim (homepage, neighboring doc, topic cluster);
- RAG false attribution: `X highlights` / `X underscored` attached to a
  named source that does not say it;
- book citation with a page range that does not contain the claim;
- DOI/ISBN with a bad checksum, or a paper whose title does not match
  the identifier;
- brand-new draft with 404 links that never existed (AISIGNS: not ordinary
  link rot);
- `исследования показывают` / `experts agree` / `widely regarded as`
  with no named study.

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

Rewrite is justified when several independent layers stack in one span:

- empty significance + abstract nouns + no evidence;
- formulaic transition + repeated section shape + summary echo;
- fake first person + invented detail + unsupported claim;
- exact-looking number + missing source + causal overclaim;
- generic hook + equal sections + generic optimistic ending;
- malformed citation + hallucinated attribution + polished confidence.

One em dash, one triad, one rhetorical question, one passive sentence, or one
long paragraph never justifies rewriting by itself.

## 17. Language-agnostic corpus signals

These are density properties of a *passage* or a *set of posts*, not of a
word. Strong only when stacked with empty content.

- complexity homogenization: every paragraph the same difficulty, same
  sentence-length band, same information weight (Sourati; DivEye
  burstiness);
- formulaicity high, hapax / idiosyncratic words low;
- artificial cheerfulness: positive sentiment with no corresponding fact
  (WIRED / Imperial 2026: AI-assisted web copy ~2× happier);
- sycophantic agreement and fake-happy closers;
- uniform fact spacing: every sentence carries one equally weighted
  statistic;
- missing numerals where the genre expects them (AINL-Eval: GigaChat
  abstracts far fewer digits than humans);
- GigaChat-as-editor residue: extra hedges and relationship markers,
  personal pronouns stripped into bureaucratic we;
- regression to the mean: specific odd facts replaced by generic prestige
  (`изобретатель сцепки` → `революционный титан индустрии`).

Treatment: restore unevenness that the thought already had. Do not inject
random difficulty or fake gloom.

## 18. English style-word excess (measured)

English-only frequencies. In a Russian draft, score the calque (§10), not
the English token, unless the span is English.

Kobak et al., PubMed 15M abstracts, post-ChatGPT style-verb spike (not
content nouns). Conservative: ≥10% of 2024 abstracts LLM-touched.

High-ratio style words (illustrative, not a ban list):

- verbs: `delves`, `underscores`, `showcasing`, `enhancing`, `fostering`,
  `harnessing`, `leveraging`, `facilitating`, `empowering`, `streamlining`;
- adjectives: `intricate`, `meticulous`, `pivotal`, `comprehensive`,
  `crucial`, `robust`, `seamless`, `vibrant`, `multifaceted`,
  `transformative`, `paramount`, `groundbreaking`;
- nouns/frames: `interplay`, `insights`, `tapestry`, `realm`, `beacon`,
  `testament`, `landscape` (as `evolving landscape`);
- adverbs: `notably`, `additionally`, `significantly`, `ever-evolving`.

Pew 2026 web crawl (post-ChatGPT pages): em dash ~2×, Oxford comma +63%,
AI vocabulary (`delve`, `interplay`, `testament`) >2×, negative
parallelism (`it's not just X, it's Y`) ~3×.

WriteHuman 2026 humanization pairs (structural, not dash): top word
`ensuring`; top phrase `rather than`; sentence shape `X plays a
crucial/critical/important role in shaping Y`.

Also over-represented (same study; not a ban list): `highlights`,
`supports`, `broader`, `essential`, `reflects`, `significantly`,
`effectively`; phrases `such as`, `role in`, `essential for`,
`ensuring that`, `shaped by`, `while maintaining`; trigrams
`is essential for`, `role in shaping`, `this paper introduces`,
`aligns well with`, `rather than relying`.

Treatment: delete or replace with a source fact. One `comprehensive` in
academic English is Soft. A cluster in a blog post is Strong. Do not strip
every em dash or Oxford comma.

## 19. English sentence DNA

- `-ing` tail analysis: `highlighting`, `underscoring`, `ensuring`,
  `reflecting`, `fostering`, `enhancing`, `contributing to` glued onto a
  finished clause (Reinhart present-participle 5.3× vs human);
- copula avoidance: `serves as`, `stands as`, `acts as` instead of `is`;
- `at its core`, `when it comes to`, `let's unpack`, `needless to say`,
  `in today's world`, `at the end of the day`;
- first-line molds (Bloomberry): `In today's landscape`, `In a world
  where`, `Have you ever wondered`, `Let's be honest`, `Here's the
  thing`, `In recent years`;
- academic scaffold: `This paper introduces`, `Understanding of how`;
- promotional travel-guide English: `nestled`, `in the heart of`,
  `boasts a`, `vibrant`, `rich tapestry`, `diverse array`;
- canned notability: `independent coverage`, `active social media
  presence`, `featured in [outlet list]`;
- creative-slop names and sensory filler (`Elara`, `shimmered`,
  `voice barely above a whisper`) — Strong in fiction/marketing, ignore
  in a technical post unless stacked.

Treatment: end the sentence on the fact. Do not add a participle of
significance.

## 20. Russian-specific neuroslop

Practitioner lists (Utov/Habr/vc.ru/antislop, SPbU ChatGPT portrait,
Gramota, ru-wiki). Not published as Kobak-style frequencies.

- канцелярит as the main RU tell: `-ание/-ение/-ация` stacks, noun:verb
  closer to 3:1 than 2:1;
- `является` / `представляет собой` / `выступает в качестве` where `это`
  or a verb works;
- adverbial-participle tails: `, подчёркивая важность`, `, тем самым
  способствуя`, `, что свидетельствует о`;
- Latin `"..."` or `"` upgraded to `«ёлочки»` in a draft that typed
  keyboard quotes — or the reverse in a book-typography source;
- perfect GOST punctuation in a messenger/Telegram register the author
  does not use;
- always-present grammatical subject (English calque) in a register that
  drops it;
- `в целях`, `в связи с тем, что`, `на данном этапе`, `в данном
  контексте`;
- `любопытно, что`, `примечательно, что`, `нельзя не отметить`;
- `хочешь честно?`, `и знаете что?`, `если откликается` as fake talk;
- aforism molds: `X — это язык Y`, `X — валюта Y`, `X становится
  ловушкой` that make the claim fuzzier.

Treatment: actor + verb, or delete. Do not install book ёлочки / тире /
particles as polish. Pass H strips ё in running prose. House Telegram
greeting and `P.S.` stay.

## 21. Promotional register and fake-happy tone

- `уникальный`, `беспрецедентный`, `инновационный`, `передовой` without
  a measure;
- `богатое наследие`, `неповторимая атмосфера`, `яркий пример`;
- `commitment to`, `align with`, `customer focus` translated into Russian
  press-release;
- every challenge immediately redeemed by an optimistic closer
  (`несмотря на вызовы, отрасль сохраняет потенциал`);
- Wikipedia-style ecosystem padding on a mundane fact;
- sycophantic praise of the reader, the product, or the cited brand;
- challenges-and-prospects coda: `Несмотря на вызовы… отрасль сохраняет
  потенциал`; `в долгосрочной перспективе продолжит устойчивое развитие`;
- travel-guide Russian: `расположенный в самом сердце`, `может
  похвастаться`, `богатое культурное наследие` on a product or town.

Treatment: keep one concrete plus if the source has it. Delete the mood.

## 22. Performative sincerity and meta-announcements

- `буду с вами честен`, `скажу как есть`, `просто вдумайтесь`,
  `и точка`, `конец истории`;
- `спойлер:`, `неожиданный поворот:`, `горькая правда в том, что`,
  `реальность такова`, `настоящая проблема в том, что`;
- `это важно, потому что` announcing importance instead of showing it;
- defending against an objection the piece never raised;
- `речь не о том, что…`, `я не утверждаю, что…` with no prior attack;
- heading restated in the first sentence under it.

Treatment: delete the frame; keep the next sentence if it has a fact.

## 23. Guessing the gap

- `сведений мало, что говорит о закрытости; вероятно, он окончил…`;
- `по всей видимости`, `судя по всему`, `предпочитает не афишировать`,
  `традиционно для отрасли` filling a missing source;
- reconstructing biography, motive, or architecture from absence;
- mind-reading a service: `наверное, они просто перегружены работой`
  with no evidence in the thread.

Treatment: state the gap and stop. Do not invent the missing year,
degree, or causal link. FLAG.

## 24. Marker stacking rubric (expanded)

Rewrite is also justified when:

- English style-word cluster + `-ing` significance tail + no numeral;
- RU канцелярит + `не просто` + `таким образом` + empty closer;
- cheerfulness + challenges-and-prospects coda + media name-drop;
- exact numeral + unnamed telemetry + neighboring URL;
- meta-announcement + performative honesty + no inconvenient fact;
- homogenization across a whole channel *fill*, while the house frame
  stays KEEP;
- world-state opener + weasel experts + challenges-and-prospects closer;
- inanimate subject (`исследование подчёркивает`) + significance tail
  + no actor;
- English sentence DNA leaking into Russian (`играет ключевую роль в
  формировании`, `в конце дня`) + missing particles + канцелярит.

## 25. Formatting and markup tells

Wikipedia AISIGNS and Telegram/Habr scans. Soft alone.

- bold on every other phrase, or bold-label bullets as answer cards;
- emoji as list markers in a register that did not use emoji;
- heading ladders H1–H4 on a 400-word note;
- `TL;DR` / `Ключевые выводы` after a short post;
- title-case English headings inside Russian copy;
- vertical-bar tables of pros/cons nobody asked for;
- every list item ending with a period and a benefit clause;
- leftover ChatGPT UI chrome: numbered `1.` `2.` `3.` of equal length
  after `Вот несколько вариантов`;
- horizontal rules (`---`) as section breaks in a short post;
- colon-for-dash swap installed as a "humanizer" (`кэш: это…` on every
  sentence). Reddit cited ranking: people now flag the colon swap too.

Treatment: keep markup that carries meaning. Strip decoration.

## 26. Humanizer residue

Pass H *is* the humanizer toolkit (ё→е, slips, sparse mixed-script, list
recast, colloquial). Residue is overdoing it. Strong when several appear.

- typos / mixed-script / ё-strip inside names, numbers, code, URLs
  (never; protected spans);
- `Короче` / `если честно` once per paragraph;
- chopped 4–8-word sentences installed as "voice";
- house `P.S.` or greeting deleted because a catalog called them ritual;
- stock templates `Разберём, почему`, `Я бы оставил такую схему`.

Treatment: use Pass H in running prose; cut residue; keep house format
and protected spans.

## 27. Russian calque lexicon (fill, not frame)

Each is Soft alone, Strong in a cluster with empty significance:

- `ландшафт рынка`, `распаковать тему`, `дипдайв`, `геймчейнджер`;
- `выйти из зоны комфорта`, `сделать шаг назад`, `двигаясь вперёд`;
- `удвоить усилия`, `быть на одной волне`, `бесшовный опыт`;
- `экосистемное решение`, `синкануться`, `иметь разговор`;
- `это не имеет смысла` as `doesn't make sense`;
- `в конце дня` as `at the end of the day`;
- `идти рука об руку`;
- `открыть для себя`, `вдохновлять на`, `наследие и традиции`
  in a product post.

Treatment: Russian verb + a fact. Do not swap one calque for another.

## 28. Opening formulas

Language-agnostic shape. Score the mold, not the first word.

English (Bloomberry / PromptIndex / WriteHuman):

- world-state: `In today's world`, `In a world where`, `In today's
  landscape`, `In recent years`;
- curiosity: `Have you ever wondered`, `What if I told you`;
- candor: `Let's be honest`, `Here's the thing`, `Let me be clear`,
  `I'll be honest`;
- academic: `This paper introduces`, `The present study aims`.

Russian twins:

- `В современном (динамично развивающемся) мире`;
- `В эпоху цифровизации / цифровых технологий`;
- `Не секрет, что`; `Задумывались ли вы…?`; `Знаете ли вы, что`;
- `Одним из ключевых аспектов является`;
- `В данной статье рассматривается`;
- `Давайте разберёмся / нырнём / погрузимся`;
- news-exception: `не стал исключением`, `начало года запомнилось серией`;
- review: `Первое, что меня удивило, это атмосфера`.

Treatment: delete the first sentence. The piece usually starts on the
second. House greeting is KEEP; this section is the *interior* opener.

## 29. Closing formulas

Endings fail more reliably than openings (PromptIndex; ru-wiki
«Заключение»).

- recap: `В заключение`, `Подводя итог`, `Вкратце`, `Ultimately`,
  `In conclusion`, `at the end of the day`;
- wish: `в заключение хочется сказать / отметить`;
- fake-profound kicker: a cute metaphor that commits to nothing
  (`в конце концов лучший промпт — тот, который не нужно писать`);
- CTA with no next action: `Начните уже сегодня!`;
- challenges-and-prospects: `Несмотря на существующие вызовы…`,
  `Перспективы на будущее`, `продолжает динамично развиваться`;
- assistant closer: `Надеюсь, это поможет`, `Если остались вопросы`;
- `Ключевые выводы` / `TL;DR` after a short post that already said it;
- review recap: `В целом, посещение X было абсолютно разочаровывающим`;
- weather/news advice: `не расстраиваться из-за смены погоды`,
  `просто быть готовыми к быстрому переходу`.

Treatment: end on the last concrete point. Do not install a kicker.
Do not delete an author `P.S.` that the draft already used.

## 30. Weasel attribution and consensus theater

Soft as a single hedge. Strong when it carries the claim.

- unnamed experts: `эксперты считают`, `учёные доказали`, `многие
  отмечают`, `experts agree`, `industry observers`;
- unnamed studies: `исследования показывают`, `studies show`,
  `according to research` with no paper;
- fake consensus: `широко признано`, `widely regarded as`,
  `it is well known that`, `не секрет`;
- practice without practice: `как показывает практика`,
  `как известно`;
- Osetrova & Sedova 2025 «модус предположения»: `возможно`,
  `вероятно`, `в большинстве случаев`, `может варьироваться`
  stacked until nothing is asserted;
- safety leftover: `не является гарантией`, `результаты могут
  отличаться` in a genre that is not a disclaimer.

Treatment: name the source or FLAG. Do not upgrade weasel into a
bare fact.

## 31. Faux-insight, drumroll, colon-reveal

The sentence promises a revelation and delivers a commonplace.

- `Вот чего никто не говорит`; `мало кто знает`; `то, что все
  упускают`; `Here's what most people get wrong`;
- `What nobody tells you`; `The part everyone misses`;
- colon-reveal as a beat: `Лучшая часть: оно учится.` / `The catch:
  nobody reads it.` Strong when every third paragraph uses it;
- rhetorical setups: `А что, если я скажу…?`; `Plot twist:`;
  `Think about it:`; self-answered `Это работает? Безусловно.`;
- heading restated under the heading (`## Скорость` → `Скорость
  важна.`);
- ellipsis-as-drama: `И тогда выяснилось… что никто не читал договор`
  in analytic prose.

Treatment: delete the drumroll; keep the next clause if it has a fact.

## 32. Empty completeness and fake nuance

The draft pretends to have covered the space.

Russian practitioner (SEOquick / vc.ru / antislop):

- `Существует множество способов`;
- `Каждый случай требует индивидуального подхода`;
- `Однозначного ответа не существует`;
- `Важно учитывать ряд факторов`;
- `Это особенно актуально в условиях…`;
- `у каждого подхода есть свои преимущества и недостатки`;
- `существуют различные точки зрения, и каждая имеет право на
  существование`;
- merisms already in §6 (`от новичков до…`, `будь то X или Y`).

English twins: `there is no one-size-fits-all`, `it depends on a
variety of factors`, `a holistic approach is needed`.

Treatment: name the actual constraint, or stop. Completeness without
a count is fog.

## 33. Notability padding and media theater

Wikipedia AISIGNS / ru-wiki «известность и освещение в СМИ». Strong
in bios, landing pages, and channel about-blocks.

- listing outlets instead of a thesis: `писали РБК, Ведомости и
  Коммерсантъ`; `featured in Vogue, Wired, and the Toronto Star`;
- classifying the sources: `независимое освещение`, `в региональных
  СМИ`, `trade publications`, `high-quality independent outlets`;
- echoing the brief: Wikipedia notability wording pasted into the
  article (`significant, substantial, secondary coverage`);
- `поддерживает активное присутствие в соцсетях` / `active social
  media presence`;
- `принимал участие в общественных дискуссиях` / `generated debate
  about authenticity` with no named debate;
- in-prose citation of a trivial fact (`The Telegraph mentioned X
  as the cheapest airline`).

Treatment: keep one mention that carries a checkable claim. Delete
the outlet list. Do not invent what the article said.

## 34. Inanimate subject and significance tails

AISIGNS / Reinhart / ru-wiki ВП:ПАИИ / humanizer-ru #55.

A person can emphasize. A fact, a festival, or a platform cannot.

- `Исследование подчёркивает важность`;
- `Платформа обеспечивает удобство`;
- `Фестиваль, подчёркивая важность культурного обмена`;
- `The update adds offline mode, showcasing the company's
  user-first philosophy`;
- English `-ing` tails already in §19: `highlighting`,
  `underscoring`, `ensuring`, `reflecting`, `fostering`;
- Russian деепричастие already in §20: `, подчёркивая важность`,
  `, тем самым способствуя`, `, что свидетельствует о`;
- copula avoidance already in §19: `serves as`, `stands as`,
  `acts as a catalyst`, `functions as a bridge` = `is`.

Treatment: restore the actor, or end on the fact. Do not replace
`подчёркивает` with `акцентирует`.

## 35. English-centric leak (translationese)

Utov 2026 / Tsinghua and Oxford multilingual-LLM notes: non-English
generation often assembles the thought in English first. This is a
practitioner reading, not a published Russian frequency table.

Signals in a Russian draft:

- English sentence DNA with Russian tokens: `играет ключевую роль в
  формировании`, `способствует повышению`, `направлен на обеспечение`;
- semantic near-miss: `основание науки` for `основы науки`,
  `уточните усилия` for `доработайте маркетинг`;
- modal hedge chain: `может стать`, `способен обеспечить`,
  `призван решить` in every sentence;
- missing Russian idioms where the genre would use one; prestige
  Latinate words instead;
- SVO only, no inversion, no spoken particles (`же`/`ведь`/`вот`)
  across a long article/post;
- Title Case English headings inside Russian copy;
- capital letter after a colon in running Russian (`Главное: Это
  работает`) against house register.

Treatment: rewrite the thought in Russian, then pick words. A calque
swap is not enough. Do not sprinkle idioms the author does not use.

## 36. Knowledge-cutoff and didactic disclaimers

ru-wiki «Отказ от ответственности» / AISIGNS.

- `По состоянию на момент моего обучения`;
- `На момент обновления базы данных`;
- `Хотя конкретные детали ограничены…`;
- `не широко доступны / задокументированы`;
- `Ниже представлен обзор на основе имеющейся информации`;
- `значения могут варьироваться`;
- `важно отличать X от не связанных организаций` (safety leftover);
- `по состоянию на [date] не было зафиксировано скандалов` as a
  paragraph of nothing.

Then filling the gap anyway → also §23.

Treatment: cut the disclaimer. If the fact is missing, FLAG and stop.

## 37. Engagement fingerprints (2025–2026)

Models imitating warmth after being told they sound dry. Utov 55;
Washington Post ChatGPT-message study; PromptIndex rhythm tells.

- pseudo-Socratic: `Зачем? Потому что. И для чего? Для этого.`;
- chopped nod-sentences: `Короткие. Точные. Отдельные. Рефлексивные.`;
- decorative emoji as list markers: ⚡ «ключевой вывод», 🎯 «цель»,
  💡 «инсайт» in a register that did not use emoji;
- coach register: `Ты не ошибаешься, что так чувствуешь`,
  `сам факт этого — тихое подтверждение`;
- empty adverbs as texture: `просто`, `на самом деле`, `буквально`,
  `честно говоря` once a paragraph (Soft if spoken rhythm; Strong
  as a sprinkle);
- emoji-heavy chat cadence in an article.

Treatment: join the nods; drop the emoji unless the house used them;
keep one spoken adverb if it carries stance. Do not install slang
to compensate.

## 38. Citation laundering and evidence shape

Extends §14. The harm is epistemic, not stylistic.

- real outlet + wrong claim (Agent Teams URL covering a different
  product);
- cluster of citations at paragraph end after several assertions;
- `согласно документации X` pointing at a homepage or a sibling
  page;
- invented precision: `92% компаний из Fortune 500` with no method;
- anecdote → trend: one case becomes `команды всё чаще`;
- process vs instance mix: a default, a timeout, or one thread
  stated as architecture;
- secondary commentary presented as primary;
- bibliography never used;
- DOI/ISBN theater already in §14.

Treatment: attach each source to *this* claim. FLAG unsourced
precision. Do not KEEP a sharp numeral as an "expensive fact".

## 39. Dataset-observed fills (tune, not detect)

Observed in public corpora. Use as review classes. Mixed human+AI
intervals (LLMTrace `ai_char_intervals`) are *authorship* spans, not
KEEP. Rewrite only the slop span. KEEP a useful fact even if the
interval is labeled AI.

**Gazetteer / travel padding** (LLMTrace RU, GigaChat wiki-continue):

- `небольшое село, расположенное в…`;
- `окружено живописными лесами`;
- `имеет богатую историю, которая начинается ещё со времён Киевской Руси`;
- `множество исторических памятников` with none named;
- cuisine merism: `свежие овощи и фрукты, мясо дичи и рыба`.

**Expand-task moral fable** (LLMTrace YandexGPT/GPT expand of a news line):

- invented dialogue around a sourced fact;
- closer `этот опыт сделает их сильнее` / `важный урок` /
  `важность соблюдения законов` / `выбирать правильный путь`.

**Review sandwich:** `сначала всё казалось отличным… но со временем
начали проявляться нюансы`.

**AI-review mold** (LLMTrace RU reviews; not lived-in). A fluent
complaint *or* praise arc with a venue name is still mold.

Disappointment:

- expectation template: `не оправдали (моих) ожиданий`;
- atmosphere census: `Первое, что меня удивило, это атмосфера` plus
  light/dark/уют with no named object;
- exclusive-claim: `считает себя эксклюзивным` with no price or dish;
- recap closer: `В целом, посещение X было абсолютно разочаровывающим`;
- title-as-verdict over a regular complaint (`Одно вылечили — второе
  подхватили`);
- epoch tail: `в условиях нынешней экономики` on an otherwise local note.

Praise brochure (the same class, inverted polarity):

- `великолепный сервис` / `положительные эмоции` with no episode;
- staff merism: `всегда готовы помочь`, `хочется отметить заботу и
  профессионализм`;
- `завтраки всегда разнообразные и вкусные` with no dish;
- `каждое блюдо было шедевром`;
- venue-as-classic: `настоящая классика Москвы` / city + `классика`;
- `превзошёл все наши ожидания` / `внимания к деталям`;
- `удобная транспортная доступность` as a hotel/cafe closer.

Treatment: one TRIM/REWRITE for the stacked arc. KEEP a named dish, bill,
room number, or staff person if it is specific. A thanks letter with a
named addressee (`семья Рюлиных`, `земной поклон`) is still False slop;
TRIM only the brochure wrapper around it. Do not KEEP the whole page
because a restaurant or hotel is named.

**Costume slang** (style-transfer / expand on a clinic or shop): stacked
`братва`, `каталка`, `вуаля`, `не кислят`, `барыга` on brochure facts.
KEEP a forum register that is the piece's voice throughout
(`зомбоящик`). TRIM the costume; KEEP the named clinic or price.

**AINL-Eval 2025 scientific-abstract mold** (Llama/GPT/GigaChat
abstracts; Genre-bound in a real paper). Strong when stacked and the
abstract has no numeral, method, or named result:

- `оказывает существенное влияние`;
- `имеет важное значение для понимания / обеспечения`;
- `представляет собой перспективный подход`;
- `Результаты показывают, что` with no number;
- `позволяет глубже понять механизмы`;
- `показана перспективность использования`.

AINL also: generated abstracts much shorter than human ones and poorer
in digits. Missing numerals in a methods genre is a signal; do not
invent them. Treatment: stacked empty abstract is TRIM. KEEP a clause
that names reagent, pH, sample, or adduct even inside `Вопросам…` /
`В рамках проделанной работы` / `Следовательно, получение новых
данных`. Empty `показана перспективность` remains this mold.

**Advice-column mold** (LLMTrace article / how-to-feel posts): pep-talk
that could sit on any topic.

- opener `Даже не пытайтесь… Это очень сложно!`;
- `сеть поддержки` / `доверенные лица` with no named person;
- `не стесняйтесь обращаться за помощью`;
- unnamed psychologist `предложит стратегии справления`;
- closer `извлечь полезный опыт`.

Treatment: delete the pep-talk. KEEP `позвони маме` / `встретьтесь в кафе`
if named. A synonym of `позитивная нота` is not a fix.

**Wiki-card / study-guide answer-card** (LLMTrace article create): numbered
bold labels that turn a post into a gazetteer card.

- `1. **История создания**` / `**Авторство**` / `**Отзывы критиков**`;
- empty cell restating the title (`Подписан именем Антон Чехов`);
- weasel critics `Отмечена глубина психологического анализа` with no name.

Treatment: one paragraph with dates and names. DELETE empty labels.
FLAG unnamed critics. Do not KEEP the grid because two cells have facts.

**Reddit cited ranking** (JCarterJohnson unslop-ai-text, 600-post
audit; English, but the *classes* travel): em dash density, `not X but
Y`, uniform rhythm, sycophancy, formulaic essay, list-first, empty
fluency. Keyword hits on `however`/`comprehensive` over-count; do not
ban those words.

**News fill_gaps** (LLMTrace mixed, GPT/o1/GigaChat inserts in RU
news): the model restates the lede, then pads with control/trust
ritual. KEEP who/what/when/how-much. DELETE `власти намерены обеспечить
прозрачность и ответственность, чтобы вернуть доверие населения` when
no new fact follows. DELETE a second copy of the same complaint-count
sentence. FLAG a quote that lost its opener after a join.

**False slop** (50-run + held-out): do not FLAG these as нейрослоп.

- lived-in review: irregularity **plus** a named object (`ни какое`,
  `суперрр`, `обалденные`, a dish/bill/sofa). A fluent disappointment
  *or* praise arc with only a venue name is AI-review mold above, not
  this bullet;
- agency wire: named outlet, complex, km, %; `сказал Фортов`; fire/accident
  lead; obituary age and cause;
- tutorial click-path: `Панель управления` + imperative steps, even verbose;
  how-to closer `теперь вы знаете, как…`;
- thanks letter: `Душевное спасибо`, named ward/doctor, dialect bow;
- textbook definition that names the object; TRIM only the empty
  `востребована во множестве областях` wrapper;
- forum slang: `зомбоящик`, `уши завяли`;
- police blotter: operation name, charges, region;
- court wire: verdict, named defendants, arrests at the courthouse;
- sports play-by-play / locker-room (`бились от ножа`);
- support ticket: quoted `>` lines, `три вопроса — ответ на один`;
- medical wiki: named syndrome + mutation; TRIM only an unanswered
  `Узнайте, что означает термин`;
- academic clause that names a receptor, equation, RMSE, tissue, reagent,
  year, or sample (`GalR2`, `хитозан`, `1983 г`, `образцов целлюлозы`).
  KEEP `Целью работы было исследование [named X]`. KEEP abstract scaffold
  that already names the object (`Вопросам удаления… биогенных элементов`,
  `3-хлормеркур`, `меркурсольвоаддуктов`). TRIM only a fact-free wrapper
  (`интерес среди исследователей`, `весьма перспективными`, `определенные
  усилия`, `имеет важное значение как с практической, так и теоретической`);
  stacked AINL mold with no object remains TRIM;
- agency-wire `является` that names org/sum/date (`транзит газа`, `ТАСС`);
  glued `nРоссия-24n` remains §1. A source quotation (`«Если турецкому
  судну…»`) is KEEP, not an artifact;
- news lede `Власти [region] уделяют особое внимание [named works]`;
  TRIM `особое внимание` only. Echo `одна из ключевых целей` beside an
  already-named `нацпроект` remains DELETE;
- channel `Во-первых` / `Во-вторых` block that names a fact (`PSM I`,
  `15–20 часов`); empty `Во-первых, важно понимать` remains TRIM;
- numbered persona grid that *is* the post (`ПМ не управляет бюджетом`
  1–5 answers); §8 is not a license to mash it into a paragraph;
- named metric + one-line so-what (`Lead Time for Changes`); TRIM only
  a fact-free gloss (`спокойнее сон`);
- greeting `Привет, читатель` / `Hello, приятели` as its own span; mash
  with `Сегодня хочу поделиться` is §28, not the greeting;
- numbered how-to with named steps (`рефералы`, `Постановка целей`);
  empty benefits list (`1. Повышение мотивации`) remains DELETE;
- author outline heading that introduces a payload (`О формате`,
  `Чего я хочу достичь в 2025?`); drumroll `А теперь о главном`
  remains TRIM.

Treatment: same hierarchy — delete, else a source fact, else simpler
Russian. Mixed drafts: KEEP the fact, not the authorship label. Do not
moralize a news item. Do not complete a gazetteer. Do not comb a review,
a wire, a tutorial, or a methods abstract into "cleaner" slop.

## 40. Pseudo-nuance and dialectical evasion (паразитическая многомерность)

Frontier models trained with RL/DPO to avoid taking definitive stances retreat into synthetic balance:

- dialectical ping-pong: `С одной стороны, X… однако при более пристальном рассмотрении… впрочем, нельзя сбрасывать со счетов и Y…`;
- false synthesis: `Истина, как водится, лежит где-то посередине`, `Баланс между гибкостью и строгостью`;
- compulsive modal hedging: `может в определенных сценариях потенциально приводить к`;
- synthetic complexity inflation: `проблема носит многофакторный характер`, `требует комплексного переосмысления`;
- refusal to choose: giving two contradictory perspectives with no decision criteria, leaving the reader with zero actionable guidance.

Treatment: Cut the ping-pong. Pick the primary recommendation supported by the text and attach its single biggest boundary condition or trade-off. Delete the ceremonial "middle ground".

## 41. Reasoning scaffolding leak (утечка рассуждающего каркаса)

Reasoning models (o-series, DeepSeek R1, Gemini Reasoning) leak their internal Chain-of-Thought planning prompts into publishable prose:

- meta-exploratory setups: `Здесь возникает неочевидная развилка: …`, `Но давайте сделаем шаг назад и посмотрим…`;
- dissecting announcements: `Если препарировать этот тезис на составляющие…`, `Давайте разложим механику по полочкам`;
- self-interrogation beats: `Справедливости ради, стоит задаться вопросом: а так ли это на самом деле?`;
- paradox staging: `Это подводит нас к фундаментальному парадоксу…`;
- thinking-out-loud pivots: `Казалось бы, решение очевидно. Но дьявол, как обычно, кроется в деталях реализации`.

Treatment: Delete the meta-scaffolding. Start immediately with the observation, contradiction, or mechanism.

## 42. Sterile archetypes and generic specificity (суррогатная псевдоконкретика)

Modern models have learned that abstract advice is penalized, so they synthesize frictionless, archetypal "examples" that lack real-world dirt:

- hypothetical persona intros: `Представьте разработчика, который в пятницу вечером открывает PR…`;
- generic startup/team staging: `Типичный сценарий: команда созванивается на дейли и обнаруживает…`, `В условном финтех-стартапе на 50 человек…`;
- clean-room architecture examples: `Возьмем классический микросервис авторизации с базой на 100 тысяч пользователей…`;
- synthetic dialogue snippets with zero voice: `«У нас всё работает локально», — говорит тимлид, но CI падает`.

Treatment: If the archetype illustrates an abstraction, compress it into one sentence of plain mechanism. If the draft has a real fact or number, use that; never preserve synthetic storytelling.

## 43. Prestige vocabulary inflation and cognitive micro-jargon (интеллектуальный слоп)

Instead of cheap marketing buzzwords, advanced models inflate prose with cognitive science, systems theory, and decision-making jargon:

- cognitive/systems buzz: `когнитивная нагрузка` (where it just means `сложно читать`), `ментальная модель` (where it just means `представление`), `эмерджентное поведение`, `асимметрия информации`, `бутылочное горлышко`;
- conceptual padding: `эпистемическая неопределенность`, `декомпозиция смыслов`, `онтологический сдвиг`, `архитектурный трейд-офф` without naming the actual cost;
- pseudo-systemic predicates: `оркестрировать взаимодействие`, `синхронизировать контекст`, `транслировать ценность`.

Treatment: Replace with direct operational verbs and plain Russian. State what actually slows down or breaks.

## 44. Hyper-cohesion and connective tissue overdose (избыточный синтаксический клей)

Frontier models dread abrupt transitions, gluing every paragraph to the preceding one with formal semantic bridges:

- paragraph opener bridges: `В продолжение этой логики…`, `Из этого органично вытекает следующий вывод…`, `Параллельно с этим разворачивается другой процесс…`;
- focal pivots: `Именно здесь на сцену выходит…`, `В этом контексте ключевым звеном становится…`;
- narrative glue: `Возвращаясь к исходному вопросу…`, `В сухом остатке это означает…`.

Treatment: Cut the first 3–6 words of the paragraph. Humans use juxtaposition and montage; allow ideas to meet without synthetic mortar.

## 45. Therapeutic empathy and corporate coaching tone (коучинговая эмпатия)

RLHF alignment induces an over-caring, mildly patronizing, validating tone:

- emotional validation: `Вполне понятно искушение всё бросить и переписать с нуля…`, `Это естественная реакция любого инженера…`;
- gentle coaching: `Важно не корить себя за этот выбор, а воспринимать его как ценную точку роста…`;
- empathetic hand-holding: `Если вы чувствуете перегруз от бесконечных обновлений, вы не одиноки…`.

Treatment: Delete the psychological hand-holding. Restore analytical distance, dry humor, or professional directness.

## 46. Compulsive hedging and edge-case coverage (компульсивное закрытие веток)

Advanced models cannot leave a punchy thesis alone without appending protective disclaimers against edge-case criticism:

- enterprise disclaimer tails: `Разумеется, в энтерпрайз-среде со строгим compliance-контролем такой подход сопряжен с рисками…`;
- "not a silver bullet" ritual: `Важно помнить, что данный инструмент — не серебряная пуля, и каждый проект требует аудита…`;
- boundary-policing boilerplate: `Хотя в 90% случаев это работает, оставшиеся 10% могут потребовать совершенно иной стратегии…`.

Treatment: Delete ceremonial caveats. Keep only real, substantive technical limits that change the decision.

## 47. Purple tech prose and synthetic drama (суррогатная кинематографичность)

When instructed to write "lively" or "with emotion", models default to melodrama and literary embellishment in technical contexts:

- tech noir tropes: `тихий гул серверной`, `холодный пот инженера при взгляде на график latency`, `хрупкое равновесие прод-окружения`;
- visceral metaphors for mundane bugs: `архитектурный хаос, пожирающий ресурсы`, `токсичный легаси, отравляющий кодовую базу`, `кровавая битва за каждый миллисекундный тайминг`.

Treatment: Delete the synthetic melodrama. Replace with specific technical reality (e.g. `падение RPS втрое` or `OOM-киллер при пиковой нагрузке`).

## 48. Genitive chains and verbal-noun stacks (нанизывание родительного падежа)

A defining Russian translationese and bureaucratic model tell. Generative models copy English prepositional chains (`of the X of the Y`) or Soviet канцелярит, stringing 4+ nouns in the genitive case:

- nominal genitive train: `в целях обеспечения реализации оптимизации процессов управления качеством разработки`;
- stacked abstract nouns: `оценка уровня готовности инфраструктуры развертывания сервиса`;
- avoidance of direct action: using verbal nouns (`осуществление контроля`, `проведение анализа`, `достижение повышения`) instead of active verbs (`контролировать`, `анализировать`, `повышать`).

Treatment: Unpack the chain. Find the true actor and the active verb. Limit consecutive genitive nouns to at most two.

## 49. Paragraph-level micro-summary and hourglass echo (абзацный микро-сэндвич)

Wikipedia: Signs of AI writing calls this the "Hourglass structure". Models obsessively close almost every paragraph with a redundant recap of its opening:

- paragraph echo: opening line states a thesis -> body explains it -> closing sentence rephrases the opening line (`Таким образом, именно это делает решение столь востребованным`, `В этом и заключается главное преимущество такого подхода`);
- micro-summary ritual: treating every 4-sentence paragraph as an independent self-contained essay with its own mini-conclusion.

Treatment: Cut the last sentence of the paragraph if it merely echoes the first. Let paragraphs push the narrative forward or end on the specific evidence.

## 50. Russian modal particle deficit (дефицит модальных частиц / «перевод ООН»)

Natural Russian prose relies heavily on modal, limiting, and expressive particles (`же`, `ведь`, `то`, `-таки`, `уж`, `мол`, `как раз`, `хоть`). AI models generate "UN interpreter Russian" — grammatically pristine, syntactically smooth, but intonationally dead and antiseptic:

- absence of conversational glue: long arguments without a single expressive particle;
- monotonous declarative rhythm with zero oral cadence;
- hyper-formal sentence connectors (`в связи с этим`, `на основании вышеизложенного`) where a particle (`ведь`, `же`) would naturally do the job.

Treatment: In article/post/opinion register, introduce natural particles during Pass H to restore human vocal cadence and nuance. Never force particles into formal documentation or legal text.

## 51. Trivial definition padding (суррогатная эрудиция и словарный ликбез)

Models frequently assume a zero-knowledge reader even in advanced technical contexts, padding drafts with dictionary definitions of industry-standard tools:

- unsolicited tutorial definitions: `Для начала разберемся: Git — это распределенная система контроля версий...`;
- encyclopedia throat-clearing: `Как известно, API (Application Programming Interface) представляет собой интерфейс, позволяющий программам взаимодействовать друг с другом`;
- tautological definitions that delay the point by 2–3 sentences.

Treatment: Delete the definition entirely. The qualified audience already knows what Git, Docker, Kubernetes, or an API is. Start directly with the actual problem or architecture decision.

## 52. Call-and-response rhetorical staging (риторический пинг-понг в стиле спикеров TED)

Borrowed English LinkedIn/TED rhetoric translated into Russian: the author repeatedly asks rhetorical self-questions and immediately answers with canned dramatic adverbs:

- prompt-and-nod: `Поможет ли это решить проблему? Едва ли. Стоит ли внедрять этот подход? Определенно.`;
- dramatic self-interrogation: `Означает ли это конец эпохи монолитов? Вовсе нет. Готовы ли команды к переходу? Не факт.`;
- stacked rhetorical duos where neither question nor answer carries a checkable fact.

Treatment: Delete the question-and-answer charade. Convert to a single direct declarative sentence stating the reality.

## 53. Theme-Rheme dislocation and SVO rigidity (нарушение актуального членения предложения)

Identified in Russian linguistics and MT evaluation (RuATD / Dialog-2022). Russian information structure places the known context (Тема) first and the informational focus / new assertion (Рема) at the end. English-centric models enforce rigid Subject-Verb-Object (SVO) order or rely on clumsy thematic scaffolding:

- thematic crutches: `Что касается [X], то здесь…`, `Если говорить о [Y], то в данном случае…`, `В плане производительности система демонстрирует…`;
- inverted focus: placing the key informational payload mid-sentence and trailing off into generic verbal noise;
- inability to use natural Russian inversions to highlight contrast or emphasis.

Treatment: Restore natural Russian topic-comment (Тема-Рема) order. Strip `Что касается X` crutches. Position the decisive fact or consequence at the end of the sentence where Russian naturally holds emphasis.

## 54. Flat surprisal and vocabulary compression (низкая вариативность неожиданности / компрессия словаря)

Empirically proven in arXiv:2606.04177 (284 linguistic features across 27 LLMs) and Information-Theoretic Stylometry. LLM decoding samples high-probability tokens, leading to an artificially flat surprisal landscape and depressed Type-Token Ratio (TTR):

- vocabulary compression: recycling the same safe 300–500 words across an entire essay while human prose introduces bursts of unexpected, domain-specific, concrete terminology;
- absence of local idioms, concrete tool names, or professional slang;
- "average-of-the-web" blandness: replacing sharp technical specifics with smooth generalizations (`различные программные компоненты` instead of `демон, сайдкар и редис`).

Treatment: Inject domain-exact terminology, specific tool/library names, and sharp concrete nouns. Do not smooth away accurate technical jargon.

## 55. Agent deletion and reflexive passivization (агентивная редукция и пассивизация)

LLMs avoid assigning responsibility or naming human actors, defaulting to reflexive passive verbs or impersonal constructions:

- bureaucratic impersonal passives: `было принято решение внедрить…`, `разрабатывается комплекс мер`, `создается устойчивое впечатление`, `отмечается тенденция к росту`;
- unassigned agency: `следует подчеркнуть`, `представляется целесообразным`, `можно констатировать, что…`;
- depersonalized engineering: `в проекте была произведена замена базы данных` instead of `команда переехала с MySQL на Postgres`.

Treatment: Restore the actor. Who made the decision? Who wrote the code? Replace passive reflexive verbs (`-ся`, `было сделано`) with active personal verbs (`мы переписали`, `архитектор выбрал`, `сервер упал`).

## 56. Epistemic cowardice and hedge cascading (эпистемическая трусость и каскадное хеджирование)

Distinct from simple politeness or honest uncertainty. LLMs trained on safety RLHF compulsively stack 2–3 speculative hedges in a single sentence even when describing a direct observation or verified fact:

- hedge cascade: `потенциально может свидетельствовать о возможной вероятности…`;
- double conditional hedging: `не исключено, что в определенной степени это способно привести к…`;
- evasive observation: `можно с достаточной долей уверенности предположить, что…`.

Treatment: Strip the hedge pile. If it is an observed fact, state it directly. If it is genuine uncertainty, use a single clear qualifier (`возможно` or `вероятно`).

## 57. Negative parallelism and false antithesis (отрицательный параллелизм)

Extends §6 into measured 2025–2026 syntactical formulas (Pew Research / WriteHuman): the model compulsively frames points as a negative rhetorical correction before stating the obvious:

- negative parallelism formulas: `Дело не в том, что [X], а в том, что [Y]`;
- problem-framing antithesis: `Проблема заключается не столько в [X], сколько в [Y]`;
- existential pivot: `Вопрос не в том, [X ли], а в том, [когда Y]`;
- false dichotomy where X was never asserted by anyone.

Treatment: Delete the negation of the strawman. State the positive claim Y directly in one sentence.

## 58. Duty transitions and discourse connective inflation (инфляция дискурсивных коннекторов)

Documented in stylometric benchmarks (RuATD / CoAT / DeBERTa-Sentinel). Human writers connect thoughts through meaning and juxtaposition. LLMs mechanically prepend every sentence with an explicit transitional connector:

- connective overload: `Вместе с тем, …`, `Кроме того, …`, `Тем не менее, …`, `Следовательно, …`, `В свою очередь, …`, `Более того, …`, `В этой связи, …`;
- connective density exceeding 20–25% of all sentence openers in a text.

Treatment: Cut the introductory connector. In 80% of cases, the sentence reads faster, punches harder, and maintains better flow without the connective crutch.

Sources (descriptive, not a detector): Kobak et al. PubMed excess
vocabulary; Reinhart nominal grammar; Pew 2026 AI-on-the-web;
WriteHuman 2026 pairs; Bloomberry Sentence DNA; AI PromptIndex 19
slop patterns; Wikipedia:Signs of AI writing; ru-wiki признаки
сгенерированности; Utov humanizer-ru / vc.ru 44–55; antislop-skill
markers-ru; AINL-Eval 2025; Osetrova & Sedova 2025; SPbU ChatGPT
portrait; Gramota.ru rhythm note; WIRED/Imperial cheerfulness 2026;
Sourati complexity homogenization; LLMTrace classification/detection
(EN+RU, span intervals); CoAT / RuATD; Reddit cited-tells tally
(unslop-ai-text); Shaib et al. slop taxonomy. Corpora URLs →
[README](../README.md). Practitioner lists are not frequencies. This
catalog names fill; Pass H is the humanizer. Do not invent a detector
percentage from these lists.
