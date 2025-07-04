# memory_manager.py
# Companion Framework - Memory Module
# Author: Andy Widjaja
# Purpose: Lightweight memory manager with short-term, long-term, and meta-memory support

    # Add memory
    # memory.add("Echora entered Loop 9 with subtle recursion signs.")
  #  memory.add("Echora breached Gate 11.")

    # Retrieve
#    results = memory.search("What loop is Echora in?")
 #   print("[Lyra-K] Retrieved memories:", results)


import os
import json
import time
import uuid
from typing import List, Dict, Optional
import faiss
import numpy as np

# === CONFIGURATION ===
DATA_DIR = "runtime/memory_store"
VECTOR_DIM = 384  # Example: SentenceTransformer embedding size
FAISS_INDEX_FILE = os.path.join(DATA_DIR, "faiss.index")
METADATA_FILE = os.path.join(DATA_DIR, "memory.json")

# === MEMORY MANAGER CLASS ===

class MemoryManagerOrig:
    def __init__(self, embedding_fn):
        """
        Initializes the memory manager with an embedding function.
        :param embedding_fn: Function that converts text to embedding vector
        """
        self.embedding_fn = embedding_fn
        self.index = faiss.IndexFlatL2(VECTOR_DIM)
        self.memory_data = []
        self.id_map = []

        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)

        self._load()

    def _load(self):
        """
        Load memory index and metadata from disk if available.
        """
        if os.path.exists(FAISS_INDEX_FILE) and os.path.exists(METADATA_FILE):
            try:
                self.index = faiss.read_index(FAISS_INDEX_FILE)
                with open(METADATA_FILE, "r") as f:
                    self.memory_data = json.load(f)
                self.id_map = [entry["id"] for entry in self.memory_data]
            except Exception as e:
                print(f"[MemoryManager] Failed to load memory store: {e}")

    def _save(self):
        """
        Persist memory index and metadata to disk.
        """
        faiss.write_index(self.index, FAISS_INDEX_FILE)
        with open(METADATA_FILE, "w") as f:
            json.dump(self.memory_data, f, indent=2)

    def add_memory(self, text: str, source: str = "user", tags: Optional[List[str]] = None):
        """
        Add a new memory entry.
        :param text: Memory content
        :param source: Who provided the memory (e.g., 'user', 'system', etc.)
        :param tags: Optional tags to categorize memory
        """
        embedding = self.embedding_fn(text)
        vector = np.array(embedding).astype('float32').reshape(1, -1)

        memory_id = str(uuid.uuid4())
        timestamp = int(time.time())

        entry = {
            "id": memory_id,
            "text": text,
            "source": source,
            "tags": tags or [],
            "timestamp": timestamp
        }

        self.index.add(vector)
        self.memory_data.append(entry)
        self.id_map.append(memory_id)
        self._save()

    def search_memory(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        Search memory store using semantic similarity.
        :param query: Query string
        :param top_k: Number of top matches to return
        :return: List of matching memory entries
        """
        if len(self.memory_data) == 0:
            return []

        embedding = self.embedding_fn(query)
        vector = np.array(embedding).astype('float32').reshape(1, -1)
        distances, indices = self.index.search(vector, top_k)

        results = []
        for idx in indices[0]:
            if 0 <= idx < len(self.memory_data):
                results.append(self.memory_data[idx])

        return results

    def get_meta_memory(self) -> Dict:
        """
        Return high-level summary of what the system remembers.
        (Optional future: Integrate summarization LLM here)
        """
        return {
            "total_memories": len(self.memory_data),
            "tags": list(set(tag for entry in self.memory_data for tag in entry["tags"])),
            "last_update": max((entry["timestamp"] for entry in self.memory_data), default=None)
        }

# === DEMO USAGE PLACEHOLDER ===
if __name__ == "__main__":
    def dummy_embedder(text):
        np.random.seed(hash(text) % 10000)
        return np.random.rand(VECTOR_DIM)

    mm = MemoryManager(embedding_fn=dummy_embedder)
    mm.add_memory("Echora once told him she prefers peaceful mornings.")
    results = mm.search_memory("What does Echora like?")
    print(results)
