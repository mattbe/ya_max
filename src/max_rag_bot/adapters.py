from __future__ import annotations

from dataclasses import dataclass


from .models import RetrievedChunk


@dataclass
class InMemoryRetriever:
    corpus: list[RetrievedChunk]

    def search(self, query: str, top_k: int) -> list[RetrievedChunk]:
        tokens = {t.lower() for t in query.split() if t.strip()}
        ranked: list[tuple[float, RetrievedChunk]] = []
        for item in self.corpus:
            hay = item.text.lower()
            score_boost = sum(1 for token in tokens if token in hay) / max(len(tokens), 1)
            ranked.append((item.score + score_boost, item))
        ranked.sort(key=lambda x: x[0], reverse=True)
        return [item for _, item in ranked[:top_k]]


@dataclass
class YandexAiStudioRetriever:
    api_key: str
    folder_id: str
    index_id: str
    timeout_seconds: float = 30.0
    endpoint: str = "https://llm.api.cloud.yandex.net/foundationModels/v1/searchIndexes/query"

    def search(self, query: str, top_k: int) -> list[RetrievedChunk]:
        headers = {
            "Authorization": f"Api-Key {self.api_key}",
            "x-folder-id": self.folder_id,
        }
        payload = {
            "indexId": self.index_id,
            "query": query,
            "limit": top_k,
        }
        import httpx

        with httpx.Client(timeout=self.timeout_seconds) as client:
            response = client.post(self.endpoint, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()

        chunks: list[RetrievedChunk] = []
        for item in data.get("chunks", []):
            chunks.append(
                RetrievedChunk(
                    doc_id=item.get("docId", "unknown_doc"),
                    chunk_id=item.get("chunkId", "unknown_chunk"),
                    text=item.get("text", ""),
                    score=float(item.get("score", 0.0)),
                )
            )
        return chunks


@dataclass
class OpenAiCompatibleGenerator:
    api_key: str
    model: str
    timeout_seconds: float = 30.0
    endpoint: str = "https://llm.api.cloud.yandex.net/v1/chat/completions"

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        headers = {
            "Authorization": f"Api-Key {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0,
        }
        import httpx

        with httpx.Client(timeout=self.timeout_seconds) as client:
            response = client.post(self.endpoint, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()

        return data["choices"][0]["message"]["content"]
