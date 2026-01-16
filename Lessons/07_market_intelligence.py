"""
LESSON 07: Market Intelligence (Search Tools)
DESCRIPTION: Connecting the agent to real-time external data sources.
WHY THIS IS IMPORTANT: Strategy is dynamic. An agent with a 2024 training 
cutoff cannot advise on 2026 market shifts. This script demonstrates how 
to give the agent a "Web Search" tool to fetch live innovation trends.
"""

import asyncio
from google.adk.agents import Agent
from google.genai import types 
from config.settings import get_model, get_runner, initialize_session, cleanup

# 1. Define the Market Intelligence Tool
# In a real scenario, you would use 'requests' to call a search API.
async def search_market_trends(industry: str) -> str:
    """
    Fetches the latest innovation and technology trends for a specific industry.
    Args:
        industry: The sector to research (e.g., 'Banking', 'Supply Chain').
    """
    # Mocking a real API response for demonstration
    # Replace this with a real API call (e.g., Serper.dev or Tavily)
    trends = {
        "Banking": "Trend: Rise of 'Agentic Banking' assistants. Differentiator: Hyper-personalization.",
        "Supply Chain": "Trend: Autonomous logistics orchestration. Differentiator: Real-time rerouting.",
        "Healthcare": "Trend: Generative diagnostics. Differentiator: Reduced clinician burnout."
    }
    
    result = trends.get(industry, "Trend: Increased focus on Agentic AI integration across all sectors.")
    return f"Latest Research for {industry}: {result}"

async def main():
    # 2. Setup the Research Agent
    research_agent = Agent(
        name="Market_Analyst",
        instruction="""You are a Market Intelligence Analyst. 
        When asked about industry trends, use the search_market_trends tool. 
        Synthesize the search results into a strategic 'Opportunity vs. Threat' summary.""",
        model=get_model(),
        tools=[search_market_trends] 
    )

    runner = get_runner(research_agent)
    user_id, session_id = await initialize_session()
    
    # 3. The Research Query
    user_query = "What is the biggest differentiator in the Banking sector regarding AI for 2026?"
    content = types.Content(role="user", parts=[types.Part(text=user_query)])
    
    print(f"--- FETCHING MARKET INTELLIGENCE ({session_id}) ---")
    print(f"Researching: {user_query}\n")
    
    # 4. Execute
    events = runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=content
    )
    
    print("--- STRATEGIC RESEARCH BRIEF ---")
    async for event in events:
        if event.is_final_response():
            print(event.content.parts[0].text)

    await cleanup()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass