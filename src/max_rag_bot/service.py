from __future__ import annotations

from dataclasses import dataclass

from .models import GroundedAnswer, RetrievedChunk
from .ports import Generator, Retriever

SYSTEM_PROMPT = """Ты — ассистент по внутренним документам.
Отвечай строго ТОЛЬКО по CONTEXT.
Если данных в CONTEXT не хватает, ответь дословно:
\"Недостаточно данных в предоставленных документах.\"
Не используй внешние знания.
Для каждого факта указывай ссылку [doc_id:chunk_id].
"""


@dataclass
class StrictRagService:
    retriever: Retriever
    generator: Generator
    top_k: int = 5
    min_score: float = 0.3

    def answer(self, user_question: str) -> GroundedAnswer:
        chunks = self.retriever.search(user_question, self.top_k)
        filtered = [chunk for chunk in chunks if chunk.score >= self.min_score]

        if not filtered:
            return GroundedAnswer(
                text="Недостаточно данных в предоставленных документах.",
                grounded=False,
            )

        context = self._build_context(filtered)
        user_prompt = (
            f"QUESTION:\n{user_question}\n\n"
            f"CONTEXT:\n{context}\n\n"
            "Сформируй ответ только по контексту и добавь ссылки вида [doc_id:chunk_id]."
        )
        answer = self.generator.generate(SYSTEM_PROMPT, user_prompt)
        return GroundedAnswer(text=answer, grounded=True)

    @staticmethod
    def _build_context(chunks: list[RetrievedChunk]) -> str:
        rows = []
        for chunk in chunks:
            rows.append(f"[{chunk.doc_id}:{chunk.chunk_id}] {chunk.text}")
        return "\n\n".join(rows)
