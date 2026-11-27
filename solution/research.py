"""AI-помічник для пошуку й структурування технічної інформації

Питання -> веб-пошук DuckDuckGo -> завантаження сторінок -> безкоштовна модель Gemini
структурує відповідь лише за знайденими джерелами -> Markdown + лог метрик.

Команди:
  python research.py ask "питання" [--manual-min 20]    # зробити дослідження
  python research.py verify <id> ok|bad [--check-min 3] # результат перевірки + хвилини на перевірку
  python research.py stats                              # підсумок для таблиці «до / після»

"""
import argparse
import csv
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path

try:
    import requests
    import trafilatura
    from ddgs import DDGS
    from google import genai
    from google.genai import errors, types
except ImportError:
    sys.exit("Не встановлено залежності. Виконайте: pip install -r requirements.txt")


MODEL = os.getenv("MODEL", "gemini-3.8-flash")
FALLBACK_MODELS = os.getenv("FALLBACK_MODELS", "gemini-3.6-flash,gemini-3.5-flash-lite").split(",")
SEARCH_BACKENDS = os.getenv("SEARCH_BACKENDS", "duckduckgo,brave,yahoo,mojeek,startpage").split(",")
MAX_RESULTS = int(os.getenv("MAX_RESULTS", "6"))    # скільки результатів пошуку брати
FETCH_TOP = int(os.getenv("FETCH_TOP", "4"))        # для скількох читати сторінку повністю
PAGE_CHARS = int(os.getenv("PAGE_CHARS", "4000"))   # максимум символів з однієї сторінки

ROOT = Path(__file__).resolve().parent.parent
EVIDENCE = ROOT / "evidence"
RESULTS = EVIDENCE / "results"
LOG = EVIDENCE / "runs_log.csv"
FIELDS = ["id", "timestamp", "query", "seconds", "manual_min_before",
          "input_tokens", "output_tokens", "searches", "sources",
          "cost_usd", "verified", "check_min", "result_file"]

SYSTEM_PROMPT = """Ти — технічний дослідник для студента-веброзробника. Відповідай українською.
Тобі надано питання та пронумеровані джерела [1], [2], ... (уривки веб-сторінок).
Складай відповідь СТРОГО за такою структурою Markdown:

## Коротка відповідь
2–3 речення.

## Деталі
Таблиця порівняння (якщо питання про вибір між варіантами) або нумеровані кроки (якщо питання «як зробити»).

## Ризики та підводні камені
Список. Окремо познач те, що залежить від версії бібліотеки.

Правила: використовуй ЛИШЕ надані джерела; після кожного важливого твердження став номер джерела, наприклад [2].
Якщо джерела суперечать одне одному або інформації бракує — прямо скажи про це, нічого не домислюй.
Не вигадуй посилань і версій. Розділ із переліком джерел не пиши, його додасть програма."""


def slugify(text: str, limit: int = 50) -> str:
    slug = re.sub(r"[^\w]+", "-", text.lower(), flags=re.UNICODE).strip("-")
    return slug[:limit] or "query"


def search(query: str) -> list[dict]:
    """Пошук через ddgs: перебирає кілька пошукових систем, поки одна не поверне результати.
    Повертає список {title, href, body}."""
    errors_seen = []
    for backend in SEARCH_BACKENDS:
        for attempt in (1, 2):
            try:
                found = list(DDGS().text(query, max_results=MAX_RESULTS, backend=backend))
                if found:
                    print(f"Пошук: {backend}, знайдено {len(found)}")
                    return found
                errors_seen.append(f"{backend}: порожньо")
            except Exception as err:
                errors_seen.append(f"{backend}: {str(err)[:60]}")
            time.sleep(2)
    raise RuntimeError("; ".join(errors_seen[-4:]) or "No results found")


def fetch_page(url: str) -> str:
    """Текст сторінки (до PAGE_CHARS символів) або порожній рядок, якщо завантажити не вдалося."""
    try:
        resp = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0 (student research script)"})
        resp.raise_for_status()
        return (trafilatura.extract(resp.text) or "")[:PAGE_CHARS]
    except Exception:
        return ""


def build_sources(results: list[dict]) -> list[dict]:
    sources = []
    for i, item in enumerate(results, 1):
        page = fetch_page(item["href"]) if i <= FETCH_TOP else ""
        sources.append({"n": i, "title": item.get("title") or item["href"], "url": item["href"],
                        "text": page or item.get("body", ""), "full": bool(page)})
    return sources


def ask_model(client, query: str, sources: list[dict]):
    """Повертає (текст, вхідні токени, вихідні токени). Одна повторна спроба при ліміті 429."""
    blocks = [f"[{s['n']}] {s['title']} ({s['url']})\n{s['text']}" for s in sources]
    prompt = f"Питання: {query}\n\nДжерела:\n\n" + "\n\n".join(blocks)
    config = types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT, temperature=0.2)
    models = [MODEL] + [m for m in FALLBACK_MODELS if m and m != MODEL]
    last_err = None
    for model in models:
        for attempt in (1, 2, 3):
            try:
                resp = client.models.generate_content(model=model, contents=prompt, config=config)
                usage = resp.usage_metadata
                if model != MODEL:
                    print(f"(використано запасну модель: {model})")
                return (resp.text or "").strip(), (usage.prompt_token_count or 0), (usage.candidates_token_count or 0)
            except errors.APIError as err:
                last_err = err
                code = getattr(err, "code", None)
                if code in (429, 500, 503, 504):  # тимчасові проблеми: ліміт або перевантаження
                    if attempt < 3:
                        print(f"Модель {model} тимчасово недоступна ({code}), чекаю 15 с (спроба {attempt}/3)...")
                        time.sleep(15)
                        continue
                    break  # перехід до запасної моделі
                sys.exit(f"Помилка API: {err}. Перевірте ключ і назву моделі (MODEL).")
    sys.exit(f"Усі моделі зараз недоступні: {last_err}. Спробуйте за кілька хвилин.")


def read_log() -> list[dict]:
    if not LOG.exists():
        return []
    with LOG.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_log(rows: list[dict]) -> None:
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def cmd_ask(args) -> None:
    key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not key:
        sys.exit("Задайте ключ: export GEMINI_API_KEY=...  (Windows: set GEMINI_API_KEY=...)")
    started = time.perf_counter()
    try:
        results = search(args.query)
    except Exception as err: 
        sys.exit(f"Пошук не спрацював: {err}. Зачекайте хвилину й повторіть або шукайте вручну.")
    if not results:
        sys.exit("Пошук нічого не знайшов. Спробуйте переформулювати (англійською часто краще).")
    sources = build_sources(results)
    text, in_tok, out_tok = ask_model(genai.Client(api_key=key), args.query, sources)
    seconds = round(time.perf_counter() - started, 1)
    if not text:
        sys.exit("Модель не повернула текст. Спробуйте переформулювати питання.")

    src_lines = ["", "## Джерела"]
    for s in sources:
        note = "" if s["full"] else " *(лише уривок із пошуку, сторінку не прочитано)*"
        src_lines.append(f"- [{s['n']}] [{s['title']}]({s['url']}){note}")
    rows = read_log()
    run_id = len(rows) + 1
    RESULTS.mkdir(parents=True, exist_ok=True)
    out_file = RESULTS / f"{run_id:03d}-{slugify(args.query)}.md"
    out_file.write_text(f"# {args.query}\n\n{text}\n" + "\n".join(src_lines) + "\n", encoding="utf-8")

    rows.append({"id": run_id, "timestamp": datetime.now().isoformat(timespec="seconds"),
                 "query": args.query, "seconds": seconds,
                 "manual_min_before": args.manual_min if args.manual_min is not None else "",
                 "input_tokens": in_tok, "output_tokens": out_tok, "searches": 1,
                 "sources": len(sources), "cost_usd": 0.0, "verified": "", "check_min": "",
                 "result_file": out_file.name})
    write_log(rows)
    print(f"Готово за {seconds} с, джерел: {len(sources)} (повністю прочитано: "
          f"{sum(s['full'] for s in sources)}), вартість: $0. Файл: {out_file}")
    print(f"Перевірте ключові твердження за джерелами, потім: python research.py verify {run_id} ok|bad")


def cmd_verify(args) -> None:
    rows = read_log()
    for row in rows:
        if row["id"] == str(args.id):
            row["verified"] = args.verdict
            if args.check_min is not None:
                row["check_min"] = args.check_min
            write_log(rows)
            print(f"Запис {args.id}: {args.verdict}")
            return
    sys.exit(f"Запис {args.id} не знайдено в {LOG}")


def cmd_stats(_args) -> None:
    rows = read_log()
    if not rows:
        sys.exit("Лог порожній. Спочатку зробіть кілька запитів (ask).")
    n = len(rows)
    avg_sec = sum(float(r["seconds"]) for r in rows) / n
    manual = [float(r["manual_min_before"]) for r in rows if r["manual_min_before"]]
    print(f"Запитів: {n}")
    print(f"Середній час AI-прогону: {avg_sec:.0f} с")
    if manual:
        print(f"Середній час вручну (оцінка до): {sum(manual) / len(manual):.1f} хв (за {len(manual)} запитами)")
    totals = [float(r["seconds"]) / 60 + float(r["check_min"]) for r in rows if r["check_min"]]
    if totals:
        print(f"Середній повний час з перевіркою: {sum(totals) / len(totals):.1f} хв (за {len(totals)} запитами)")
    tokens = sum(int(r["input_tokens"]) + int(r["output_tokens"]) for r in rows)
    print(f"Токенів усього: {tokens}; вартість прогону: $0 (безкоштовний рівень)")
    checked = [r for r in rows if r["verified"] in ("ok", "bad")]
    if checked:
        ok = sum(1 for r in checked if r["verified"] == "ok")
        print(f"Підтверджено джерелами: {ok}/{len(checked)} = {100 * ok / len(checked):.0f}%")
    else:
        print("Перевірених відповідей ще немає (команда verify).")


def main() -> None:
    parser = argparse.ArgumentParser(description="Тех-дослідник")
    sub = parser.add_subparsers(dest="cmd", required=True)
    p_ask = sub.add_parser("ask", help="зробити дослідження")
    p_ask.add_argument("query")
    p_ask.add_argument("--manual-min", type=float, default=None,
                       help="скільки хвилин це зайняло б вручну (для порівняння)")
    p_ask.set_defaults(func=cmd_ask)
    p_ver = sub.add_parser("verify", help="позначити результат перевірки")
    p_ver.add_argument("id", type=int)
    p_ver.add_argument("verdict", choices=["ok", "bad"])
    p_ver.add_argument("--check-min", type=float, default=None,
                       help="скільки хвилин пішло на ручну перевірку джерел")
    p_ver.set_defaults(func=cmd_verify)
    sub.add_parser("stats", help="підсумок метрик").set_defaults(func=cmd_stats)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()