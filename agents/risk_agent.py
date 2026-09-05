from agents.base_agent import SpecialistAgent


class RiskAgent(SpecialistAgent):
	name = "Risk Agent"
	focus = "cross-functional downside risk, mitigations, and dependencies"
	concern_terms = ("risk", "dependency", "uncertain", "delay", "concentration")
	strength_terms = ("mitigation", "contingency", "insurance", "control")
