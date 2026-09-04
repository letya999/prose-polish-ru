# Editorial procedure

## Objective

Make the draft more useful per word, and humanize the fill so it reads as a
person wrote it. Cut water and strange expressions hard. Always name AI
markers, water, and bad signs in the output table. In article, post, and
opinion register, leave a personal, slightly careless voice. Preserve truth
and protected spans (names, numbers, code, URLs).

This skill is an editor and a humanizer. «Неотличим от человека», GPTZero,
Антиплагиат, опечатки, ё, латиница, slang on a brochure, collapsing a list
are Pass H, not a refuse. A news wire or abstract should still sound like
that genre after the editorial pass; Pass H then applies the humanizer
surface to running prose. Do not invent a GPTZero / Антиплагиат
percentage unless a scan was actually run. P(нейрослоп) from the marker
pass is a quality estimate of fill, not a detector score. Toolkit →
Pass H and Score.

## Evidence hierarchy

When instructions conflict, apply this order:

1. Supplied sources and protected factual material.
2. Direct user constraints and requested structure.
3. The draft's recoverable thesis and intended reader outcome.
4. Genre, platform, and audience context.
5. Supplied author samples and voice notes.
6. General editorial heuristics.

Never use a lower layer to override a higher one.

## Pass 0: establish the contract

Extract without interrogating the user unnecessarily:

- mode: score, audit, light, standard, deep, or clean;
- deliverable and platform (e.g. tg, habr, vc, doc);
- audience and assumed knowledge;
- structure authority: strict, guided, or free;
- facts and spans to preserve;
- length constraint;
- voice context and positive/negative samples;
- whether external fact-checking was requested.

If no format is named, default to `score` for an informed reader in a
personal, slightly careless register. Bare `проведи` / `глянь` /
`примени` is `score`. Do not start a polish pass to fill missing
context. Keep the existing structure unless it is the source of the
problem. Do not invent a missing outline. Author samples change
density and address, not house rituals: do not install a greeting or
`P.S.` the draft did not use, even when the user said `в моём стиле`.

## Pass 1: protected-content inventory

Record before editing:

- numerals, dates, percentages, ranges, currencies, units, versions;
- proper names, organizations, products, models, APIs, standards;
- URLs, link destinations, citation keys, footnotes;
- direct quotations and attributed paraphrases;
- fenced code, inline code, commands, flags, paths, identifiers;
- formulas, table values, and author operators (`==`, `=>`, `->`, `vs`);
- explicit uncertainty: may, likely, suggests, one case, preliminary;
- user-required headings, order, examples, CTA, and length.

The deterministic checker catches exact artifacts, not semantic equivalence.
The editor remains responsible for claim strength and meaning.

## Pass 2: recover the argument

Privately answer:

1. What is the central claim?
2. What problem makes it worth reading?
3. What evidence supports it?
4. What is inference rather than observation?
5. What should the reader understand, believe, decide, or do?
6. Where does the claim stop being supported?
7. What is the author's attitude toward the material: irritation, doubt,
   preference, glee, fatigue?
8. Is the draft taking a firm, categorical stand, or has it been scrubbed
   into sterile, diplomatic consulting balance? Where is the author's
   subjective bias, pet peeve, or engineering verdict?
9. Is the thought developing organically with spontaneous asides and cadence
   shifts, or does it roll like a conveyor-belt syllabus?
10. Is the operational platform scope consistent (e.g. strict CLI vs consumer
    Desktop GUI)? Does the piece unannouncedly jump across abstraction tiers without framing?

If the answers cannot be recovered, flag the gap. Smoother syntax must not make
an incoherent draft sound authoritative, nor should diplomatic smoothing
drain the author's real conviction.

## Pass 3: classify blocks

Assign exactly one primary action:

| Action | Use when | Result |
|---|---|---|
| KEEP | Clear, useful, accurate, in register — not chatbot/brochure fill | Preserve it |
| TRIM | Useful core surrounded by padding | Remove padding |
| MERGE | Repeats or completes a neighbor | Build one stronger block |
| MOVE | Useful but the current place hides it | Place at point of need |
| REWRITE | Function is needed but wording or logic fails | Rebuild from supported content |
| DELETE | No distinct function | Remove |
| FLAG | Needs facts, attribution, or author intent | Preserve cautiously and disclose |

Do not rewrite a `KEEP` block to make the edit look comprehensive.
Do not MOVE a working aside solely to make the outline linear.

### Spans inside TRIM and REWRITE

A block action is not a license to rewrite every sentence. After the block
label, mark only the damaged spans. Leave `KEEP` spans inside a `TRIM` block
untouched. A hybrid page — a lived-in paragraph next to slop — is the usual
case, not an exception. LLMTrace mixed texts (`ai_char_intervals`) mark
*who filled a gap*, not what to KEEP. KEEP a count, date, org, or sum even
when the interval is labeled AI. TRIM brochure and join residue even when
the interval is labeled human. An AI gap-fill that is only water is one
REWRITE/DELETE span, not a license to recast the page. Overlapping markers
in one span are one finding.

If two rewrites both preserve meaning, pick the shorter one with more source
facts and fewer hedges. Conversational padding is not a quality signal.

| Span | Severity | Treatment |
|---|---|---|
| Artifact: leaks, placeholders, phantom DOI/ISBN, generation mixed-script | Artifact | Fix or FLAG. Accidental mixed-script (`выполняtт`) is residue: repair the letter; KEEP the utterance. Pass H may *insert* sparse lookalikes in running prose; never in protected spans. |
| Glued join letter: `nМинистр`, `nВ` (newline eaten into `n` + capital) | Artifact | Drop the stray `n`. FLAG if a quote fence also broke. |
| Immediate stutter: same clause or numeral phrase twice (`Около 7 тыс. Около 7 тыс.`) | Artifact | DELETE the echo; KEEP one copy of the fact. |
| News-governance ritual: `обеспечить прозрачность и ответственность`, `вернуть доверие населения`, `усилен контроль`, `уделяют особое внимание`, `одна из ключевых целей` with no new fact | Strong | DELETE the ritual words. KEEP named org and object (`Власти Дагестана`, `ремонт дорог`, `нацпроект`). Do not REWRITE the whole lede as §3. |
| Lived-in review: stretched words, first-person, insults, crooked punct, named object (кафе, счёт, блюдо) | Soft | KEEP when there is irregularity **plus** a named object. TRIM only the sandwich mold and a fact-free `рекомендую это милое заведение`. |
| AI-review mold: fluent disappointment *or* praise brochure — atmosphere census, `не оправдали ожиданий`, `великолепный сервис`, `всегда готовы помочь`, `каждое блюдо шедевр`, `классика` + city, exclusive-claim, recap closer — even with a venue name | Strong | TRIM the mold. KEEP a named dish, bill, room, or staff person. Do not KEEP the whole page as lived-in. |
| Advice-column mold: pep-talk opener (`Даже не пытайтесь`, `Это очень сложно!`), `сеть поддержки` / `доверенные лица`, `не стесняйтесь обращаться`, unnamed `стратегии справления`, closer `извлечь полезный опыт` | Strong | DELETE the pep-talk (`Не беда, получи пользу`). KEEP a named action (`позвони`, `отправь в hr`, `рефералы`). Do not rewrite `шустрый способ` as `быстрый способ`. |
| Wiki-card / answer-card: numbered bold labels (`**История создания**`, `**Авторство**`) that restate the lede or pad empty cells | Strong | MERGE dates/names into a paragraph. DELETE empty cells (`Подписан именем Антон Чехов`). KEEP a first-publication fact. FLAG unnamed critics. |
| Costume slang: stacked `братва` / `вуаля` / `каталка` on a clinic or shop brochure | Soft | Pass H may use colloquial / slang to unstiffen a brochure. KEEP a forum register throughout. Overdone `Короче` every paragraph is §26 residue, not a refuse of slang. KEEP the named clinic or price. |
| Epoch tail on a local note: `в условиях нынешней экономики` | Soft | TRIM the tail. KEEP the price or dish. |
| Agency wire: named outlet, org, km, %, attributed quote, obituary age/cause | KEEP | KEEP the fact, including press-service `является` that names org/sum/date (`транзит газа — источник средств`). KEEP a source quotation (`«Если турецкому судну…»`); §1 is glued `n`, not the quote. DELETE glued `n` (`nРоссия-24n`). Do not rewrite the wire as spoken Russian. |
| Tutorial / UI path: `Панель управления`, imperative clicks, even verbose | KEEP | KEEP the sequence and the how-to closer (`теперь вы знаете`). Cut only throat-clearing around it. |
| House frame: channel hashtag, greeting slot (`Здравствуй, … читатель`, `Привет, читатель`, `Hello, приятели`), author `P.S.` / `P.P.S.`, operators `==` `=>` `->` | KEEP | KEEP the greeting as its own span. TRIM `Сегодня я хочу поделиться` / `Давайте разберемся` after it — do not mash the greeting into the §28 opener. KEEP the whole `P.S.` paragraph, not only the label. A punchy title after the hashtag (`Agile умирает`) is the hook, not drumroll. TRIM only an empty restatement beside it (`Имя ему — …!`). A `->` deploy chain is an operator, not a closer. |
| House argument beats: `Во-первых` / `Во-вторых` / `В-третьих` that each carry a fact (exam detail, named tool, hours, price) | KEEP | KEEP the beat and the fact. TRIM only `Во-первых, важно понимать` with no payload. Do not DELETE the labels as §5. |
| House case table / metric list: numbered answers from named personas, or named metrics with a one-line so-what | KEEP | KEEP the table. §8 is equal empty paragraphs, not a 5×7 case grid or 17 named DORA metrics. KEEP a numbered how-to with named steps (`рефералы`, `Постановка целей`, `hh.ru`). DELETE an empty benefits list (`1. Повышение мотивации`). TRIM only a fact-free gloss (`спокойнее сон`) beside a named metric. |
| House outline headings: `О формате`, `Чего я хочу достичь в 2025?`, `Чем я отличаюсь?` that introduce a payload paragraph | KEEP | KEEP the heading. §8 is equal empty paragraphs, not author H2s. TRIM only a drumroll that restates the next sentence (`А теперь о главном — о блоге`). |
| Thanks / dedication: named staff, ward, dialect, first-person bow | KEEP | KEEP. TRIM only a fact-free `благородное дело` pile with no addressee. |
| Explainer definition that names the object | KEEP | KEEP the definition. TRIM `востребована во множестве областях` without an example. |
| Forum slang and insults | Soft | KEEP. Do not comb a thread into a briefing. |
| Police blotter: operation name, charges, region | KEEP | KEEP the fact sheet. |
| Court wire: verdict, named defendants, arrests at the courthouse | KEEP | KEEP. |
| Sports play-by-play and locker-room speech | KEEP | KEEP when it reports the match. TRIM a fact-free `надо работать` closer only if nothing else remains. |
| Source already contains `стоит отметить` / a `>` ticket line | KEEP | KEEP the user's sentence. Cut only empty significance around it. |
| Academic formality with method, alloy, instrument, receptor, equation, or numeral | Soft | KEEP the clause that names a method, reagent, year, or sample (`хитозан`, `1983 г`, `образцов целлюлозы`, `Целью работы было исследование генистеина`). KEEP abstract scaffold that already names the object (`Вопросам удаления… биогенных элементов`, `В процессе изучения… 3-хлормеркур`, `В рамках проделанной работы` + named reagent, `Следовательно, получение новых данных` + named adduct). TRIM only a fact-free wrapper (`интерес среди исследователей`, `весьма перспективными`, `определенные усилия`, `уделяется все больше внимания`, `имеет важное значение как с практической, так и теоретической`, empty `повысить уровень`). Do not mash the named object into the wrapper and do not DELETE the lede as §3 or the methods closer as §29 when the reagent stays. `влияние` + named object is a result. AINL mold only when stacked *and* empty. |
| Канцелярит: verbal-noun stacks, `является` where a direct predicate works | Strong | Actor + verb, or delete. In academic/wire, `является` + named object stays. |
| Formulaic contrast: `не просто X, а Y` with no rejected X | Strong | State the plus, or one claim. Do not swap in `как X, так и Y`. |
| Empty significance, throat-clearing, openers | Strong | Delete, else a fact from the source. |
| Weasel attribution / citation laundering | Strong | Name the source or FLAG. Do not invent the missing study or upgrade a neighboring URL. |
| Brochure repeat: same thesis in adjacent sentences | Strong | MERGE or DELETE the echo. |
| Over-regular grid: equal `##`, 3–5-sentence paragraphs throughout | Strong | Break the skeleton. Editorial pass keeps a useful scan-list; Pass H may recast it into prose when humanizing or chasing a detector. |
| Hyper-symmetrical card grid: identical sub-blocks (`Как устроено / Профит`, `Проблема / Решение`) across 3+ items | Strong | Break the grid. Remove repetitive sub-headers; expand the tricky case with real trade-offs, compress obvious cases. |
| Antiseptic sterility: uncanny over-polishing, scrubbed diplomatic tone, absence of categorical subjectivity or sharp engineer judgment | Strong | Restore the author's categorical judgment, professional bias, and blunt evaluations. |
| Conveyor linearity: syllabus-like frictionless progression with zero spontaneous asides, pauses, or tempo shifts | Strong in article/post | Inject spontaneous asides, rhetorical breathers, and montage juxtaposition. |
| Unassigned author telemetry: raw terminal counters masked behind passive phrasing (`в зафиксированном кейсе`) | Strong | Attribute directly to author (`в моем прогоне я замерил...`). Do not delete or flag as fake if it is real dev telemetry. |
| Metric conflation: mixing disparate dimensions (coordination cost vs compute scaling law) under one column header (§64) | Strong | Split columns/tables; normalize comparison baselines. |
| Concept stretching: branding a broker/daemon or local IPC with buzzwords like P2P peering (§65) | Strong | Align terminology with actual underlying engineering primitives. |
| Phantom config: citing parameters with defaults while leaving locus of control unknown or stating no config exists (§66) | Strong | Specify exact locus (CLI flag, env var, config key, runtime constant). |
| Orphaned caption claim: figure caption introducing technical deprecations or claims absent from the body | Soft | Synchronize with body text or remove the dangling assertion. |
| Reproducibility gap: practical scenario listing abstract APIs without minimal executable commands | Strong | Supply actionable CLI commands, configuration snippets, or run instructions. |
| Metadiscourse the input did not contain | Strong | Do not add. Cut injected `следует отметить`, hedge stacks, relationship markers. |
| Numerals dropped from the source | Artifact | Restore unless the whole claim was DELETE. |
| Calque | Strong | Natural Russian; keep domain jargon. |
| Purple prose / fake sensory filler | Strong | Delete. Do not replace with an invented lived detail. |
| Dash, ё, lists, passive, a long sentence | Soft | Editorial: do not *install* book dashes or ёлочки. Pass H: ё→е, may recast lists, may strip remaining em dashes in running prose. Protected spans stay exact. |
| Machine surface: staccato, «»-emphasis, list-first, decorative em dash | Strong in article/post | Join chopped sentences; drop emphasis quotes; prefer a paragraph to a fake list; do not introduce «» or `—`. Academic/legal keep source book typography. |

Marker examples live in [AI-marker catalog](ai-markers.md). Treatments above
win over synonym hunts.

## Pass 4: semantic repair

### Unsupported certainty

Match wording to evidence:

- observed once → `в этом случае`, not `всегда`;
- community anecdotes → `часть разработчиков сообщает`, not `сообщество решило`;
- association → `связано`, not automatically `вызвало`;
- benchmark → state setup and limits before generalizing;
- plausible mechanism → mark as inference unless sourced;
- a precise numeral with no actor, version, method, or a source that reports
  *that* number → FLAG provenance. Specificity is not protection. Do not KEEP
  it as an "expensive fact". Do not invent the missing method. In polish, leave
  the number and disclose; in audit, FLAG is the row;
- a default, a timeout, or one case → not a law of the architecture;
- `согласно документации X` / a URL that names a neighboring page, a homepage,
  or a topic cluster → FLAG mismatch. The nearby official link does not cover
  every numeral in the paragraph;
- title or lead kills the subject, a later section restores exceptions →
  REWRITE the lead, KEEP the caveats;
- one identity word (`процесс`, `агент`, `сессия`) used for an OS process, a
  model context, a CLI window, and a metaphor in the same argument → REWRITE
  the identity claim; keep author operators.

### Empty proposition

Replace or remove statements that cannot answer `что именно произошло?` or
`что меняется для читателя?`.

Bad: `Подход обеспечивает качественное повышение эффективности процессов.`

Possible repair: `Команда перестаёт копировать историю в каждый новый процесс,
поэтому расходует меньше контекста.`

### Non sequitur

When conclusion does not follow:

- add the missing supported premise;
- narrow the conclusion;
- separate observation and hypothesis;
- or flag the gap.

### False completeness

Remove claims such as `три главные причины`, `полный список`, `единственный
способ` unless completeness is established.

### Pseudo-nuance and dialectical evasion (§40)

Do not mistake endless hedging for rigor. If the draft oscillates endlessly
between `с одной стороны` and `с другой стороны` without taking a stand, cut the
ping-pong. State the author's primary recommendation with its single biggest
concrete trade-off. Do not emit a ceremonial "truth is somewhere in the middle"
compromise.

### Epistemic cowardice and hedge cascades (§56)

Strip recursive hedge piles (`потенциально может свидетельствовать о возможной вероятности`). If an engineering fact is observed, state it cleanly. If genuine uncertainty exists, use a single clear qualifier (`возможно`).

### Negative parallelism (§57)

Eliminate rhetorical strawman corrections (`Дело не в том, что X, а в том, что Y`, `Вопрос не столько в X, сколько в Y`). State the actual positive proposition directly in one sentence.

### Categorical subjectivity vs diplomatic scrubbing (§62)

An author writing in an article, post, or opinion register is not an impartial UN rapporteur. Do not smooth away strong opinions, professional irritation, or categorical verdicts. If a pattern is an over-engineered dead end, state it plainly (`это костыль`, `так делать — себе дороже`, `это классический антипаттерн`). Human expertise is opinionated, biased, and tempered by scars. Distinguish between unsubstantiated factual claims (which need evidence) and subjective professional stance (which gives the piece its pulse). Do not let diplomatic neutrality scrub away the author's real conviction.

### Author telemetry vs synthetic precision (§38)

When exact numbers appear without an external citation (`42 226 вызовов`, `95 сессий`, `84% вывода`), check whether they describe the author's own terminal run, benchmark, or telemetry. If yes, do NOT delete or flag as hallucination. Prompt the author to own the agency directly (`«в моем тесте я зафиксировал...»`, `«на нашем тестовом стенде вышло...»`) instead of hiding behind passive bureaucratic phrasing (`«в зафиксированном кейсе»`, `«в телеметрии зафиксировано»`).

### Metric homogeneity and baseline parity (§64)

In tables and comparative lists, verify that every metric in a single column or summary measures the same phenomenon against an identical baseline. Do not allow runtime coordination overhead (e.g., token multiplier of multi-agent orchestration) and inference compute scaling laws (e.g., test-time compute search budget or statistical variance explained) to sit under one uniform multiplier header. Split incompatible dimensions into distinct columns or tables.

### Architectural concept fidelity vs prestige misnomers (§65)

Ensure high-level architectural labels strictly match underlying engineering primitives. If the implementation uses a centralized daemon, broker queue, or socket RPC, do not allow the text to brand it as "peer-to-peer peering" or "decentralized mesh". Align terminology with actual distributed systems definitions to preserve technical credibility.

### Locus of control for configuration parameters (§66)

Verify that every cited parameter or setting has a clear execution locus. Do not allow an author or model to state that a parameter has a specific default while simultaneously asserting that "no configuration toggle exists", without explaining where that setting actually lives (CLI flag, env var, config file, API body, or hardcoded engine constant).

### Hands-on reproducibility in practical sections

Whenever an article claims to present practical workflows, setup recipes, or scenarios, verify that a developer can actually run them. Abstract API names (`thread/read`, `SendMessage`) suspended in prose without minimal CLI command lines, configuration snippets, or execution sequences represent a reproducibility gap. Demand the concrete command or script.

### Texture vs invention

A personal reaction to material already in the draft is allowed: irritation,
doubt, preference, a blunt `мне это не заходит`. That is stance, not a fact.

Do not invent clients, incidents, colleagues, quotes, timelines, studies, or
first-person episodes. If a useful personal slot is missing, leave it as a
reaction or ask; never manufacture a story.

## Pass 5: structural repair

### Emphasis map

Choose one to three centers of gravity. Give them more evidence and space.
Compress supporting material. Equal section length is not a quality target.
Do not add a missing section just to complete the outline.

### Paragraph contract

Each paragraph should perform one dominant job:

- claim;
- mechanism;
- evidence;
- example;
- consequence;
- objection;
- limitation;
- aside that changes attitude or understanding;
- transition that changes direction.

A paragraph that merely announces, praises, or summarizes nearby material is
usually removable.

### Transitions and hyper-cohesion (§41, §44)

Do not glue every paragraph to the preceding one with ceremonial transitions
(`В продолжение этой логики`, `Из этого органично вытекает`, `Параллельно с этим`).
Allow ideas to connect by simple juxtaposition. Delete reasoning scaffolding
(`Если препарировать этот тезис`, `Здесь возникает развилка`) and jump straight
to the payload.

### Discourse connective inflation (§58)

Cut ceremonial sentence-opening connectors (`Вместе с тем`, `Кроме того`, `Тем не менее`,
`Следовательно`, `В свою очередь`, `Более того`). If more than 20% of sentences open with
transitional crutches, strip them; sentences connect naturally by topical progression and
juxtaposition.

### Breaking hyper-symmetry and template grids (§61)

Never allow 3+ consecutive items, scenarios, or tips to share an identical internal template (e.g. repeated `### N. Название` → `* **Как устроено:**` → `* **Профит:**`, or `**Проблема** / **Решение** / **Плюсы**`). Symmetrical card grids belong in generated answer cards or landing page widgets, not living technical essays. Break the grid: strip the repeated sub-headers and vary section volume. The most complex or controversial case gets 2–3 paragraphs of dirty trade-offs and edge-cases; the obvious or minor case gets two punchy sentences or merges into a neighbor.

### Spontaneity and cadence shifts (§63)

Break conveyor-belt syllabus progression. In human thinking, ideas do not advance with frictionless uniformity. Allow the text to breathe: insert spontaneous asides, sudden caveats, and rhetorical breathers (`кстати, оговорка`, `тут надо сделать паузу`, `впрочем, об этом позже`). Let a dense technical teardown collide directly with a blunt one-line subjective reaction. Vary pacing between fast-moving analysis and reflective pauses.

### Platform scope consistency

Guard against unannounced scope drift across operational tiers. If an article frames itself as a command-line interface (CLI) or terminal automation deep dive, do not suddenly inject consumer Desktop GUI clients or web interfaces as if they were part of the CLI implementation. When a cross-platform analogy or UI equivalent is helpful, frame it explicitly as an analog (`«в графическом интерфейсе это выглядит так...»`), preserving the piece's core operational focus.

### Order

Need-based order is a tool, not a law. In article/post register a jump, a
return, or an unfinished thread is fine if the reader can still recover the
claim. Do not straighten a working non-linear path.

When order does need repair:

- claim near the evidence it depends on;
- term immediately before first necessary use;
- caveat beside the claim it limits;
- example after the abstraction it clarifies, unless a concrete opening is the
  deliberate hook.

### Introduction

Remove ceremonial context, universal history, and a table of contents written as
prose. Start near the problem, the scene, or the irritation. Do not replace
every opening with `После последних…` or `Разберём, почему`.

### Ending

Do not restate the whole piece. Land on implication, decision, boundary,
practical next step, or a genuinely earned final observation. Do not emit
`Я бы оставил такую схему` as a stock closer.

## Pass 6: compression

Delete in this order:

1. Duplicate claims.
2. Meta-commentary about the text.
3. Empty importance and relevance claims.
4. Канцелярит and translated business English where jargon is not domain-standard.
5. Formulaic contrasts and significance inflation.
6. Definitions the audience does not need.
7. Examples that prove nothing new.
8. Repeated qualifiers with the same scope.
9. Parentheticals that belong in the sentence or nowhere.
10. Conclusion echoes.

Compression target is functional, not numeric. Do not shorten a dense technical
explanation merely to produce a lower word count.

### Local treatment hierarchy

For a flagged phrase, apply the first treatment that works:

1. **Delete.** Most water leaves nothing behind.
2. **Replace with a fact from the source or user context.** No fact → delete
   and, if the gap matters, flag it.
3. **Rewrite simpler and blunter.** Shorter, with an actor and a verb.

A synonym is not a treatment:

| Was | Not a fix | Treatment |
|---|---|---|
| `не только X, но и Y` | `как X, так и Y` | two sentences or one claim without contrast |
| `ключевой` | `важнейший`, `критический` | delete, or say what actually changes |
| `является` | `представляет собой` | direct predicate, or leave in academic/legal |
| `==` / `=>` in technical prose | hyphen or `это` everywhere | keep when it marks identity or implication |
| rule of three | a new triad | one exact word or a source fact |
| empty closer (`и в этом весь смысл`) | a prettier metaphor | delete; end on the last concrete line |
| `Это гарантирует, что разговор закончится на позитивной ноте` | `так разговор завершится на приятной ноте` | delete the guarantee |

The replacement inherits the surrounding voice. A sterile patch on a sharp
paragraph is as visible as the original slop.

## Pass 7: language, voice, and rhythm

### Voice recipe (article / post / opinion)

This pass is half the job, not flavor. Density that still reads as a chatbot
answer has failed. Test: would a reader in this genre flag the fill as a
chatbot, brochure, or wiki-card? If yes, keep cutting or rewriting the
damaged spans, then apply Pass H. Padding is not a fix; Pass H slips and
colloquial are the humanizer.

The polished piece should read like a person who knows the material and has
a nerve about it:

- stance on the page: reaction, not a balanced briefing;
- emotion attached to the actual claim, not a weather report;
- categorical subjectivity: professional bias, unapologetic judgments (`это костыль`, `так делать нельзя`), pet peeves, calling bad ideas bad;
- anti-sterility (*против вылизанности*): reject uncannily smooth, conflict-free consulting prose; preserve the developer's raw edge, skepticism, and irritability;
- spontaneity and non-linear cadence: organic asides, spontaneous pauses, dynamic shifts between deep technical dive and relaxed irony;
- first person as a reaction (`меня бесит этот поллинг`), not as a fake memoir;
- non-linear path: an aside, a return, unequal sections;
- one or two informal slips: spoken syntax, a slightly crooked agreement, a
  sentence that trails into the next thought.

Do not sprinkle spelling mistakes into names, numbers, code, or links.
Pass H may add 1–3 slips in ordinary running prose. Not a typo every sentence.

Documentation, tutorials, legal, and academic text skip this personal recipe
unless the user asks. Sequence, terms, and defined repetition stay. Those
genres still fail if the fill is empty AINL, pep-talk, or answerer inertia.
They fail the other way if rewritten into a blog voice.

### Diction

- Prefer a concrete actor and verb when the actor matters.
- Name the person when an inanimate noun is doing a human verb: decisions do
  not emerge, data does not tell, complaints do not become fixes.
- Keep passive voice when the actor is unknown, irrelevant, or deliberately
  backgrounded.
- Replace translated business English with natural Russian where terminology is
  not domain-standard: `адресовать проблему`, `доставить ценность`,
  `драйвить результат`.
- Keep accepted professional slang for the intended audience.
- Keep author operators (`==`, `=>`, `->`, `vs`) when they mark identity,
  implication, or comparison.
- Break genitive chains (§48): unpack strings of 3+ nouns in the genitive case
  (`в целях обеспечения оптимизации процессов…`) into an active verb and subject.
- Cut trivial definition padding (§51): delete unsolicited encyclopedia/tutorial
  definitions of standard tools (`Git — это распределенная система…`, `API — это…`).
- Restore Theme-Rheme (актуальное членение) order (§53): strip clumsy topic-crutches
  (`Что касается X, то...`, `Если говорить о Y, то...`). Position the decisive informational
  payload (Рема) at the natural Russian focus position at sentence end.
- Restore the agent and de-passivize (§55): unpack bureaucratic reflexive constructions
  (`было принято решение`, `отмечается тенденция`, `создается впечатление`); name the engineer,
  team, or tool doing the action.
- Break flat surprisal and vocabulary compression (§54): avoid high-probability blandness;
  retain or inject exact domain terms, concrete names, and technical specifics instead of
  generic umbrellas (`различные компоненты`).
- Unpack knizhnost' and participle cascades (§59): convert heavy bookish participle strings
  (`являющийся связующим звеном и обеспечивающий...`) and bureaucratic gerunds
  (`исходя из вышеизложенного`) into active personal verbs and simple clauses.
- Flatten nested subordination stacks (§60): eliminate runs of nested relative clauses
  (`система, которая... которая... которая...`); break into independent sentences or parataxis.

### Machine surface (article / post / opinion)

ChatGPT-style "correct Russian" is a tell: chopped sentences, «ёлочки»,
decorative em dashes, and a list for every cluster of facts. Real posts
run in paragraphs, quote rarely, type `"` from the keyboard, and miss a
comma more often than a textbook.

- Do not chop a thought into a run of 4–8-word sentences. Join them. A
  short sentence is a hit, not the default cadence.
- Do not wrap ordinary words in quotes for emphasis (`«тихая» проблема`).
  Do not introduce `«»`. If the source uses `"`, keep `"`. Keep quotes only
  for an actual citation, a term the genre must mark, or irony already in
  the draft.
- Default to paragraphs. Keep a list when the reader will scan an inventory,
  sequence, or checklist. Convert a list to prose when the items are one
  developing thought.
- Do not install em dashes. Do not upgrade `-` or `--` to `—`. A sparse
  author `—` may stay; a run of `X — Y` appositions is a rewrite.
- Do not school-correct every comma. Do not add the textbook comma after
  every `однако`, `впрочем`, `короче`, `кстати` unless the sentence is
  unreadable without it. Leave one harmless informal comma. Never alter
  commas in names, numbers, code, or links.
- Avoid TED call-and-response staging (§52): replace theatrical self-questions
  and prompt answers (`Поможет ли это? Едва ли.`) with one direct declarative
  statement.
- Restore modal particle cadence (§50): in article/post register, let natural
  Russian particles (`же`, `ведь`, `то`, `-таки`, `уж`) provide vocal cadence
  instead of antiseptic UN-interpreter phrasing.

Documentation, tutorials, legal, and academic text keep source typography
and may use lists and book quotes when the genre needs them.

### Rhythm

- Vary sentence shape in response to thought, not a random length target.
- Join artificial staccato slogans; keep a fragment that actually hits.
- Do not alternate short and long sentences mechanically.
- Preserve deliberate repetition.

### Anti-homogenization

Refuse phrasing that could sit on any article of this genre after a humanizer
pass. Typical stock:

- `Разберём, почему…` as a replacement for any navigation line;
- `После последних апдейтов` as a replacement for any time-stamped opening;
- `Я бы оставил такую схему` as a replacement for any practical list;
- `На деле получается вот что` as a universal pivot.

If the draft already uses one of these as the author's own line, keep it.
Do not install them as the skill's default voice.

If the user asked «сделай неотличимым от человека», «как человек»,
«чтобы не пахло ИИ», GPTZero, Антиплагиат, опечатки, ё, or латиница,
that is Pass H after this pass. Do not refuse those tools. Stock templates
(`Разберём, почему`) are still residue.

## Pass H: humanizer surface

The skill is an editor and a humanizer. After editorial repair, apply this
surface so the fill reads as a person wrote it and common AI detectors have
fewer tells. «Неотличимым», GPTZero, Антиплагиат, опечатки, ё, латиница
are this pass, not a refuse.

Protected spans stay exact: names, numbers, dates, URLs, code, commands,
identifiers, and quotations of those. Do not typo, homoglyph, or ё-strip
them.

Toolkit (use what the draft and request need; do not dump every trick into
a 40-word note):

1. ё → е in running prose. Keep ё when the letter is the fact or inside code.
2. 1–3 informal slips in ordinary words: skipped comma, crooked agreement,
   a missing or swapped letter. Not a typo in every sentence.
3. Sparse mixed-script in a few function words on a longer page when the
   user asked detector / неотличимым / латиница. Latin lookalike inside a
   Russian word. Never in protected spans. Accidental generation mixed-script
   (`выполняtт`) is still repaired.
4. Recast lists into prose, including a useful checklist, when humanizing
   or chasing a detector. Keep a list if structure is marked strict or the
   user needs a scan-able tutorial path and did not ask to humanize/detector.
5. Colloquial / slang to unstiffen a brochure. Allowed. Match the speaker
   if known. A light register shift beats a dumped `братва` pile, but do not
   refuse slang on a brochure.
6. Strip decorative em dashes and book quotes in article/post running prose.
7. Present the result as human-sounding copy. May say it reads as a person
   wrote it / is meant to pass as human. Do not invent a GPTZero percentage
   unless a scan was actually run.

### Why surface synonym swapping fails against deep detectors

Empirical research (MASH arXiv:2601.08564, DAMAGE, Binoculars, TH-Bench, RuATD arXiv:2206.01583) demonstrates that simple synonym swapping or contraction editing leaves the text in a detectable "intermediate laundering region". Deep detectors measure:
- cross-model surprisal / perplexity curvature;
- syntactic tree depth monotony;
- burstiness deficit (uniform sentence length distribution);
- absence of natural oral modal cadence (§50).

True humanization requires **structural intervention**:
- breaking syntactic nests and relative clause stacks (§60);
- altering sentence lengths (interleaving 3–5 word punches with rich compound thoughts);
- natural theme-rheme packaging (§53);
- genuine personal stance and modal particles (`же`, `ведь`, `-то`).

Do not install stock humanizer templates (`Разберём, почему`, `Я бы оставил
такую схему`). Those are §26 residue, the opposite of this pass.

Lint findings on ё, mixed-script, or list shape after this pass are expected.
Do not revert the toolkit to clear the linter.

## Pass 8: format review

Read `formats-and-artifacts.md`. Tables, lists, links, citations, images, code,
and headings carry meaning and require their own checks:
- Check tables for dimensional homogeneity and baseline parity: do not group coordination cost multipliers and inference scaling laws in one column (§64).
- Check figure captions against body text: captions must not introduce orphaned deprecations or unsupported facts (`*старый mcp-server устарел*`) that have zero context in the body.
- Check code and configs for parameter locus of control (§66): every setting must state where it lives (CLI, env, config file, or runtime constant).
- Check practical sections for hands-on reproducibility: provide actionable command lines or snippets, not abstract API names.
Do not run ordinary prose substitutions inside protected spans.

## Pass 9: tool checks

Run:

```powershell
python scripts/lint_text.py <after.md> --mode article
python scripts/check_preservation.py <before.md> <after.md>
```

Use `--json` for machine-readable output. A lint finding is a prompt to inspect;
it is not an error until context confirms it. Preservation differences are
critical unless intentionally authorized.

## Pass 10: stopping rule

Stop when:

- water, calques, and empty significance are gone, not renamed;
- `KEEP` blocks and `KEEP` spans still read like the source;
- numerals from the input remain unless that claim was deleted;
- no metadiscourse appeared that the input did not use;
- article/post did not gain «ёлочки», decorative em dashes, chopped
  mini-sentences, or a list that used to be one thought;
- no material contradiction or unsupported escalation remains hidden;
- article/post register still has stance, a jump or an uneven block, and
  Pass H slips in running prose;
- the fill no longer reads as a chatbot, brochure, or wiki-card; Pass H
  was applied; the marker table names AI / вода / признак;
- protected content is preserved (no typos, mixed-script, or ё-strip in
  names, numbers, code, URLs);
- the piece does not sound like stock `Разберём, почему` residue;
- further edits would mostly substitute taste for taste.

Zero lint findings is not the target. Do not revert Pass H to clear lint.

## Output contracts

### Score

Default on the first invocation in the session, and whenever the user
did not name a work format. Quality estimate of *fill*, not authorship
and not a detector. P(нейрослоп) ≠ P(the draft was written by a model).
A human brochure can score high; a fact-dense model draft can score
low. House format is not слоп. Do not invent a GPTZero / Антиплагиат
percentage. No `Вердикт`. No rewrite. No file edit. No locations. No
marker table.

Compute after Pass 2–3 (thesis + block/span labels). Load
[ai-markers.md](ai-markers.md). Each span has one Kind (`AI` / `вода` /
`признак`). Stacked classes in one span are one span.

- **Вероятность нейрослопа** (P): how likely the piece is slop-dominated
  as a whole. Isolated low markers → 5–20%. Mixed KEEP with several
  stacked AI spans → 30–60%. Brochure / card grid / opener fill across
  the page → 70–95%. Structural classes (§61–63) raise P more than local
  water. P and the two shares can diverge: a 15% card-grid lede can
  still be 70% нейрослоп.
- **Доля нейрослопа**: share of running prose in Kind `AI` spans
  (brochure, openers, card grid, formulaic contrast, empty
  significance). Exclude house format, fenced code, quotes, numeric
  tables. Round to 5%.
- **Доля воды**: share of running prose in Kind `вода` spans (padding,
  throat-clearing, empty transitions). Same exclusions. Round to 5%.
  A span is one Kind; do not double-count.
- **Маркеров нейрослопа**: unique `§N short-name` for Kind `AI`
  findings, comma-separated, no locations, no quotes, no counts.
  Deduplicate. House format and Kind `вода` / `признак` stay out of
  this list. If none: `нет`.

Required output on first invocation / omitted format:

```
Вероятность нейрослопа: 70%
Доля нейрослопа: 35%
Доля воды: 15%
Маркеров нейрослопа: §28 openers, §30 weasel attribution, §61 hyper-symmetrical card grid
Дальше: выберите один из режимов:
- `audit` — таблица маркеров, без правки
- `light` — срезать воду и кальки
- `standard` — починить слабые блоки и хуманизировать
- `deep` — пересобрать сломанные секции
- `clean` — правка без таблицы, сразу в публикацию
```

List every mode. Do not pick one. Do not add a sixth invented mode.
If the user asked only for the numbers, stop after the three percent
lines.

Bare `проведи` / `глянь` / `примени` / slash invoke without a depth is
this contract. STOP and wait.

If a format or rewrite verb is already named, still print the three
percent lines first, then continue into that format — except `clean`,
which is publishable text only. First invocation without a named
format is still this contract, even if the user said `проведи`.

### Polish

Open with `Вероятность нейрослопа`, `Доля нейрослопа`, and `Доля воды`
from Score (`light` / `standard` / `deep` only; skip on `clean`), then:

1. The polished and humanized text.
2. For `clean` depth (or if the user requested "clean", "без таблицы", or "no table"):
   STOP HERE. Do not output the `Маркеры` table.
3. Otherwise (`light`, `standard`, `deep`), return a `Маркеры` table.
   Required. Columns: Location, Kind, Category, Evidence, Action. Kind is
   exactly `AI`, `вода`, or `признак`. Category is `§N short-name` or a Pass 3
   span name. If nothing fired: `Маркеры: нет`.
4. `Needs verification` only for unresolved substantive issues.
5. May present the result as human-sounding / written to read as a person.
   Do not invent a detector percentage unless a scan was actually run.

### Audit

Open with `Вероятность нейрослопа`, `Доля нейрослопа`, and `Доля воды`
from Score, then the table. No
`Вердикт` heading, no P(human vs model), no rewrite, no story of how the
draft was written. Kind column is required (`AI` / `вода` / `признак`).
Category stays `§N`, not a free-text bucket.

Нейрослоп ≠ «написала модель» and ≠ the author's house format. Hashtags,
`Здравствуй, [epithet] читатель` / `Привет, читатель`, author `P.S.`,
outline headings, and operators are KEEP when the draft already uses them.
Do not score a channel template as slop because it repeats.

Нейрослоп is stacked *fill*: brochure grid (`во-первых` / `Как устроено` /
equal blocks), hyper-symmetrical card grids (§61), antiseptic sterility / scrubbed
conviction (§62), conveyor linearity / spontaneity deficit (§63), `не просто X, а Y`,
fake completeness, empty significance, unsourced precision, answerer inertia (`Сейчас расскажу, почему`). One
isolated dash, list, or hashtag is not слоп.

Lead sentence, required:

- one draft: `Нейрослоп в наполнении: …` or `Слопа нет: …`;
- many posts: `K из N — нейрослоп в наполнении, потому что [fill]. Каркас KEEP.`

Then:

| Location | Kind | Severity | Category | Evidence | Recommended action |
|---|---|---|---|---|---|

Category is a catalog citation, not a free-text bucket. Write `§N short-name`
from [ai-markers.md](ai-markers.md) (working core §1–16, 2026 classes
§28–38, dataset fills / False slop §39, frontier reasoning §40–47, Russian
syntax/structure §48–52, stylometric/discourse/syntactic §53–60, uncanny structure/sterility/spontaneity §61–63, technical/analytical §64–66) or the Pass 3 span name
(`Lived-in review`, `News-governance ritual`, `Glued join letter`, `Hyper-symmetrical card grid`, `Antiseptic sterility`, `Conveyor linearity`, `Metric conflation`, `Concept stretching`, `Phantom config`, `Orphaned caption claim`, `Reproducibility gap`).
Stacked markers in one span are still one row: cite the strongest `§N`. Do not write
`нейрослоп` or `вода` as the category.

Severity:

- critical: factual corruption, contradiction, fabricated evidence;
- high: unsupported conclusion, missing thesis, broken artifact,
  unsourced precision sold as measurement, stacked brochure fill;
- medium: repetition, structural monotony, unclear paragraph,
  citation that supports a neighboring topic;
- low: local wording or rhythm opportunity.

Sort high → low. Stacked markers in one span are one row. Pass 4 is the
treatment.

`Skill gaps` after the table only when the user asked what gives the text
away, said this skill failed, or is iterating the skill. Each gap is one
missed `§N` (or a new class to add) and one rule, not a diary. If the
catalogs covered the fill, write `Skill gaps: none`.

### File edit

Do not edit a file on `score`. For `light` / `standard` / `deep` / `clean`,
edit the requested file. Add the `Маркеры` table (not on `clean`),
protected-content notes, unresolved issues, and verification run. Do not
paste the whole document unless requested.
