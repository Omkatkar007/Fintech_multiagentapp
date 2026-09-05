"""Proposal text extraction and deterministic chunking."""

from pathlib import Path
import re

from config import settings


def load_text(source: str | Path | bytes, filename: str = "proposal") -> str:
	if isinstance(source, bytes):
		raw = source
	elif isinstance(source, (str, Path)):
		try:
			path = Path(source)
			if path.exists():
				raw = path.read_bytes()
			else:
				return str(source)
		except (OSError, ValueError):
			return str(source)
	if filename.lower().endswith(".pdf") or raw[:4] == b"%PDF":
		try:
			from pypdf import PdfReader
			import io
			return "\n".join(page.extract_text() or "" for page in PdfReader(io.BytesIO(raw)).pages)
		except Exception:
			return raw.decode("utf-8", errors="ignore")
	if filename.lower().endswith(".docx"):
		try:
			import docx
			import io
			doc = docx.Document(io.BytesIO(raw))
			return "\n".join(para.text for para in doc.paragraphs)
		except Exception:
			pass
	return raw.decode("utf-8", errors="ignore")


def chunk_text(text: str, size: int = settings.chunk_size, overlap: int = settings.chunk_overlap) -> list[str]:
	cleaned = re.sub(r"\s+", " ", text).strip()
	if not cleaned:
		return []
	chunks = []
	start = 0
	while start < len(cleaned):
		end = min(start + size, len(cleaned))
		if end < len(cleaned):
			boundary = cleaned.rfind(" ", start, end)
			end = boundary if boundary > start else end
		chunks.append(cleaned[start:end].strip())
		if end >= len(cleaned):
			break
		start = max(end - overlap, start + 1)
	return chunks
