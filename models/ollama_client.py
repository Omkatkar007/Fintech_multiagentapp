"""Small optional Ollama client. The app remains usable without Ollama."""

import json
from urllib.request import Request, urlopen

from config import settings


class OllamaClient:
	def __init__(self, base_url: str = settings.ollama_base_url, model: str = settings.ollama_model):
		self.base_url = base_url.rstrip("/")
		self.model = model

	def generate(self, prompt: str) -> str | None:
		payload = json.dumps({"model": self.model, "prompt": prompt, "stream": False}).encode()
		request = Request(f"{self.base_url}/api/generate", data=payload, headers={"Content-Type": "application/json"})
		try:
			with urlopen(request, timeout=45) as response:
				return json.loads(response.read().decode()).get("response")
		except Exception:
			return None
