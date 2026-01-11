import asyncio
from google.adk.agents import Agent
from google.genai import types 
from config.settings import get_model, get_runner, initialize_session, cleanup

async def main():
    roadmap_agent = Agent(
        name="Roadmap_Architect",
        instruction="""You are a Lead Strategy Architect. 
        Split roadmaps into: Short-term (6mo), Mid-term (2yr), and Long-term (5yr).
        Identify one 'Critical Dependency' and one 'Business Outcome' per phase.""",
        model=get_model()
    )

    runner = get_runner(roadmap_agent)
    user_id, session_id = await initialize_session()
    
    user_query = "Draft a 5-year roadmap for moving our legacy ERP to an Agentic AI-driven infrastructure."
    content = types.Content(role="user", parts=[types.Part(text=user_query)])
    
    print(f"--- ARCHITECTING STRATEGIC ROADMAP ---")
    
    events = runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=content
    )
    
    async for event in events:
        if event.is_final_response():
            print(event.content.parts[0].text)

    # FIX: Call the cleanup before the loop closes
    await cleanup()

if __name__ == "__main__":
    asyncio.run(main())