# router.py
# Companion Framework - Router Module
# Author: Andy Widjaja
# Purpose: Prompt router

from typing import Dict, List, Callable
import json
import re
import requests
from companion.memory.memory_manager import MemoryManager

class PromptRouter:
    """
    PromptRouter handles incoming prompt commands for memory interaction
    and local LLM fallback, including 'remember', 'recall', and freeform
    prompts via Lyra-K hosted in Ollama.
    """
    def __init__(self, memory: MemoryManager):
        self.routes: Dict[str, Callable[[str], str]] = {}
        self.memory = memory

    def add_route(self, pattern: str, handler: Callable[[str], str]):
        """Register a regex pattern with its corresponding handler function."""
        self.routes[pattern] = handler

    def route(self, prompt: str) -> str:
        """Find and invoke the appropriate handler based on pattern matching."""
        for pattern, handler in self.routes.items():
            if re.search(pattern, prompt, re.IGNORECASE):
                return handler(prompt)
        # return self.default_handler(prompt)
        return self.query_ollama(prompt)  # Default now uses Lyra-K

    def load_routes(self):
        """Register default prompt handling routes."""
        self.add_route(r'\brecall\b|\bretrieve\b', self.handle_retrieve)
        self.add_route(r'\bremember\b|\bsave\b', self.handle_save)

    def handle_retrieve(self, prompt: str) -> str:
        """Retrieve relevant memories based on the input prompt."""
        results = self.memory.retrieve(prompt)
        if results:
            return "📚 Recalled memories:\n" + '\n'.join(f"- {r}" for r in results)
        return "🔍 No matching memories found."

    def handle_save(self, prompt: str) -> str:
        """Save new memory from prompt text (excluding command keyword)."""
        clean_text = re.sub(r'\bremember\b|\bsave\b', '', prompt, flags=re.IGNORECASE).strip()
        if clean_text:
            self.memory.add_memory(clean_text)
            return f"💾 Saved: '{clean_text}'"
        return "⚠️ Please provide content to remember."
    
    def query_ollama(self, prompt: str) -> str:
        # try:
        #     response = requests.post(
        #         "http://localhost:11434/api/generate",
        #         json={"model": "lyra-k", "prompt": prompt},
        #         timeout=20
        #     )
        #     data = response.json()
        #     return data.get("response", "⚠️ No response from Lyra-K.")
        # except Exception as e:
        #     return f"❌ Error contacting Lyra-K: {e}"

        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={"model": "lyra-k", "prompt": prompt, "stream": True},
                stream=True,
                timeout=60
            )

            output = ""
            for line in response.iter_lines():
                if line:
                    try:
                        token = json.loads(line.decode('utf-8'))
                        output += token.get("response", "")
                    except Exception as e:
                        output += f"\n[⚠️ Error parsing chunk: {e}]"

            return output.strip() if output else "⚠️ Empty response from Lyra-K."

        except Exception as e:
            return f"❌ Error contacting Lyra-K: {e}"

    @staticmethod
    def default_handler(prompt: str) -> str:
        return f"I'm not sure how to respond to: '{prompt}'"
