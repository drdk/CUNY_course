from collections import Counter
from typing import Dict, List, Optional

from CUNY_course.example_code.rag_pipeline._embedding import search_index
from CUNY_course.example_code.rag_pipeline._types import (
    Chunk,
    EmbeddingIndex,
    RetrievalHit,
)


def _tokenize(text: str) -> List[str]:
    return [token.strip(".,;:!?\"'").lower() for token in text.split() if token.strip()]


def _lexical_overlap_score(query: str, text: str) -> float:
    query_tokens = _tokenize(query)
    text_tokens = _tokenize(text)
    if not query_tokens or not text_tokens:
        return 0.0

    query_counter = Counter(query_tokens)
    text_counter = Counter(text_tokens)
    overlap = sum(
        min(query_counter[token], text_counter[token]) for token in query_counter
    )
    return overlap / max(len(query_tokens), 1)


def retrieve_with_rerank(
    query: str,
    embedding_index: EmbeddingIndex,
    chunk_lookup: Dict[str, Chunk],
    metadata_filter: Optional[Dict[str, str]] = None,
    top_k: int = 4,
    candidate_k: int = 10,
    semantic_weight: float = 0.75,
) -> List[RetrievalHit]:
    if candidate_k < top_k:
        raise ValueError("candidate_k must be >= top_k")

    scores, indices = search_index(
        embedding_index,
        query=query,
        top_k=candidate_k,
    )

    hits: List[RetrievalHit] = []
    for semantic_score, index_position in zip(
        scores.tolist(),
        indices.tolist(),
    ):
        if index_position < 0:
            continue

        chunk_id = embedding_index.chunk_ids[index_position]
        chunk = chunk_lookup[chunk_id]

        if metadata_filter:
            if any(
                chunk.metadata.get(key) != value
                for key, value in metadata_filter.items()
            ):
                continue

        lexical_score = _lexical_overlap_score(query=query, text=chunk.text)
        rerank_score = (
            semantic_weight * float(semantic_score)
            + (1.0 - semantic_weight) * lexical_score
        )

        hits.append(
            RetrievalHit(
                chunk=chunk,
                semantic_score=float(semantic_score),
                lexical_score=lexical_score,
                rerank_score=rerank_score,
            )
        )

    hits.sort(key=lambda hit: hit.rerank_score, reverse=True)
    return hits[:top_k]
