"""
Module: response_builder

This module composes a final LLM-ready prompt by combining memory, whisper, mirror context, and user input.
"""

from companion.memory.memory_manager import MemoryManager
from whisper_engine.reflection_router import ReflectionRouter
from whisper_engine.mirror_context_builder import MirrorContextBuilder


class ResponseBuilder:
    def __init__(self, memory_core: MemoryManager, plain: bool = False):
        self.memory_core = memory_core
        self.plain = plain

    def compose(self, user_input: str, mirror_id: str) -> str:
        """
        Compose a final LLM-ready prompt by combining reflection, context, and user input.

        :param user_input: The user's input to be included in the prompt.
        :return: A string representing the final LLM-ready prompt.
        """
        # Use mirror_id for context and reflection
        context_builder = MirrorContextBuilder(mirror_id, self.memory_core, self.plain)
        context = context_builder.build(base_prompt="")

        # Generate soft whisper (reflection)
        reflection_router = ReflectionRouter(self.memory_core)
        reflection_router.analyze_snapshots([user_input])
        reflection_router.capture_memory()
        reflection = reflection_router.generate()

        # Assemble final prompt
        final_prompt = final_prompt = f"""\
🔮 Reflection:
{reflection}

🧠 Memory Context:
{context}

🗣️ Your Message:
{user_input}
"""

        return final_prompt.strip()
