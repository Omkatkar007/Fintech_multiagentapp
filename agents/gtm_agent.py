from agents.base_agent import SpecialistAgent


class GTMAgent(SpecialistAgent):
	name = "GTM Agent"
	focus = "go-to-market plan, sales channels, adoption, and execution"
	concern_terms = ("sales", "channel", "adoption", "marketing", "pilot")
	strength_terms = ("pilot", "partnership", "sales", "customer")
