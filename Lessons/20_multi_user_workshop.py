"""
LESSON 20: Collaborative Multi-User Sessions
DESCRIPTION: Handling multiple distinct stakeholder perspectives in a single session.
WHY THIS IS IMPORTANT: To resolve conflicts, the agent needs to hear from 
everyone.

FIX APPLIED: 
- Standardized the 'user_id' to a single session owner to prevent 
  ValueError: Session not found.
- Passed stakeholder roles inside the prompt content instead of the 
  user_id parameter.
"""

import asyncio
from google.adk.agents import Agent
from google.genai import types 
from config.settings import get_model, get_runner, initialize_session, cleanup

async def add_stakeholder_input(runner, session_id, admin_user, role, comment):
    """Injects input into a session while maintaining session ownership."""
    print(f"--- Recording {role}'s Perspective ---")
    
    # We attribute the role within the message content
    tagged_text = f"STAKEHOLDER [{role}]: {comment}"
    content = types.Content(role="user", parts=[types.Part(text=tagged_text)])
    
    # We use the 'admin_user' (session owner) for every call
    events = runner.run_async(user_id=admin_user, session_id=session_id, new_message=content)
    
    async for event in events:
        if event.is_final_response():
            # Return the response so we know it's processed
            return event.content.parts[0].text

async def main():
    # 1. Setup the "Mediator" Agent
    mediator = Agent(
        name="Workshop_Mediator",
        instruction="""You are a Strategic Mediator. 
        Analyze the inputs from different stakeholders. 
        Identify where their goals conflict and propose a compromise.""",
        model=get_model()
    )

    runner = get_runner(mediator)
    
    # Initialize session with a master 'admin_user'
    admin_user, session_id = await initialize_session() 
    
    print(f"--- STARTING STRATEGY WORKSHOP: {session_id} ---\n")
    
    # 2. Sequential Stakeholder Inputs (All using the same session owner)
    # Turn 1: CIO
    await add_stakeholder_input(runner, session_id, admin_user, "CIO", 
                               "We must migrate to AI-native infrastructure by Q4 to stay competitive.")
    
    # Turn 2: CFO
    await add_stakeholder_input(runner, session_id, admin_user, "CFO", 
                               "The budget is frozen until next year. No new infrastructure spend is allowed.")

    # 3. The Final Synthesis
    # The agent now has both messages in its history
    final_query = "Summarize the conflict and provide a consensus-based recommendation."
    content_final = types.Content(role="user", parts=[types.Part(text=final_query)])
    
    print("\n--- MEDIATOR'S CONSENSUS REPORT ---")
    events = runner.run_async(user_id=admin_user, session_id=session_id, new_message=content_final)
    
    async for event in events:
        if event.is_final_response():
            print(event.content.parts[0].text)

    await cleanup()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass