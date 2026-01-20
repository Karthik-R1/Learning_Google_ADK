"""
LESSON 11: Portfolio Audit (Asynchronous Batching)
DESCRIPTION: Processing multiple strategic proposals in parallel.
WHY THIS IS IMPORTANT: Strategy teams often face "Batch Peaks" (e.g., Annual 
Planning). This script demonstrates how to use Python's 'asyncio.gather' 
to run multiple agents concurrently, turning hours of manual review into 
seconds of automated auditing.
"""

import asyncio
import time
from google.adk.agents import Agent
from google.genai import types 
from config.settings import get_model, get_runner, initialize_session, cleanup

async def audit_proposal(runner, user_id, session_id, proposal_name, proposal_text):
    """Helper function to run a single audit as a task."""
    query = f"Audit this proposal for strategic alignment and risk: {proposal_text}"
    content = types.Content(role="user", parts=[types.Part(text=query)])
    
    # We use a simplified collection for the final response
    full_response = ""
    events = runner.run_async(user_id=user_id, session_id=session_id, new_message=content)
    
    async for event in events:
        if event.is_final_response():
            full_response = event.content.parts[0].text
            
    return f"RESULT FOR {proposal_name}:\n{full_response}\n{'-'*30}"

async def main():
    # 1. Setup the Auditor Agent
    auditor = Agent(
        name="Portfolio_Auditor",
        instruction="Analyze proposals for ROI, technical debt, and 2026 strategic fit. Be brief.",
        model=get_model()
    )

    runner = get_runner(auditor)
    user_id, session_id = await initialize_session()
    
    # 2. Define a Portfolio of Proposals
    portfolio = {
        "Project_Zodiac": "Migrate on-prem data to a sovereign cloud in the EU.",
        "Project_Quantum": "Implement AI-driven predictive maintenance for manufacturing.",
        "Project_Nexus": "Deploy a company-wide internal knowledge bot for HR."
    }
    
    print(f"--- STARTING BATCH PORTFOLIO AUDIT ---")
    start_time = time.perf_counter()

    # 3. CONCURRENCY: We create a list of tasks to run at the same time
    tasks = [
        audit_proposal(runner, user_id, session_id, name, text) 
        for name, text in portfolio.items()
    ]
    
    # Execute all audits in parallel
    results = await asyncio.gather(*tasks)
    
    # 4. Output Results
    for result in results:
        print(result)

    end_time = time.perf_counter()
    print(f"Batch Audit Completed in {end_time - start_time:.2f} seconds.")

    await cleanup()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass