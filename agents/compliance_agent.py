from agents.base_agent import SpecialistAgent


class ComplianceAgent(SpecialistAgent):
	name = "Legal Agent"
	focus = "regulatory obligations, contracts, privacy, and legal exposure"
	concern_terms = ("regulatory", "compliance", "privacy", "license", "contract")
	strength_terms = ("policy", "license", "compliance", "contract")
