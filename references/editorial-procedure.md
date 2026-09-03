# Editorial procedure

## Objective

Make the draft more useful per word. Cut water and strange expressions hard.
In article, post, and opinion register, leave a personal, slightly careless
voice: emotion, jumps, uneven structure, a couple of informal slips. Preserve
truth, working formatting, and individual texture. Humanization is a side
effect of good editing, not a claim about authorship.

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

- mode: audit, light, standard, or deep;
- deliverable and platform;
- audience and assumed knowledge;
- structure authority: strict, guided, or free;
- facts and spans to preserve;
- length constraint;
- voice context and positive/negative samples;
- whether external fact-checking was requested.

If no context is supplied, default to standard polish for an informed reader
in a personal, slightly careless register. Keep the existing structure unless
it is the source of the problem. Do not invent a missing outline.

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

If the answers cannot be recovered, flag the gap. Smoother syntax must not make
an incoherent draft sound authoritative.

## Pass 3: classify blocks

Assign exactly one primary action:

| Action | Use when | Result |
|---|---|---|
| KEEP | Clear, useful, accurate, in register | Preserve it |
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
| Artifact: leaks, mixed-script, placeholders, phantom DOI/ISBN | Artifact | Fix or FLAG. Mixed-script is residue to repair, not a humanizer trick to insert. |
| Glued join letter: `nМинистр`, `nВ` (newline eaten into `n` + capital) | Artifact | Drop the stray `n`. FLAG if a quote fence also broke. |
| Immediate stutter: same clause or numeral phrase twice (`Около 7 тыс. Около 7 тыс.`) | Artifact | DELETE the echo; KEEP one copy of the fact. |
| News-governance ritual: `обеспечить прозрачность и ответственность`, `вернуть доверие населения`, `усилен контроль` with no new fact | Strong | DELETE. KEEP adjacent sums, dates, orgs. |
| Lived-in review: stretched words, first-person, insults, crooked punct, named object (кафе, счёт, блюдо) | Soft | KEEP when there is irregularity **plus** a named object. TRIM only the sandwich mold and a fact-free `рекомендую это милое заведение`. |
| AI-review mold: fluent disappointment *or* praise brochure — atmosphere census, `не оправдали ожиданий`, `великолепный сервис`, `всегда готовы помочь`, `каждое блюдо шедевр`, `классика` + city, exclusive-claim, recap closer — even with a venue name | Strong | TRIM the mold. KEEP a named dish, bill, room, or staff person. Do not KEEP the whole page as lived-in. |
| Advice-column mold: pep-talk opener (`Даже не пытайтесь`, `Это очень сложно!`), `сеть поддержки` / `доверенные лица`, `не стесняйтесь обращаться`, unnamed `стратегии справления`, closer `извлечь полезный опыт` | Strong | DELETE the pep-talk (`Не беда, получи пользу`). KEEP a named action (`позвони`, `отправь в hr`, `рефералы`). Do not rewrite `шустрый способ` as `быстрый способ`. |
| Wiki-card / answer-card: numbered bold labels (`**История создания**`, `**Авторство**`) that restate the lede or pad empty cells | Strong | MERGE dates/names into a paragraph. DELETE empty cells (`Подписан именем Антон Чехов`). KEEP a first-publication fact. FLAG unnamed critics. |
| Costume slang: stacked `братва` / `вуаля` / `каталка` on a clinic or shop brochure | Strong | TRIM the costume. KEEP the named clinic or price. Real forum register throughout stays KEEP. |
| Epoch tail on a local note: `в условиях нынешней экономики` | Soft | TRIM the tail. KEEP the price or dish. |
| Agency wire: named outlet, org, km, %, attributed quote, obituary age/cause | KEEP | KEEP the fact, including press-service `является` that names org/sum/date (`транзит газа — источник средств`). DELETE glued `n` (`nРоссия-24n`). Do not rewrite the wire as spoken Russian. |
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
| Academic formality with method, alloy, instrument, receptor, equation, or numeral | Soft | KEEP the clause that names a method, reagent, year, or sample (`хитозан`, `1983 г`, `образцов целлюлозы`, `Целью работы было исследование генистеина`). TRIM only a fact-free wrapper beside it (`интерес среди исследователей`, `обосновывают целесообразность`). Do not mash the named object into the wrapper. `влияние` + named object is a result. AINL mold only when stacked *and* empty. |
| Канцелярит: verbal-noun stacks, `является` where a direct predicate works | Strong | Actor + verb, or delete. In academic/wire, `является` + named object stays. |
| Formulaic contrast: `не просто X, а Y` with no rejected X | Strong | State the plus, or one claim. Do not swap in `как X, так и Y`. |
| Empty significance, throat-clearing, openers | Strong | Delete, else a fact from the source. |
| Weasel attribution / citation laundering | Strong | Name the source or FLAG. Do not invent the missing study or upgrade a neighboring URL. |
| Brochure repeat: same thesis in adjacent sentences | Strong | MERGE or DELETE the echo. |
| Over-regular grid: equal `##`, 3–5-sentence paragraphs throughout | Strong | Break the skeleton. Keep useful lists; do not mash them into a paragraph. |
| Metadiscourse the input did not contain | Strong | Do not add. Cut injected `следует отметить`, hedge stacks, relationship markers. |
| Numerals dropped from the source | Artifact | Restore unless the whole claim was DELETE. |
| Calque | Strong | Natural Russian; keep domain jargon. |
| Purple prose / fake sensory filler | Strong | Delete. Do not replace with an invented lived detail. |
| Dash, ё, lists, passive, a long sentence | Soft | Leave a useful checklist, an author dash, or ё. Do not *install* these as polish. |
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

The polished piece should read like a person who knows the material and has
a nerve about it:

- stance on the page: reaction, not a balanced briefing;
- emotion attached to the actual claim, not a weather report;
- first person as a reaction (`меня бесит этот поллинг`), not as a fake memoir;
- non-linear path: an aside, a return, unequal sections;
- one or two informal slips: spoken syntax, a slightly crooked agreement, a
  sentence that trails into the next thought.

Do not sprinkle spelling mistakes into names, numbers, code, or links. Do not
add a typo to every paragraph. One crooked sentence in a tight page is enough.

Documentation, tutorials, legal, and academic text skip this recipe unless the
user asks. Sequence, terms, and defined repetition stay.

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

Detector-evasion moves are the same class of stock: replacing ё with е,
injecting typos, mixed-script or homoglyphs. If the user asked for those,
refuse the evasion and still cut water. Collapsing a *useful checklist* to
dodge a detector is evasion. Converting a fake list back into a paragraph
is editing.

## Pass 8: format review

Read `formats-and-artifacts.md`. Tables, lists, links, citations, images, code,
and headings carry meaning and require their own checks. Do not run ordinary
prose substitutions inside protected spans.

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
- article/post register still has stance, a jump or an uneven block, and a
  couple of informal slips;
- protected content is preserved;
- the piece does not sound like the same humanizer output as last time;
- further edits would mostly substitute taste for taste.

Zero lint findings is not the target.

## Output contracts

### Polish

Return the publishable text. Add `Needs verification` only for unresolved
substantive issues. Do not narrate routine changes.

### Audit

Open with the slop call, then the table. No `Вердикт` heading, no
authorship probability, no detector score, no rewrite, no story of how
the draft was written.

Нейрослоп ≠ «написала модель» and ≠ the author's house format. Hashtags,
`Здравствуй, [epithet] читатель` / `Привет, читатель`, author `P.S.`,
outline headings, and operators are KEEP when the draft already uses them.
Do not score a channel template as slop because it repeats.

Нейрослоп is stacked *fill*: brochure grid (`во-первых` / `Как устроено` /
equal blocks), `не просто X, а Y`, fake completeness, empty significance,
unsourced precision, answerer inertia (`Сейчас расскажу, почему`). One
isolated dash, list, or hashtag is not слоп.

Lead sentence, required:

- one draft: `Нейрослоп в наполнении: …` or `Слопа нет: …`;
- many posts: `K из N — нейрослоп в наполнении, потому что [fill]. Каркас KEEP.`

Then:

| Location | Severity | Category | Evidence | Recommended action |
|---|---|---|---|---|

Category is a catalog citation, not a free-text bucket. Write `§N short-name`
from [ai-markers.md](ai-markers.md) (working core §1–16, 2026 classes
§28–38, dataset fills / False slop §39) or the Pass 3 span name
(`Lived-in review`, `News-governance ritual`, `Glued join letter`). Stacked
markers in one span are still one row: cite the strongest `§N`. Do not write
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

Edit the requested file. Report protected-content changes, unresolved issues,
and verification run. Do not paste the whole document unless requested.
