"""
LESSON 08: Internal Data Connectivity (The MCP Pattern)
DESCRIPTION: Grounding the agent in internal company data using a 
standardized connector pattern.
WHY THIS IS IMPORTANT: To be a differentiator, an agent must know your 
unique business context (e.g., current active projects, internal KPIs). 
This lesson simulates the Model Context Protocol (MCP) to bridge the 
gap between the LLM and your private "Strategy Knowledge Base."
"""

import asyncio
from google.adk.agents import Agent
from google.genai import types 
from config.settings import get_model, get_runner, initialize_session, cleanup

# 1. Define the "Internal Knowledge Base" Connector
# In a production MCP setup, this would query a SQL DB or a Vector Store.
async def query_strategy_kb(query_term: str) -> str:
    """
    Queries the internal Strategy Knowledge Base for project status and KPIs.
    Args:
        query_term: The project name or KPI to look up.
    """
    # Simulated internal data repository
    internal_kb = {
        "Project_Alpha": "Status: Delayed. Risk: Integration hurdles. Budget: $1.2M.",
        "Cloud_Migration": "Status: On Track. Savings: $300k YTD. Completion: 65%.",
        "Cyber_Shield": "Status: Planning. Priority: High. Launch: Q3 2026."
    }
    
    result = internal_kb.get(query_term, "No internal record found. Suggesting general best practices instead.")
    return f"[INTERNAL DATA] {query_term}: {result}"

async def main():
    # 2. Setup the Internal Strategy Agent
    # We instruct the agent to ALWAYS check internal data before answering.
    internal_agent = Agent(
        name="Internal_Advisor",
        instruction="""You are a Strategic Advisor. 
        Before providing advice on any project, use the query_strategy_kb tool 
        to verify our internal status. If data is found, prioritize it over 
        general model knowledge.""",
        model=get_model(),
        tools=[query_strategy_kb] 
    )

    runner = get_runner(internal_agent)
    user_id, session_id = await initialize_session()
    
    # 3. The Internal Query
    user_query = "Should we reallocate resources from Project Alpha to the Cloud Migration?"
    content = types.Content(role="user", parts=[types.Part(text=user_query)])
    
    print(f"--- ACCESSING INTERNAL KNOWLEDGE BASE ({session_id}) ---")
    print(f"Inquiry: {user_query}\n")
    
    # 4. Execute
    events = runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=content
    )
    
    print("--- INTERNAL STRATEGY ADVICE ---")
    async for event in events:
        if event.is_final_response():
            print(event.content.parts[0].text)

    await cleanup()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass