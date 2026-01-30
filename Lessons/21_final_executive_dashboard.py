"""
LESSON 21: The Strategic Executive Dashboard (Full Integration)
DESCRIPTION: The Grand Finale. A production-ready blueprint combining 
Tool Calling, Long-Term Memory (RAG), and Multi-Stakeholder Synthesis.

GOVERNANCE PATTERN: Uses "Session Sovereignty" to maintain a stable 
connection between the Advisor and the Session Store.
"""

import asyncio
from google.adk.agents import Agent
from google.genai import types 
from config.settings import get_model, get_runner, initialize_session, cleanup

# --- 1. CORE ENTERPRISE TOOLS ---
def calculate_roi(investment, savings) -> str:
    """
    Calculates ROI percentage for a project. 
    Explicitly casts inputs to floats to handle LLM string passing.
    """
    try:
        # Cast to float to handle strings passed by the LLM
        inv = float(investment)
        sav = float(savings)
        
        if inv == 0:
            return "Error: Investment cannot be zero."
            
        roi = ((sav - inv) / inv) * 100
        return f"PRECISION CALCULATION: ROI is {roi:.2f}%."
    except (ValueError, TypeError):
        return "Error: Investment and savings must be numeric values."

async def fetch_history(topic: str) -> str:
    """Simulates RAG retrieval from institutional archives."""
    archives = {
        "AI Gateway": "2024 LESSON: Centralized gateways reduced API sprawl by 35% but required strict latency monitoring."
    }
    return archives.get(topic, "No specific historical data found for this topic.")

async def main():
    # --- 2. SETUP THE ULTIMATE STRATEGIST ---
    executive_agent = Agent(
        name="Global_CIO_Advisor",
        instruction="""You are the Lead Strategic Advisor. 
        Your goal is to provide a Go/No-Go recommendation for major IT spends.
        1. Always check 'fetch_history' to avoid past mistakes.
        2. Always use 'calculate_roi' for financial validation.
        3. Reconcile conflicting stakeholder perspectives into a single summary.""",
        model=get_model(),
        tools=[calculate_roi, fetch_history]
    )

    runner = get_runner(executive_agent)
    
    # Use one primary session owner to prevent 'Session not found'
    admin_user, session_id = await initialize_session()
    
    # --- 3. THE CONSOLIDATED STRATEGY PROMPT ---
    # We combine multi-user input and a complex task into one "Context Packet"
    final_query = """
    STRATEGIC DOSSIER:
    - PROJECT: '2026 AI Gateway Implementation'
    - FINANCIALS: $3M Investment vs. $6.5M Projected Efficiency Savings.
    - CIO INPUT: "We need this to govern our decentralized agent teams."
    - CFO INPUT: "I am concerned about the high upfront cost and 2024's integration delays."
    
    TASK: Analyze the ROI, consult the 2024 archives for context, and provide a 
    final Executive Recommendation.
    """
    
    print(f"--- INITIALIZING EXECUTIVE NERVE CENTER: {session_id} ---")
    
    content = types.Content(role="user", parts=[types.Part(text=final_query)])
    
    # --- 4. THE EXECUTION ---
    print("\n--- ANALYZING HISTORY, FINANCES, AND STRATEGY ---")
    events = runner.run_async(user_id=admin_user, session_id=session_id, new_message=content)
    
    async for event in events:
        if event.is_final_response():
            print("\n" + "█"*50)
            print("       OFFICE OF THE CIO: FINAL STRATEGY       ")
            print("█"*50)
            print(event.content.parts[0].text)
            
            # Metadata Observability (from Lesson 13)
            usage = event.usage_metadata
            print(f"\n[DASHBOARD METRICS] Session ID: {session_id} | Total Tokens: {usage.total_token_count}")

    await cleanup()
    print("\n--- 21-DAY ADK MASTERCLASS COMPLETE ---")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass