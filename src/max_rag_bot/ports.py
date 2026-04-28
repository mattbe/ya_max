from __future__ import annotations

from typing import Protocol

from .models import RetrievedChunk


class Retriever(Protocol):
    def search(self, query: str, top_k: int) -> list[RetrievedChunk]:
        ...


class Generator(Protocol):
    def generate(self, system_prompt: str, user_prompt: str) -> str:
        ...
