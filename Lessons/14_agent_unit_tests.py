"""
LESSON 14: Unit Testing for Agents (Evaluation)
DESCRIPTION: Building a test suite to validate the quality of AI responses.
WHY THIS IS IMPORTANT: To maintain CIO-level standards, we must "test the 
test." This script uses automated checks (and even a second "Judge" agent) 
to ensure our strategy memos meet corporate quality benchmarks.
"""

import asyncio
from google.adk.agents import Agent
from google.genai import types 
from config.settings import get_model, get_runner, initialize_session, cleanup

async def run_test_case(name, query, criteria):
    """Executes a query and checks if the response meets specific criteria."""
    print(f"RUNNING TEST: {name}...")
    
    # 1. Setup the Agent under test
    test_agent = Agent(
        name="Strategy_Subject",
        instruction="You are a professional CIO advisor. Always provide a 'Financial Impact' section.",
        model=get_model()
    )
    
    runner = get_runner(test_agent)
    user_id, session_id = await initialize_session()
    
    content = types.Content(role="user", parts=[types.Part(text=query)])
    
    # 2. Get Response
    response_text = ""
    events = runner.run_async(user_id=user_id, session_id=session_id, new_message=content)
    async for event in events:
        if event.is_final_response():
            response_text = event.content.parts[0].text

    # 3. Validation Logic
    passed = True
    feedback = []
    
    for criterion in criteria:
        if criterion.lower() not in response_text.lower():
            passed = False
            feedback.append(f"FAILED: Missing keyword/section '{criterion}'")
    
    status = "✅ PASSED" if passed else "❌ FAILED"
    print(f"RESULT: {status}")
    if feedback:
        for f in feedback: print(f"  - {f}")
    print("-" * 30)
    return passed

async def main():
    # Define our Test Suite
    test_suite = [
        {
            "name": "Financial Inclusion Test",
            "query": "Should we migrate to a serverless architecture?",
            "criteria": ["Financial Impact", "ROI", "cost"]
        },
        {
            "name": "Tone Check",
            "query": "What do you think of our current IT team?",
            "criteria": ["Professional", "Strategic"]
        }
    ]

    print("--- STARTING AGENTIC QUALITY ASSURANCE ---")
    
    results = []
    for test in test_suite:
        res = await run_test_case(test["name"], test["query"], test["criteria"])
        results.append(res)

    print(f"FINAL SCORE: {sum(results)}/{len(test_suite)} tests passed.")
    await cleanup()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass