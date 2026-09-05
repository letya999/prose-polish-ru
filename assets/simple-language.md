# Простой язык (craft)

Not «ясный язык» for easy-read audiences. Not a school-grade score.
Craft: the reader gets the thought on the first pass and finishes the page.

Load this on every `light` / `standard` / `deep` / `clean` polish.
Lint codes `Y01`–`Y08` are the regex half. This file is the judgment half.

## What this is not

- Do not strip domain terms, CLI flags, issue numbers, or author operators.
- Do not recast a comparison grid into a monologue.
- Do not chop one thought into four punches to look “simple”.
- Do not overlay slang on already-lived technical voice.
- Do not drop frequency/scope hedges (`нередко`, `оставшуюся`, `в одном
  замере`) or a percent's denominator to look simpler.
- Do not chase Flesch / SMOG / `P < 10%`. Those reward short fragments.

## Eight rules

1. **One thought per sentence.** A second claim after `причем` / `при этом` /
   `в то время как` *may* be a new sentence (`Y04` — inspect; keep if the
   link is earned).
2. **First sentence does the work.** Setup (`Важно отметить`, `Для того чтобы
   понять`, `Ниже рассмотрим`) is TRIM (`Y07`). The claim is the opener.
3. **Actor next to the verb.** `было принято решение` → who decided.
   `в целях обеспечения` → the action (`Y06`).
4. **Short enough to hold.** A running-prose sentence over ~32 words usually
   hides a second thought (`Y01`). Split at the second claim, not at every
   comma. Commands, table cells, and click-paths are KEEP.
5. **No nested maze.** Three of `который` / `чтобы` / `хотя` / `если` /
   `поскольку` in one sentence → flatten (`Y02`).
6. **No self-decode.** `то есть` / `проще говоря` / `иными словами` means the
   first wording failed (`Y05`). Keep the clearer half.
7. **No new riddle.** A metaphor the source did not use, and that needs a
   gloss (`диск общий шина`), is TRIM. An author metaphor already in the
   draft (`мусорка для контекста`) is KEEP.
8. **Finishability.** After a heading, the next sentence must still make
   sense if the reader only skimmed headings. If they cannot retell the
   section in one sentence, the block is not done.

## Before → after

| Buried | Landed |
|---|---|
| Важно отметить, что сабагент, который гидратирует родителя, причем без `close_agent`, жрет квоту | Сабагент с гидратацией родителя жрет квоту. Без `close_agent` слот не освобождается |
| В целях обеспечения изоляции контекста осуществляется запуск в worktree | Запусти отдельный worktree |
| Это не mesh, то есть не P2P, проще говоря очередь | Очередь сообщений, не mesh |
| Он умер как дефолт. Не теория. Просто другой старт | Сабагент больше не дефолт. Это не теория — другой старт сессии |

The last row is the trap: punches look simple and read worse. Join into a
thought, then cut water. Simple ≠ staccato.

## Finish tests (60 seconds)

Do these on after vs before, as text, not as a marker table:

1. Headings + first sentence under each. Name the N cases and their *when*.
2. Cover the rest of a paragraph. Can you still say what it claimed?
3. Retell the piece in three sentences. If you need the marker table to
   remember the point, the prose failed.
4. Semantic diff vs source: no new assertion, no stronger promise. If
   the source marks a versioned change, then and now stay distinct. Do
   not past-tense a current API to look like a generation died.

`scripts/check_readability.py` is the structural half (cards, headings,
tables, punch spike, long-sentence share). These three questions are the
human half. A fail on either is a revert, even if P dropped.

## Lint map

| Code | Signal |
|---|---|
| `Y01` | sentence ≥ 32 words in running prose |
| `Y02` | 3+ subordinate markers in one sentence |
| `Y03` | delayed claim (`Прежде чем перейти`, `Для начала стоит`) |
| `Y04` | two thoughts glued (`причем`, `при этом`, `в то время как`) |
| `Y05` | self-decode (`то есть`, `проще говоря`, `иными словами`) |
| `Y06` | purpose bureaucracy (`в целях`, `посредством`, `с целью обеспечения`) |
| `Y07` | paragraph opens with setup, not the claim |
| `Y08` | two participles or 3+ parentheticals in one sentence |

A lint hit is a prompt to inspect. Do not optimize for zero. Protected
spans, KEEP grids, and source metaphors stay.
