import os
from textwrap import dedent
from agno.agent import Agent
from agno.db.postgres import PostgresDb
from Guardrails.data_guardrails import validate_data_integrity
from Guardrails.prompt_guardrails import detect_prompt_injection
from agno.models.mistral import MistralChat
from Tools.microgrid_tools import (
    BUILTIN_TOOLS,
    load_microgrid_data,
    generate_report_summary,
    log_guardrail_event
)
from dotenv import load_dotenv
load_dotenv()


def create_report_agent(model=None):
    db_url = os.getenv("DB_URL", "postgresql+psycopg://ai:ai@localhost:5532/ai")
    mistral_api_key = os.getenv("MISTRAL_API_KEY")

    db = PostgresDb(db_url=db_url, memory_table="report_memory")

    ReportAgent = Agent(
        name="Report Agent",
        role="Compile data summaries and generate Markdown performance reports.",
        description=dedent("""
        The Report Agent consolidates insights from all previous stages,
        generates performance summaries, and prepares Markdown reports 
        for engineers and decision-makers.
        """),
        model=MistralChat(id="mistral-large-latest", api_key=mistral_api_key),
        tools=BUILTIN_TOOLS + [
            load_microgrid_data,
            generate_report_summary,
            log_guardrail_event
        ],
        instructions=dedent("""
        1. Load processed microgrid data using `load_microgrid_data`.
        2. Generate a concise performance report with `generate_report_summary`.
        3. Log report generation events using `log_guardrail_event`.
        4. Output a clean Markdown summary ready for the Reports folder.
        """),
        db=db,
        enable_agentic_memory=True,
        markdown=True,
    )
    return ReportAgent
