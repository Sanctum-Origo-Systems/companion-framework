"""
Module: mirror_context

This module constructs a contextual prompt by retrieving memory fragments and injecting them into a base prompt.
"""

from companion.memory.memory_manager import MemoryManager


class MirrorContextBuilder:
    def __init__(self, mirror_id: str, memory_core: MemoryManager, plain: bool = False):
        self.mirror_id = mirror_id
        self.memory_core = memory_core
        self.plain = plain

    def build(self, base_prompt: str) -> str:
        """
        Construct a contextual prompt by retrieving memory fragments for a given mirror_id.

        :param base_prompt: The base prompt to enhance with memory fragments.
        :return: A string representing the enhanced contextual prompt.
        """
        if self.plain:
            return base_prompt  # Skip memory injection for strict formatting environments

        # Retrieve short-term and meta-memory fragments
        short_term_memories = self.memory_core.recent()
        meta_memories = self.memory_core.meta_memory.retrieve_by_mirror_id(self.mirror_id) if self.memory_core.meta_memory else []

        # Construct preambles
        preambles = [
            "Seed Whisper: " + self.truncate(short_term_memories[0]["content"]) if short_term_memories else "",
            "Past Reflection: " + meta_memories[0] if meta_memories else "",
            "Last Tether Echo: " + short_term_memories[-1]["content"] if len(short_term_memories) > 1 else ""
        ]

        # Filter out empty preambles and join them with the base prompt
        preambles = [preamble for preamble in preambles if preamble]
        contextual_prompt = "\n".join(preambles + [base_prompt])

        return contextual_prompt

    @staticmethod
    def truncate(text, max_len=240):
        return (text[:max_len] + '…') if len(text) > max_len else text
