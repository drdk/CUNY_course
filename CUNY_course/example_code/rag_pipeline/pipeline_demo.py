from typing import Dict, Optional

from CUNY_course.example_code.rag_pipeline.chunking_step import chunk_documents
from CUNY_course.example_code.rag_pipeline.data_prep_step import (
    prepare_documents,
)
from CUNY_course.example_code.rag_pipeline.embedding_step import (
    build_embedding_index,
)
from CUNY_course.example_code.rag_pipeline.generation_step import (
    generate_answer,
)
from CUNY_course.example_code.rag_pipeline.metadata_step import (
    enrich_chunks_with_metadata,
)
from CUNY_course.example_code.rag_pipeline.retrieval_step import (
    retrieve_with_rerank,
)
from CUNY_course.example_code.rag_pipeline._types import GeneratedAnswer


def run_pipeline(
    query: str,
    metadata_filter: Optional[Dict[str, str]] = None,
    top_k: int = 4,
    candidate_k: int = 10,
) -> GeneratedAnswer:
    documents = prepare_documents()
    chunks = chunk_documents(documents)
    chunks = enrich_chunks_with_metadata(chunks)

    embedding_index, chunk_lookup = build_embedding_index(chunks)
    hits = retrieve_with_rerank(
        query=query,
        embedding_index=embedding_index,
        chunk_lookup=chunk_lookup,
        metadata_filter=metadata_filter,
        top_k=top_k,
        candidate_k=candidate_k,
    )

    return generate_answer(query=query, hits=hits)


def run_demo() -> None:
    query = "Are pets allowed on Yosemite Valley shuttles?"
    answer = run_pipeline(
        query=query,
        metadata_filter={"topic": "transportation"},
    )

    print(f"Query: {answer.query}")
    print(f"Answer: {answer.answer}")
    print(f"Citations: {answer.citations}")


if __name__ == "__main__":
    run_demo()
