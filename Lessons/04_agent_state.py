"""
LESSON 04: Handling Agent State (Persistent Context)
DESCRIPTION: Demonstrating how the session service maintains memory across turns.
WHY THIS IS IMPORTANT: Strategy is iterative. An agent that forgets the 
"Innovation Budget" from the previous prompt is useless in a workshop. 
This script proves that our ADK setup maintains a 'Stateful' conversation.
"""

import asyncio
from google.adk.agents import Agent
from google.genai import types 
from config.settings import get_model, get_runner, initialize_session, cleanup

async def main():
    # 1. Setup the Stateful Agent
    # We give it instructions to be a 'Memory-Aware' strategist.
    state_agent = Agent(
        name="Stateful_Strategist",
        instruction="You are a strategy partner. Remember and build upon all context provided.",
        model=get_model()
    )

    runner = get_runner(state_agent)
    
    # 2. FIX: Initialize ONE session to use for multiple turns
    user_id, session_id = await initialize_session()
    
    print(f"--- STARTING STATEFUL SESSION: {session_id} ---")

    # --- TURN 1: Providing the Data ---
    print("\n[Turn 1] User: Setting the 2026 AI Innovation Budget to $4.5 Million.")
    turn_1_query = "Our AI innovation budget for 2026 is officially $4.5 million. Acknowledge this."
    content_1 = types.Content(role="user", parts=[types.Part(text=turn_1_query)])
    
    events_1 = runner.run_async(user_id=user_id, session_id=session_id, new_message=content_1)
    async for event in events_1:
        if event.is_final_response():
            print(f"Strategist: {event.content.parts[0].text}")

    # --- TURN 2: Relying on Memory ---
    # Note: We do NOT mention the budget amount here. The agent must remember it.
    print("\n[Turn 2] User: How should we split this across 3 pilot projects?")
    turn_2_query = "Based on that budget, suggest a split across three high-impact pilot projects."
    content_2 = types.Content(role="user", parts=[types.Part(text=turn_2_query)])
    
    events_2 = runner.run_async(user_id=user_id, session_id=session_id, new_message=content_2)
    async for event in events_2:
        if event.is_final_response():
            print(f"Strategist: {event.content.parts[0].text}")

    # 3. Cleanup
    await cleanup()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass