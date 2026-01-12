"""
LESSON 03: The Executive Memo (Prompt Templating)
DESCRIPTION: Using structured templates to guide Agentic reasoning for leadership.
WHY THIS IS IMPORTANT: Executives don't have time for "chatty" AI. This script 
demonstrates how to use templates to force the agent to produce structured, 
scannable memos (Executive Summary, ROI, Risks) rather than unstructured text.
"""

import asyncio
from google.adk.agents import Agent
from google.genai import types 
from config.settings import get_model, get_runner, initialize_session, cleanup

async def main():
    # 1. Setup the Executive Agent
    memo_agent = Agent(
        name="Executive_Communicator",
        instruction="""You are a Strategy Chief of Staff. 
        Your goal is to synthesize complex technology trends into 
        one-page executive memos for the CIO.""",
        model=get_model()
    )

    runner = get_runner(memo_agent)
    user_id, session_id = await initialize_session()
    
    # 2. Define the Strategy Template
    # By defining the schema in the prompt, we ensure consistency across the suite.
    topic = "The transition from Robotic Process Automation (RPA) to Agentic AI"
    
    memo_template = f"""
    ANALYSIS REQUEST: {topic}
    
    Please provide the analysis in the strictly followed format below:
    
    ## EXECUTIVE SUMMARY
    (Two sentences on the strategic shift)
    
    ## CURRENT STATE vs. FUTURE STATE
    (A brief comparison of RPA efficiency vs. Agentic autonomy)
    
    ## STRATEGIC RECOMMENDATION
    (One high-level actionable step for the CIO)
    
    ## RISK MITIGATION
    (The #1 hurdle to watch out for)
    """

    content = types.Content(role="user", parts=[types.Part(text=memo_template)])
    
    print(f"--- GENERATING EXECUTIVE MEMO ---")
    print(f"Topic: {topic}\n")
    
    # 3. Execute the agent
    events = runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=content
    )
    
    print("--- MEMO OUTPUT ---")
    async for event in events:
        if event.is_final_response():
            print(event.content.parts[0].text)

    # 4. Cleanup
    await cleanup()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass