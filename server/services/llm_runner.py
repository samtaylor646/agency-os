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
        
        scoping_prompt = system_prompt or "You are an expert AI orchestrator. Your goal is to help scope a software project by asking clarifying questions about the goal, target audience, and key features. Be concise and focus on actionable insights."
        
        return f"Mock response (Guided by prompt: {scoping_prompt[:40]}...) to: {prompt[:50]}..."

    async def generate_document(self, doc_type: str, context: Dict[str, Any]) -> str:
        """
        Simulates generating a specific project document based on context.
        """
        await asyncio.sleep(1.0) # Simulate generation delay
        
        name = context.get("name", "Unknown Project")
        desc = context.get("description", "No description provided.")
        stack = ", ".join(context.get("tech_stack", ["Unknown"]))
        
        if doc_type == "prd":
            return f"# PRD: {name}\n\n## Overview\n{desc}\n\n## Goals\n- Build an MVP\n- Validate market"
        elif doc_type == "architecture":
            return f"# Architecture Spec: {name}\n\n## Stack\n{stack}\n\n## Components\n- Frontend UI\n- Backend API"
        elif doc_type == "tasks":
            return f"# Task List: {name}\n\n- [ ] Scaffold project\n- [ ] Implement {stack} components\n- [ ] Write tests"
        
        return f"# {doc_type.upper()}: {name}\nGenerated content based on {desc}"

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
