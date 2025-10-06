

import os
from textwrap import dedent


os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
os.environ["MISTRAL_API_KEY"] = MISTRAL_API_KEY

USE_MODEL = "openai" 

from agno.team import Team
from agno.models.openai import OpenAIChat
from agno.models.mistral import MistralChat

if USE_MODEL == "openai":
    model = OpenAIChat(id="gpt-4o", api_key=OPENAI_API_KEY)
    print(" Using OpenAI model: gpt-4o")
elif USE_MODEL == "mistral":
    model = MistralChat(id="mistral-large-latest", api_key=MISTRAL_API_KEY)
    print(" Using Mistral model: mistral-large-latest")
else:
    raise ValueError(" Invalid model choice. Set USE_MODEL to 'openai' or 'mistral'.")

os.makedirs("backend/Reports", exist_ok=True)
os.makedirs("backend/Tools", exist_ok=True)
os.makedirs("backend/Reports/logs", exist_ok=True)

from Modules.MicrogridMonitoring.energy_ingest_agent import create_energy_ingest_agent
from Modules.MicrogridMonitoring.anomaly_detection_agent import create_anomaly_detection_agent
from Modules.MicrogridMonitoring.optimization_agent import create_optimization_agent
from Modules.MicrogridMonitoring.report_agent import create_report_agent


def create_microgrid_team():
    """
    Creates a team of 4 agents for data ingestion, anomaly detection,
    optimization, and reporting. Each has its own guardrails & DB memory.
    """
    ingest_agent = create_energy_ingest_agent(model=model)
    anomaly_agent = create_anomaly_detection_agent(model=model)
    optimize_agent = create_optimization_agent(model=model)
    report_agent = create_report_agent(model=model)

    team = Team(
        members=[
            ingest_agent,
            anomaly_agent,
            optimize_agent,
            report_agent,
        ],
        name="Kemiwatt Microgrid AI Team",
        description=dedent("""
        Multi-agent AI system that monitors, validates, and optimizes 
        energy performance for Kemiwatt’s microgrid. Each agent applies 
        guardrails for data integrity, safety, and explainability.
        """),
    )

    return team


def print_stage(title: str, color: str = "cyan"):
    """Pretty print stage titles with colors."""
    colors = {
        "cyan": "\033[96m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "red": "\033[91m",
        "reset": "\033[0m",
    }
    print(f"{colors.get(color, '')}{title}{colors['reset']}")


def run_microgrid_pipeline():
    """Runs the full OS workflow in 4 stages."""
    team = create_microgrid_team()

    print("\n===================================================")
    print("⚡  KEMIWATT MICROGRID OS PIPELINE STARTED")
    print("===================================================\n")

    print_stage(" Stage 1 — Ingestion & Validation", "cyan")
    team.print_response("Load and validate the microgrid CSV data using guardrails.")
    print_stage(" Ingestion complete.\n", "green")

    print_stage(" Stage 2 — Anomaly Detection", "cyan")
    team.print_response("Analyze processed microgrid data and detect any anomalies.")
    print_stage(" Anomaly detection complete.\n", "green")

    print_stage(" Stage 3 — Optimization Analysis", "cyan")
    team.print_response("Compute system efficiency and propose optimization actions.")
    print_stage(" Optimization complete.\n", "green")

    print_stage(" Stage 4 — Report Generation", "cyan")
    team.print_response("Generate a Markdown summary report consolidating results.")
    print_stage(" Report generation complete.\n", "green")

    print("===================================================")
    print_stage("🏁 PIPELINE FINISHED SUCCESSFULLY", "yellow")
    print("Report available in backend/Reports/microgrid_report.md")
    print("===================================================\n")


if __name__ == "__main__":
    run_microgrid_pipeline()
