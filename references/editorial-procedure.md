# Editorial procedure

## Objective

Make the draft more useful per word. Preserve truth, intended meaning, genre,
working formatting, and individual voice. Humanization is a side effect of good
editing, not a claim about authorship.

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

If no context is supplied, default to standard polish for an informed general
reader. Keep the existing structure unless it is the source of the problem.

## Pass 1: protected-content inventory

Record before editing:

- numerals, dates, percentages, ranges, currencies, units, versions;
- proper names, organizations, products, models, APIs, standards;
- URLs, link destinations, citation keys, footnotes;
- direct quotations and attributed paraphrases;
- fenced code, inline code, commands, flags, paths, identifiers;
- formulas and table values;
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

If the answers cannot be recovered, flag the gap. Smoother syntax must not make
an incoherent draft sound authoritative.

## Pass 3: classify blocks

Assign exactly one primary action:

| Action | Use when | Result |
|---|---|---|
| KEEP | Clear, useful, accurate, in register | Preserve it |
| TRIM | Useful core surrounded by padding | Remove padding |
| MERGE | Repeats or completes a neighbor | Build one stronger block |
| MOVE | Useful but interrupts the argument | Place at point of need |
| REWRITE | Function is needed but wording or logic fails | Rebuild from supported content |
| DELETE | No distinct function | Remove |
| FLAG | Needs facts, attribution, or author intent | Preserve cautiously and disclose |

Do not rewrite a `KEEP` block to make the edit look comprehensive.

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

### Fabricated texture

Delete invented clients, incidents, emotions, quotes, timelines, and first-person
experience. If a useful personal slot is missing, leave it absent or ask for a
real example; never manufacture authenticity.

## Pass 5: structural repair

### Emphasis map

Choose one to three centers of gravity. Give them more evidence and space.
Compress supporting material. Equal section length is not a quality target.

### Paragraph contract

Each paragraph should perform one dominant job:

- claim;
- mechanism;
- evidence;
- example;
- consequence;
- objection;
- limitation;
- transition that changes direction.

A paragraph that merely announces, praises, or summarizes nearby material is
usually removable.

### Order

Prefer need-based ordering:

- claim near the evidence it depends on;
- term immediately before first necessary use;
- caveat beside the claim it limits;
- example after the abstraction it clarifies, unless a concrete opening is the
  deliberate hook;
- recommendation after mechanism and constraints.

### Introduction

Remove ceremonial context, universal history, and a table of contents written as
prose. Keep enough to establish problem, angle, stakes, and reader promise.

### Ending

Do not restate the whole piece. Land on implication, decision, boundary,
practical next step, or a genuinely earned final observation.

## Pass 6: compression

Delete in this order:

1. Duplicate claims.
2. Meta-commentary about the text.
3. Empty importance and relevance claims.
4. Definitions the audience does not need.
5. Examples that prove nothing new.
6. Repeated qualifiers with the same scope.
7. Parentheticals that belong in the sentence or nowhere.
8. Decorative adjectives and abstract nouns.
9. Redundant transitions.
10. Conclusion echoes.

Compression target is functional, not numeric. Do not shorten a dense technical
explanation merely to produce a lower word count.

## Pass 7: language and rhythm

- Prefer a concrete actor and verb when the actor matters.
- Keep passive voice when the actor is unknown, irrelevant, or deliberately
  backgrounded.
- Vary sentence shape in response to thought, not randomly.
- Join artificial staccato; split overloaded multi-claim sentences.
- Preserve deliberate fragments, repetition, and long sentences when they carry
  voice or emphasis.
- Replace translated business English with natural Russian where terminology is
  not domain-standard.
- Keep accepted professional slang for the intended audience.
- Use correct Russian typography; punctuation is not an authorship marker.

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

- every retained block has a distinct function;
- no material contradiction or unsupported escalation remains hidden;
- obvious water and duplicated reasoning are gone;
- remaining markers are contextual choices;
- protected content is preserved;
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
