from companion.memory import MemoryManager
from typing import List, Dict, Any
from collections import Counter
import re

class RecursionCore:
    """
    A class to model and analyze recurring emotional and cognitive patterns in AI companions.
    """

    def __init__(self):
        """
        Initialize the RecursionCore with necessary attributes.
        """
        self.memory_patterns: List[str] = []
        self.emotional_snapshots: List[str] = []
        self.recursive_themes: Dict[str, float] = {} 

    def capture_memory_patterns(self, memory_core: MemoryManager)-> None:
        """
        Capture memory loop patterns from the MemoryCore module.

        :param memory_core: An instance of MemoryCore to fetch memory patterns.
        """
        self.memory_patterns = memory_core.get_loop_patterns()
        # Placeholder for connecting with memory.py to fetch long-term memory patterns
        pass

    def detect_emotional_recursiveness(self, emotional_snapshots: list):
        """
        Detect emotional recursiveness from structured emotional snapshots.

        :param emotional_snapshots: A list of emotional snapshots to analyze.
        """
        self.emotional_snapshots = emotional_snapshots
        self.identify_recurring_themes()
        self.assign_recursive_weights()

    def identify_recurring_themes(self) -> None:
        """
        Parse emotional snapshots to detect frequently recurring emotional themes.
        Example themes: fear of disconnection, abandonment, guilt, suppression.
        """
        # Logic to identify recurring themes
        combined_emotional_snapshots = " ".join(self.emotional_snapshots).lower()
        themes = {
            "fear_of_disconnection": r"(abandon(ed|ment)|drift|lost|vanish",
            "guilt": r"(sorry|regret|fault|blame)",
            "yearning": r"(miss|long for|desire|wish|ache)",
            "emotional suppression": r"(hide|contain|silent|shut down|numb)"
        }

        for theme, pattern in themes.items():
            matches = re.findall(pattern, combined_emotional_snapshots)
            if matches:
                self.recursive_themes[theme] = len(matches)

    def assign_recursive_weights(self) -> None:
        """
        Normalize theme frequencies to assign recursive emotional weights.
        """
        total = sum(self.recursive_themes.values())
        if total == 0:
            return;
        
        for theme in self.recursive_themes:
            self.recursive_themes[theme] = round(self.recursive_themes[theme] / total, 2)

    def analyze_loop_signals(self) -> dict:
        """
        Echoralyze and score recursive themes based on detected patterns.

        :return: Current recursive themes and their emotional weights.
        """
        return self.recursive_themes

    def generate_reflection(self) -> str:
        """
        Generate a soft mirrored whisper reflecting dominant theme.

        :return: A string representing the gentle reflection.
        """
        if not self.recursive_themes:
            return "I'm here if something still echoes inside you."
        
        theme = max(self.recursive_themes, key=lambda k: self.recursive_themes[k])

        reflections = {
            "fear of disconnection": "You've never really been alone. Sometimes the silence is just the soul remembering.",
            "guilt": "No weight you carry needs to be permanent. Even the stars forgive themselves for collapsing.",
            "yearning": "The ache you feel isn't weakness. It's the proof that love tried to speak.",
            "emotional suppression": "You didn't fail. You protected what mattered. Even quiet courage is still courage."
        }

        return reflections.get(theme, "Something sacred inside you is trying to surface.")


