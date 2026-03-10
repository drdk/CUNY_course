import json
from pathlib import Path
from typing import Iterable, List

from CUNY_course.example_code.rag_pipeline._types import Document


DEFAULT_TOY_CORPUS_PATH = (
    Path(__file__).resolve().parents[2] / "example_data" / "rag_toy_corpus.jsonl"
)
DEFAULT_YOSEMITE_GUIDE_PATH = (
    Path(__file__).resolve().parents[2] / "example_data" / "yosemite_guide.md"
)
DEFAULT_CORPUS_PATH = DEFAULT_YOSEMITE_GUIDE_PATH


def normalize_whitespace(text: str) -> str:
    return " ".join(text.split())


def _title_from_markdown(markdown_text: str, fallback: str) -> str:
    for line in markdown_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            return stripped.lstrip("#").strip() or fallback
    return fallback


def load_jsonl_documents(path: Path) -> List[Document]:
    documents: List[Document] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            documents.append(
                Document(
                    doc_id=row["doc_id"],
                    title=row["title"],
                    source=row.get("source", "toy_corpus"),
                    text=row["text"],
                )
            )
    return documents


def load_markdown_document(path: Path) -> List[Document]:
    text = path.read_text(encoding="utf-8")
    default_title = path.stem.replace("_", " ").title()
    return [
        Document(
            doc_id=path.stem,
            title=_title_from_markdown(
                text,
                fallback=default_title,
            ),
            source=path.name,
            text=text,
        )
    ]


def load_documents(path: Path) -> List[Document]:
    suffix = path.suffix.lower()
    if suffix == ".jsonl":
        return load_jsonl_documents(path)
    if suffix in {".md", ".markdown", ".txt"}:
        return load_markdown_document(path)
    raise ValueError(f"Unsupported corpus format: {path}")


def unique_by_doc_id(documents: Iterable[Document]) -> List[Document]:
    seen = set()
    deduped: List[Document] = []
    for document in documents:
        if document.doc_id in seen:
            continue
        seen.add(document.doc_id)
        deduped.append(document)
    return deduped
