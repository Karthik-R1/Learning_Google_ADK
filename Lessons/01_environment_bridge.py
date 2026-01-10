"""
LESSON 01: The Environment Bridge
DESCRIPTION: Validating the connection between Google ADK and local Llama 3.2.
WHY THIS IS IMPORTANT: This script verifies the "Strategy Suite" infrastructure.
By using the 'cleanup' utility, we ensure all backend connections close 
gracefully, leaving the console clean for executive presentations.
"""

import asyncio
from google.adk.agents import Agent
from google.genai import types 
# Import the new cleanup function along with our standard helpers
from config.settings import get_model, get_runner, initialize_session, cleanup

async def main():
    # 1. Setup the Strategy Agent
    foundational_agent = Agent(
        name="Strategy_Validator",
        instruction="You are a CIO Strategy Analyst. Explain AI benefits concisely.",
        model=get_model()
    )

    # 2. Setup the Runner
    runner = get_runner(foundational_agent)
    
    # 3. Register the session (The 'Check-in' pattern)
    user_id, session_id = await initialize_session()
    
    # 4. Format the Content object for the 2026 ADK Runner
    user_query = "Why is Google ADK a differentiator for a CIO's AI strategy in 2026?"
    content = types.Content(role="user", parts=[types.Part(text=user_query)])
    
    print(f"--- SYSTEM: Session {session_id} Initialized ---")
    print(f"Connecting to Local Strategy Brain (Llama 3.2)...\n")
    
    # 5. Execute with registered IDs
    events = runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=content
    )
    
    print("--- STRATEGIC INSIGHT ---")
    async for event in events:
        if event.is_final_response():
            print(event.content.parts[0].text)

    # 6. FINAL CLEANUP: Prevents RuntimeWarnings from LiteLLM
    await cleanup()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
