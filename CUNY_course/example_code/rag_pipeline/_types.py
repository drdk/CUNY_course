from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class Document:
    doc_id: str
    title: str
    source: str
    text: str


@dataclass
class Chunk:
    chunk_id: str
    doc_id: str
    title: str
    source: str
    text: str
    start_offset: int
    end_offset: int
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EmbeddingIndex:
    model_name: str
    index: Any
    embedding_dim: int
    chunk_ids: List[str]
    chunk_vectors: Any


@dataclass
class RetrievalHit:
    chunk: Chunk
    semantic_score: float
    lexical_score: float
    rerank_score: float


@dataclass
class GeneratedAnswer:
    query: str
    answer: str
    citations: List[str]
    context_chunk_ids: List[str]
    prompt: Optional[str] = None
