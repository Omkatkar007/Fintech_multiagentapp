# Multi-Agent Business Proposal Reviewer

Upload a business proposal PDF and receive independent market, finance, legal, technology, HR, GTM, ESG, and risk findings followed by a committee decision: **Approve**, **Reject**, or **Conditional Approval**.

## Run the app

```bash
pip install -r requirements.txt
streamlit run app.py
```

For automation or a quick local smoke test:

```bash
python app.py path/to/proposal.pdf --report risk_assessment.pdf
```

The default implementation uses local hashed embeddings and deterministic reviews. Set `OLLAMA_BASE_URL` and `OLLAMA_MODEL` and pass an Ollama client to `ProposalOrchestrator` when LLM-backed narrative output is desired.
