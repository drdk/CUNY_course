from CUNY_course.example_code.rag_pipeline.chunking_step import chunk_documents
from CUNY_course.example_code.rag_pipeline.data_prep_step import (
    prepare_documents,
)


def run_demo() -> None:
    documents = prepare_documents()
    chunks = chunk_documents(documents)
    print(f"Created {len(chunks)} chunks from {len(documents)} documents")
    print(f"First chunk id: {chunks[0].chunk_id}")


if __name__ == "__main__":
    run_demo()
