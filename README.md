# prose-polish-ru

Редакционный скилл для русского текста: режет воду, кальки и нейрослоп
в *наполнении*, сохраняет факты, Markdown и авторский каркас (хештег,
приветствие, `P.S.`, операторы). Не детектор авторства и не humanizer
под GPTZero.

Контракт: [`SKILL.md`](SKILL.md). Каталог маркеров:
[`references/ai-markers.md`](references/ai-markers.md). Процедура:
[`references/editorial-procedure.md`](references/editorial-procedure.md).

Установка: `npx skills add . -g -y --skill prose-polish-ru --copy -a grok`

## Датасеты

Корпуса, по которым тюнился каталог. Это источники *классов* слопа
(gazetteer-padding, abstract-mold, span KEEP), не обучающая выборка
для классификатора. Не гонять по ним detector score.

### Русский (приоритет)

| Корпус | Что внутри | Зачем скиллу |
|---|---|---|
| [iitolstykh/LLMTrace_classification](https://huggingface.co/datasets/iitolstykh/LLMTrace_classification) | ~340k RU + ~249k EN, human/AI, 8–9 доменов, GPT-4o, GigaChat, YaGPT, Qwen, Gemini | Живой RU-слоп: wiki-continue, expand-news, отзывы. Бумага: [arXiv:2509.21269](https://arxiv.org/abs/2509.21269) |
| [iitolstykh/LLMTrace_detection](https://huggingface.co/datasets/iitolstykh/LLMTrace_detection) | human / ai / mixed + `ai_char_intervals` (символьные спаны) | Смешанный черновик: KEEP человеческий интервал, REWRITE только слоп-спан |
| [iis-research-team/AINL-Eval-2025](https://huggingface.co/datasets/iis-research-team/AINL-Eval-2025) · [GitHub](https://github.com/iis-research-team/AINL-Eval-2025) | 52k русских научных тезисов, human vs GPT-4-Turbo / Gemma2 / Llama3.3 / DeepSeek-V3 / GigaChat-Lite | Шаблон аннотации: `оказывает существенное влияние`, `перспективный подход`, мало цифр. [arXiv:2508.09622](https://arxiv.org/abs/2508.09622) |
| [RussianNLP/coat](https://huggingface.co/datasets/RussianNLP/coat) · [GitHub](https://github.com/RussianNLP/CoAT) | 246k RU, 13 генераторов, 6 доменов (RuATD → CoAT) | Жанровый сдвиг: парафраз / суммаризация / упрощение vs человек |
| [CoffeBank/Ru-hard-detection-dataset](https://github.com/CoffeBank/Ru-hard-detection-dataset) | Новости, эссе, наука; human / ai / ai+rew (Gemini, GPT-4o-mini, DeepSeek) | Парафраз-слой: слоп после «перепиши» |
| [GigaCheck](https://github.com/ai-forever/gigacheck) | Код + модели на LLMTrace; span localization | Не корпус текстов; ссылка на ту же span-логику. [arXiv:2410.23728](https://arxiv.org/abs/2410.23728) |

Страница LLMTrace: https://sweetdream779.github.io/LLMTrace-info/

### Английский (классы, не токены)

| Корпус | Что внутри | Зачем скиллу |
|---|---|---|
| [Shaib et al. slop](https://github.com/cshaib/slop) | Span-разметка slop по таксономии Density / Templatedness / Factuality / Tone (150 news + 100 QA) | Слоп = качество спана, не «кто писал». [arXiv:2509.19163](https://arxiv.org/abs/2509.19163) |
| [unslop-ai-text](https://github.com/JCarterJohnson/vibecoded-design-tells/tree/main/unslop-ai-text) | Reddit 2021–2026, 7984 on-topic, 600 постов hand-audit, `verified_tally.csv` | Что люди *цитируют* как tell: em dash, `not X but Y`, ритм, sycophancy. Keyword-pass врёт |
| [sam-paech/antislop-sampler](https://github.com/sam-paech/antislop-sampler) | Over-represented phrases (`slop_phrases_*.json`), regex `not just X but Y` | EN fiction/blog fingerprints; в RU смотреть кальку |
| [sam-paech/gemma-3-27b-it-antislop-ftpo-preference-dataset](https://huggingface.co/datasets/sam-paech/gemma-3-27b-it-antislop-ftpo-preference-dataset) | Preference-пары, поле `slop_phrase` / regex | Размеченный нейрослоп на уровне фразы (Elara, negative parallelism) |
| [N8Programs/unslop-good](https://huggingface.co/datasets/N8Programs/unslop-good) | 1k EN «polish this AI passage» | Purple travel/marketing fill |
| [WriteHuman 2026 tells](https://writehuman.ai/blog/ai-tells-in-2026) | 80k humanization pairs: `ensuring`, `rather than`, `plays a crucial role in shaping` | Измеренные EN-формы 2026 |

### Не использовать как учебный слоп-корпус

- [Solenopsisbot/real-slop](https://huggingface.co/datasets/Solenopsisbot/real-slop) — 155k сырых чатов, много NSFW, без разметки слопа.
- Детекторные super-corpus вроде AIvsHuman-SuperCorpus — бинарный human/AI, не span-слоп.

## Как тюнить целиком (не только SKILL.md)

Каталоги — часть скилла. Eval, который пихает в system только `SKILL.md`,
не проверяет, узнаёт ли модель классы из `ai-markers.md`, и все патчи
съезжают в карту. Честный цикл грузит те же файлы, что скилл велел бы
загрузить, и правит *владеющий* файл.

1. Заморозить срез постов/статей (article, story, short_form, factual;
   квоты по типу, без wiki-continue/gazetteer; 8 постов канала как house):
   `python scripts/corpus_eval.py sample --seed 51 --force`
2. Прогнать пакет, не карту:

```powershell
python scripts/corpus_eval.py run --pack audit
# ablation:  --pack map
# heuristics+formats тоже:  --pack full
```

3. `python scripts/corpus_eval.py grade` — спаны против золота **и** какие
   `§N` модель процитировала, плюс линт на том же тексте.
4. Читать `disagreements.md`: у каждого MISS/FP есть `route →` файл.
   Не больше трёх атомарных правок за круг, **по одному файлу**:

| Куда | Когда |
|---|---|
| `SKILL.md` | сломались depth / invocation / output contract / progressive disclosure |
| `references/editorial-procedure.md` | KEEP/TRIM treatment, таблица Pass 3 |
| `references/ai-markers.md` | новый *класс* или False slop; не запрещённое слово |
| `references/heuristics.md` | аргумент, ритм, дикция, голос |
| `references/formats-and-artifacts.md` | Markdown, таблицы, списки, ссылки, код |
| `scripts/lint_text.py` | regex-стабильный fill, который глаз уже назвал |

5. Если линт уже видит класс, а модель KEEP — это miss *узнавания*
   (пакет не доехал / Category без `§N`), а не дыра в каталоге.
6. Тот же срез после патча, потом held-out с новым seed.
   Recall/precision — диагностика, не цель. Не оптимизировать под detector.

Линтер отдельно: `python scripts/lint_text.py --self-test`. То, что линтер
не видит, а глаз видит — новый класс в `ai-markers.md`.

## Прогон скилла по датасету

Модель — Gemini через cliproxy (`ai-stp-cliproxy-1`). Золото —
`ai_char_intervals` из LLMTrace_detection: это *авторство*, не слоп.
Смотрим, совпали ли слоп-спаны, и назвала ли модель класс каталога.

```powershell
python scripts/corpus_eval.py sample
python scripts/corpus_eval.py run --pack audit
python scripts/corpus_eval.py grade
```

Пилот на 2 текстах: `python scripts/corpus_eval.py run --pack audit --limit 2`

`--pack`: `map` (только SKILL.md, evals 2–6) · `audit` (карта + procedure +
ai-markers, default) · `full` (ещё heuristics и formats) · `auto` (audit +
formats, если в черновике Markdown).

Артефакты: `corpus-eval-2/` … `corpus-eval-6/` — map-only;
`corpus-eval-7/` — pack. Перегон: `run --force`.

| Файл | Что внутри |
|---|---|
| `slice.jsonl` | 80 постов/статей: 40 LLMTrace_detection (24 mixed / 8 ai / 8 human) + 32 classification (24 AI / 8 human) + 8 house-постов канала. Домены с квотой: article, story, short_form, factual. AINL только с `--ainl`. House не входит в recall/precision — только §N и treatment |
| `pack-manifest.json` | какие файлы уехали в system prompt |
| `runs/<id>/audit.md` | ответ модели |
| `runs/<id>/spans.json` | KEEP/TRIM/REWRITE/DELETE/FLAG + offsets |
| `span-agreement.json` | recall/precision по символам + cited `§N` |
| `catalog-usage.json` | какие секции каталога модель назвала |
| `disagreements.md` | MISS/FP + `route →` файл |

Как читать `disagreements.md`:

- **MISS** — золото сказало «тут AI», скилл оставил KEEP. Либо дыра в каталоге, либо золото разметило нормальный кусок как AI, либо модель не увидела уже описанный класс.
- **FP** — золото сказало «человек», скилл пометил слоп. Либо ложный вызов (False slop), либо золото пропустило слоп.
- **Catalog usage** — доля ответов с `§N`. Ноль при `--pack audit` значит, что цитирование классов не работает.
- Не поднимать precision, сваливая KEEP-примеры в `SKILL.md`.

Нужен docker-контейнер `ai-stp-litellm-1` (он ходит на `http://cliproxy:8317`). Модель по умолчанию `gemini-3.6-flash-high`.
