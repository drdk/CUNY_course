from CUNY_course.example_code.rag_pipeline.embedding_step import (
    build_embedding_index,
)
from CUNY_course.example_code.rag_pipeline.metadata_step import (
    enrich_chunks_with_metadata,
)
from CUNY_course.example_code.rag_pipeline.retrieval_step import (
    retrieve_with_rerank,
)
from CUNY_course.example_code.rag_pipeline._stage_support import (
    load_prepared_chunks,
)


def run_demo() -> None:
    chunks = enrich_chunks_with_metadata(load_prepared_chunks())
    embedding_index, chunk_lookup = build_embedding_index(chunks)

    query = "Where should I park in Yosemite Valley?"
    hits = retrieve_with_rerank(
        query,
        embedding_index,
        chunk_lookup,
        top_k=3,
        candidate_k=8,
    )

    print(f"Retrieved {len(hits)} chunks for query: {query}")
    for rank, hit in enumerate(hits, start=1):
        topic = hit.chunk.metadata.get("topic")
        print(
            f"{rank}. {hit.chunk.chunk_id} | "
            f"score={hit.rerank_score:.3f} | topic={topic}"
        )


if __name__ == "__main__":
    run_demo()
