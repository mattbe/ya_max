from max_rag_bot.adapters import InMemoryRetriever
from max_rag_bot.models import RetrievedChunk
from max_rag_bot.service import StrictRagService


class DummyGenerator:
    def generate(self, system_prompt: str, user_prompt: str) -> str:
        assert "CONTEXT" in user_prompt
        return "SLA составляет 99.9% [policy:1]"


def test_no_context_no_answer():
    retriever = InMemoryRetriever(corpus=[])
    service = StrictRagService(retriever=retriever, generator=DummyGenerator(), top_k=3, min_score=0.5)

    answer = service.answer("Какой SLA?")

    assert answer.grounded is False
    assert answer.text == "Недостаточно данных в предоставленных документах."


def test_grounded_answer_with_chunks():
    retriever = InMemoryRetriever(
        corpus=[
            RetrievedChunk(doc_id="policy", chunk_id="1", text="SLA составляет 99.9%.", score=0.9),
            RetrievedChunk(doc_id="faq", chunk_id="2", text="Санкции при нарушении SLA.", score=0.6),
        ]
    )
    service = StrictRagService(retriever=retriever, generator=DummyGenerator(), top_k=3, min_score=0.5)

    answer = service.answer("Какой SLA?")

    assert answer.grounded is True
    assert "[policy:1]" in answer.text
