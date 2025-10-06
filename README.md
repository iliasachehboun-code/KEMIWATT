#  KEMIWATT Microgrid Monitoring 

An **AI-powered multi-agent system** designed to monitor, analyze, and optimize microgrid operations for **Kemiwatt** using the **Agno framework** with integrated **Guardrails** for safety, compliance, and data integrity.

---

## 🧭 Overview

The **Microgrid Monitoring OS** automates the analysis pipeline for energy data.  
It uses intelligent agents to **ingest**, **validate**, **detect anomalies**, **optimize performance**, and **generate reports** — all with built-in guardrails to ensure trustworthy AI behavior.

---

## 🧩 System Architecture

```mermaid
flowchart TD
    A[Energy CSV Data] --> B[Energy Ingest Agent]
    B --> C[Anomaly Detection Agent]
    C --> D[Optimization Agent]
    D --> E[Report Agent]
    subgraph Guardrails
        F1[Data Guardrails]
        F2[Log Guardrails]
        F3[Prompt Guardrails]
    end
    B --> F1
    C --> F2
    D --> F3
    E --> |Markdown Report| G[Reports/microgrid_report.md]
🧠 Agents & Responsibilities
Agent	Role	Key Inputs	Outputs
Energy Ingest Agent	Loads and validates CSV data	sample_microgrid_data.csv	Clean structured dataset
Anomaly Detection Agent	Detects outliers or irregular readings	Clean dataset	List of anomalies
Optimization Agent	Analyzes patterns and suggests optimizations	Validated dataset	Efficiency metrics & recommendations
Report Agent	Summarizes insights into a Markdown report	All previous agent outputs	Reports/microgrid_report.md

🛡️ Guardrails Layer
Guardrail	Description
Data Guardrails	Validates timestamps, checks missing or negative readings, enforces numeric consistency
Prompt Guardrails	Detects prompt injections, sensitive data leaks, and unsafe instructions
Log Guardrails	Tracks agent activity, ensures auditability, and stores secure logs in /Reports/logs/

Each guardrail ensures reliability, reproducibility, and alignment with Kemiwatt’s data-governance policies.

⚙️ Project Structure

backend/
│
├── Guardrails/
│   ├── data_guardrails.py
│   ├── log_guardrails.py
│   ├── prompt_guardrails.py
│
├── Modules/
│   └── MicrogridMonitoring/
│       ├── energy_ingest_agent.py
│       ├── anomaly_detection_agent.py
│       ├── optimization_agent.py
│       ├── report_agent.py
│
├── Tools/
│   └── microgrid_tools.py
│
├── Reports/
│   ├── logs/
│   └── microgrid_report.md
│
├── sample_microgrid_data.csv
├── .env
├── Pipfile
└── main.py
🚀 Running the System
1️⃣ Set up your environment
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
2️⃣ Configure your .env
OPENAI_API_KEY=sk-xxxx
MISTRAL_API_KEY=xxxxxxxx
3️⃣ Launch the OS
python backend/main.py
💡 Tip: The system automatically creates logs in backend/Reports/logs/system.log
and a Markdown report in backend/Reports/microgrid_report.md

📊 Example Outputs
Stage	Description	Output
Stage 1	Data ingestion and validation	“✅ Clean dataset with 1000 records.”
Stage 2	Anomaly detection	“⚠️ 3 anomalies detected in power readings.”
Stage 3	Optimization	“Suggested 8% reduction in power load imbalance.”
Stage 4	Report generation	“Report successfully generated in Markdown format.”

🧱 Tech Stack
Framework: Agno 2.1.1

LLMs: OpenAI GPT-4o / Mistral-Large

Database: PostgreSQL or local SQLite (optional)

Language: Python 3.12+

Environment: .env + Pipfile

🔒 Compliance & Safety
All modules follow strict Guardrail-Driven Development (GDD) principles:

PII masking

Prompt injection detection

Bias & toxicity filters

Data integrity validation

Ensuring every AI action remains transparent, compliant, and auditable.

