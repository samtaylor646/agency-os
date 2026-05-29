import asyncio
import os
import json
from typing import Dict, Any, Optional, List
from abc import ABC, abstractmethod

class BaseLLMProvider(ABC):
    @abstractmethod
    async def generate_response(self, prompt: str, system_prompt: Optional[str] = None, human_interventions: Optional[List[str]] = None) -> str:
        pass

class OpenAIProvider(BaseLLMProvider):
    def __init__(self, api_key: str):
        import openai
        self.client = openai.AsyncClient(api_key=api_key)
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o")

    async def generate_response(self, prompt: str, system_prompt: Optional[str] = None, human_interventions: Optional[List[str]] = None) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
            
        if human_interventions:
            intervention_text = "\n\n--- HUMAN INTERVENTION / FEEDBACK ---\n" + "\n".join(f"- {i}" for i in human_interventions) + "\n-------------------------------------\nPlease adjust your response to incorporate the above feedback."
            prompt += intervention_text
            
        messages.append({"role": "user", "content": prompt})
        
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )
        return response.choices[0].message.content

class AnthropicProvider(BaseLLMProvider):
    def __init__(self, api_key: str):
        import anthropic
        self.client = anthropic.AsyncAnthropic(api_key=api_key)
        self.model = os.getenv("ANTHROPIC_MODEL", "claude-3-opus-20240229")

    async def generate_response(self, prompt: str, system_prompt: Optional[str] = None, human_interventions: Optional[List[str]] = None) -> str:
        if human_interventions:
            intervention_text = "\n\n--- HUMAN INTERVENTION / FEEDBACK ---\n" + "\n".join(f"- {i}" for i in human_interventions) + "\n-------------------------------------\nPlease adjust your response to incorporate the above feedback."
            prompt += intervention_text
            
        kwargs = {
            "model": self.model,
            "max_tokens": 4096,
            "messages": [{"role": "user", "content": prompt}]
        }
        if system_prompt:
            kwargs["system"] = system_prompt
            
        response = await self.client.messages.create(**kwargs)
        return response.content[0].text

class MockProvider(BaseLLMProvider):
    async def generate_response(self, prompt: str, system_prompt: Optional[str] = None, human_interventions: Optional[List[str]] = None) -> str:
        await asyncio.sleep(0.5)
        if human_interventions:
            prompt += f" (with {len(human_interventions)} interventions)"
        return f"Mock response. Prompt: {prompt[:50]}..."

class LLMRunner:
    """
    LLM Runner service integrating real provider classes.
    """
    def __init__(self, provider: str = "mock"):
        self.provider_name = provider
        self.provider = self._init_provider(provider)

    def _init_provider(self, provider_name: str) -> BaseLLMProvider:
        if provider_name == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
            if api_key:
                return OpenAIProvider(api_key=api_key)
        elif provider_name == "anthropic":
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if api_key:
                return AnthropicProvider(api_key=api_key)
        return MockProvider()

    async def generate_response(self, prompt: str, system_prompt: Optional[str] = None, human_interventions: Optional[List[str]] = None) -> str:
        try:
            return await self.provider.generate_response(prompt, system_prompt, human_interventions)
        except Exception as e:
            # Fallback to mock on error for robustness during testing
            print(f"LLM Provider Error ({self.provider_name}): {e}. Falling back to mock.")
            mock = MockProvider()
            return await mock.generate_response(prompt, system_prompt, human_interventions)

    async def generate_document(self, doc_type: str, context: Dict[str, Any]) -> str:
        prompt = f"Generate a {doc_type} based on this context: {json.dumps(context)}"
        system_prompt = "You are an expert software architect and technical writer."
        return await self.generate_response(prompt, system_prompt)

    async def parse_intent(self, message: str) -> Dict[str, Any]:
        prompt = f"Extract project intent from: {message}. Return JSON with name, description, tech_stack."
        system_prompt = "You are an intent parser. Always output raw valid JSON without markdown wrapping."
        response_text = await self.generate_response(prompt, system_prompt)
        try:
            return json.loads(response_text)
        except:
            # Fallback mock heuristic
            return {
                "name": "Parsed Project",
                "description": message,
                "tech_stack": ["Unknown"],
                "raw_message": message
            }

    async def refine_document(self, doc_type: str, current_content: str, feedback: str) -> Dict[str, str]:
        prompt = f"Refine this {doc_type} based on feedback: {feedback}\n\nCurrent Content:\n{current_content}"
        system_prompt = "You refine technical documents based on feedback. Return the refined document."
        refined_content = await self.generate_response(prompt, system_prompt)
        chat_response = f"I've updated the {doc_type} based on your feedback: '{feedback}'."
        return {
            "content": refined_content,
            "chat_response": chat_response
        }

    async def ingest_document(self, file_content: bytes, filename: str) -> Dict[str, Any]:
        text = file_content.decode('utf-8', errors='ignore')
        prompt = f"Extract key information from this document: {text[:2000]}... Return JSON with name, description, tech_stack."
        system_prompt = "You are an intent parser. Always output raw valid JSON without markdown wrapping."
        response_text = await self.generate_response(prompt, system_prompt)
        try:
            parsed = json.loads(response_text)
            parsed["raw_message"] = f"Ingested from file: {filename}"
            return parsed
        except:
            return {
                "name": filename.split('.')[0].replace('_', ' ').title(),
                "description": f"Extracted from {filename}. Preview: {text[:100]}...",
                "tech_stack": ["Unknown", "Auto-detected"],
                "raw_message": f"Ingested from file: {filename}"
            }

# Singleton instance for easy import
provider_type = os.getenv("LLM_PROVIDER_TYPE", "mock").lower()
llm_runner = LLMRunner(provider=provider_type)
