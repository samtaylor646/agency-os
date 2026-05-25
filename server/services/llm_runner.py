import asyncio
from typing import Dict, Any, Optional

class LLMRunner:
    """
    Mock LLM Runner service for Phase 1 of the Core Pivot Roadmap.
    This simulates interactions with external LLM providers (e.g., OpenAI, Anthropic).
    """
    def __init__(self, provider: str = "mock"):
        self.provider = provider

    async def generate_response(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        Simulates generating a text response from an LLM.
        """
        await asyncio.sleep(0.5) # Simulate network delay
        return f"Mock response to: {prompt[:50]}..."

    async def parse_intent(self, message: str) -> Dict[str, Any]:
        """
        Simulates parsing a user message to extract core project details.
        In a real implementation, this would use a structured output call (e.g. OpenAI function calling).
        """
        await asyncio.sleep(0.5) # Simulate network delay
        
        # Simple heuristic mocking for demonstration
        name = "Unknown Project"
        if "project" in message.lower() or "app" in message.lower():
            words = message.split()
            for i, word in enumerate(words):
                if word.lower() in ["project", "app"] and i > 0:
                    name = f"{words[i-1].capitalize()} {word.capitalize()}"
                    break

        return {
            "name": name,
            "description": message,
            "tech_stack": ["React", "FastAPI", "Python"] if "web" in message.lower() else ["Unknown"],
            "raw_message": message
        }

# Singleton instance for easy import
llm_runner = LLMRunner()
