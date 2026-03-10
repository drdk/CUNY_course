from typing import List

from CUNY_course.example_code.rag_pipeline.chunking_step import chunk_documents
from CUNY_course.example_code.rag_pipeline.data_prep_step import (
    prepare_documents,
)
from CUNY_course.example_code.rag_pipeline._types import Chunk, Document


def load_prepared_documents() -> List[Document]:
    return prepare_documents()


def load_prepared_chunks() -> List[Chunk]:
    return chunk_documents(load_prepared_documents())
