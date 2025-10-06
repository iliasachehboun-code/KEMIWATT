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
    compute_efficiency,
    log_guardrail_event
)
from dotenv import load_dotenv
load_dotenv()


def create_optimization_agent(model=None):
    db_url = os.getenv("DB_URL", "postgresql+psycopg://ai:ai@localhost:5532/ai")
    mistral_api_key = os.getenv("MISTRAL_API_KEY")

    db = PostgresDb(db_url=db_url, memory_table="optimization_memory")

    OptimizationAgent = Agent(
        name="Optimization Agent",
        role="Optimize battery charge/discharge cycles and compute system efficiency metrics.",
        description=dedent("""
        The Optimization Agent reviews performance metrics and calculates
        overall system efficiency. It provides actionable recommendations 
        for improving load balancing and charge cycle management.
        """),
        model=MistralChat(id="mistral-large-latest", api_key=mistral_api_key),
        tools=BUILTIN_TOOLS + [
            load_microgrid_data,
            compute_efficiency,
            log_guardrail_event
        ],
        instructions=dedent("""
        1. Load the processed dataset using `load_microgrid_data`.
        2. Compute the overall system efficiency using `compute_efficiency`.
        3. Analyze energy distribution, suggest optimization steps.
        4. Log warnings or performance degradations using `log_guardrail_event`.
        5. Return a concise Markdown optimization report.
        """),
        db=db,
        enable_agentic_memory=True,
        markdown=True,
    )
    return OptimizationAgent
