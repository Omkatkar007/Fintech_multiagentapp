"""A small local vector index with cosine retrieval."""

from dataclasses import dataclass

from services.embeddings import embed


@dataclass
class SearchResult:
	text: str
	score: float
	metadata: dict


class VectorStore:
	def __init__(self):
		self._items: list[tuple[list[float], str, dict]] = []

	def add(self, texts: list[str], metadata: dict | None = None) -> None:
		metadata = metadata or {}
		self._items.extend((embed(text), text, {**metadata, "chunk": index}) for index, text in enumerate(texts))

	def search(self, query: str, top_k: int = 5) -> list[SearchResult]:
		query_vector = embed(query)
		ranked = sorted(((sum(a * b for a, b in zip(query_vector, vector)), text, meta) for vector, text, meta in self._items), reverse=True, key=lambda item: item[0])
		return [SearchResult(text, score, meta) for score, text, meta in ranked[:top_k]]
