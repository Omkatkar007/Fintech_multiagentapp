"""Dependency-free hashed embeddings for local semantic retrieval."""

import hashlib
import math
import re


def embed(text: str, dimensions: int = 256) -> list[float]:
	vector = [0.0] * dimensions
	for token in re.findall(r"[a-z0-9]+", text.lower()):
		digest = hashlib.sha256(token.encode()).digest()
		index = int.from_bytes(digest[:4], "big") % dimensions
		vector[index] += 1.0
	norm = math.sqrt(sum(value * value for value in vector)) or 1.0
	return [value / norm for value in vector]
