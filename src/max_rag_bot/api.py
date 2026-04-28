from __future__ import annotations

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

from .adapters import OpenAiCompatibleGenerator, YandexAiStudioRetriever
from .config import Settings
from .service import StrictRagService


class MaxMessage(BaseModel):
    user_id: str
    text: str


class MaxWebhookRequest(BaseModel):
    message: MaxMessage


class MaxWebhookResponse(BaseModel):
    reply: str
    grounded: bool


def create_app(settings: Settings | None = None) -> FastAPI:
    cfg = settings or Settings()

    retriever = YandexAiStudioRetriever(
        api_key=cfg.yandex_api_key,
        folder_id=cfg.yandex_folder_id,
        index_id=cfg.yandex_index_id,
        timeout_seconds=cfg.request_timeout_seconds,
    )
    generator = OpenAiCompatibleGenerator(
        api_key=cfg.yandex_api_key,
        model=cfg.yandex_gpt_model_uri,
        timeout_seconds=cfg.request_timeout_seconds,
    )
    rag_service = StrictRagService(
        retriever=retriever,
        generator=generator,
        top_k=cfg.rag_top_k,
        min_score=cfg.rag_min_score,
    )

    app = FastAPI(title="MAX RAG Bot", version="0.1.0")

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/webhook/max", response_model=MaxWebhookResponse)
    def max_webhook(
        payload: MaxWebhookRequest,
        x_max_secret: str | None = Header(default=None),
    ) -> MaxWebhookResponse:
        if cfg.max_webhook_secret and x_max_secret != cfg.max_webhook_secret:
            raise HTTPException(status_code=401, detail="Invalid webhook secret")

        answer = rag_service.answer(payload.message.text)
        return MaxWebhookResponse(reply=answer.text, grounded=answer.grounded)

    return app
