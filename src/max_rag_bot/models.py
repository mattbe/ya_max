from dataclasses import dataclass


@dataclass(frozen=True)
class RetrievedChunk:
    doc_id: str
    chunk_id: str
    text: str
    score: float


@dataclass(frozen=True)
class GroundedAnswer:
    text: str
    grounded: bool
