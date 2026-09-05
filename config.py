"""Application configuration loaded from environment variables."""

from dataclasses import dataclass
import os
from pathlib import Path


@dataclass(frozen=True)
class Settings:
	groq_api_key: str = os.getenv("GROQ_API_KEY", "")
	llm_model: str = os.getenv("LLM_MODEL", "llama-3.1-70b-versatile")
	data_dir: Path = Path(os.getenv("DATA_DIR", ".data"))
	chunk_size: int = int(os.getenv("CHUNK_SIZE", "1200"))
	chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "180"))


settings = Settings()
