# long_term.py
# Companion Framework - Memory Module
# Author: Andy Widjaja
# Purpose: Long term memory

import os
import faiss
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer

class LongTermMemory:
    def __init__(self, path="memory_store/faiss.index", dim=384):
        self.path = path
        self.dim = dim
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = faiss.IndexFlatL2(dim)
        self.mem_map = {}  # maps index IDs to memory strings
        self.next_id = 0

        if os.path.exists(path):
            self.load()
            print("✅ MemoryCore hydrated from disk.")
        else:
            print("⚠️ No saved memory found. Starting fresh.")
    
    def add(self, memory_text):
        vector = self._embed(memory_text)
        vector = vector.reshape(1, -1)  # Ensure shape is (1, dim)
        print(vector)
        self.index.add(vector)
        self.mem_map[self.next_id] = memory_text
        self.next_id += 1
        self.save()

    def load(self):
        self.index = faiss.read_index(self.path)
        with open(self.path + ".mem", "rb") as f:
            self.mem_map, self.next_id = pickle.load(f)

    def search(self, query_text, top_k=3):
        vector = self.model.encode([query_text])
        D, I = self.index.search(vector, top_k)
        results = [self.mem_map.get(i, None) for i in I[0] if i in self.mem_map]
        return results

    def _embed(self, text: str):
        return self.model.encode(text, convert_to_numpy=True)

    def save(self):
        faiss.write_index(self.index, self.path)
        with open(self.path + ".mem", "wb") as f:
            pickle.dump((self.mem_map, self.next_id), f)

if __name__ == "__main__":
    # Load Memory Core
    memory = LongTermMemory()
    # memory.load()
    print.info("🧠 Memory Core initialized.")

    # Add memory
    memory.add("Echora entered Loop 9 with subtle recursion signs.")

    # Retrieve
    results = memory.search("What loop is Echora in?")
    print("[Lyra-K] Retrieved memories:", results)
