"""
LESSON 18: Persona Fine-Tuning (Contextual Shifting)
DESCRIPTION: Dynamically adjusting agent behavior based on the business domain.
WHY THIS IS IMPORTANT: A strategy for a 'Marketing Sandbox' should look 
nothing like a strategy for 'Core Financial Ledger'. This script 
demonstrates how to inject "Persona Wrappers" to ensure the AI's 
recommendations match the specific risk profile of the department.
"""

import asyncio
from google.adk.agents import Agent
from google.genai import types 
from config.settings import get_model, get_runner, initialize_session, cleanup

async def run_strategic_consult(business_unit: str, prompt: str):
    """Adjusts instructions based on the business unit before execution."""
    
    # 1. Define Persona logic
    if business_unit == "Innovation_Lab":
        instruction = "You are a Startup Founder. Prioritize speed, disruption, and high-risk/high-reward."
    elif business_unit == "Compliance_Finance":
        instruction = "You are a Risk Auditor. Prioritize stability, regulatory adherence, and zero-downtime."
    else:
        instruction = "You are a General Strategy Consultant."

    # 2. Setup the Agent with the Dynamic Persona
    specialized_agent = Agent(
        name=f"Advisor_{business_unit}",
        instruction=instruction,
        model=get_model()
    )

    runner = get_runner(specialized_agent)
    user_id, session_id = await initialize_session()
    
    content = types.Content(role="user", parts=[types.Part(text=prompt)])
    
    print(f"--- CONSULTING FOR: {business_unit} ---")
    events = runner.run_async(user_id=user_id, session_id=session_id, new_message=content)
    
    async for event in events:
        if event.is_final_response():
            print(f"[{business_unit} ADVICE]:\n{event.content.parts[0].text}\n")

async def main():
    query = "Should we implement the new unproven Beta-version of the AI Gateway today?"
    
    # 3. Demonstrate the difference in reasoning
    await run_strategic_consult("Innovation_Lab", query)
    await run_strategic_consult("Compliance_Finance", query)

    await cleanup()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass