# short_term.py
# Companion Framework - Memory Module
# Author: Andy Widjaja
# Purpose: Short term memory

from collections import deque
from datetime import datetime, timezone
import json

class ShortTermMemory:
    def __init__(self, max_length=10):
        self.max_length = max_length
        self.buffer = deque(maxlen=max_length)

    def add(self, thought):
        timestamped = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "content": thought
        }
        self.buffer.append(timestamped)

    def recall(self, n=None):
        if n is None or n > len(self.buffer):
            return list(self.buffer)
        return list(self.buffer)[-n:]

    def clear(self):
        self.buffer.clear()

    def save(self, path="memory_store/short_term_mem.json"):
        with open(path, "w") as f:
            json.dump(list(self.buffer), f, indent=2)

    def load(self, path="memory_store/short_term_mem.json"):
        try:
            with open(path, "r") as f:
                self.buffer = deque(json.load(f), maxlen=self.max_length)
        except FileNotFoundError:
            self.buffer = deque(maxlen=self.max_length)
