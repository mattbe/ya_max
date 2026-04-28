# MAX RAG Bot Skeleton

Рабочий каркас бота для MAX, который отвечает **только на основе документов из Search Index Yandex AI Studio**.

## Что реализовано
- FastAPI webhook endpoint для MAX: `POST /webhook/max`
- Реальный HTTP-адаптер `MaxApiClient` для отправки ответа в MAX Bot API (`POST /messages`)
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

## Формат webhook payload
```json
{
  "message": {
    "message_id": "msg-1",
    "chat_id": "chat-1",
    "user_id": "user-1",
    "text": "Что сказано в регламенте про SLA?"
  }
}
```

После генерации ответа сервис отправляет сообщение обратно в MAX через Bot API.

## Локальная проверка
```bash
pytest
curl -X POST http://127.0.0.1:8000/webhook/max \
  -H 'Content-Type: application/json' \
  -d '{"message": {"message_id":"m1", "chat_id": "c1", "user_id": "u1", "text": "Что говорится о SLA?"}}'
```

> Если retrieval не вернул релевантных чанков, бот отвечает:
> `Недостаточно данных в предоставленных документах.`
