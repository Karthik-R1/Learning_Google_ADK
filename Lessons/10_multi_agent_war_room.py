"""
LESSON 10: Multi-Agent Orchestration (The War Room)
DESCRIPTION: Orchestrating multiple agents with conflicting personas to stress-test a strategy.
WHY THIS IS IMPORTANT: Critical decisions require a 360-degree view. This script 
simulates a board-room debate where an Innovator pushes for growth and a CFO 
checks for risk, resulting in a balanced, high-fidelity recommendation.
"""

import asyncio
from google.adk.agents import Agent
from google.genai import types 
from config.settings import get_model, get_runner, initialize_session, cleanup

async def main():
    # 1. Setup the Two Specialist Agents
    innovator = Agent(
        name="Innovator",
        instruction="Focus exclusively on growth, competitive advantage, and speed-to-market.",
        model=get_model()
    )

    cfo = Agent(
        name="CFO_Skeptical",
        instruction="Focus exclusively on ROI, operational risk, and long-term sustainability.",
        model=get_model()
    )

    # 2. Shared Setup
    runner_innovator = get_runner(innovator)
    runner_cfo = get_runner(cfo)
    user_id, session_id = await initialize_session()
    
    proposal = "We should replace our entire customer support team with Agentic AI in Q1."
    
    print(f"--- STRATEGIC WAR ROOM: SESSION {session_id} ---")
    print(f"PROPOSAL: {proposal}\n")

    # --- PHASE 1: The Innovator's Pitch ---
    content_inv = types.Content(role="user", parts=[types.Part(text=f"Pitch the benefits of: {proposal}")])
    resp_inv = ""
    async for event in runner_innovator.run_async(user_id=user_id, session_id=session_id, new_message=content_inv):
        if event.is_final_response():
            resp_inv = event.content.parts[0].text
    
    print(f"🚀 INNOVATOR'S VIEW:\n{resp_inv}\n")

    # --- PHASE 2: The CFO's Rebuttal ---
    # We pass the Innovator's response TO the CFO to create a "Debate"
    content_cfo = types.Content(role="user", parts=[types.Part(text=f"Critique this pitch from a risk/cost perspective: {resp_inv}")])
    resp_cfo = ""
    async for event in runner_cfo.run_async(user_id=user_id, session_id=session_id, new_message=content_cfo):
        if event.is_final_response():
            resp_cfo = event.content.parts[0].text

    print(f"⚖️ CFO'S COUNTER-POINT:\n{resp_cfo}\n")

    # --- PHASE 3: The Final Board Recommendation ---
    # We use a third, neutral agent to synthesize the two views.
    synthesizer = Agent(name="CEO", instruction="Synthesize the debate into a final 'Go/No-Go' decision.", model=get_model())
    runner_ceo = get_runner(synthesizer)
    
    final_query = f"Based on the Innovator ({resp_inv}) and the CFO ({resp_cfo}), what is the final recommendation?"
    content_final = types.Content(role="user", parts=[types.Part(text=final_query)])
    
    print("--- FINAL BOARD RECOMMENDATION ---")
    async for event in runner_ceo.run_async(user_id=user_id, session_id=session_id, new_message=content_final):
        if event.is_final_response():
            print(event.content.parts[0].text)

    await cleanup()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass