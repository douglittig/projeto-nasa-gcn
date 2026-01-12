"""
NASA GCN RAG Agent (Prototype)

Demonstrates how to query the Vector Database to retrieve scientific narratives 
and answer astronomical questions.
"""

from typing import List, Dict, Any
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer

# 1. Connect to Vector Store (Mockup)
# In production, use Databricks Vector Search Client
class MockVectorStore:
    def __init__(self, table_path: str):
        self.table_path = table_path
        print(f"initialized connection to {table_path}...")
    
    def search(self, query_vector: np.array, k: int = 3) -> List[Dict[str, Any]]:
        # Mock results - in production this would query the vector index
        return [
            {
                "event_id": "GRB 230101A", 
                "score": 0.95, 
                "text": "SUBJECT: GRB 230101A: Swift detection... \\n\\n--- \\n\\n AUTHOR: Phil Evans... \\n We detected an optical counterpart..."
            },
            {
                "event_id": "S190425z", 
                "score": 0.88, 
                "text": "ID: S190425z | TYPE: PRELIMINARY... \\n\\n--- \\n\\n The LVC reports a compact binary merger..."
            }
        ]

# 2. Main Agent Logic
class GCNAgent:
    def __init__(self):
        print("Loading embedding model (BAAI/bge-m3)...")
        self.embedder = SentenceTransformer("BAAI/bge-m3")
        self.db = MockVectorStore("sandbox.nasa_gcn_dev.gcn_embeddings")
        
    def answer(self, question: str) -> str:
        print(f"\nQUERY: {question}")
        
        # A. Embed Query
        print("Embedding query...")
        q_vec = self.embedder.encode(question)
        
        # B. Retrieve Context (RAG)
        print("Retrieving relevant events...")
        results = self.db.search(q_vec)
        
        context_str = "\n\n".join([f"Event [{r['event_id']}] (Score: {r['score']}):\n{r['text']}..." for r in results])
        
        # C. Generate Answer (Mockup LLM)
        # In production, use dbrx-instruct or GPT-4
        prompt = f"""
        CONTEXT:
        {context_str}
        
        QUESTION: {question}
        
        INSTRUCTION: Answer the question based on the context provided. Cite the Event ID.
        """
        
        print("-" * 40)
        print(f"GENERATED PROMPT:")
        print(prompt)
        print("-" * 40)
        
        return "Simulated Answer: Based on the context, GRB 230101A had an optical counterpart detected by Swift."

if __name__ == "__main__":
    agent = GCNAgent()
    agent.answer("Which recent GRB had an optical counterpart?")
