import os
import textwrap
from functools import lru_cache
from typing import List, Tuple

import gradio as gr
from openai import AzureOpenAI

from CUNY_course.example_code.rag_pipeline.chunking_step import chunk_documents
from CUNY_course.example_code.rag_pipeline.data_prep_step import prepare_documents
from CUNY_course.example_code.rag_pipeline.embedding_step import build_embedding_index
from CUNY_course.example_code.rag_pipeline.metadata_step import (
    enrich_chunks_with_metadata,
)
from CUNY_course.example_code.rag_pipeline.retrieval_step import retrieve_with_rerank


def _require_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


@lru_cache(maxsize=1)
def _get_client() -> AzureOpenAI:
    return AzureOpenAI(
        api_version="2025-03-01-preview",
        azure_endpoint=_require_env("AZURE_OPENAI_ENDPOINT"),
        api_key=_require_env("AZURE_OPENAI_API_KEY"),
        timeout=30,
        max_retries=3,
    )


def build_prompt(query: str, hits) -> str:
    context_lines = [f"[{h.chunk.chunk_id}] {h.chunk.text}" for h in hits]
    context_block = "\n".join(context_lines)
    return (
        "Use only the context to answer the question in 1-3 complete sentences. "
        "If the context is insufficient, say: 'I don't know based on the provided context.' "
        "Do not include citation IDs in your response.\n\n"
        f"Question: {query}\n\n"
        f"Context:\n{context_block}\n\n"
        "Answer:"
    )


def _extract_text_from_response_output(response) -> str:
    parts: List[str] = []
    for out in getattr(response, "output", []) or []:
        for item in getattr(out, "content", []) or []:
            text = getattr(item, "text", None)
            if text:
                parts.append(text)
    return "\n".join(parts).strip()


def generate_with_azure(prompt: str) -> str:
    client = _get_client()
    deployment = _require_env("AZURE_OPENAI_DEPLOYMENT")

    response = client.responses.create(
        model=deployment,
        input=[{"role": "user", "content": prompt}],
        reasoning={"effort": "minimal"},
        max_output_tokens=400,
    )

    text = (response.output_text or "").strip()
    if not text:
        text = _extract_text_from_response_output(response)
    if text:
        return text

    chat = client.chat.completions.create(
        model=deployment,
        messages=[
            {"role": "system", "content": "You are a concise, factual assistant."},
            {"role": "user", "content": prompt},
        ],
        max_completion_tokens=400,
    )
    return (chat.choices[0].message.content or "").strip()


@lru_cache(maxsize=20)
def _build_index_for_params(
    chunk_size_chars: int,
    overlap_chars: int,
):
    documents = prepare_documents()
    chunks = chunk_documents(
        documents,
        strategy="character",
        chunk_size_chars=chunk_size_chars,
        overlap_chars=overlap_chars,
    )
    chunks = enrich_chunks_with_metadata(chunks)
    embedding_index, chunk_lookup = build_embedding_index(chunks)
    return chunks, embedding_index, chunk_lookup


def run_rag(
    query: str,
    chunk_size_chars: int,
    overlap_chars: int,
    top_k: int,
    candidate_k: int,
) -> Tuple[str, str, str]:
    query = (query or "").strip()
    if not query:
        return "Please enter a query.", "", ""

    if overlap_chars >= chunk_size_chars:
        return "Overlap must be smaller than chunk size.", "", ""

    try:
        chunks, embedding_index, chunk_lookup = _build_index_for_params(
            int(chunk_size_chars),
            int(overlap_chars),
        )
        hits = retrieve_with_rerank(
            query=query,
            embedding_index=embedding_index,
            chunk_lookup=chunk_lookup,
            top_k=int(top_k),
            candidate_k=int(candidate_k),
        )

        prompt = build_prompt(query, hits)
        answer = generate_with_azure(prompt).strip()
        citations = [h.chunk.chunk_id for h in hits]
        answer_with_citations = (
            f"{answer} [{' '.join(citations)}]" if citations else answer
        )

        citation_lines = "\n".join([f"- {c}" for c in citations])
        preview_blocks = []
        for h in hits[:3]:
            preview_blocks.append(
                "\n".join(
                    [
                        f"### {h.chunk.chunk_id}",
                        textwrap.fill(h.chunk.text, width=110),
                    ]
                )
            )

        diagnostics = f"Chunks created: {len(chunks)}\n" f"Retrieved hits: {len(hits)}"
        previews = "\n\n".join(preview_blocks)
        return answer_with_citations, citation_lines, f"{diagnostics}\n\n{previews}"
    except Exception as exc:
        return f"Error: {exc}", "", ""


with gr.Blocks(title="Yosemite RAG Demo") as demo:
    gr.Markdown("# Yosemite RAG Demo")
    gr.Markdown(
        "Ask questions over the Yosemite guide with adjustable chunking and retrieval settings."
    )

    query = gr.Textbox(
        label="Query",
        value="Can I bring my pet?",
    )

    with gr.Row():
        chunk_size = gr.Slider(
            minimum=80,
            maximum=800,
            step=20,
            value=200,
            label="Chunk size (characters)",
        )
        overlap = gr.Slider(
            minimum=0,
            maximum=300,
            step=10,
            value=50,
            label="Overlap (characters)",
        )

    with gr.Row():
        top_k = gr.Slider(minimum=1, maximum=10, step=1, value=5, label="Top K")
        candidate_k = gr.Slider(
            minimum=2,
            maximum=20,
            step=1,
            value=8,
            label="Candidate K",
        )

    run_button = gr.Button("Run RAG")

    answer_out = gr.Textbox(label="Answer", lines=5)
    citations_out = gr.Textbox(label="Citations", lines=6)
    previews_out = gr.Markdown(label="Top Hit Previews")

    run_button.click(
        fn=run_rag,
        inputs=[query, chunk_size, overlap, top_k, candidate_k],
        outputs=[answer_out, citations_out, previews_out],
    )


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=int(os.getenv("PORT", "7860")))
