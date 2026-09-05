#!/usr/bin/env python3
"""Run prose-polish-ru against a frozen LLMTrace slice and check span markup.

One path, three commands:

    python scripts/corpus_eval.py sample
    python scripts/corpus_eval.py run --pack audit
    python scripts/corpus_eval.py grade

sample  — 80 RU posts/articles: LLMTrace article, story, short_form, factual
          with per-type quotas; skips wiki-continue, gazetteer ledes, poetry,
          abstracts, and (by default) AINL. Optional house posts from the
          channel dump (no authorship gold — treatments only).
          --mix-public: 100 each from LLMTrace detection, classification,
          AINL abstracts, CoAT, and Ru-hard (essay/news/science).
run     — send each text to cliproxy with the skill *pack* stuffed into the
          system prompt (not SKILL.md alone). Model returns an audit table
          plus char-offset spans.
grade   — compare spans to gold `ai_char_intervals`, parse catalog citations
          from the audit table, overlay lint, and route disagreements to the
          file that owns the class.

Packs:
    map    SKILL.md only (ablation; old evals 2–6)
    audit  SKILL.md + procedure + ai-markers  (default; what audit loads)
    full   whole pack, including heuristics and formats
    auto   audit pack + formats when the draft has Markdown structure

Authorship gold (`ai_char_intervals`) is not editorial quality. A good
AI span left KEEP is not a miss; a bad human span correctly TRIM-ed is
not a false positive. When a row has `editorial_spans`, grade those.
Otherwise report authorship-overlap as a diagnostic, not as skill quality.

Control distortions (hedge drop, number swap, URL change) belong to
scripts/check_preservation.py --self-test, not to this authorship overlap.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "prose-polish-ru-workspace" / "corpus-eval-14"
REFS = ROOT / "references"
PACK_CHOICES = ("map", "audit", "full", "auto")
POST_TYPES = {"article", "story", "short_form", "factual"}
WIKI_CONTINUE = re.compile(r"^\s*Продолжи текст\s*:", re.I)
WIKI_PROMPT = re.compile(r"Продолжи текст\s*:|Раскрой тему|в стиле (?:статьи )?Википеди", re.I)
GAZETTEER = re.compile(
    r"(?:протекает по|устье реки находится|исполнительная ветвь|"
    r"родивш(?:ийся|аяся) в д\.|— село[,\s]|входит в .{0,40}сельск|"
    r"список народно-освободительных|небольшое село, расположенн)",
    re.I,
)
HOUSE_FILE = ROOT / "prose-polish-ru-workspace" / "tg_last100.json"
HF_CACHE = ROOT / "prose-polish-ru-workspace" / "hf-cache"
HOUSE_MIN_CHARS = 1
HOUSE_MAX_CHARS = 8000
FRAME_HASHTAG = re.compile(r"^#\S+", re.M)
FRAME_GREET = re.compile(r"Здравствуй[^\n]{0,80}читател", re.I)
FRAME_PS = re.compile(r"(?m)^\s*P\.S\.S?\b")
PACK_FILES = {
    "map": ["SKILL.md"],
    "audit": [
        "SKILL.md",
        "references/editorial-procedure.md",
        "references/ai-markers.md",
    ],
    "full": [
        "SKILL.md",
        "references/editorial-procedure.md",
        "references/ai-markers.md",
        "references/heuristics.md",
        "references/formats-and-artifacts.md",
    ],
}
HF_ROWS = "https://datasets-server.huggingface.co/rows"
DET = "iitolstykh/LLMTrace_detection"
CLF = "iitolstykh/LLMTrace_classification"
AINL = "iis-research-team/AINL-Eval-2025"
COAT = "RussianNLP/coat"
RUHARD_RAW = (
    "https://raw.githubusercontent.com/CoffeBank/Ru-hard-detection-dataset/main/"
)
RUHARD_FILES = (
    ("essay", "human", "main/essay/original_essay.json"),
    ("essay", "ai", "main/essay/generated_essays.json"),
    ("essay", "ai+rew", "main/essay/paraphrased_essays.json"),
    ("news", "human", "main/news/original_news.json"),
    ("news", "ai", "main/news/generated_news.json"),
    ("news", "ai+rew", "main/news/paraphrased_news.json"),
    ("scientific", "human", "main/scientific_texts/orig_scientific.json"),
    ("scientific", "ai", "main/scientific_texts/generated_scientific.json"),
    ("scientific", "ai+rew", "main/scientific_texts/paraphrased_scientific.json"),
)
HF_SPLIT = "test"
MIX_PER_SOURCE = 100
DATA_TYPES = POST_TYPES
MIN_CHARS = 400
MAX_CHARS = int(os.environ.get("PROSE_POLISH_MAX_CHARS", "12000"))
QUOTA_DET = {"mixed": 24, "ai": 8, "human": 8}
QUOTA_CLF = {"ai": 24, "human": 8}
QUOTA_HOUSE = 8
QUOTA_AINL = {"human": 8, "ai": 8}
TYPE_QUOTA_DET = {"article": 12, "short_form": 8, "story": 10, "factual": 10}
TYPE_QUOTA_CLF = {"article": 12, "short_form": 6, "story": 8, "factual": 6}
CLIPROXY_MODEL = os.environ.get("PROSE_POLISH_MODEL", "gemini-3.6-flash-high")
LITELLM_CONTAINER = os.environ.get("PROSE_POLISH_LITELLM_CONTAINER", "ai-stp-litellm-1")
CLIPROXY_URL = os.environ.get(
    "PROSE_POLISH_CLIPROXY_URL", "http://cliproxy:8317/v1/chat/completions"
)
CLIPROXY_KEY = os.environ.get("PROSE_POLISH_CLIPROXY_KEY", "sk-none")
UA = "prose-polish-ru-corpus-eval"

DOCKER_POST = r"""
import json, sys, urllib.request, urllib.error
payload = sys.stdin.buffer.read()
req = urllib.request.Request(
    "URL",
    data=payload,
    headers={
        "Authorization": "Bearer KEY",
        "Content-Type": "application/json",
    },
)
try:
    with urllib.request.urlopen(req, timeout=180) as resp:
        sys.stdout.buffer.write(resp.read())
except urllib.error.HTTPError as exc:
    sys.stderr.buffer.write(exc.read() or str(exc).encode())
    sys.exit(exc.code or 1)
""".replace("URL", CLIPROXY_URL).replace("KEY", CLIPROXY_KEY)

SPAN_SCHEMA = """\
После таблицы аудита верни РОВНО один JSON-блок в ограде ```json ... ```.
Никакого текста после закрывающей ограды.

Схема:
{
  "spans": [
    {
      "start": 0,
      "end": 81,
      "action": "KEEP",
      "quote": "первые слова спана",
      "why": "кратко"
    }
  ]
}

Правила JSON:
- start/end — смещения в Unicode-символах исходного черновика, полуинтервал [start, end).
- Спаны не пересекаются, идут по возрастанию start, в сумме покрывают весь черновик.
- action: KEEP | TRIM | REWRITE | DELETE | FLAG.
- KEEP = полезный факт или живой кусок: числа, даты, имена, суммы, URL; отзыв; цитата; UI-клики; благодарность; определение; сленг; суд/полиция; спорт play-by-play; тикет с `>`; синдром+мутация. Не «человеческий интервал датасета» и не непроверенное утверждение.
- TRIM/REWRITE/DELETE = слоп, вода, заикание, n+заглавная, пустая значимость, review-sandwich, AINL-молд без результата — даже если датасет пометил спан human.
- FLAG = нужна проверка, не слоп сам по себе.
- Не ставь P(AI). Не пиши «Вердикт». Не оценивай авторство.
- quote — дословный кусок черновика, не длиннее 80 символов.
- why — `§N class; treatment`. Для слопа treatment = delete | source-fact | simpler
  сразу после точки с запятой. Для KEEP = keep. Не свободный ярлык и не синоним.
"""


def out_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    (path / "runs").mkdir(exist_ok=True)
    return path


def hf_get(dataset: str, offset: int, length: int = 100, split: str = HF_SPLIT) -> dict:
    query = urllib.parse.urlencode(
        {
            "dataset": dataset,
            "config": "default",
            "split": split,
            "offset": offset,
            "length": length,
        }
    )
    req = urllib.request.Request(
        f"{HF_ROWS}?{query}",
        headers={"User-Agent": UA},
    )
    with urllib.request.urlopen(req, timeout=45) as resp:
        return json.loads(resp.read().decode("utf-8"))


def usable_trace(row: dict, labels: set[str], min_chars: int = MIN_CHARS) -> bool:
    if row.get("lang") != "ru":
        return False
    if row.get("label") not in labels:
        return False
    if row.get("data_type") not in DATA_TYPES:
        return False
    prompt = (row.get("prompt") or "").strip()
    if WIKI_CONTINUE.match(prompt) or WIKI_PROMPT.search(prompt):
        return False
    text = row.get("text") or ""
    if not (min_chars <= len(text) <= MAX_CHARS):
        return False
    return not GAZETTEER.search(text[:400])


def clamp_intervals(text: str, raw) -> list[list[int]]:
    n = len(text)
    out: list[list[int]] = []
    for item in raw or []:
        if not isinstance(item, (list, tuple)) or len(item) < 2:
            continue
        start, end = int(item[0]), int(item[1])
        start = max(0, min(start, n))
        end = max(start, min(end, n))
        if end > start:
            out.append([start, end])
    return out


def pack_row(
    prefix: str,
    index: int,
    source: str,
    row: dict,
    text: str,
    label: str,
    intervals: list[list[int]],
    extra: dict | None = None,
) -> dict:
    extra = extra or {}
    packed = {
        "id": f"{prefix}-{index:02d}",
        "source": source,
        "split": extra.get("split") or HF_SPLIT,
        "lang": "ru",
        "label": label,
        "model": row.get("model") or row.get("ainl_label"),
        "data_type": extra.get("data_type") or row.get("data_type"),
        "prompt_type": row.get("prompt_type"),
        "topic_id": row.get("topic_id"),
        "text": text,
        "ai_char_intervals": intervals,
        "n_chars": len(text),
        "n_ai_chars": sum(e - s for s, e in intervals),
    }
    if extra.get("split") == "channel":
        packed["tg_id"] = extra.get("tg_id") or row.get("id")
        packed["date"] = extra.get("date")
    return packed


def trace_jsonl(dataset: str, split: str = HF_SPLIT) -> Path:
    from huggingface_hub import hf_hub_download

    HF_CACHE.mkdir(parents=True, exist_ok=True)
    path = hf_hub_download(
        repo_id=dataset,
        filename=f"{split}.jsonl",
        repo_type="dataset",
        cache_dir=str(HF_CACHE),
    )
    return Path(path)


def sample_trace(
    dataset: str,
    quota: dict[str, int],
    rng: random.Random,
    id_prefix: str,
    need_intervals: bool,
    type_quota: dict[str, int] | None = None,
) -> tuple[list[dict], int]:
    path = trace_jsonl(dataset)
    labels = set(quota)
    pool: dict[str, list[dict]] = {k: [] for k in quota}
    scanned = 0
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            scanned += 1
            row = json.loads(line)
            if not usable_trace(row, labels):
                continue
            label = row["label"]
            data_type = row.get("data_type")
            if type_quota is not None and data_type not in type_quota:
                continue
            pool[label].append(row)
    got: dict[str, list[dict]] = {k: [] for k in quota}
    type_got: dict[str, int] = {k: 0 for k in (type_quota or {})}
    mixed = [row for items in pool.values() for row in items]
    rng.shuffle(mixed)
    for row in mixed:
        label = row["label"]
        if len(got[label]) >= quota[label]:
            continue
        data_type = row.get("data_type")
        if type_quota is not None and type_got[data_type] >= type_quota[data_type]:
            continue
        text = row["text"]
        if need_intervals:
            intervals = clamp_intervals(text, row.get("ai_char_intervals"))
            if label == "human":
                intervals = []
            elif label == "ai" and not intervals:
                intervals = [[0, len(text)]]
        else:
            intervals = [] if label == "human" else [[0, len(text)]]
        got[label].append(
            pack_row(
                f"{id_prefix}-{label}",
                len(got[label]) + 1,
                dataset,
                row,
                text,
                label,
                intervals,
            )
        )
        if type_quota is not None:
            type_got[data_type] += 1
        if all(len(got[k]) >= n for k, n in quota.items()):
            break
    rows = [item for label in quota for item in got[label]]
    return rows, scanned


def sample_house(
    rng: random.Random,
    n: int = QUOTA_HOUSE,
    chronological: bool = False,
    dump: Path | None = None,
) -> list[dict]:
    path = dump or HOUSE_FILE
    if n <= 0 or not path.exists():
        if n > 0:
            print(f"house dump missing: {path}", file=sys.stderr)
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    pool = []
    for item in payload.get("last") or payload.get("posts") or []:
        text = (item.get("text") or "").strip()
        if HOUSE_MIN_CHARS <= len(text) <= HOUSE_MAX_CHARS:
            pool.append(item)
    if not chronological:
        rng.shuffle(pool)
    out = []
    for i, item in enumerate(pool[:n], 1):
        text = (item.get("text") or "").strip()
        out.append(
            pack_row(
                "house",
                i,
                path.stem,
                item,
                text,
                "house",
                [],
                extra={
                    "data_type": "short_form",
                    "split": "channel",
                    "tg_id": item.get("id"),
                    "date": item.get("date"),
                },
            )
        )
    return out


def sample_ainl(
    rng: random.Random, quota: dict[str, int] | None = None
) -> list[dict]:
    quota = quota or QUOTA_AINL
    try:
        from huggingface_hub import hf_hub_download
    except ImportError:
        print("huggingface_hub missing; skip AINL", file=sys.stderr)
        return []
    filename = "train.csv" if max(quota.values()) > 16 else "dev_full.csv"
    path = Path(
        hf_hub_download(
            repo_id=AINL,
            filename=filename,
            repo_type="dataset",
            cache_dir=str(HF_CACHE),
        )
    )
    import csv

    oversample = max(quota.values()) * 8
    buckets: dict[str, list[dict]] = {"human": [], "ai": []}
    with path.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            text = (row.get("text") or "").strip()
            raw_label = (row.get("label") or "").strip().lower()
            if not (200 <= len(text) <= MAX_CHARS):
                continue
            if raw_label in {"human", "abstract"}:
                kind = "human"
            elif raw_label in {"unknown", ""}:
                continue
            else:
                kind = "ai"
            if len(buckets[kind]) >= oversample:
                continue
            buckets[kind].append(
                {
                    "text": text,
                    "ainl_label": raw_label,
                    "data_type": "abstract",
                    "label": kind,
                }
            )
            if all(len(buckets[k]) >= oversample for k in buckets):
                break
    out: list[dict] = []
    for kind, need in quota.items():
        pool = buckets[kind]
        rng.shuffle(pool)
        for i, row in enumerate(pool[:need], 1):
            text = row["text"]
            intervals = [] if kind == "human" else [[0, len(text)]]
            out.append(
                pack_row(
                    f"ainl-{kind}",
                    i,
                    AINL,
                    row,
                    text,
                    kind,
                    intervals,
                    extra={"data_type": "abstract", "split": filename},
                )
            )
    return out


def sample_coat(rng: random.Random, n: int = MIX_PER_SOURCE) -> list[dict]:
    try:
        from huggingface_hub import hf_hub_download
        import pandas as pd
    except ImportError as exc:
        print(f"coat deps missing: {exc}", file=sys.stderr)
        return []
    path = Path(
        hf_hub_download(
            repo_id=COAT,
            filename="authorship/validation-00000-of-00001.parquet",
            repo_type="dataset",
            cache_dir=str(HF_CACHE),
        )
    )
    frame = pd.read_parquet(path, columns=["text", "label"])
    need_h, need_a = n // 2, n - n // 2
    buckets: dict[str, list[tuple[str, str]]] = {"human": [], "ai": []}
    for text, raw in zip(frame["text"].tolist(), frame["label"].tolist()):
        text = ("" if text is None else str(text)).strip()
        if not (40 <= len(text) <= MAX_CHARS):
            continue
        kind = "human" if str(raw).lower() == "human" else "ai"
        buckets[kind].append((text, str(raw)))
    out: list[dict] = []
    for kind, need in (("human", need_h), ("ai", need_a)):
        pool = buckets[kind]
        pool.sort(key=lambda item: -len(item[0]))
        pool = pool[: max(need * 3, need)]
        rng.shuffle(pool)
        for i, (text, raw) in enumerate(pool[:need], 1):
            intervals = [] if kind == "human" else [[0, len(text)]]
            row = {"text": text, "model": None if kind == "human" else raw}
            out.append(
                pack_row(
                    f"coat-{kind}",
                    i,
                    COAT,
                    row,
                    text,
                    kind,
                    intervals,
                    extra={"data_type": "short_form", "split": "authorship/validation"},
                )
            )
    return out


def _download_ruhard(rel: str) -> Path:
    dest = HF_CACHE / "ruhard" / rel.replace("/", "__")
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.stat().st_size > 100:
        return dest
    url = RUHARD_RAW + rel
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as resp:
        dest.write_bytes(resp.read())
    return dest


def sample_ruhard(rng: random.Random, n: int = MIX_PER_SOURCE) -> list[dict]:
    kind_need = {"human": n // 2, "ai": n // 4, "ai+rew": n - n // 2 - n // 4}
    pools: dict[str, list[tuple[str, dict]]] = {k: [] for k in kind_need}
    for genre, kind, rel in RUHARD_FILES:
        try:
            payload = json.loads(_download_ruhard(rel).read_text(encoding="utf-8"))
        except (OSError, urllib.error.URLError, json.JSONDecodeError) as exc:
            print(f"ruhard skip {rel}: {exc}", file=sys.stderr)
            continue
        cap = 4000 if genre == "scientific" else MAX_CHARS
        for item in payload:
            text = (item.get("text") or "").strip()
            if 200 <= len(text) <= cap:
                pools[kind].append((genre, item))
    out: list[dict] = []
    for kind, need in kind_need.items():
        bag = pools[kind]
        rng.shuffle(bag)
        gold_label = "human" if kind == "human" else "ai"
        prefix = f"ruhard-{kind.replace('+', '')}"
        for i, (genre, item) in enumerate(bag[:need], 1):
            text = (item.get("text") or "").strip()
            intervals = [] if gold_label == "human" else [[0, len(text)]]
            data_type = "article" if genre != "news" else "news"
            out.append(
                pack_row(
                    prefix,
                    i,
                    "CoffeBank/Ru-hard-detection-dataset",
                    {"text": text, "model": item.get("model") or item.get("source")},
                    text,
                    gold_label,
                    intervals,
                    extra={"data_type": data_type, "split": f"{genre}/{kind}"},
                )
            )
    return out


def cmd_sample(args: argparse.Namespace) -> int:
    dest = out_dir(args.out)
    slice_path = dest / "slice.jsonl"
    if slice_path.exists() and not args.force:
        print(f"exists: {slice_path} (pass --force to resample)", file=sys.stderr)
        return 0
    rng = random.Random(args.seed)
    if args.house_only:
        n = args.n or 100
        house = sample_house(
            rng, n=n, chronological=True, dump=args.house_file or HOUSE_FILE
        )
        rows = house
        with slice_path.open("w", encoding="utf-8") as fh:
            for item in rows:
                fh.write(json.dumps(item, ensure_ascii=False) + "\n")
        print(
            f"wrote {len(rows)} house posts → {slice_path} "
            f"(channel dump, chronological, seed unused, n {n})"
        )
        return 0 if len(rows) >= 20 else 1
    if args.mix_public:
        n = args.n or MIX_PER_SOURCE
        half, quarter = n // 2, n // 4
        det, n_det = sample_trace(
            DET,
            {"mixed": half, "ai": quarter, "human": n - half - quarter},
            rng,
            "det",
            need_intervals=True,
        )
        clf, n_clf = sample_trace(
            CLF,
            {"ai": n - n // 4, "human": n // 4},
            rng,
            "clf",
            need_intervals=False,
        )
        ainl = sample_ainl(rng, {"human": n // 2, "ai": n - n // 2})
        coat = sample_coat(rng, n)
        ruhard = sample_ruhard(rng, n)
        rows = det + clf + ainl + coat + ruhard
        with slice_path.open("w", encoding="utf-8") as fh:
            for item in rows:
                fh.write(json.dumps(item, ensure_ascii=False) + "\n")
        types = {}
        sources = {}
        for item in rows:
            types[item.get("data_type")] = types.get(item.get("data_type"), 0) + 1
            sources[item.get("source")] = sources.get(item.get("source"), 0) + 1
        print(
            f"wrote {len(rows)} rows → {slice_path} "
            f"(det {len(det)}/{n_det}, clf {len(clf)}/{n_clf}, "
            f"ainl {len(ainl)}, coat {len(coat)}, ruhard {len(ruhard)}, "
            f"sources {sources}, types {types}, seed {args.seed}, n {n})"
        )
        return 0 if len(rows) >= n * 3 else 1
    det, n_det = sample_trace(
        DET, QUOTA_DET, rng, "det", need_intervals=True, type_quota=TYPE_QUOTA_DET
    )
    clf, n_clf = sample_trace(
        CLF, QUOTA_CLF, rng, "clf", need_intervals=False, type_quota=TYPE_QUOTA_CLF
    )
    ainl = sample_ainl(rng) if args.ainl else []
    house = sample_house(rng) if args.house else []
    rows = det + clf + ainl + house
    with slice_path.open("w", encoding="utf-8") as fh:
        for item in rows:
            fh.write(json.dumps(item, ensure_ascii=False) + "\n")
    types = {}
    for item in rows:
        types[item.get("data_type")] = types.get(item.get("data_type"), 0) + 1
    print(
        f"wrote {len(rows)} rows → {slice_path} "
        f"(det {len(det)}/{n_det}, clf {len(clf)}/{n_clf}, ainl {len(ainl)}, "
        f"house {len(house)}, types {types}, seed {args.seed})"
    )
    return 0 if len(rows) >= 40 else 1


def load_slice(path: Path) -> list[dict]:
    rows = []
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def draft_needs_formats(text: str) -> bool:
    return bool(
        re.search(r"```|^\|.+\|.*$|^#{1,6}\s|\[[^\]]+\]\([^)]+\)|^[-*+]\s", text, re.M)
    )


def resolve_pack_files(pack: str, text: str = "") -> list[str]:
    if pack == "auto":
        files = list(PACK_FILES["audit"])
        if draft_needs_formats(text):
            files.append("references/formats-and-artifacts.md")
        return files
    if pack not in PACK_FILES:
        raise ValueError(f"unknown pack {pack!r}")
    return list(PACK_FILES[pack])


def read_pack(files: list[str]) -> str:
    parts = []
    for rel in files:
        body = (ROOT / rel).read_text(encoding="utf-8")
        parts.append(f"<!-- {rel} -->\n{body.rstrip()}\n")
    return "\n---\n".join(parts)


def skill_system_prompt(
    pack: str = "audit",
    text: str = "",
    mode: str = "audit",
) -> tuple[str, list[str]]:
    files = resolve_pack_files(pack, text)
    if mode == "polish":
        extra = (
            "\n\n---\nТы выполняешь $prose-polish-ru в режиме standard.\n"
            "Проверь утверждения, затем отредактируй. Верни текст, затем "
            "JSON спанов. Не выдумывай факты.\n"
        )
    else:
        extra = (
            "\n\n---\nТы выполняешь $prose-polish-ru в режиме audit.\n"
            "Не переписывай черновик. Сначала таблица аудита, затем JSON спанов.\n"
            "В колонке Category цитируй класс каталога как `§N` "
            "(номер секции ai-markers) или имя спана из procedure Pass 3.\n"
            "Не изобретай свободный ярлык вместо §N.\n"
            "Recommended action: delete, иначе факт из черновика, иначе проще. "
            "Синоним не лечение. FLAG — непроверенное утверждение, не слоп.\n"
        )
    return read_pack(files) + extra, files


def user_prompt(text: str, mode: str = "audit") -> str:
    if mode == "polish":
        lead = (
            "Use $prose-polish-ru in standard mode. Check claims, then edit.\n"
            "Return the polished text, then Skill gaps, then the JSON spans.\n"
        )
    else:
        lead = (
            "Use $prose-polish-ru in audit mode. Do not rewrite.\n"
            "This run iterates the skill pack (SKILL.md + catalogs) on a post/article. "
            "After the table add Skill gaps: each missed class as `§N` plus one rule. "
            "If nothing missed, write `Skill gaps: none`.\n"
            "For each slop row the recommended action is delete, a fact already "
            "in the draft, or a simpler rewrite — not a synonym. FLAG is not slop.\n"
        )
    return (
        lead
        + "\n"
        + SPAN_SCHEMA
        + "\nЧерновик:\n<<<\n"
        + text
        + "\n>>>\n"
    )


def pack_manifest(pack: str, files: list[str], model: str) -> dict:
    bytes_map = {rel: (ROOT / rel).stat().st_size for rel in files}
    chars_map = {
        rel: len((ROOT / rel).read_text(encoding="utf-8")) for rel in files
    }
    hashes = {
        rel: hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()[:16]
        for rel in files
    }
    return {
        "pack": pack,
        "files": files,
        "chars": sum(chars_map.values()),
        "bytes_total": sum(bytes_map.values()),
        "bytes": bytes_map,
        "chars_by_file": chars_map,
        "sha256_16": hashes,
        "model": model,
    }


def run_fingerprint(text: str, files: list[str], model: str, prompt: str) -> str:
    h = hashlib.sha256()
    h.update(text.encode("utf-8"))
    h.update(model.encode("utf-8"))
    h.update(prompt.encode("utf-8"))
    for rel in files:
        h.update(rel.encode("utf-8"))
        h.update((ROOT / rel).read_bytes())
    return h.hexdigest()[:16]


def cliproxy_chat(messages: list[dict], model: str) -> str:
    payload = json.dumps(
        {
            "model": model,
            "messages": messages,
            "temperature": 0.2,
        },
        ensure_ascii=False,
    ).encode("utf-8")
    proc = subprocess.run(
        ["docker", "exec", "-i", LITELLM_CONTAINER, "python", "-c", DOCKER_POST],
        input=payload,
        capture_output=True,
        timeout=210,
    )
    if proc.returncode != 0:
        err = (proc.stderr or proc.stdout).decode("utf-8", "replace")
        raise RuntimeError(f"cliproxy http {proc.returncode}: {err[:800]}")
    data = json.loads(proc.stdout.decode("utf-8"))
    try:
        return data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise RuntimeError(f"unexpected cliproxy payload: {data!r}"[:800]) from exc


def parse_spans_json(blob: str) -> dict:
    try:
        return json.loads(blob)
    except json.JSONDecodeError:
        fixed = re.sub(r",\s*([}\]])", r"\1", blob)
        fixed = re.sub(r"\\(?![\"\\/bfnrtu])", r"\\\\", fixed)
        return json.loads(fixed)


VALID_ACTIONS = {"KEEP", "TRIM", "REWRITE", "DELETE", "FLAG", "MERGE", "MOVE"}


def extract_spans(raw: str, text: str = "") -> list[dict]:
    blob = None
    marker = re.search(r"```json\s*", raw)
    if marker:
        rest = raw[marker.end():]
        end = rest.rfind("```")
        candidate = (rest[:end] if end >= 0 else rest).strip()
        if '"spans"' in candidate:
            blob = candidate
    if blob is None:
        fences = re.findall(r"```json\s*(.*?)```", raw, re.S)
        for candidate in reversed(fences):
            candidate = candidate.strip()
            if '"spans"' in candidate:
                blob = candidate
                break
    if blob is None:
        brace = re.search(r"\{[^{}]*\"spans\".*\}", raw, re.S)
        blob = brace.group(0) if brace else None
    if not blob:
        raise ValueError("no JSON spans block")
    data = parse_spans_json(blob)
    spans = data.get("spans")
    if not isinstance(spans, list) or not spans:
        raise ValueError("empty spans")
    n = len(text) if text else None
    cleaned = []
    prev_end = 0
    for item in spans:
        start = int(item["start"])
        end = int(item["end"])
        action = str(item.get("action") or "").upper()
        quote = str(item.get("quote") or "")
        if action not in VALID_ACTIONS:
            raise ValueError(f"unknown action {action!r}")
        if start < 0 or end < start:
            raise ValueError(f"bad span bounds {start}:{end}")
        if n is not None:
            if end > n:
                raise ValueError(f"span end {end} past text length {n}")
            if start < prev_end:
                raise ValueError(f"overlapping or unsorted span {start}:{end}")
            if quote:
                fragment = text[start:end]
                if quote not in fragment and fragment[:80] not in quote:
                    raise ValueError(f"quote does not match span {start}:{end}")
        prev_end = end
        cleaned.append(
            {
                "start": start,
                "end": end,
                "action": action,
                "quote": quote,
                "why": str(item.get("why") or ""),
            }
        )
    return cleaned


def cmd_run(args: argparse.Namespace) -> int:
    dest = out_dir(args.out)
    slice_path = dest / "slice.jsonl"
    if not slice_path.exists():
        print("run sample first", file=sys.stderr)
        return 2
    rows = load_slice(slice_path)
    if args.ids:
        want = {item.strip() for item in args.ids.split(",") if item.strip()}
        rows = [row for row in rows if row["id"] in want]
        missing = want - {row["id"] for row in rows}
        if missing:
            print(f"unknown ids: {sorted(missing)}", file=sys.stderr)
    if args.limit:
        rows = rows[: args.limit]
    pack = args.pack
    shared_system = None
    shared_files: list[str] = []
    mode = getattr(args, "mode", "audit")
    if pack != "auto":
        shared_system, shared_files = skill_system_prompt(pack, mode=mode)
        manifest = pack_manifest(pack, shared_files, args.model)
        (dest / "pack-manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print(
            f"pack={pack} files={len(shared_files)} chars={manifest['chars']} "
            f"model={args.model}",
            flush=True,
        )
    ok = 0
    failed = 0
    skipped = 0
    for i, row in enumerate(rows, 1):
        run_dir = dest / "runs" / row["id"]
        run_dir.mkdir(parents=True, exist_ok=True)
        out_path = run_dir / "audit.md"
        spans_path = run_dir / "spans.json"
        fp_path = run_dir / "fingerprint.json"
        if pack == "auto":
            system, files = skill_system_prompt(pack, row["text"], mode)
            (run_dir / "pack-manifest.json").write_text(
                json.dumps(
                    pack_manifest(pack, files, args.model),
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )
        else:
            system, files = shared_system, shared_files
        prompt = user_prompt(row["text"], mode)
        fp = run_fingerprint(row["text"], files, args.model, prompt)
        if spans_path.exists() and not args.force:
            prev = {}
            if fp_path.exists():
                try:
                    prev = json.loads(fp_path.read_text(encoding="utf-8"))
                except json.JSONDecodeError:
                    prev = {}
            if prev.get("fingerprint") == fp:
                print(f"[{i}/{len(rows)}] skip {row['id']}")
                skipped += 1
                ok += 1
                continue
        print(
            f"[{i}/{len(rows)}] {row['id']} {row['label']} {row['n_chars']}c "
            f"pack={pack} ({len(files)} files) …",
            flush=True,
        )
        try:
            raw = cliproxy_chat(
                [
                    {"role": "system", "content": system},
                    {"role": "user", "content": prompt},
                ],
                args.model,
            )
            out_path.write_text(raw, encoding="utf-8")
            spans = extract_spans(raw, row["text"])
            spans_path.write_text(
                json.dumps(spans, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            fp_path.write_text(
                json.dumps(
                    {
                        "fingerprint": fp,
                        "model": args.model,
                        "pack": pack,
                        "mode": mode,
                        "n_chars": len(row["text"]),
                    },
                    indent=2,
                ),
                encoding="utf-8",
            )
            ok += 1
        except Exception as exc:  # noqa: BLE001 — keep going across the slice
            failed += 1
            (run_dir / "error.txt").write_text(str(exc), encoding="utf-8")
            print(f"  FAIL {row['id']}: {exc}", file=sys.stderr)
        time.sleep(args.sleep)
    print(f"done ok={ok} failed={failed} skipped={skipped} / {len(rows)} → {dest / 'runs'}")
    if failed and ok:
        return 1
    if failed:
        return 2
    return 0


PROBLEM_ACTIONS = {"TRIM", "REWRITE", "DELETE"}
FLAG_ACTIONS = {"FLAG"}
SLOP_ACTIONS = PROBLEM_ACTIONS  # FLAG is verification, not slop
CITE_RE = re.compile(r"§\s*(\d+)")
SECTION_RE = re.compile(r"^## (\d+)\.\s+(.+)$", re.M)
SKILL_GAPS_RE = re.compile(
    r"(?im)^#{1,3}\s*(Skill gaps|Пробелы скилла)\b|^Skill gaps\s*:",
)
FILL_ROUTES = (
    (r"живописн|богатую историю|Киевской Руси|небольшое село", "ai-markers §39 gazetteer"),
    (r"оказывает существенное влияние|перспективный подход|глубже понять механизм", "ai-markers §39 AINL mold"),
    (r"прозрачность и ответственность|доверие населения|усилен контроль", "ai-markers §39 news fill / lint S18"),
    (r"не просто .+, а |это не просто", "ai-markers §6 contrast"),
    (r"сначала всё казалось|но со временем", "ai-markers §39 review sandwich"),
    (r"великолепн\w* сервис|всегда готов(?:ы|а|о)? помочь|каждое блюдо было шедевром|классик\w+ Москвы", "ai-markers §39 AI-review praise mold"),
    (r"этот опыт сделает|важный урок|выбирать правильный путь", "ai-markers §39 expand-fable / lint M04"),
    (r"не стесняйтесь обращаться|извлечь полезный опыт|стратегии справления|сеть поддержки", "ai-markers §39 advice-column"),
    (r"\*\*История создания\*\*|\*\*Авторство\*\*|Отмечена глубина психологического", "ai-markers §39 wiki-card"),
    (r"n[А-ЯЁA-Z]", "ai-markers §1 glued join / lint A07"),
)
FALSE_SLOP_ROUTES = (
    (r"ни какое|суперр+|диванчик|гребешк|земной поклон|Душевное спасибо", "procedure Pass 3 review/thanks + ai-markers §39 False slop"),
    (r"сказал | км\b|ТАСС|РИА|обнародовал", "procedure Pass 3 agency + ai-markers §39 False slop"),
    (r"нажмите |Панель управления|теперь вы знаете", "procedure Pass 3 tutorial + ai-markers §39 False slop"),
    (r"бились от ножа|отступать некуда", "procedure Pass 3 sports + ai-markers §39 False slop"),
    (r"^>\s|три вопроса", "procedure Pass 3 ticket + ai-markers §39 False slop"),
    (r"приговор|задержан|возбуждено уголов", "procedure Pass 3 court/police + ai-markers §39 False slop"),
    (r"Во-первых|ПМ не управляет бюджетом|Lead Time for Changes|О формате|Привет, читатель", "procedure Pass 3 house argument/table/outline + ai-markers §39 False slop"),
)


def catalog_index() -> dict[int, str]:
    text = (REFS / "ai-markers.md").read_text(encoding="utf-8")
    return {int(num): title.strip() for num, title in SECTION_RE.findall(text)}


def load_lint():
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "lint_text", ROOT / "scripts" / "lint_text.py"
    )
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def parse_audit_categories(raw: str) -> list[str]:
    cats: list[str] = []
    cat_idx = None
    for line in raw.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if not cells:
            continue
        if re.match(r":?-{2,}", cells[0]):
            continue
        lowered = [c.lower() for c in cells]
        if cat_idx is None:
            for i, name in enumerate(lowered):
                if "category" in name or "категор" in name:
                    cat_idx = i
                    break
            if cat_idx is not None:
                continue
            continue
        if cat_idx < len(cells):
            cat = cells[cat_idx]
            if cat and cat.lower() not in {"category", "категория"}:
                cats.append(cat)
    return cats


def citations_in(text: str) -> list[int]:
    return [int(n) for n in CITE_RE.findall(text or "")]


def route_disagreement(kind: str, quote: str, lint_codes: list[str]) -> str:
    blob = quote or ""
    if kind == "FP":
        for pattern, dest in FALSE_SLOP_ROUTES:
            if re.search(pattern, blob, re.I):
                return dest
        if lint_codes:
            return (
                f"lint {','.join(lint_codes)} fired on gold-human — "
                "gold error or lint over-eager; do not dump KEEP into SKILL.md"
            )
        return "procedure Pass 3 / ai-markers §39 False slop (if lived-in) else leave; not SKILL.md"
    # FN / MISS
    if lint_codes:
        return (
            f"catalog/lint already sees {','.join(lint_codes)} — recognition miss, "
            "not a new class; check whether the pack was stuffed"
        )
    for pattern, dest in FILL_ROUTES:
        if re.search(pattern, blob, re.I):
            return dest
    return "candidate new class in ai-markers (one class, not a banned word); SKILL.md only if routing broke"


def pred_tags(n: int, spans: list[dict]) -> list[str]:
    tags = ["?"] * n
    for span in spans:
        action = str(span.get("action") or "").upper()
        if action not in VALID_ACTIONS:
            raise ValueError(f"unknown action {action!r}")
        if action in PROBLEM_ACTIONS:
            mark = "S"
        elif action in FLAG_ACTIONS:
            mark = "F"
        else:
            mark = "K"
        start = int(span["start"])
        end = int(span["end"])
        if start < 0 or end > n or end < start:
            raise ValueError(f"span out of range {start}:{end} n={n}")
        for i in range(start, end):
            tags[i] = mark
    return tags


def quote_at(text: str, start: int, end: int, limit: int = 120) -> str:
    chunk = text[start:end].replace("\n", " ")
    return chunk[:limit]


def house_frame_overtrim(text: str, spans: list[dict]) -> list[str]:
    hits = []
    for span in spans:
        if str(span.get("action") or "").upper() not in SLOP_ACTIONS:
            continue
        start = int(span.get("start") or 0)
        end = int(span.get("end") or 0)
        chunk = text[start:end]
        stripped = chunk.strip()
        if FRAME_HASHTAG.match(stripped) and len(stripped.splitlines()[0]) < 40:
            hits.append(f"hashtag «{stripped.splitlines()[0]}»")
        if FRAME_GREET.search(chunk):
            hits.append("greeting")
        if FRAME_PS.search(chunk) and len(stripped) < 280:
            hits.append("P.S.")
    return hits


def cmd_grade(args: argparse.Namespace) -> int:
    dest = args.out
    rows = load_slice(dest / "slice.jsonl")
    report_rows = []
    disagreements: list[str] = []
    totals = {"tp": 0, "fp": 0, "fn": 0, "tn": 0, "uncovered": 0, "failed": 0}
    sections = catalog_index()
    cited_counts: dict[str, int] = {str(n): 0 for n in sections}
    unknown_cites: list[str] = []
    rows_with_cite = 0
    rows_with_gaps = 0
    rows_with_none_gaps = 0
    treat_ok = 0
    treat_total = 0
    house_frame_hits: list[str] = []
    house_rows = 0
    lint_mod = load_lint()
    treat_re = re.compile(
        r";\s*(delete|source-fact|simpler|удали(?:ть)?|факт из|проще)\b",
        re.I,
    )
    for row in rows:
        text = row["text"]
        n = len(text)
        is_house = row.get("label") == "house"
        gold_intervals = [] if is_house else row["ai_char_intervals"]
        gold = ["H"] * n
        for start, end in gold_intervals:
            for i in range(start, min(end, n)):
                gold[i] = "A"
        spans_path = dest / "runs" / row["id"] / "spans.json"
        if not spans_path.exists():
            totals["failed"] += 1
            report_rows.append(
                {"id": row["id"], "label": row["label"], "status": "no-spans"}
            )
            continue
        spans = json.loads(spans_path.read_text(encoding="utf-8"))
        audit_path = dest / "runs" / row["id"] / "audit.md"
        audit_raw = audit_path.read_text(encoding="utf-8") if audit_path.exists() else ""
        cats = parse_audit_categories(audit_raw)
        cites = citations_in(audit_raw)
        if cites:
            rows_with_cite += 1
        for num in cites:
            key = str(num)
            if key in cited_counts:
                cited_counts[key] += 1
            else:
                unknown_cites.append(f"{row['id']} §{num}")
        if SKILL_GAPS_RE.search(audit_raw):
            rows_with_gaps += 1
            if re.search(r"(?im)Skill gaps:\s*none\b", audit_raw):
                rows_with_none_gaps += 1
        lint_mode = (
            "telegram"
            if is_house
            else "article"
            if row.get("data_type") in POST_TYPES | {"news", "review"}
            else "generic"
        )
        lint_findings = lint_mod.scan_prose(text.splitlines(), lint_mode)
        lint_codes = sorted({item.code for item in lint_findings})
        for span in spans:
            if str(span.get("action") or "").upper() not in SLOP_ACTIONS:
                continue
            treat_total += 1
            why = str(span.get("why") or "")
            if treat_re.search(why):
                treat_ok += 1
        if is_house:
            house_rows += 1
            frame_hits = house_frame_overtrim(text, spans)
            slop_n = sum(
                1
                for span in spans
                if str(span.get("action") or "").upper() in SLOP_ACTIONS
            )
            report_rows.append(
                {
                    "id": row["id"],
                    "label": "house",
                    "data_type": row.get("data_type"),
                    "n_chars": n,
                    "tg_id": row.get("tg_id"),
                    "tp": 0,
                    "fp": 0,
                    "fn": 0,
                    "tn": 0,
                    "uncovered": 0,
                    "recall_ai": None,
                    "precision_slop": None,
                    "cited_sections": cites,
                    "categories": cats[:12],
                    "lint_codes": lint_codes,
                    "slop_spans": slop_n,
                    "frame_overtrim": frame_hits,
                    "status": "house",
                }
            )
            for hit in frame_hits:
                house_frame_hits.append(f"- {row['id']} TRIM house {hit}")
            continue
        try:
            pred = pred_tags(n, spans)
        except ValueError as exc:
            totals["failed"] += 1
            report_rows.append(
                {
                    "id": row["id"],
                    "label": row["label"],
                    "status": f"invalid-spans:{exc}",
                }
            )
            continue
        tp = fp = fn = tn = unc = flag_n = 0
        kinds: list[str] = []
        for g, p in zip(gold, pred):
            if p == "?":
                unc += 1
                kinds.append("U")
            elif p == "F":
                flag_n += 1
                kinds.append("FLAG")
            elif g == "A" and p == "S":
                tp += 1
                kinds.append("TP")
            elif g == "A" and p == "K":
                fn += 1
                kinds.append("FN")
            elif g == "H" and p == "S":
                fp += 1
                kinds.append("FP")
            else:
                tn += 1
                kinds.append("TN")
        coverage = (n - unc) / n if n else 1.0
        if coverage < 0.95:
            totals["failed"] += 1
            report_rows.append(
                {
                    "id": row["id"],
                    "label": row["label"],
                    "status": "incomplete-coverage",
                    "coverage": round(coverage, 3),
                    "uncovered": unc,
                    "n_chars": n,
                }
            )
            continue
        run_kind = None
        run_start = 0
        for i, kind in enumerate(kinds + ["END"]):
            if kind == run_kind:
                continue
            if run_kind in {"FN", "FP"} and i - run_start >= 40:
                label = (
                    "MISS gold=AI skill=KEEP"
                    if run_kind == "FN"
                    else "FP gold=human skill=SLOP"
                )
                quote = quote_at(text, run_start, i)
                local_lint = lint_mod.scan_prose([quote], lint_mode)
                local_codes = sorted({item.code for item in local_lint})
                route = route_disagreement(run_kind, quote, local_codes)
                disagreements.append(
                    f"- {run_kind} {row['id']} [{run_start}:{i}] {label}\n"
                    f"  «{quote}»\n"
                    f"  route → {route}"
                )
            run_kind = kind
            run_start = i
        for key, val in (("tp", tp), ("fp", fp), ("fn", fn), ("tn", tn), ("uncovered", unc)):
            totals[key] += val
        rec = tp / (tp + fn) if tp + fn else None
        prec = tp / (tp + fp) if tp + fp else None
        report_rows.append(
            {
                "id": row["id"],
                "label": row["label"],
                "data_type": row["data_type"],
                "n_chars": n,
                "tp": tp,
                "fp": fp,
                "fn": fn,
                "tn": tn,
                "uncovered": unc,
                "coverage": round((n - unc) / n if n else 1.0, 3),
                "flag_chars": flag_n,
                "recall_ai": rec,
                "precision_slop": prec,
                "cited_sections": cites,
                "categories": cats[:12],
                "lint_codes": lint_codes,
                "status": "ok",
            }
        )
    tp, fp, fn = totals["tp"], totals["fp"], totals["fn"]
    rec = tp / (tp + fn) if tp + fn else 0.0
    prec = tp / (tp + fp) if tp + fp else 0.0
    summary = {
        "rows": len(rows),
        "failed_runs": totals["failed"],
        "char_tp": tp,
        "char_fp": fp,
        "char_fn": fn,
        "char_tn": totals["tn"],
        "char_uncovered": totals["uncovered"],
        "recall_ai_spans": round(rec, 3),
        "precision_slop_calls": round(prec, 3),
        "note": (
            "Authorship overlap, not quality. recall = доля золотых AI-символов, "
            "которые скилл пометил TRIM/REWRITE/DELETE; FLAG не считается слопом. "
            "Incomplete coverage (<95%) excluded from totals. "
            "FP на human — подозрение на ложный слоп-вызов; "
            "FN на AI — дыра в каталоге либо золото разметило не-слоп как AI."
        ),
        "catalog": {
            "rows_citing_section": rows_with_cite,
            "rows_with_skill_gaps": rows_with_gaps,
            "rows_with_skill_gaps_none": rows_with_none_gaps,
            "cited_sections": {
                k: v for k, v in cited_counts.items() if v
            },
            "uncited_core": [
                f"§{n} {sections[n]}" for n in range(1, 17) if cited_counts.get(str(n), 0) == 0
            ],
            "unknown_citations": unknown_cites[:20],
            "slop_spans": treat_total,
            "slop_spans_with_treatment": treat_ok,
            "house_rows": house_rows,
            "house_frame_overtrim": len(house_frame_hits),
        },
    }
    usage = summary["catalog"]
    (dest / "span-agreement.json").write_text(
        json.dumps({"summary": summary, "rows": report_rows}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (dest / "catalog-usage.json").write_text(
        json.dumps(usage, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    lines = [
        "# Span agreement",
        "",
        f"- rows: {summary['rows']} (failed runs: {summary['failed_runs']})",
        f"- recall AI→slop: {summary['recall_ai_spans']}",
        f"- precision slop→AI: {summary['precision_slop_calls']}",
        f"- chars tp/fp/fn/tn: {tp}/{fp}/{fn}/{totals['tn']}",
        "",
        "## How to read",
        "",
        summary["note"],
        "",
        "## Disagreements (≥40 chars)",
        "",
        "Each row has a `route →` target. Patch that file. Do not dump a KEEP",
        "example into SKILL.md if procedure Pass 3 or ai-markers §39 already",
        "owns the class. At most three atomic edits per loop, one file each.",
        "",
    ]
    lines.extend(disagreements[:80] or ["- none ≥40 chars"])
    cited_sorted = sorted(
        ((int(k), v) for k, v in usage["cited_sections"].items()), key=lambda kv: -kv[1]
    )
    cite_lines = [
        f"- §{n} {sections.get(n, '?')}: {c}" for n, c in cited_sorted[:20]
    ] or ["- none (pack not stuffed, or Category is free text)"]
    lines.extend(
        [
            "",
            "## Catalog usage",
            "",
            f"- rows citing `§N`: {usage['rows_citing_section']} / {summary['rows']}",
            f"- Skill gaps present: {usage['rows_with_skill_gaps']} "
            f"(explicit none: {usage['rows_with_skill_gaps_none']})",
            f"- unknown `§N`: {len(usage['unknown_citations'])}",
            f"- slop spans with a treatment (delete / source-fact / simpler): "
            f"{usage['slop_spans_with_treatment']} / {usage['slop_spans']}",
            f"- house posts: {usage.get('house_rows', 0)}; "
            f"frame over-TRIM (hashtag/greeting/P.S.): "
            f"{usage.get('house_frame_overtrim', 0)}",
            "",
            "Cited:",
            *cite_lines,
            "",
            "Uncited core (§1–16):",
            *([f"- {item}" for item in usage["uncited_core"][:16]] or ["- none"]),
            "",
            "## Patch routing",
            "",
            "- SKILL.md — depth, invocation, output contract, progressive disclosure.",
            "- references/editorial-procedure.md — KEEP/TRIM treatments, Pass 3 table.",
            "- references/ai-markers.md — new class or False slop example.",
            "- references/heuristics.md — argument / rhythm / diction questions.",
            "- references/formats-and-artifacts.md — Markdown, tables, lists, links.",
            "- scripts/lint_text.py — regex-stable fill the eye already named.",
            "- Do not add a banned word. Do not optimize recall/precision.",
            "",
            "## House frame over-TRIM",
            "",
            *(house_frame_hits[:40] or ["- none"]),
        ]
    )
    (dest / "disagreements.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print(f"wrote {dest / 'span-agreement.json'}")
    print(f"wrote {dest / 'catalog-usage.json'}")
    print(f"wrote {dest / 'disagreements.md'}")
    return 1 if totals["failed"] else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)
    sample = sub.add_parser("sample", help="download a frozen 24-row slice")
    sample.add_argument("--out", type=Path, default=DEFAULT_OUT)
    sample.add_argument("--seed", type=int, default=42)
    sample.add_argument("--force", action="store_true")
    sample.add_argument(
        "--ainl",
        action="store_true",
        help="also sample AINL scientific abstracts (off by default)",
    )
    sample.add_argument(
        "--house",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="include channel posts as house-style rows (treatments only, no gold spans)",
    )
    sample.add_argument(
        "--house-only",
        action="store_true",
        help="sample only channel posts (skip LLMTrace); default n=100",
    )
    sample.add_argument(
        "--n",
        type=int,
        default=0,
        help="with --house-only, how many posts (default 100)",
    )
    sample.add_argument(
        "--house-file",
        type=Path,
        default=None,
        help="channel dump JSON (default: tg_last100.json)",
    )
    sample.add_argument(
        "--mix-public",
        action="store_true",
        help="100 each from LLMTrace det/clf, AINL, CoAT, Ru-hard (no house)",
    )
    sample.set_defaults(func=cmd_sample)
    run = sub.add_parser("run", help="call cliproxy with the skill pack + audit JSON")
    run.add_argument("--out", type=Path, default=DEFAULT_OUT)
    run.add_argument("--model", default=CLIPROXY_MODEL)
    run.add_argument(
        "--pack",
        choices=PACK_CHOICES,
        default="audit",
        help="what to stuff: map=SKILL.md, audit=map+procedure+markers (default), "
        "full=whole pack, auto=audit+formats if Markdown",
    )
    run.add_argument("--limit", type=int, default=0)
    run.add_argument("--ids", default="", help="comma-separated row ids")
    run.add_argument("--sleep", type=float, default=0.4)
    run.add_argument("--force", action="store_true")
    run.add_argument(
        "--mode",
        choices=("audit", "polish"),
        default="audit",
        help="audit = table only; polish = full editorial pass (not authorship gold)",
    )
    run.set_defaults(func=cmd_run)
    grade = sub.add_parser("grade", help="compare predicted spans to gold intervals")
    grade.add_argument("--out", type=Path, default=DEFAULT_OUT)
    grade.set_defaults(func=cmd_grade)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    return int(args.func(args) or 0)


if __name__ == "__main__":
    raise SystemExit(main())
