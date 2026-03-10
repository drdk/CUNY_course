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
from CUNY_course.example_code.rag_pipeline._stage_support import (
    load_prepared_chunks,
)


def run_demo() -> None:
    chunks = enrich_chunks_with_metadata(load_prepared_chunks())
    embedding_index, chunk_lookup = build_embedding_index(chunks)
    query = "When does Tioga Road usually open?"
    hits = retrieve_with_rerank(
        query,
        embedding_index,
        chunk_lookup,
        top_k=3,
        candidate_k=8,
    )
    answer = generate_answer(query=query, hits=hits)

    print(answer.answer)
    print(f"Citations: {answer.citations}")


if __name__ == "__main__":
    run_demo()
