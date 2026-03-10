import re
from typing import List, Optional

from CUNY_course.example_code.rag_pipeline._types import (
    GeneratedAnswer,
    RetrievalHit,
)

DEFAULT_GENERATION_MODEL = "google/flan-t5-small"
_GENERATOR_CACHE = {}


def build_prompt(query: str, hits: List[RetrievalHit]) -> str:
    context_lines = []
    for hit in hits:
        context_lines.append(f"[{hit.chunk.chunk_id}] {hit.chunk.text}")
    context_block = "\n".join(context_lines)

    return (
        "You are a helpful assistant. "
        "Use only the context to answer the question. "
        "Include the most relevant citation IDs "
        "in square brackets at the end.\n\n"
        f"Question: {query}\n\n"
        f"Context:\n{context_block}\n\n"
        "Answer:"
    )


def _generate_text(
    prompt: str,
    model_name: str = DEFAULT_GENERATION_MODEL,
    max_new_tokens: int = 120,
) -> str:
    try:
        from transformers import pipeline
    except ImportError as exc:
        raise ImportError(
            "Missing generation dependency. " "Install transformers and torch."
        ) from exc

    generator = _GENERATOR_CACHE.get(model_name)
    if generator is None:
        generator = pipeline(
            "text2text-generation",
            model=model_name,
            device=-1,
        )
        _GENERATOR_CACHE[model_name] = generator

    response = generator(
        prompt,
        max_new_tokens=max_new_tokens,
        do_sample=False,
        truncation=True,
        max_length=512,
    )
    return response[0]["generated_text"].strip()


def _extractive_answer(query: str, hits: List[RetrievalHit]) -> str:
    query_tokens = {
        token.strip(".,;:!?\"'()").lower() for token in query.split() if token.strip()
    }

    scored_sentences = []
    for hit in hits:
        sentences = re.split(r"(?<=[.!?])\s+", hit.chunk.text)
        for sentence in sentences:
            stripped = sentence.strip()
            if not stripped:
                continue
            sentence_tokens = {
                token.strip(".,;:!?\"'()").lower()
                for token in stripped.split()
                if token.strip()
            }
            overlap = len(query_tokens.intersection(sentence_tokens))
            scored_sentences.append((overlap, stripped))

    scored_sentences.sort(key=lambda item: item[0], reverse=True)

    selected = []
    seen = set()
    for score, sentence in scored_sentences:
        if score <= 0 and selected:
            break
        if sentence in seen:
            continue
        seen.add(sentence)
        selected.append(sentence)
        if len(selected) >= 3:
            break

    if selected:
        return " ".join(selected)

    if hits:
        return hits[0].chunk.text[:300].strip()

    return "I could not find relevant context to answer that question."


def generate_answer(
    query: str,
    hits: List[RetrievalHit],
    model_name: Optional[str] = None,
) -> GeneratedAnswer:
    prompt = build_prompt(query=query, hits=hits)
    if model_name:
        generated_text = _generate_text(prompt=prompt, model_name=model_name)
    else:
        generated_text = _extractive_answer(query=query, hits=hits)

    citations = [hit.chunk.chunk_id for hit in hits[:2]]
    if citations:
        generated_text = f"{generated_text} [{' '.join(citations)}]"

    return GeneratedAnswer(
        query=query,
        answer=generated_text,
        citations=citations,
        context_chunk_ids=[hit.chunk.chunk_id for hit in hits],
        prompt=prompt,
    )
