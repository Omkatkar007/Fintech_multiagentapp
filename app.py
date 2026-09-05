import streamlit as st
import pdfplumber
import docx
from crewai import Agent, Task, Crew, Process
from langchain_community.llms import Ollama

st.set_page_config(page_title="Agentic Credit Floor", layout="wide")

st.title("The Agentic Credit Floor - Multi-Agent Commercial Loan Underwriting")
st.write("Upload a commercial loan proposal to automatically underwrite it using 8 specialist AI agents.")

# Config for Ollama
model_name = st.sidebar.text_input("Local Ollama Model Name", value="llama3")

def read_pdf(file):
    with pdfplumber.open(file) as pdf:
        text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
    return text

def read_docx(file):
    doc = docx.Document(file)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

uploaded_file = st.file_uploader("Upload Proposal File (PDF/DOCX/TXT)", type=["pdf", "docx", "txt"])

if uploaded_file is not None:
    st.info("File uploaded successfully. Reading content...")
    
    file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type}
    
    if uploaded_file.name.endswith('.pdf'):
        proposal_text = read_pdf(uploaded_file)
    elif uploaded_file.name.endswith('.docx'):
        proposal_text = read_docx(uploaded_file)
    else:
        proposal_text = uploaded_file.read().decode("utf-8")
        
    st.text_area("Proposal Preview", proposal_text[:1000] + "...", height=200)
    
    if st.button("Run Agentic Underwriting"):
        with st.spinner("Initializing Agents and analyzing proposal..."):
            
            llm = Ollama(model=model_name)
            
            # Define Agents
            market_agent = Agent(
                role='Market Specialist',
                goal='Analyze customer, market, and user base evidence.',
                backstory='Expert in market sizing, competition validation, and pricing strategy.',
                verbose=True,
                allow_delegation=False,
                llm=llm
            )

            financial_agent = Agent(
                role='Financial Specialist',
                goal='Analyze revenue, profit, and forecasts.',
                backstory='Expert in validating forecast models, cash flow, and underlying assumptions.',
                verbose=True,
                allow_delegation=False,
                llm=llm
            )

            legal_agent = Agent(
                role='Legal Specialist',
                goal='Analyze regulatory compliance, governance, and data privacy.',
                backstory='Expert in contractual agreements, privacy frameworks, and legal liabilities.',
                verbose=True,
                allow_delegation=False,
                llm=llm
            )

            tech_agent = Agent(
                role='Technology Specialist',
                goal='Analyze architectural concepts, platform feasibility, and security.',
                backstory='Expert in system scalability, technical debt, uptime, and cybersecurity.',
                verbose=True,
                allow_delegation=False,
                llm=llm
            )

            hr_agent = Agent(
                role='HR Specialist',
                goal='Analyze founder experience and team capability.',
                backstory='Expert in validating hiring plans, incentives, and people risks.',
                verbose=True,
                allow_delegation=False,
                llm=llm
            )

            gtm_agent = Agent(
                role='GTM Specialist',
                goal='Analyze partnerships, sales, and customer engagement.',
                backstory='Expert in sales strategy, distribution channels, and marketing plans.',
                verbose=True,
                allow_delegation=False,
                llm=llm
            )

            esg_agent = Agent(
                role='ESG Specialist',
                goal='Analyze sustainability and impact metrics.',
                backstory='Expert in environmental impact, social outcomes, and ethical standards.',
                verbose=True,
                allow_delegation=False,
                llm=llm
            )

            risk_agent = Agent(
                role='Risk Specialist',
                goal='Analyze mitigations, contingencies, and cross-functional downside risks.',
                backstory='Expert in enterprise risk, dependency validation, and control.',
                verbose=True,
                allow_delegation=False,
                llm=llm
            )

            # Define Tasks
            base_prompt = f"Analyze the following loan proposal text based on your domain of expertise.\n\nPROPOSAL:\n{proposal_text}\n\n"
            
            tasks = [
                Task(
                    description=base_prompt + "Identify strengths, validate competition/market share/pricing, and answer: What supporting evidence quantifies market size, customer demand, competition, and pricing? Output your findings clearly.",
                    agent=market_agent,
                    expected_output="A structured report detailing market strengths, concerns, and outstanding questions."
                ),
                Task(
                    description=base_prompt + "Identify strengths, validate forecast models/financial projections, and answer: What supporting evidence quantifies the revenue model, cash flow, underlying assumptions, and funding needs?",
                    agent=financial_agent,
                    expected_output="A structured report detailing financial strengths, concerns, and outstanding questions."
                ),
                Task(
                    description=base_prompt + "Identify strengths in compliance, validate regulatory compliance/governance standards/data privacy, and answer: What supporting evidence quantifies regulatory obligations, contractual agreements, privacy frameworks, and legal liabilities?",
                    agent=legal_agent,
                    expected_output="A structured report detailing legal strengths, concerns, and outstanding questions."
                ),
                Task(
                    description=base_prompt + "Identify strengths in architecture/feasibility/platform/security, validate system scalability/cybersecurity/infrastructure/integration, and answer: What supporting evidence quantifies system architecture, technical debt, uptime, security protocols, and timelines?",
                    agent=tech_agent,
                    expected_output="A structured report detailing technology strengths, concerns, and outstanding questions."
                ),
                Task(
                    description=base_prompt + "Identify strengths in experience, validate founders/team, and answer: What supporting evidence quantifies team capability, hiring plan, incentives, and people risks?",
                    agent=hr_agent,
                    expected_output="A structured report detailing HR strengths, concerns, and outstanding questions."
                ),
                Task(
                    description=base_prompt + "Identify strengths in partnerships/sales/engagement, validate sales strategy/distribution channels/marketing plan, and answer: What supporting evidence quantifies the go-to-market plan, sales channels, customer adoption, and execution strategy?",
                    agent=gtm_agent,
                    expected_output="A structured report detailing GTM strengths, concerns, and outstanding questions."
                ),
                Task(
                    description=base_prompt + "Identify strengths in sustainability/impact, validate social impact/ethical standards/sustainability targets, and answer: What supporting evidence quantifies environmental impact, social outcomes, governance frameworks, and long-term sustainability metrics?",
                    agent=esg_agent,
                    expected_output="A structured report detailing ESG strengths, concerns, and outstanding questions."
                ),
                Task(
                    description=base_prompt + "Identify strengths in mitigation/contingency/control, validate overall risks/dependencies/delays, and answer: What supporting evidence quantifies cross-functional downside risk, mitigations, and dependencies? Then, compile all preceding agents' findings into a FINAL LOAN APPROVAL DOCUMENT with a final risk assessment.",
                    agent=risk_agent,
                    expected_output="A comprehensive Final Loan Approval Document summarizing all domains and providing a final decision/risk assessment."
                )
            ]

            crew = Crew(
                agents=[market_agent, financial_agent, legal_agent, tech_agent, hr_agent, gtm_agent, esg_agent, risk_agent],
                tasks=tasks,
                verbose=True,
                process=Process.sequential
            )

            result = crew.kickoff()
            
            st.success("Analysis Complete!")
            st.markdown("### Final Loan Approval Document")
            st.markdown(result)
