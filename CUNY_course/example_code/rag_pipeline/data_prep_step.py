from pathlib import Path
from typing import List

from CUNY_course.example_code.rag_pipeline._types import Document
from CUNY_course.example_code.rag_pipeline._utils import (
    DEFAULT_CORPUS_PATH,
    load_documents,
    normalize_whitespace,
    unique_by_doc_id,
)


def prepare_documents(
    corpus_path: Path = DEFAULT_CORPUS_PATH,
) -> List[Document]:
    raw_documents = load_documents(corpus_path)

    cleaned_documents: List[Document] = []
    for document in raw_documents:
        cleaned_text = normalize_whitespace(document.text)
        if not cleaned_text:
            continue
        cleaned_documents.append(
            Document(
                doc_id=document.doc_id,
                title=document.title.strip(),
                source=document.source.strip(),
                text=cleaned_text,
            )
        )

    return unique_by_doc_id(cleaned_documents)


def run_demo() -> None:
    documents = prepare_documents()
    print(f"Prepared {len(documents)} documents")
    print("Sample:")
    for document in documents[:2]:
        print(f"- {document.doc_id}: {document.title} ({document.source})")
