"""
LESSON 13: Usage Monitoring & Cost Control
DESCRIPTION: Tracking token consumption to calculate the "Cost per Insight."
WHY THIS IS IMPORTANT: Enterprise AI must be cost-effective. This script 
demonstrates how to extract usage metadata from the ADK response to monitor 
token spend, ensuring the Strategy Suite remains within its operational budget.
"""

import asyncio
from google.adk.agents import Agent
from google.genai import types 
from config.settings import get_model, get_runner, initialize_session, cleanup

# Mock cost per 1k tokens (e.g., for a mid-tier 2026 model)
COST_PER_1K_TOKENS = 0.002 

async def main():
    # 1. Setup the Cost-Aware Agent
    cost_agent = Agent(
        name="Efficiency_Strategist",
        instruction="Analyze the provided industry report. Be detailed but concise to optimize token usage.",
        model=get_model()
    )

    runner = get_runner(cost_agent)
    user_id, session_id = await initialize_session()
    
    # 2. The High-Context Query
    user_query = "Analyze the impact of 2026 Sovereign Cloud regulations on our EU operations."
    content = types.Content(role="user", parts=[types.Part(text=user_query)])
    
    print(f"--- STARTING COST-MONITORED ANALYSIS ---")
    
    # 3. Execute and Capture Metadata
    events = runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=content
    )
    
    async for event in events:
        if event.is_final_response():
            print("\n--- STRATEGIC ANALYSIS ---")
            print(event.content.parts[0].text)
            
            # 4. Extracting Token Metadata
            # Note: Usage data is typically found in the final response metadata
            usage = event.usage_metadata
            prompt_tokens = usage.prompt_token_count
            candidate_tokens = usage.candidates_token_count
            total_tokens = prompt_tokens + candidate_tokens
            
            estimated_cost = (total_tokens / 1000) * COST_PER_1K_TOKENS
            
            print(f"\n" + "="*30)
            print(f"METRICS FOR SESSION: {session_id}")
            print(f"Prompt Tokens: {prompt_tokens}")
            print(f"Response Tokens: {candidate_tokens}")
            print(f"Total Tokens: {total_tokens}")
            print(f"Estimated Cost: ${estimated_cost:.4f}")
            print("="*30)

    await cleanup()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass