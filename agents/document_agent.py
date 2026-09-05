from services.pdf_loader import chunk_text, load_text


class DocumentAgent:
	def process(self, source, filename: str = "proposal") -> tuple[str, list[str]]:
		text = load_text(source, filename)
		return text, chunk_text(text)
