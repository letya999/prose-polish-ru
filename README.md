# prose-polish-ru

Редакционный скилл и жёсткий хуманизатор для русского текста. Вход —
тезисы, сгенерированный черновик или готовый авторский текст. Процесс:
авторские тезисы → проверенные утверждения → связный текст → проверка
результата.

По просьбе написать или отредактировать — делает работу. По просьбе
оценить — аудит. Без глагола — карточка `score`. Режет воду, кальки и
нейрослоп в *наполнении*. На статье/посте обязателен Pass H: авторский
стиль, лёгкие опечатки и шероховатость, косноязычие, эмоциональность и
категоричность. Сохраняет защищённые спаны (имена, код, URL). Число из
черновика — не факт, пока его не проверили. Не выдумывает процент
GPTZero без скана. P(нейрослоп) — оценка наполнения, не P(написала модель).

Контракт: [`SKILL.md`](SKILL.md). Каталог маркеров:
[`references/ai-markers.md`](references/ai-markers.md). Процедура:
[`references/editorial-procedure.md`](references/editorial-procedure.md).

Установка: `npx skills add . -g -y --skill prose-polish-ru --copy -a "*"`

## Датасеты

Корпуса, по которым тюнился каталог. Это источники *классов* слопа
(gazetteer-padding, abstract-mold, span KEEP), не обучающая выборка
для классификатора. Не гонять по ним detector score.

### Русский (приоритет)

| Корпус | Что внутри | Зачем скиллу |
|---|---|---|
| [iitolstykh/LLMTrace_classification](https://huggingface.co/datasets/iitolstykh/LLMTrace_classification) | ~340k RU + ~249k EN, human/AI, 8–9 доменов, GPT-4o, GigaChat, YaGPT, Qwen, Gemini | Живой RU-слоп: wiki-continue, expand-news, отзывы. Бумага: [arXiv:2509.21269](https://arxiv.org/abs/2509.21269) |
| [iitolstykh/LLMTrace_detection](https://huggingface.co/datasets/iitolstykh/LLMTrace_detection) | human / ai / mixed + `ai_char_intervals` (символьные спаны) | Смешанный черновик: KEEP полезный факт, не «человеческий интервал». Авторство ≠ качество |
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
   Сто постов канала: `python scripts/corpus_eval.py sample --house-only --n 100 --force`
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
| `references/editorial-procedure.md` | KEEP/TRIM treatment, таблица Pass 3, точность выше голоса |
| `references/ai-markers.md` | новый *класс* или False slop; не запрещённое слово |
| `references/heuristics.md` | аргумент, ритм, дикция, голос |
| `references/formats-and-artifacts.md` | Markdown, таблицы, списки, ссылки, код |
| `scripts/lint_text.py` | regex-стабильный fill + простой язык `Y01`–`Y08` + подписи `F42` |
| `scripts/check_readability.py` | before/after скан: карточки, заголовки, таблицы, рубленые удары, длинные фразы. Не Флеш |
| `assets/simple-language.md` | ремесло простого языка: одна мысль, первое предложение работает. Не «ясный язык» |

5. Если линт уже видит класс, а модель KEEP — сначала смотреть, не
   ложный ли это вызов линтера. Иначе miss узнавания (пакет не доехал /
   Category без `§N`), а не дыра в каталоге.
6. Тот же срез после патча. Held-out — отдельный замороженный срез, не
   «тот же sample с новым seed»: новый seed сам по себе не гарантирует
   непересечение. Recall/precision по `ai_char_intervals` — диагностика
   авторского перекрытия, не оценка качества правки.

Линтер отдельно: `python scripts/lint_text.py --self-test`. Отсутствие
`§N` в ответе — проблема формата отчёта, не доказательство, что правило
не применили. «Линтер видит, модель KEEP» не значит, что ошиблась модель:
линтер тоже ошибается.

## Прогон скилла по датасету

Модель и прокси задаются переменными `PROSE_POLISH_MODEL`,
`PROSE_POLISH_LITELLM_CONTAINER`, `PROSE_POLISH_CLIPROXY_URL`
(по умолчанию Gemini через cliproxy в контейнере `ai-stp-litellm-1`).
Золото `ai_char_intervals` — *авторство*, не слоп и не качество правки.
Хороший ИИ-фрагмент, оставленный KEEP, не обязан быть FN. Плохой
человеческий фрагмент, правильно срезанный, не обязан быть FP.

Три группы проверки (авторство — только диагностика):

1. **Контрольные искажения** — `check_preservation.py --self-test`,
   `check_readability.py --self-test`, `lint_text.py --self-test`:
   убрана оговорка, переставлены числа, сломан URL, карточки vs таблица.
2. **Полный редакторский прогон** — `corpus_eval.py run --mode polish`
   (тезисы или черновик → текст). Нужна отдельная редакторская разметка
   (`editorial_spans`: проблема, тип, что менять, что сохранить).
3. **Слепое сравнение** — исходник / обычная генерация / скилл; люди из
   аудитории. «Неотличим от человека» так и проверяется, не одним процентом.

Рабочие критерии приёмки: существенные факты проверены или ограничены;
не добавлены новые неподтверждённые обещания; читатель понимает тезис и
находит действие; голос узнаваем, на статье/посте есть шероховатость и
позиция, без выдуманного опыта.

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

Контейнер, URL и модель — через `PROSE_POLISH_*` (см. выше). Пропуск
готового `spans.json` срабатывает только если совпал fingerprint текста,
пакета, промпта и модели. `run` возвращает 0 только если все кейсы ок;
частичный прогон — код 1.

`assets/simple-language.md` и `agents/openai.yaml` входят в пакет.
