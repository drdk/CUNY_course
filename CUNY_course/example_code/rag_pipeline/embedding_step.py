from typing import Dict, List, Tuple

from CUNY_course.example_code.rag_pipeline._embedding import build_index
from CUNY_course.example_code.rag_pipeline._types import Chunk, EmbeddingIndex

DEFAULT_EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def build_embedding_index(
    chunks: List[Chunk], model_name: str = DEFAULT_EMBED_MODEL
) -> Tuple[EmbeddingIndex, Dict[str, Chunk]]:
    embedding_index = build_index(chunks=chunks, model_name=model_name)
    chunk_lookup = {chunk.chunk_id: chunk for chunk in chunks}
    return embedding_index, chunk_lookup
