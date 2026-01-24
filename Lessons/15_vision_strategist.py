"""
LESSON 15: Multi-Modal Strategy (Vision)
DESCRIPTION: Using Vision-capable models to analyze technical diagrams.
WHY THIS IS IMPORTANT: Strategy often lives in diagrams. This script 
demonstrates how to send an image (e.g., a cloud architecture or a 
workflow) to an agent to identify single points of failure or 
misalignment with CIO standards.
"""

import asyncio
from google.adk.agents import Agent
from google.genai import types 
from config.settings import get_model, get_runner, initialize_session, cleanup

async def main():
    # 1. Setup the Vision-Capable Agent
    # Note: Ensure your local model (like Llama 3.2 Vision) supports multi-modal.
    vision_agent = Agent(
        name="Architecture_Critic",
        instruction="""You are a Principal Enterprise Architect. 
        Analyze the provided image of a system architecture. 
        1. Identify the primary components.
        2. Point out one potential 'Single Point of Failure'.
        3. Suggest one optimization for cost or scalability.""",
        model=get_model()
    )

    runner = get_runner(vision_agent)
    user_id, session_id = await initialize_session()
    
    # 2. Prepare the Image Path (Assume you have a 'diagram.png' in your assets folder)
    # For this demo, we'll use a placeholder logic for the Part creation.
    image_path = "assets/cloud_architecture.png" 
    
    print(f"--- ANALYZING VISUAL ARCHITECTURE ---")
    print(f"File: {image_path}\n")

    try:
        # 3. Create Multi-Modal Content
        # We combine a text prompt with an image part
        with open(image_path, "rb") as f:
            image_data = f.read()

        content = types.Content(
            role="user",
            parts=[
                types.Part(text="Review this architecture for a 2026 AI-First migration."),
                types.Part(
                    inline_data=types.Blob(
                        data=image_data,
                        mime_type="image/png"
                    )
                )
            ]
        )
        
        # 4. Execute
        events = runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=content
        )
        
        print("--- ARCHITECTURAL CRITIQUE ---")
        async for event in events:
            if event.is_final_response():
                print(event.content.parts[0].text)

    except FileNotFoundError:
        print(f"SKIPPING: Please place an architecture diagram at {image_path} to run this lesson.")

    await cleanup()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass