from agents.base_agent import SpecialistAgent


class HRAgent(SpecialistAgent):
    name = "HR Agent"
    focus = "team capability, hiring plan, incentives, and people risks"
    concern_terms = ("hiring", "talent", "retention", "headcount", "founder")
    strength_terms = ("team", "experience", "hiring", "advisor")