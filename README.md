# MAX RAG Bot Skeleton

Рабочий каркас бота для MAX, который отвечает **только на основе документов из Search Index Yandex AI Studio**.

## Что реализовано
- FastAPI webhook endpoint для MAX: `POST /webhook/max`
- Strict RAG service с правилом `no-context-no-answer`
- Retriever адаптер для Yandex AI Studio Search Index
- Generator адаптер для YandexGPT OpenAI-compatible Chat API
- Жесткая фильтрация retrieval по `RAG_MIN_SCORE`

## Быстрый старт
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
cp .env.example .env
uvicorn max_rag_bot.main:app --reload
```

## Локальная проверка
```bash
pytest
curl -X POST http://127.0.0.1:8000/webhook/max \
  -H 'Content-Type: application/json' \
  -d '{"message": {"user_id": "u1", "text": "Что говорится о SLA?"}}'
```

> Если retrieval не вернул релевантных чанков, бот отвечает:
> `Недостаточно данных в предоставленных документах.`
