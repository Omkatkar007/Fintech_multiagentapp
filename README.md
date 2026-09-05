# 📊 RiskSight AI

**Live Demo**: [https://risksightai.streamlit.app/](https://risksightai.streamlit.app/)

Upload a business proposal PDF and receive independent market, finance, legal, technology, HR, GTM, ESG, and risk findings followed by a committee decision: **Approve**, **Reject**, or **Conditional Approval**.

---

## 🛡️ Multi-Agent Review System

| Agent | Responsibility |
|-------|----------------|
| **Market** | Evaluates market sizing, trends, and competition |
| **Finance** | Analyzes revenue projections and financial health |
| **Legal** | Identifies compliance and regulatory risks |
| **Technology** | Assesses technical feasibility and architecture |
| **HR** | Reviews team composition and hiring plans |
| **GTM** | Evaluates Go-To-Market strategy and sales channels |
| **ESG** | Checks environmental, social, and governance impact |
| **Risk** | Consolidates vulnerabilities into a final risk score |

---

## 💻 Tech Stack

| Component | Technology |
|-----------|-----------|
| **Frontend UI** | Streamlit |
| **Backend Orchestration** | Python (Concurrent Futures) |
| **LLM Provider** | Groq Cloud / Ollama |
| **PDF Parsing** | PyPDF, python-docx |
| **Report Generation**| ReportLab |
| **Data Processing** | Pandas |

---

## 📂 Project Structure

```
RiskSight_AI/
├── app.py                     # Streamlit frontend & CLI entry point
├── config.py                  # Environment and settings configuration
├── requirements.txt           # Python dependencies
├── .env                       # API keys (not committed)
├── agents/                    # Specialist agent definitions
│   ├── base_agent.py          # Base class for all agents
│   ├── committee_agent.py     # Final decision maker
│   └── ... (finance, legal, etc.)
├── models/                    # LLM client integrations
│   ├── llm_client.py          # Groq integration
│   └── ollama_client.py       # Local Ollama integration
└── services/                  # Core orchestration and utilities
    ├── orchestrator.py        # Manages agent concurrency
    ├── pdf_loader.py          # Document parsing
    ├── report_generator.py    # PDF report building
    └── vector_store.py        # Embeddings and search
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- A free [Groq API Key](https://console.groq.com) or local [Ollama](https://ollama.com/) instance

### 1. Clone & Install

```bash
git clone https://github.com/YOUR_USERNAME/RiskSight_AI.git
cd RiskSight_AI
python -m venv .venv
# Windows
.venv\Scripts\activate        
# macOS/Linux
# source .venv/bin/activate   
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file in the project root:

```env
# Groq LLM API
GROQ_API_KEY=your-groq-api-key
LLM_MODEL=llama-3.1-70b-versatile

# (Optional) Local Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3
```

### 3. Run Locally (Streamlit UI)

```bash
streamlit run app.py
```

Open **http://localhost:8501** in your browser.

### 4. Run Locally (CLI Automation)

For automation or a quick local smoke test without the UI:

```bash
python app.py path/to/proposal.pdf --report risk_assessment.pdf
```

---



---

<div align="center">

**Built for financial committees who need comprehensive, unbiased proposal reviews.**

*RiskSight AI — Because every investment decision needs a 360° perspective.*

</div>
