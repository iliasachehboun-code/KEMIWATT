import os
from textwrap import dedent
from agno.agent import Agent
from agno.db.postgres import PostgresDb
from Guardrails.data_guardrails import validate_data_integrity
from Guardrails.prompt_guardrails import detect_prompt_injection
from agno.models.mistral import MistralChat
from Tools.microgrid_tools import (
    BUILTIN_TOOLS,
    detect_outliers,
    load_microgrid_data,
    log_guardrail_event
)
from dotenv import load_dotenv
load_dotenv()


def create_anomaly_detection_agent(model=None):
    db_url = os.getenv("DB_URL", "postgresql+psycopg://ai:ai@localhost:5532/ai")
    mistral_api_key = os.getenv("MISTRAL_API_KEY")

    db = PostgresDb(db_url=db_url, memory_table="anomaly_detection_memory")

    AnomalyDetectionAgent = Agent(
        name="Anomaly Detection Agent",
        role="Identify abnormal energy readings and detect outliers from processed microgrid data.",
        description=dedent("""
        The Anomaly Detection Agent analyzes cleaned sensor data to find anomalies such as
        abnormal temperature spikes, low voltage, or irregular power drops.
        It uses statistical methods (Z-score) and logs anomalies for system reliability.
        """),
        model=MistralChat(id="mistral-large-latest", api_key=mistral_api_key),
        tools=BUILTIN_TOOLS + [
            load_microgrid_data,
            detect_outliers,
            log_guardrail_event
        ],
        instructions=dedent("""
        1. Load the processed dataset using `load_microgrid_data`.
        2. Use `detect_outliers` to detect extreme temperature, voltage, or power readings.
        3. Log any anomaly events using `log_guardrail_event`.
        4. Return a Markdown summary of the anomalies found.
        """),
        db=db,
        enable_agentic_memory=True,
        markdown=True,
    )
    return AnomalyDetectionAgent
