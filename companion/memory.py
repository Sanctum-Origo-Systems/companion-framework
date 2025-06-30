# memory_manager.py
# Companion Framework - Memory Module
# Author: Andy Widjaja
# Purpose: Lightweight memory manager with short-term, long-term, and meta-memory support

import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class MemoryCore:
    def __init__(self, dim=384, model_name='all-MiniLM-L6-v2'):
        self.index = faiss.IndexFlatL2(dim)
        self.text_store = []
        self.model = SentenceTransformer(model_name)
        self.dim = dim
        self.memory_path = './memory'  # Default memory path; can be overridden
    
    def add_memory(self, text: str):
        embedding = self._embed(text)
        self.index.add(np.array([embedding]))
        self.text_store.append(text)

    def hydrate(self):
        if os.path.exists(os.path.join(self.memory_path, 'faiss.index')) and \
           os.path.exists(os.path.join(self.memory_path, 'store.txt')):
            self.load_index(self.memory_path)
            print("✅ MemoryCore hydrated from disk.")
        else:
            print("⚠️ No saved memory found. Starting fresh.")

    def retrieve(self, query: str, top_k=5):
        query_embedding = self._embed(query)
        D, I = self.index.search(np.array([query_embedding]), top_k)
        return [self.text_store[i] for i in I[0] if i < len(self.text_store)]

    def _embed(self, text: str):
        return self.model.encode(text, convert_to_numpy=True)

    def save_index(self, path: str):
        faiss.write_index(self.index, os.path.join(path, 'faiss.index'))
        with open(os.path.join(path, 'store.txt'), 'w') as f:
            f.writelines('\n'.join(self.text_store))

    def load_index(self, path: str):
        self.index = faiss.read_index(os.path.join(path, 'faiss.index'))
        with open(os.path.join(path, 'store.txt'), 'r') as f:
            self.text_store = [line.strip() for line in f.readlines()]