"""End-to-end proposal review orchestration."""

import concurrent.futures

from agents.base_agent import SpecialistAgent
from agents.committee_agent import CommitteeAgent
from agents.compliance_agent import ComplianceAgent
from agents.document_agent import DocumentAgent
from agents.esg_agent import ESGAgent
from agents.finance_agent import FinanceAgent
from agents.gtm_agent import GTMAgent
from agents.hr_agent import HRAgent
from agents.market_agent import MarketAgent
from agents.risk_agent import RiskAgent
from agents.technology_agent import TechnologyAgent
from models.llm_client import GroqClient
from services.vector_store import VectorStore
from config import settings


class ProposalOrchestrator:
    def __init__(self, llm=None):
        if llm is None and settings.groq_api_key:
            llm = GroqClient()
            
        self.document_agent = DocumentAgent()
        self.agents: list[SpecialistAgent] = [
            MarketAgent(llm), FinanceAgent(llm), ComplianceAgent(llm), TechnologyAgent(llm),
            HRAgent(llm), GTMAgent(llm), ESGAgent(llm), RiskAgent(llm),
        ]
        self.committee = CommitteeAgent()

    def review(self, source, filename: str = "proposal") -> dict:
        text, chunks = self.document_agent.process(source, filename)
        if not text.strip():
            raise ValueError("The proposal did not contain extractable text.")
        index = VectorStore()
        index.add(chunks, {"filename": filename})
        context = "\n\n".join(result.text for result in index.search("business proposal financial market risk technology team compliance", 8))
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = list(executor.map(lambda agent: agent.review(context), self.agents))
            
        decision = self.committee.decide(results)
        return {"filename": filename, "text_length": len(text), "chunks": len(chunks), "agents": [result.to_dict() for result in results], "decision": decision.to_dict()}