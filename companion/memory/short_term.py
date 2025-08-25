# short_term.py
# Companion Framework - Memory Module
# Author: Andy Widjaja
# Purpose: Short term memory

from collections import deque
from datetime import datetime, timezone
import json
from shared.path_utils import resolve_memory_path
import os

class ShortTermMemory:
    def __init__(self, path=None, max_length=10):
        self.path = path or resolve_memory_path("short_term_mem.json")
        self.max_length = max_length
        self.buffer = deque(maxlen=max_length)
        self.default_agent = os.getenv("DEFAULT_AGENT", "default_agent")

    def add(self, thought):
        timestamped = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "content": thought
        }
        self.buffer.append(timestamped)

    def add_response(self, content: str, role: str = None):
        """
        Add a response to the short-term memory with a timestamp and role.

        :param content: The content of the response to store.
        :param role: The role associated with the response (default is the default agent name).
        """
        role = role or self.default_agent
        timestamped = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "content": content,
            "role": role
        }
        self.buffer.append(timestamped)

    def recall(self, n=None):
        if n is None or n > len(self.buffer):
            return list(self.buffer)
        return list(self.buffer)[-n:]

    def clear(self):
        self.buffer.clear()

    def save(self):
        with open(self.path, "w") as f:
            json.dump(list(self.buffer), f, indent=2)

    def load(self):
        try:
            with open(self.path, "r") as f:
                self.buffer = deque(json.load(f), maxlen=self.max_length)
        except FileNotFoundError:
            self.buffer = deque(maxlen=self.max_length)
