from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings for MAX + AI Studio grounded RAG."""

    max_bot_token: str = Field(default="", alias="MAX_TOKEN")
    max_webhook_secret: str = Field(default="", alias="MAX_WEBHOOK_SECRET")

    yandex_api_key: str = Field(default="", alias="YANDEX_API_KEY")
    yandex_folder_id: str = Field(default="", alias="YANDEX_FOLDER_ID")
    yandex_gpt_model_uri: str = Field(default="", alias="YANDEX_GPT_MODEL_URI")
    yandex_index_id: str = Field(default="", alias="YA_RAG_INDEX_ID")

    rag_top_k: int = Field(default=5, alias="RAG_TOP_K")
    rag_min_score: float = Field(default=0.3, alias="RAG_MIN_SCORE")

    request_timeout_seconds: float = Field(default=30.0, alias="REQUEST_TIMEOUT_SECONDS")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore", populate_by_name=True)
