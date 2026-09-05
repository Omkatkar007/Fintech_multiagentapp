from agents.base_agent import SpecialistAgent


class ESGAgent(SpecialistAgent):
    name = "ESG Agent"
    focus = "environmental impact, social outcomes, governance, and ethics"
    concern_terms = ("emission", "impact", "governance", "ethics", "sustainability")
    strength_terms = ("sustainable", "impact", "governance", "diversity")