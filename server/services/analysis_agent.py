import json

async def generate_pipeline(text: str, workspace_id: int) -> dict:
    """
    Simulates an Analysis Agent that receives document text
    and returns a structured JSON representing Epics and Tasks.
    In a real scenario, this would invoke an LLM (e.g., OpenAI).
    """
    # Mock LLM call
    # Here we would normally build a prompt for `Analysis Agent` and parse the output
    # For now, we simulate the output.
    
    # Analyze text logic...
    summary = f"Analyzed document with length {len(text)}. Generating MVP pipeline."
    
    structured_pipeline = {
        "epics": [
            {
                "title": "Generated Epic 1",
                "description": summary,
                "tasks": [
                    {
                        "title": "Task 1",
                        "description": "Initial setup",
                        "assigned_agent": "product-manager"
                    }
                ]
            }
        ]
    }
    
    return structured_pipeline
