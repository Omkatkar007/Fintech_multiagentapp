from agents.base_agent import SpecialistAgent


class FinanceAgent(SpecialistAgent):
	name = "Financial Agent"
	focus = "revenue model, cash flow, assumptions, and funding needs"
	concern_terms = ("cash flow", "burn", "debt", "assumption", "forecast")
	strength_terms = ("revenue", "profit", "cash flow", "forecast")
