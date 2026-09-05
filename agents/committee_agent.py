from dataclasses import dataclass

from agents.base_agent import AgentResult


@dataclass
class CommitteeDecision:
	decision: str
	rationale: str
	conditions: list[str]
	priority_risks: list[str]
	score: int

	def to_dict(self) -> dict:
		return {
			"decision": self.decision,
			"rationale": self.rationale,
			"conditions": self.conditions,
			"priority_risks": self.priority_risks,
			"score": self.score,
		}


class CommitteeAgent:
	def decide(self, results: list[AgentResult]) -> CommitteeDecision:
		score = 100
		for result in results:
			if result.risk_level == "high":
				score -= 20
			elif result.risk_level == "medium":
				score -= 5
		score = max(0, score)

		high_risk = [result for result in results if result.risk_level == "high"]
		concerns = [concern for result in results for concern in result.concerns]
		priority = concerns[:6]
		if len(high_risk) >= 3:
			return CommitteeDecision("REJECT", "Multiple specialist reviews identified material unmitigated risks.", [], priority, score)
		if high_risk or len(concerns) >= 5:
			return CommitteeDecision("CONDITIONAL APPROVAL", "The proposal is potentially viable, subject to closing the identified evidence gaps.", concerns[:5], priority, score)
		return CommitteeDecision("APPROVE", "Specialist reviews found no material blockers in the supplied evidence.", [], priority, score)
