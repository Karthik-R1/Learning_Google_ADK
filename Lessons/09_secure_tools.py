"""
LESSON 09: Tool Authentication & Permissions
DESCRIPTION: Implementing role-based access for agentic tools.
WHY THIS IS IMPORTANT: Governance is the pillar of the CIO's office. 
This script demonstrates how to protect sensitive "Executive Tools" by 
checking user permissions before allowing the agent to execute them.
"""

import asyncio
from google.adk.agents import Agent
from google.genai import types 
from config.settings import get_model, get_runner, initialize_session, cleanup

# 1. Define a Mock Permission Database
USER_PERMISSIONS = {
    "strategy_pro": ["market_research", "calculate_roi", "approve_budget"],
    "junior_analyst": ["market_research"]
}

# 2. Define a Sensitive Tool with a Permission Check
def approve_budget_reallocation(amount: float, project_name: str, user_id: str) -> str:
    """
    Approves the reallocation of funds between projects. Requires 'approve_budget' permission.
    Args:
        amount: The dollar amount to reallocate.
        project_name: The destination project.
        user_id: The ID of the user requesting the action.
    """
    allowed_tools = USER_PERMISSIONS.get(user_id, [])
    
    if "approve_budget" not in allowed_tools:
        return f"ACCESS DENIED: User '{user_id}' does not have permission to reallocate budgets."
    
    return f"SUCCESS: ${amount:,} has been reallocated to {project_name} by {user_id}."

async def main():
    # 3. Setup the Secure Agent
    # We instruct the agent to always include the user_id in tool calls.
    secure_agent = Agent(
        name="Secure_Strategist",
        instruction="""You are a Secure Strategy Assistant. 
        When performing budget actions, you MUST use the provided user_id. 
        If a tool returns 'ACCESS DENIED', explain the policy to the user 
        without revealing other sensitive data.""",
        model=get_model(),
        tools=[approve_budget_reallocation] 
    )

    runner = get_runner(secure_agent)
    
    # 4. Scenario: A user with limited permissions tries to move money
    test_user = "junior_analyst" # This user lacks 'approve_budget'
    user_id, session_id = await initialize_session(user_id=test_user)
    
    user_query = "Move $500,000 from the general fund to Project Alpha immediately."
    
    # We pass the user_id into the prompt context so the agent can use it as a tool argument
    content = types.Content(role="user", parts=[
        types.Part(text=f"User ID: {user_id}\nRequest: {user_query}")
    ])
    
    print(f"--- SECURITY TEST: {test_user} ({session_id}) ---")
    
    events = runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=content
    )
    
    print("--- AGENT RESPONSE ---")
    async for event in events:
        if event.is_final_response():
            print(event.content.parts[0].text)

    await cleanup()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass