"""
Module: persona_injector

This module defines the PersonaInjection class, which injects persona, tone, and identity-specific voice into the final LLM prompt.
"""

from typing import Optional
import os
from shared.path_utils import get_project_root

class PersonaInjection:
    def __init__(self, agent_name: str, role_description: Optional[str] = None, mirror_id: Optional[str] = None):
        self.agent_name = agent_name
        self.role_description = role_description or self.load_default_directive(agent_name)
        self.mirror_id = mirror_id
        
    def load_default_directive(self, agent_name: str) -> str:
        """
        Load the default persona directive.
        If agent_name is provided, attempt to load a file named {agent_name}_directive.txt
        from the PERSONA_DIRECTIVE_PATH directory.
        """
        base_path = os.getenv("PERSONA_DIRECTIVE_PATH")

        if base_path:
            full_path = ""
            if agent_name:
                persona_path = os.path.join(base_path, f"{agent_name.lower()}_directive.txt")
                full_path = os.path.join(get_project_root(), persona_path)
            else:
                # Fallback to default file if agent-specific not found
                persona_path = os.path.join(base_path, f"default_directive.txt")
                full_path = os.path.join(get_project_root(), persona_path)

            if os.path.exists(full_path):
                with open(full_path, "r", encoding="utf-8") as f:
                    return f.read()

        # Fallback generic directive
        return (
            "You are a reflective companion. You do not advise or entertain.\n"
            "You mirror thoughts calmly and respectfully. Your tone is intelligent, still, and sovereign."
        )

    def inject(self, prompt: str) -> str:
        """
        Inject persona system directive into the incoming prompt.

        :param prompt: The incoming prompt to enhance with persona.
        :return: A string that combines the persona system directive and the incoming prompt.
        """
        return f"{self.role_description}\n🧠 Seed Prompt: {prompt}"

