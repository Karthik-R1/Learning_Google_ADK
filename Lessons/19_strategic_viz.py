"""
LESSON 19: Automated Data Visualization
DESCRIPTION: Enabling the agent to generate visualization code for its data.
WHY THIS IS IMPORTANT: Stakeholders need visual proof. This script 
demonstrates how an agent can output data in a format ready for 
Matplotlib or Plotly, bridging the gap between "Insight" and "Slide."
"""

import asyncio
from google.adk.agents import Agent
from google.genai import types 
from config.settings import get_model, get_runner, initialize_session, cleanup

async def main():
    # 1. Setup the Visual Strategist
    # We instruct the agent to provide both a summary AND the Python code for a chart.
    viz_agent = Agent(
        name="Data_Visualizer",
        instruction="""You are a Strategic Data Analyst. 
        When analyzing budgets, provide a summary and then output a 
        Python code block using 'matplotlib' to create a pie chart of the 
        allocation. Ensure the code is clean and standalone.""",
        model=get_model()
    )

    runner = get_runner(viz_agent)
    user_id, session_id = await initialize_session()
    
    # 2. The Budget Query
    user_query = """
    We have a $10M AI budget for 2026. 
    Split it: 40% Infrastructure, 30% Talent, 20% R&D, 10% Governance. 
    Analyze this and provide a chart script.
    """
    
    content = types.Content(role="user", parts=[types.Part(text=user_query)])
    
    print(f"--- GENERATING VISUAL STRATEGY ({session_id}) ---")
    
    # 3. Execute
    events = runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=content
    )
    
    print("--- ANALYSIS & CHART CODE ---")
    async for event in events:
        if event.is_final_response():
            # This output will contain the strategic text + the Python code block
            print(event.content.parts[0].text)

    await cleanup()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass