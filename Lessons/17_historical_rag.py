"""
LESSON 17: Long-Term Memory (Historical RAG)
DESCRIPTION: Using an external vector-style lookup to inform current decisions.
WHY THIS IS IMPORTANT: Strategy is iterative. If your company failed at a 
Cloud migration in 2023, the 2026 AI agent should know WHY. This script 
demonstrates how to "Retrieve" historical lessons before "Generating" 
new strategic advice.
"""

import asyncio
from google.adk.agents import Agent
from google.genai import types 
from config.settings import get_model, get_runner, initialize_session, cleanup

# 1. Define the "Lessons Learned" Repository
# In production, this would be a Vector Database (Chroma, Pinecone, or BigQuery)
async def fetch_historical_lessons(topic: str) -> str:
    """
    Retrieves historical 'Post-Mortem' data from previous years.
    Args:
        topic: The strategic area (e.g., 'Cloud', 'Data', 'ERP').
    """
    archive = {
        "Cloud": "2023 POST-MORTEM: Migration delayed 6 months due to 'Egress Cost' miscalculations.",
        "Data": "2024 AUDIT: Data Lake became a 'Data Swamp' due to lack of tagging standards.",
        "ERP": "2022 LESSON: Customizations made the core system un-upgradeable."
    }
    return archive.get(topic, "No specific historical failure recorded for this topic.")

async def main():
    # 2. Setup the "Wise" Agent
    # We instruct it to check history before suggesting anything new.
    wise_agent = Agent(
        name="Historical_Strategist",
        instruction="""You are a Senior Strategy Advisor. 
        Before recommending a path forward, use the fetch_historical_lessons tool. 
        If a past failure is found, explicitly explain how your new 
        plan avoids that specific pitfall.""",
        model=get_model(),
        tools=[fetch_historical_lessons]
    )

    runner = get_runner(wise_agent)
    user_id, session_id = await initialize_session()
    
    # 3. The Query: Re-attempting a Cloud strategy
    user_query = "Draft a plan for our 2026 Multi-Cloud expansion."
    content = types.Content(role="user", parts=[types.Part(text=user_query)])
    
    print(f"--- CONSULTING HISTORICAL ARCHIVES ---")
    print(f"Topic: {user_query}\n")
    
    # 4. Execute
    events = runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=content
    )
    
    print("--- 2026 STRATEGY (INFORMED BY HISTORY) ---")
    async for event in events:
        if event.is_final_response():
            print(event.content.parts[0].text)

    await cleanup()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass