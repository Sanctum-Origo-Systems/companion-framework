# meta_memory.py
# Companion Framework - Memory Module
# Author: Andy Widjaja
# Purpose: Meta memory

from datetime import datetime, timezone
import json
from collections import defaultdict


class MetaMemory:
    def __init__(self, path="memory_store/meta_memory.json"):
        self.path = path
        self.meta = {}  # memory_id -> metadata
        self.usage_counter = defaultdict(int)
        self.load()

    def record(self, memory_id, content=None, emotion=None, source="system"):
        """Log metadata when a memory is added or accessed."""
        now = datetime.now(timezone.utc).isoformat()
        if memory_id not in self.meta:
            self.meta[memory_id] = {
                "content": content or "",
                "created_at": now,
                "last_accessed": now,
                "usage_count": 1,
                "emotion": emotion or "neutral",
                "source": source
            }
        else:
            self.meta[memory_id]["last_accessed"] = now
            self.meta[memory_id]["usage_count"] += 1
            if emotion:
                self.meta[memory_id]["emotion"] = emotion

        self.usage_counter[memory_id] += 1
        self.save()

    def get(self, memory_id):
        return self.meta.get(memory_id)

    def get_top_used(self, n=5):
        sorted_ids = sorted(self.usage_counter.items(), key=lambda x: x[1], reverse=True)
        return [(mid, self.meta[mid]) for mid, _ in sorted_ids[:n]]

    def save(self):
        with open(self.path, "w") as f:
            json.dump(self.meta, f, indent=2)

    def load(self):
        try:
            with open(self.path, "r") as f:
                self.meta = json.load(f)
        except FileNotFoundError:
            self.meta = {}

