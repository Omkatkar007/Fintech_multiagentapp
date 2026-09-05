"""Streamlit UI and programmatic entry point for proposal review."""

import argparse
import json
from pathlib import Path
import pandas as pd

from services.orchestrator import ProposalOrchestrator
from services.report_generator import build_report


def review_proposal(source, filename: str = "proposal") -> dict:
	return ProposalOrchestrator().review(source, filename)


def main() -> None:
	parser = argparse.ArgumentParser(description="Review a business proposal with specialist agents.")
	parser.add_argument("proposal", nargs="?", help="Path to a PDF or text proposal")
	parser.add_argument("--report", default="risk_assessment.pdf")
	args = parser.parse_args()
	if args.proposal:
		result = review_proposal(args.proposal, Path(args.proposal).name)
		Path(args.report).write_bytes(build_report(Path(args.proposal).name, result["agents"], result["decision"]))
		print(json.dumps(result["decision"], indent=2))
		return
	try:
		import streamlit as st
	except ImportError as exc:
		raise SystemExit("Install requirements.txt or provide a proposal path on the command line.") from exc
	st.set_page_config(page_title="Proposal Review Committee", page_icon="P", layout="wide")
	st.title("Business Proposal Review Committee")
	st.caption("Upload a proposal to run market, finance, legal, technology, HR, GTM, ESG, and risk reviews.")
	
	upload_mode = st.radio("Upload Mode", ["Single File Upload", "Bulk Folder Upload"], horizontal=True)

	if upload_mode == "Single File Upload":
		uploaded = st.file_uploader("Business proposal PDF, DOCX, or text file", type=["pdf", "docx", "txt", "md"])
		if uploaded and st.button("Run review", type="primary"):
			with st.spinner("Agents are reviewing the proposal..."):
				result = review_proposal(uploaded.getvalue(), uploaded.name)
			decision = result["decision"]
			st.subheader(f"{decision['decision']} (Score: {decision.get('score', 100)}/100)")
			st.write(decision["rationale"])
			cols = st.columns(4)
			for index, item in enumerate(result["agents"]):
				with cols[index % 4]:
					st.metric(item["agent"], item["risk_level"].upper())
			with st.expander("Conditions and priority risks"):
				st.write(decision["conditions"] or decision["priority_risks"])
			pdf = build_report(uploaded.name, result["agents"], decision)
			st.download_button("Download PDF risk assessment", pdf, "risk_assessment.pdf", "application/pdf")
			
	else:
		uploaded_files = st.file_uploader("Upload multiple PDF, DOCX, or text files", type=["pdf", "docx", "txt", "md"], accept_multiple_files=True)
		if uploaded_files and st.button("Run Bulk Review", type="primary"):
			results_data = []
			
			progress_bar = st.progress(0)
			status_text = st.empty()
			
			for i, file in enumerate(uploaded_files):
				status_text.text(f"Processing {file.name} ({i+1}/{len(uploaded_files)})...")
				try:
					result = review_proposal(file.getvalue(), file.name)
					decision = result["decision"]
					results_data.append({
						"Filename": file.name,
						"Score (%)": decision.get("score", 100),
						"Decision": decision["decision"]
					})
				except Exception as e:
					results_data.append({
						"Filename": file.name,
						"Score (%)": 0,
						"Decision": f"Failed: {str(e)}"
					})
				progress_bar.progress((i + 1) / len(uploaded_files))
				
			status_text.text("Bulk review complete!")
			df = pd.DataFrame(results_data)
			st.dataframe(df, width='stretch')
			
			csv = df.to_csv(index=False).encode('utf-8')
			st.download_button(
				label="Download Results as CSV",
				data=csv,
				file_name='bulk_review_results.csv',
				mime='text/csv',
			)

if __name__ == "__main__":
	main()
