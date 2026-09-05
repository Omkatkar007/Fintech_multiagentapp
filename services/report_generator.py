"""Generate a portable PDF decision report."""

from datetime import datetime, timezone
from io import BytesIO


def build_report(proposal_name: str, agent_results: list[dict], decision: dict) -> bytes:
	try:
		from reportlab.lib.pagesizes import letter
		from reportlab.lib.styles import getSampleStyleSheet
		from reportlab.lib.units import inch
		from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
		from reportlab.lib import colors
	except ImportError as exc:
		raise RuntimeError("PDF export requires reportlab. Install requirements.txt.") from exc

	stream = BytesIO()
	document = SimpleDocTemplate(stream, pagesize=letter, rightMargin=0.65 * inch, leftMargin=0.65 * inch)
	styles = getSampleStyleSheet()
	story = [Paragraph("Business Proposal Risk Assessment", styles["Title"]),
			 Paragraph(f"{proposal_name} | Generated {datetime.now(timezone.utc):%Y-%m-%d %H:%M UTC}", styles["Normal"]), Spacer(1, 16)]
	decision_color = colors.green if decision["decision"] == "APPROVE" else colors.orange if "CONDITIONAL" in decision["decision"] else colors.red
	score_str = f" (Score: {decision.get('score', 100)}/100)"
	story.append(Table([[Paragraph(f"<b>Decision: {decision['decision']}{score_str}</b>", styles["Heading2"])]], style=TableStyle([("BACKGROUND", (0, 0), (-1, -1), decision_color), ("TEXTCOLOR", (0, 0), (-1, -1), colors.white), ("BOX", (0, 0), (-1, -1), 0, decision_color), ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10)])))
	story += [Spacer(1, 8), Paragraph(decision["rationale"], styles["BodyText"])]
	if decision["conditions"]:
		story.append(Paragraph("Conditions", styles["Heading2"]))
		story.extend(Paragraph(f"- {condition}", styles["BodyText"]) for condition in decision["conditions"])
	story.append(Paragraph("Specialist Findings", styles["Heading2"]))
	for result in agent_results:
		story.append(Paragraph(f"<b>{result['agent']} - {result['risk_level'].upper()} RISK</b>", styles["Heading3"]))
		story.append(Paragraph(result["summary"], styles["BodyText"]))
		for label in ("strengths", "concerns", "questions"):
			if result[label]:
				story.append(Paragraph(f"<b>{label.title()}:</b> " + "; ".join(result[label]), styles["BodyText"]))
		story.append(Spacer(1, 6))
	document.build(story)
	return stream.getvalue()
