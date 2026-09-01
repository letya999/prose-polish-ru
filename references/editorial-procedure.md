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

## Pass 4: semantic repair

### Unsupported certainty

Match wording to evidence:

- observed once → `в этом случае`, not `всегда`;
- community anecdotes → `часть разработчиков сообщает`, not `сообщество решило`;
- association → `связано`, not automatically `вызвало`;
- benchmark → state setup and limits before generalizing;
- plausible mechanism → mark as inference unless sourced.

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
- Use correct Russian typography; punctuation is not an authorship marker.
- Keep author operators (`==`, `=>`, `->`, `vs`) when they mark identity,
  implication, or comparison.

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

Use columns:

| Location | Severity | Category | Evidence | Recommended action |
|---|---|---|---|---|

Severity:

- critical: factual corruption, contradiction, fabricated evidence;
- high: unsupported conclusion, missing thesis, broken artifact;
- medium: repetition, structural monotony, unclear paragraph;
- low: local wording or rhythm opportunity.

### File edit

Edit the requested file. Report protected-content changes, unresolved issues,
and verification run. Do not paste the whole document unless requested.
