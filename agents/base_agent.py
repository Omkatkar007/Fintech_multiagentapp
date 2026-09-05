"""Shared specialist-agent behavior and result contract."""

from dataclasses import asdict, dataclass, field
import re

from models.llm_client import GroqClient
from models.prompts import REVIEW_PROMPT


@dataclass
class AgentResult:
    agent: str
    summary: str
    strengths: list[str] = field(default_factory=list)
    concerns: list[str] = field(default_factory=list)
    questions: list[str] = field(default_factory=list)
    risk_level: str = "medium"

    def to_dict(self) -> dict:
        return asdict(self)


class SpecialistAgent:
    name = "Specialist"
    focus = "overall business viability"
    concern_terms: tuple[str, ...] = ()
    strength_terms: tuple[str, ...] = ()

    def __init__(self, llm: GroqClient | None = None):
        self.llm = llm

    def review(self, context: str) -> AgentResult:
        if self.llm:
            generated = self.llm.generate(REVIEW_PROMPT.format(role=self.name, focus=self.focus, context=context[:7000]))
            if generated:
                return AgentResult(self.name, generated, risk_level="medium")
        lower = context.lower()
        strengths = [f"Evidence mentions {term}." for term in self.strength_terms if term in lower][:3]
        concerns = [f"Validate {term} before approval." for term in self.concern_terms if term in lower][:4]
        if not strengths:
            strengths = ["Proposal evidence was available for review."]
        if not concerns:
            concerns = [f"No explicit {self.focus} evidence was found in the extracted text."]
        risk = "high" if len(concerns) >= 3 else "medium" if concerns else "low"
        questions = [f"What supporting evidence quantifies {self.focus}?"]
        return AgentResult(self.name, f"{self.name} review completed against the proposal evidence.", strengths, concerns, questions, risk)


def terms_in(text: str, terms: tuple[str, ...]) -> list[str]:
    lower = text.lower()
    return [term for term in terms if re.search(rf"\b{re.escape(term)}\b", lower)]