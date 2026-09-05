from agents.base_agent import SpecialistAgent


class MarketAgent(SpecialistAgent):
	name = "Market Agent"
	focus = "market size, customer demand, competition, and pricing"
	concern_terms = ("competition", "market share", "customer validation", "pricing")
	strength_terms = ("customer", "market", "revenue", "pricing")
