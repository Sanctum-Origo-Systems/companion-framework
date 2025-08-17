"""
Module: reflection_router

This module provides functionality to generate whisper reflections using the RecursionCore.
"""

from typing import List
from companion.recursion import RecursionCore
from companion.memory.memory_manager import MemoryManager


class ReflectionRouter:
    def __init__(self, memory_core: MemoryManager):
        self.memory_core = memory_core
        self.recursion_core = RecursionCore()

    def analyze_snapshots(self, emotional_snapshots: List[str]) -> None:
        """
        Analyze emotional snapshots to detect recursiveness.

        :param emotional_snapshots: A list of emotional snapshots to analyze.
        """
        self.recursion_core.detect_emotional_recursiveness(emotional_snapshots)

    def capture_memory(self) -> None:
        """
        Capture memory patterns from the memory core.
        """
        self.recursion_core.capture_memory_patterns(self.memory_core)

    def generate(self) -> str:
        """
        Generate a whisper reflection based on analyzed data.

        :return: A string representing the generated reflection.
        """
        return self.recursion_core.generate_reflection()
