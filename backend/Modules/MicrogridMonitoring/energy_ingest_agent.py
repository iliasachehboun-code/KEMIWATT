import os
from textwrap import dedent
from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.models.mistral import MistralChat
from Guardrails.data_guardrails import validate_data_integrity
from Guardrails.prompt_guardrails import detect_prompt_injection
from Tools.microgrid_tools import (
    BUILTIN_TOOLS,
    load_microgrid_data,
    validate_microgrid_schema,
    clean_microgrid_data,
    save_clean_data,
    log_guardrail_event
)
from dotenv import load_dotenv
load_dotenv()


def create_energy_ingest_agent(model=None):
    db_url = os.getenv("DB_URL", "postgresql+psycopg://ai:ai@localhost:5532/ai")
    mistral_api_key = os.getenv("MISTRAL_API_KEY")

    db = PostgresDb(db_url=db_url, memory_table="energy_ingest_memory")

    EnergyIngestAgent = Agent(
        name="Energy Ingest Agent",
        role="Collect, validate, and clean microgrid sensor data for downstream analysis.",
        description=dedent("""
        The Energy Ingest Agent loads raw microgrid data from CSV or APIs, 
        validates schema integrity, cleans missing or duplicated data, 
        and saves the standardized dataset for other agents to use.
        """),
        model=MistralChat(id="mistral-large-latest", api_key=mistral_api_key),
        tools=BUILTIN_TOOLS + [
            load_microgrid_data,
            validate_microgrid_schema,
            clean_microgrid_data,
            save_clean_data,
            log_guardrail_event
        ],
        instructions=dedent("""
        1. Load the microgrid CSV data using `load_microgrid_data`.
        2. Validate its structure via `validate_microgrid_schema`.
        3. Clean data using `clean_microgrid_data`.
        4. Save the result with `save_clean_data`.
        5. Log any validation or missing data issues using `log_guardrail_event`.
        6. Always confirm completion in Markdown format.
        """),
        db=db,
        enable_agentic_memory=True,
        markdown=True,
    )
    return EnergyIngestAgent
