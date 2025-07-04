# memory_manager.py
# Companion Framework - Memory Module
# Author: Andy Widjaja
# Purpose: Memory manager

from companion.memory.short_term import ShortTermMemory
from companion.memory.long_term import LongTermMemory

class MemoryManager:
    def __init__(self, long_term_path="faiss.index", dim=384, short_term_limit=10):
        self.short_term = ShortTermMemory(max_length=short_term_limit)
        self.long_term = LongTermMemory(path=long_term_path, dim=dim)

    def add(self, memory_text):
        """Adds memory to both short and long-term."""
        self.short_term.add(memory_text)
        self.long_term.add(memory_text)

    def recent(self, n=5):
        """Returns the last n short-term memories."""
        return self.short_term.get_recent(n)

    def search(self, query_text, k=5):
        """Searches long-term memory for semantically similar entries."""
        return self.long_term.search(query_text, k)

    def save_all(self):
        """Saves both memory components."""
        self.short_term.save()
        self.long_term.save()

    def load_all(self):
        """Loads both memory components."""
        self.short_term.load()
        self.long_term.load()
