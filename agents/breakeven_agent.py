from agents.base_agent import SpecialistAgent


class BreakevenAgent(SpecialistAgent):
	name = "Breakeven Agent"
	focus = "unit economics, break-even volume, and sensitivity to assumptions"
	concern_terms = ("break-even", "margin", "cost", "fixed cost", "unit economics")
	strength_terms = ("margin", "break-even", "gross profit", "unit economics")
