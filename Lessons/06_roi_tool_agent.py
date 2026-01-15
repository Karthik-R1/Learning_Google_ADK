"""
LESSON 06: Function Calling (Strategic Tools)
DESCRIPTION: Teaching the agent to use external Python functions for precision.
WHY THIS IS IMPORTANT: Strategy agents must be data-accurate. By providing a 
dedicated ROI calculator tool, we ensure the agent provides mathematically 
sound advice rather than "hallucinating" financial outcomes.
"""

import asyncio
from google.adk.agents import Agent
from google.genai import types 
from config.settings import get_model, get_runner, initialize_session, cleanup

# 1. Define the Strategic Tool
# The docstring and type hints are CRITICAL; they tell the Agent WHEN and HOW to use it.
def calculate_ai_roi(investment: float, annual_savings: float) -> str:
    """
    Calculates the Return on Investment (ROI) for an AI initiative.
    Args:
        investment: The total cost of the AI pilot/infrastructure.
        annual_savings: The projected cost reduction or efficiency gains per year.
    """
    if investment <= 0:
        return "Investment must be greater than zero."
    
    roi_percentage = ((annual_savings - investment) / investment) * 100
    return f"The calculated ROI is {roi_percentage:.2f}%."

async def main():
    # 2. Setup the Agent with the Tool registered
    financial_agent = Agent(
        name="Financial_Strategist",
        instruction="""You are a Strategy Consultant. 
        When users ask about the value of an investment, ALWAYS use the 
        calculate_ai_roi tool to provide an accurate percentage.""",
        model=get_model(),
        tools=[calculate_ai_roi] # We pass the function directly here
    )

    runner = get_runner(financial_agent)
    user_id, session_id = await initialize_session()
    
    # 3. The Query: Forcing the agent to use the tool
    user_query = "We are planning a $250,000 AI Agent pilot that is expected to save $400,000 in its first year. What is our ROI?"
    content = types.Content(role="user", parts=[types.Part(text=user_query)])
    
    print(f"--- ANALYZING INVESTMENT ({session_id}) ---")
    print(f"Query: {user_query}\n")
    
    # 4. Execute
    events = runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=content
    )
    
    print("--- STRATEGIC FINANCIAL RESPONSE ---")
    async for event in events:
        if event.is_final_response():
            print(event.content.parts[0].text)

    # 5. Cleanup
    await cleanup()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass