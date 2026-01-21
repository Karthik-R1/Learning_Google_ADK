"""
LESSON 12: Human-in-the-Loop (HITL)
DESCRIPTION: Implementing a manual approval gate for high-risk strategic decisions.
WHY THIS IS IMPORTANT: Governance requires accountability. This script 
demonstrates how to pause an agentic workflow to allow a human strategist 
to review, edit, or veto a recommendation before it is finalized.
"""

import asyncio
from google.adk.agents import Agent
from google.genai import types 
from config.settings import get_model, get_runner, initialize_session, cleanup

async def main():
    # 1. Setup the Strategic Advisor
    advisor = Agent(
        name="Pivot_Advisor",
        instruction="""You are a Strategy Advisor. 
        When suggesting a budget cut, be bold but provide clear reasoning. 
        Your recommendation will be reviewed by a human before being sent to the board.""",
        model=get_model()
    )

    runner = get_runner(advisor)
    user_id, session_id = await initialize_session()
    
    # 2. Phase 1: The AI Proposal
    user_query = "We need to free up $1M. Suggest which project to deprioritize."
    content = types.Content(role="user", parts=[types.Part(text=user_query)])
    
    print(f"--- AGENT IS GENERATING PROPOSAL ---")
    
    proposal_text = ""
    events = runner.run_async(user_id=user_id, session_id=session_id, new_message=content)
    async for event in events:
        if event.is_final_response():
            proposal_text = event.content.parts[0].text

    print(f"\n[AI PROPOSAL]:\n{proposal_text}\n")

    # 3. THE HUMAN GATEWAY
    # In a real app, this would be a UI button or an email approval.
    print("--- HUMAN VALIDATION REQUIRED ---")
    feedback = input("Type 'APPROVE' to proceed, or enter your manual feedback: ")

    if feedback.upper() == "APPROVE":
        final_query = "The human has approved your proposal. Generate the final board-ready executive summary."
    else:
        final_query = f"The human strategist rejected your proposal with this feedback: '{feedback}'. Revise your plan accordingly."

    # 4. Phase 2: Finalizing based on Human Input
    content_final = types.Content(role="user", parts=[types.Part(text=final_query)])
    
    print("\n--- GENERATING FINAL OUTPUT ---")
    events_final = runner.run_async(user_id=user_id, session_id=session_id, new_message=content_final)
    async for event in events_final:
        if event.is_final_response():
            print(event.content.parts[0].text)

    await cleanup()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass