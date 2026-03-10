import re
from typing import Iterable, List

from CUNY_course.example_code.rag_pipeline._types import Chunk

TOPIC_KEYWORDS = {
    "wildlife": {"bear", "coyote", "wildlife", "animal", "food"},
    "transportation": {"shuttle", "bus", "parking", "road", "yarts"},
    "trails": {"trail", "hike", "hiking", "fall", "permit"},
    "services": {"center", "store", "lodge", "clinic", "campground"},
}


def infer_topic(text: str) -> str:
    words = {word.strip(".,;:!?\"'").lower() for word in text.split()}
    scores = {
        topic: len(words.intersection(keywords))
        for topic, keywords in TOPIC_KEYWORDS.items()
    }
    best_topic = max(scores, key=scores.get)
    return best_topic if scores[best_topic] > 0 else "general"


def enrich_chunks_with_metadata(chunks: Iterable[Chunk]) -> List[Chunk]:
    enriched: List[Chunk] = []
    for chunk in chunks:
        year_match = re.search(r"(19|20)\\d{2}", chunk.text)
        chunk.metadata.update(
            {
                "topic": infer_topic(chunk.text),
                "has_year": bool(year_match),
                "source_type": ("markdown" if chunk.source.endswith(".md") else "text"),
                "year_mentioned": year_match.group(0) if year_match else None,
            }
        )
        enriched.append(chunk)
    return enriched
