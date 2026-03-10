from CUNY_course.example_code.rag_pipeline.embedding_step import (
    build_embedding_index,
)
from CUNY_course.example_code.rag_pipeline._stage_support import (
    load_prepared_chunks,
)


def run_demo() -> None:
    chunks = load_prepared_chunks()
    embedding_index, _ = build_embedding_index(chunks)
    print(f"Embedded {len(chunks)} chunks")
    print(f"Embedding dim: {embedding_index.embedding_dim}")


if __name__ == "__main__":
    run_demo()
