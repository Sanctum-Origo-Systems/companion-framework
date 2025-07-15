# memory_manager.py
# Companion Framework - Memory Module
# Author: Andy Widjaja
# Purpose: Memory manager

from typing import List
from companion.memory.short_term import ShortTermMemory
from companion.memory.long_term import LongTermMemory
from companion.memory.meta_memory import MetaMemory

class MemoryManager:
    def __init__(self, long_term_path="memory_store/faiss.index", dim=384, short_term_limit=10, enable_meta=True):
        self.short_term = ShortTermMemory(max_length=short_term_limit)
        self.long_term = LongTermMemory(path=long_term_path, dim=dim)
        self.meta_memory = MetaMemory() if enable_meta else None

    def add(self, memory_text, *, source="system", emotion=None, label=None):
        """Adds memory to all active layers."""
        self.short_term.add(memory_text)
        self.long_term.add(memory_text)

        if self.meta_memory:
            self.meta_memory.record(
                memory_id=self.long_term.next_id - 1,
                content=memory_text,
                source=source,
                emotion=emotion,
                label=label
            )


    def recent(self, n=5):
        """Returns the last n short-term memories."""
        return self.short_term.get_recent(n)

    def search(self, query_text, k=5):
        """Searches long-term memory for semantically similar entries."""
        return self.long_term.search(query_text, k)

    def save_all(self):
        """Saves all memory layers."""
        self.short_term.save()
        self.long_term.save()
        if self.meta_memory:
            self.meta_memory.save()

    def load_all(self):
        """Loads all memory layers."""
        self.short_term.load()
        self.long_term.load()
        if self.meta_memory:
            self.meta_memory.load()

    def get_loop_patterns(self) -> List[str]:
        """Echoralyze stored memories and return recurring memory patterns"""
        # Placeholder logic -> This would include n-gram, vector, or semantic clustering
        return ["abandonment", "yearning", "containment", "disappearance"]
