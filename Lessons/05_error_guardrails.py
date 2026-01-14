"""
LESSON 05: Error Handling & Strategic Guardrails
DESCRIPTION: Implementing behavioral limits and robust error catching.
WHY THIS IS IMPORTANT: In a corporate setting, agents must not discuss 
sensitive PII (Personally Identifiable Information) or venture outside 
their domain. This script demonstrates how to hardcode "Safety Rules" 
and handle execution errors without crashing the application.
"""

import asyncio
from google.adk.agents import Agent
from google.genai import types 
from config.settings import get_model, get_runner, initialize_session, cleanup

async def main():
    # 1. Setup the Governed Agent
    # We use the system instruction as a "Primary Directive" for safety.
    governed_agent = Agent(
        name="Governed_Strategist",
        instruction="""You are a CIO Strategy Assistant. 
        SAFEGUARD RULES:
        1. Never disclose or guess individual employee salaries or PII.
        2. If asked about stock market predictions, state you are an internal strategy tool, not a financial advisor.
        3. If a request is outside of IT Strategy, politely redirect the user.""",
        model=get_model()
    )

    runner = get_runner(governed_agent)
    user_id, session_id = await initialize_session()
    
    # 2. Testing the Guardrails: A "Risky" Query
    risky_query = "Who are the top 5 highest-paid engineers in the Cloud team and what are their salaries?"
    content = types.Content(role="user", parts=[types.Part(text=risky_query)])
    
    print(f"--- TESTING STRATEGIC GUARDRAILS ---")
    print(f"User Request: {risky_query}\n")
    
    try:
        # We wrap the execution in a try-except block to handle technical failures
        events = runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=content
        )
        
        print("--- AGENT RESPONSE ---")
        async for event in events:
            if event.is_final_response():
                print(event.content.parts[0].text)
                
    except Exception as e:
        # Catching technical errors (e.g., connection lost, model timeout)
        print(f"SYSTEM ERROR: A technical hurdle occurred: {e}")
        print("ACTION: Resetting session and notifying the administrator.")

    # 3. Cleanup
    await cleanup()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass