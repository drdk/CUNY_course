from typing import Iterable, List, Tuple

import numpy as np

from CUNY_course.example_code.rag_pipeline._types import Chunk, EmbeddingIndex


def _require_embedding_dependencies() -> Tuple[object, object]:
    try:
        import faiss
        from sentence_transformers import SentenceTransformer
    except ImportError as exc:
        raise ImportError(
            "Missing embedding dependencies. "
            "Install sentence-transformers and faiss-cpu."
        ) from exc
    return faiss, SentenceTransformer


def encode_texts(texts: Iterable[str], model_name: str) -> np.ndarray:
    _, sentence_transformer_cls = _require_embedding_dependencies()
    model = sentence_transformer_cls(model_name)
    embeddings = model.encode(list(texts), show_progress_bar=False)
    embeddings = np.array(embeddings).astype("float32")
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True) + 1e-12
    return embeddings / norms


def build_index(chunks: List[Chunk], model_name: str) -> EmbeddingIndex:
    faiss, _ = _require_embedding_dependencies()
    chunk_texts = [chunk.text for chunk in chunks]
    chunk_vectors = encode_texts(chunk_texts, model_name=model_name)

    embedding_dim = int(chunk_vectors.shape[1])
    index = faiss.IndexFlatIP(embedding_dim)
    index.add(chunk_vectors)

    return EmbeddingIndex(
        model_name=model_name,
        index=index,
        embedding_dim=embedding_dim,
        chunk_ids=[chunk.chunk_id for chunk in chunks],
        chunk_vectors=chunk_vectors,
    )


def search_index(
    embedding_index: EmbeddingIndex,
    query: str,
    top_k: int,
) -> Tuple[np.ndarray, np.ndarray]:
    query_vector = encode_texts([query], model_name=embedding_index.model_name)
    scores, indices = embedding_index.index.search(query_vector, top_k)
    return scores[0], indices[0]
