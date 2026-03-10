from typing import Iterable, List

from CUNY_course.example_code.rag_pipeline._types import Chunk, Document


def chunk_documents(
    documents: Iterable[Document],
    strategy: str = "character",
    chunk_size_chars: int = 500,
    overlap_chars: int = 100,
    chunk_size_words: int = 90,
    overlap_words: int = 20,
) -> List[Chunk]:
    if strategy not in {"character", "word"}:
        raise ValueError(f"Unsupported chunking strategy: {strategy}")

    if strategy == "word":
        return _chunk_by_words(
            documents=documents,
            chunk_size_words=chunk_size_words,
            overlap_words=overlap_words,
        )

    return _chunk_by_characters(
        documents=documents,
        chunk_size_chars=chunk_size_chars,
        overlap_chars=overlap_chars,
    )


def _chunk_by_characters(
    documents: Iterable[Document],
    chunk_size_chars: int,
    overlap_chars: int,
) -> List[Chunk]:
    if overlap_chars >= chunk_size_chars:
        raise ValueError("overlap_chars must be smaller than chunk_size_chars")

    chunks: List[Chunk] = []
    for document in documents:
        step = chunk_size_chars - overlap_chars
        chunk_number = 0

        for start in range(0, len(document.text), step):
            end = min(start + chunk_size_chars, len(document.text))
            chunk_text = document.text[start:end].strip()
            if not chunk_text:
                continue

            chunks.append(
                Chunk(
                    chunk_id=f"{document.doc_id}_chunk_{chunk_number}",
                    doc_id=document.doc_id,
                    title=document.title,
                    source=document.source,
                    text=chunk_text,
                    start_offset=start,
                    end_offset=end,
                )
            )
            chunk_number += 1

            if end >= len(document.text):
                break

    return chunks


def _chunk_by_words(
    documents: Iterable[Document],
    chunk_size_words: int,
    overlap_words: int,
) -> List[Chunk]:
    if overlap_words >= chunk_size_words:
        raise ValueError("overlap_words must be smaller than chunk_size_words")

    chunks: List[Chunk] = []
    for document in documents:
        words = document.text.split()
        step = chunk_size_words - overlap_words
        chunk_number = 0

        for start in range(0, len(words), step):
            end = min(start + chunk_size_words, len(words))
            chunk_words = words[start:end]
            if not chunk_words:
                continue

            chunks.append(
                Chunk(
                    chunk_id=f"{document.doc_id}_chunk_{chunk_number}",
                    doc_id=document.doc_id,
                    title=document.title,
                    source=document.source,
                    text=" ".join(chunk_words),
                    start_offset=start,
                    end_offset=end,
                )
            )
            chunk_number += 1

            if end >= len(words):
                break

    return chunks
