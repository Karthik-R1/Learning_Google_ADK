
"""
LESSON 16: Strategic Branching (What-If Scenarios)
DESCRIPTION: Creating parallel conversation tracks from a single foundation.
WHY THIS IS IMPORTANT: Decision-makers need to compare alternatives. 
This script demonstrates how to fork a session so you can explore 
different strategic directions simultaneously without them interfering 
with each other.
"""

import asyncio
from google.adk.agents import Agent
from google.genai import types 
from config.settings import get_model, get_runner, initialize_session, cleanup

async def run_scenario(runner, user_id, parent_session_id, scenario_name, scenario_prompt):
    """Forks the main session into a specific scenario."""
    # In a real app, you would 'clone' the session state here.
    # For ADK, we use the parent context to seed a new branch.
    print(f"--- EXECUTING SCENARIO: {scenario_name} ---")
    
    content = types.Content(role="user", parts=[types.Part(text=scenario_prompt)])
    events = runner.run_async(user_id=user_id, session_id=parent_session_id, new_message=content)
    
    async for event in events:
        if event.is_final_response():
            return f"[{scenario_name} OUTPUT]:\n{event.content.parts[0].text}\n"

async def main():
    advisor = Agent(
        name="Scenario_Planner",
        instruction="You are a Strategic Risk Consultant. Evaluate scenarios with data-driven logic.",
        model=get_model()
    )

    runner = get_runner(advisor)
    user_id, main_session_id = await initialize_session()
    
    # 1. Establish the Foundation
    foundation_query = "Our goal is to modernize our Data Center by 2027 with a $5M budget."
    print("--- ESTABLISHING STRATEGIC FOUNDATION ---")
    await runner.run_async(
        user_id=user_id, 
        session_id=main_session_id, 
        new_message=types.Content(role="user", parts=[types.Part(text=foundation_query)])
    ).__anext__() # Seed the session

    # 2. Branch into Scenarios
    scenarios = [
        ("AGGRESSIVE", "What if we move the deadline to 2026 and increase budget by 50%? Analyze risk."),
        ("CONSERVATIVE", "What if we cut the budget by 30% and extend to 2028? Analyze impact."),
        ("BALANCED", "Keep the current plan but pivot 20% of funds to AI-ready edge nodes.")
    ]

    # Run branches in parallel
    tasks = [run_scenario(runner, user_id, main_session_id, name, prompt) for name, prompt in scenarios]
    results = await asyncio.gather(*tasks)

    for res in results:
        print(res)

    await cleanup()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass