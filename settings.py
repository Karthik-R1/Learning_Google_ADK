"""
FILE: config/settings.py
DESCRIPTION: Centralized configuration and service provider for the Strategy Suite.
"""
import os
import uuid
import logging
import warnings
import litellm  # Added for explicit cleanup

# Silence the Pydantic noise
os.environ["PYDANTIC_SKIP_VALIDATION"] = "1"
warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")

from google.adk.models.lite_llm import LiteLlm 
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner

from dotenv import load_dotenv
load_dotenv()

APP_NAME = "CIO_Strategy_Accelerator_2026"
OLLAMA_BASE_URL = os.getenv("OLLAMA_API_BASE", "http://localhost:11434")
MODEL_ID = os.getenv("MODEL_NAME", "ollama_chat/llama3.2")

_SESSION_SERVICE = InMemorySessionService()

def get_model():
    return LiteLlm(model=MODEL_ID, api_base=OLLAMA_BASE_URL)

def get_runner(agent):
    return Runner(agent=agent, app_name=APP_NAME, session_service=_SESSION_SERVICE)

async def initialize_session(user_id="strategy_pro"):
    session_id = str(uuid.uuid4())
    await _SESSION_SERVICE.create_session(app_name=APP_NAME, user_id=user_id, session_id=session_id)
    return user_id, session_id

async def cleanup():
    """FIX: Manually awaits the LiteLLM cleanup coroutine to stop the warning."""
    try:
        await litellm.close_litellm_async_clients()
    except Exception:
        pass