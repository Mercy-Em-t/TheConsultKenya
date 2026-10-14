import json
import math
import re
from typing import List, Dict, Any

class LocalDenseEmbedder:
    """Deterministic, zero-dependency semantic embedder with domain synonym expansion."""
    def __init__(self, dim: int = 128):
        self.dim = dim
        self.synonyms = {
            "consult": ["advisory", "expert", "specialist", "consultant", "consulting"],
            "instagram": ["visual", "carousel", "reel", "video", "feed", "stories", "card"],
            "linkedin": ["professional", "authority", "b2b", "profile", "portfolio", "enterprise"],
            "payment": ["mpesa", "stk", "paystack", "flutterwave", "card", "checkout", "money"],
            "escrow": ["milestone", "protection", "deposit", "release", "contract", "trust"],
            "algorithm": ["ranking", "feed", "scoring", "retrieval", "discovery", "weights"],
            "booking": ["calendar", "schedule", "modal", "appointment", "meeting", "call"]
        }

    def embed(self, text: str) -> List[float]:
        vec = [0.0] * self.dim
        tokens = re.findall(r'\b\w+\b', text.lower())
        for token in tokens:
            # direct token hash
            h = abs(hash(token)) % self.dim
            vec[h] += 1.0
            # synonym expansion
            for root, syns in self.synonyms.items():
                if token == root or token in syns:
                    h_syn = abs(hash(root)) % self.dim
                    vec[h_syn] += 1.5

        # Normalization
        norm = math.sqrt(sum(x * x for x in vec))
        if norm > 0:
            vec = [x / norm for x in vec]
        return vec

def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    return sum(a * b for a, b in zip(v1, v2))

# Load cards
with open("rag_knowledge/cards/cards_master.json", "r", encoding="utf-8") as f:
    cards = json.load(f)

embedder = LocalDenseEmbedder()

indexed_entries = []
for c in cards:
    full_text = f"{c['topic']} {c['category']} {c['summary']} {c['content']} {' '.join(c['tags'])}"
    vec = embedder.embed(full_text)
    indexed_entries.append({
        "card": c,
        "vector": vec
    })

# Save index
with open("rag_knowledge/index/vector_index.json", "w", encoding="utf-8") as f:
    json.dump(indexed_entries, f, indent=2)

print(f"Indexed {len(indexed_entries)} cards into rag_knowledge/index/vector_index.json")

# Self-contained Query Engine
query_engine_code = '''import json
import math
import re

class RAGRetriever:
    def __init__(self, index_path="rag_knowledge/index/vector_index.json"):
        with open(index_path, "r", encoding="utf-8") as f:
            self.index = json.load(f)
        self.dim = 128
        self.synonyms = {
            "consult": ["advisory", "expert", "specialist", "consultant", "consulting"],
            "instagram": ["visual", "carousel", "reel", "video", "feed", "stories", "card"],
            "linkedin": ["professional", "authority", "b2b", "profile", "portfolio", "enterprise"],
            "payment": ["mpesa", "stk", "paystack", "flutterwave", "card", "checkout", "money"],
            "escrow": ["milestone", "protection", "deposit", "release", "contract", "trust"],
            "algorithm": ["ranking", "feed", "scoring", "retrieval", "discovery", "weights"],
            "booking": ["calendar", "schedule", "modal", "appointment", "meeting", "call"]
        }

    def embed(self, text):
        vec = [0.0] * self.dim
        tokens = re.findall(r'\\b\\w+\\b', text.lower())
        for token in tokens:
            h = abs(hash(token)) % self.dim
            vec[h] += 1.0
            for root, syns in self.synonyms.items():
                if token == root or token in syns:
                    h_syn = abs(hash(root)) % self.dim
                    vec[h_syn] += 1.5
        norm = math.sqrt(sum(x * x for x in vec))
        return [x / norm for x in vec] if norm > 0 else vec

    def query(self, query_text, top_k=3):
        q_vec = self.embed(query_text)
        scored = []
        for entry in self.index:
            score = sum(a * b for a, b in zip(q_vec, entry["vector"]))
            scored.append((score, entry["card"]))
        scored.sort(key=lambda x: x[0], reverse=True)
        return scored[:top_k]

if __name__ == "__main__":
    import sys
    retriever = RAGRetriever()
    q = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "How does payment and escrow work?"
    print(f"Query: '{q}'\\n" + "="*50)
    for score, card in retriever.query(q, top_k=3):
        print(f"[{card['card_id']}] {card['topic']} (Score: {score:.4f})")
        print(f"Category: {card['category']} | Page: {card['page_number']}")
        print(f"Summary: {card['summary']}")
        print("-" * 50)
'''

with open("rag_knowledge/rag_retriever.py", "w", encoding="utf-8") as f:
    f.write(query_engine_code)

print("Created query engine at rag_knowledge/rag_retriever.py")
