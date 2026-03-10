from CUNY_course.example_code.rag_pipeline.metadata_step import (
    enrich_chunks_with_metadata,
)
from CUNY_course.example_code.rag_pipeline._stage_support import (
    load_prepared_chunks,
)


def run_demo() -> None:
    chunks = load_prepared_chunks()
    enriched = enrich_chunks_with_metadata(chunks)
    print(f"Annotated {len(enriched)} chunks with metadata")
    print(f"Sample metadata: {enriched[0].metadata}")


if __name__ == "__main__":
    run_demo()
