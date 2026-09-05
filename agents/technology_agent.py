from agents.base_agent import SpecialistAgent


class TechnologyAgent(SpecialistAgent):
	name = "Technology Agent"
	focus = "technical feasibility, security, scalability, and delivery risk"
	concern_terms = ("security", "scalability", "dependency", "technical debt", "integration")
	strength_terms = ("prototype", "platform", "architecture", "security")
