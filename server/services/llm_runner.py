import asyncio
import os
import json
from typing import Dict, Any, Optional, List
from abc import ABC, abstractmethod

class LLMProviderStrategy(ABC):
    @abstractmethod
    async def generate_response(self, messages: list, credentials: dict, model: str, **kwargs) -> str:
        pass

class OpenAIStrategy(LLMProviderStrategy):
    async def generate_response(self, messages: list, credentials: dict, model: str, **kwargs) -> str:
        import openai
        api_key = credentials.get("api_key")
        client = openai.AsyncClient(api_key=api_key)
        
        response = await client.chat.completions.create(
            model=model,
            messages=messages,
            **kwargs
        )
        return response.choices[0].message.content

class AnthropicStrategy(LLMProviderStrategy):
    async def generate_response(self, messages: list, credentials: dict, model: str, **kwargs) -> str:
        import anthropic
        api_key = credentials.get("api_key")
        client = anthropic.AsyncAnthropic(api_key=api_key)
        
        # Anthropic expects 'system' out of messages
        system_prompt = next((m["content"] for m in messages if m["role"] == "system"), None)
        filtered_messages = [m for m in messages if m["role"] != "system"]
        
        call_kwargs = {
            "model": model,
            "max_tokens": kwargs.get("max_tokens", 4096),
            "messages": filtered_messages
        }
        if system_prompt:
            call_kwargs["system"] = system_prompt
            
        response = await client.messages.create(**call_kwargs)
        return response.content[0].text

class GeminiStrategy(LLMProviderStrategy):
    async def generate_response(self, messages: list, credentials: dict, model: str, **kwargs) -> str:
        import google.generativeai as genai
        api_key = credentials.get("api_key")
        genai.configure(api_key=api_key)
        
        gemini_model = genai.GenerativeModel(model)
        
        # Convert messages to Gemini format
        history = []
        for m in messages:
            role = "user" if m["role"] in ["user", "system"] else "model"
            history.append({"role": role, "parts": [m["content"]]})
            
        # Simplistic approach for Gemini
        response = gemini_model.generate_content(history)
        return response.text

class MockStrategy(LLMProviderStrategy):
    async def generate_response(self, messages: list, credentials: dict, model: str, **kwargs) -> str:
        await asyncio.sleep(0.5)
        prompt = messages[-1]["content"] if messages else ""
        return f"Mock response from {model}. Prompt: {prompt[:50]}..."


class LLMRunner:
    """
    LLM Runner service integrating Strategy pattern for multiple providers.
    """
    def __init__(self):
        self.strategies = {
            "openai": OpenAIStrategy(),
            "anthropic": AnthropicStrategy(),
            "gemini": GeminiStrategy(),
            "mock": MockStrategy()
        }
        self.default_provider = os.getenv("LLM_PROVIDER_TYPE", "mock").lower()
        self.mcp_sessions = {}  # Store active MCP sessions

    async def get_mcp_session(self, server_name: str, command: str, args: List[str]):
        """
        Initializes and returns an MCP client session using StdioServerParameters.
        This provides a session that can be used to call tools on the MCP server.
        """
        if server_name in self.mcp_sessions:
            return self.mcp_sessions[server_name]["session"]

        try:
            from mcp.client.stdio import stdio_client, StdioServerParameters
            from mcp.client.session import ClientSession
            from contextlib import AsyncExitStack
        except ImportError:
            print("MCP SDK not installed. Please install 'mcp>=1.0.0'.")
            return None

        server_params = StdioServerParameters(
            command=command,
            args=args,
            env=None
        )

        exit_stack = AsyncExitStack()
        try:
            stdio_transport = await exit_stack.enter_async_context(stdio_client(server_params))
            stdio, write = stdio_transport
            session = await exit_stack.enter_async_context(ClientSession(stdio, write))
            await session.initialize()
            
            self.mcp_sessions[server_name] = {
                "session": session,
                "exit_stack": exit_stack
            }
            return session
        except Exception as e:
            print(f"Failed to initialize MCP client for {server_name}: {e}")
            await exit_stack.aclose()
            return None

    async def close_mcp_sessions(self):
        """Closes all active MCP sessions. Used for cleanup or Kill Switch."""
        for server_name, session_data in list(self.mcp_sessions.items()):
            try:
                await session_data["exit_stack"].aclose()
            except Exception as e:
                print(f"Error closing MCP session for {server_name}: {e}")
        self.mcp_sessions.clear()

    async def handle_fallback(self, provider: str, messages: list, credentials: dict, model: str, **kwargs) -> str:
        print(f"LLM Provider Error ({provider}). Falling back to mock.")
        strategy = self.strategies.get("mock")
        return await strategy.generate_response(messages, credentials, "mock-fallback-model", **kwargs)

    async def execute(self, provider: str, messages: list, credentials: dict, model: str, **kwargs) -> str:
        strategy = self.strategies.get(provider.lower())
        if not strategy:
            raise ValueError(f"Unsupported provider: {provider}")
        
        try:
            return await strategy.generate_response(messages, credentials, model, **kwargs)
        except Exception as e:
            return await self.handle_fallback(provider, messages, credentials, model, **kwargs)

    # Legacy wrapper for backwards compatibility
    async def generate_response(self, prompt: str, system_prompt: Optional[str] = None, human_interventions: Optional[List[str]] = None) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
            
        if human_interventions:
            intervention_text = "\n\n--- HUMAN INTERVENTION / FEEDBACK ---\n" + "\n".join(f"- {i}" for i in human_interventions) + "\n-------------------------------------\nPlease adjust your response to incorporate the above feedback."
            prompt += intervention_text
            
        messages.append({"role": "user", "content": prompt})
        
        provider = self.default_provider
        
        # Try to pull creds from env for legacy calls
        credentials = {}
        model = "mock-model"
        if provider == "openai":
            credentials["api_key"] = os.getenv("OPENAI_API_KEY")
            model = os.getenv("OPENAI_MODEL", "gpt-4o")
        elif provider == "anthropic":
            credentials["api_key"] = os.getenv("ANTHROPIC_API_KEY")
            model = os.getenv("ANTHROPIC_MODEL", "claude-3-opus-20240229")
            
        return await self.execute(provider, messages, credentials, model)

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

llm_runner = LLMRunner()
