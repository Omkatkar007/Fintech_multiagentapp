"""Groq API client."""

import json
from urllib.request import Request, urlopen

from config import settings


class GroqClient:
	def __init__(self, api_key: str = settings.groq_api_key, model: str = settings.llm_model):
		self.api_key = api_key
		self.model = model

	def generate(self, prompt: str) -> str | None:
		if not self.api_key:
			return None
			
		payload = json.dumps({
			"model": self.model,
			"messages": [{"role": "user", "content": prompt}],
			"temperature": 0.2
		}).encode()
		
		request = Request(
			"https://api.groq.com/openai/v1/chat/completions",
			data=payload,
			headers={"Content-Type": "application/json", "Authorization": f"Bearer {self.api_key}"}
		)
		
		try:
			with urlopen(request, timeout=45) as response:
				data = json.loads(response.read().decode())
				return data["choices"][0]["message"]["content"]
		except Exception as e:
			print(f"LLM Error: {e}")
			return None
