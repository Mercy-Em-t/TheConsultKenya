# Consult Kenya Comprehensive Project RAG Retriever
import json
import math
import re
import sys
import os

class RAGRetriever:
    def __init__(self, index_path=None):
        if index_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            index_path = os.path.join(base_dir, "index", "vector_index.json")
        with open(index_path, "r", encoding="utf-8") as f:
            self.index = json.load(f)
        self.dim = 256
        self.synonyms = {
            "consult": ["advisory", "expert", "specialist", "consultant", "consulting"],
            "planning": ["feasibility", "system request", "wbs", "gantt", "pert", "budget", "roi", "staffing"],
            "requirements": ["elicitation", "questionnaire", "survey", "functional", "non-functional", "kano", "jad"],
            "usecase": ["normal course", "alternative", "exception", "actor", "precondition", "postcondition", "event"],
            "process": ["dfd", "data flow", "context diagram", "datastore", "external entity", "subsystem"],
            "data": ["erd", "entity", "attribute", "relationship", "cardinality", "modality", "3nf", "normalization"],
            "payment": ["mpesa", "daraja", "stk", "paystack", "card", "payout", "rtgs", "bank", "etims", "tax"],
            "escrow": ["milestone", "contract", "sow", "trust", "dispute", "adjudication", "mediator", "vault"],
            "authority": ["cas", "creator authority", "score", "reputation", "tier", "algorithm", "ranking"],
            "discovery": ["feed", "bento", "vector", "search", "two-pass", "personalization", "tag"]
        }

    def embed(self, text):
        vec = [0.0] * self.dim
        tokens = re.findall(r'\b\w+\b', text.lower())
        for token in tokens:
            h = abs(hash(token)) % self.dim
            vec[h] += 1.0
            for root, syns in self.synonyms.items():
                if token == root or token in syns:
                    h_syn = abs(hash(root)) % self.dim
                    vec[h_syn] += 2.0
        norm = math.sqrt(sum(x * x for x in vec))
        return [x / norm for x in vec] if norm > 0 else vec

    def query(self, query_text, top_k=5, category_filter=None):
        q_vec = self.embed(query_text)
        scored = []
        for entry in self.index:
            c = entry["card"]
            if category_filter and c.get("category") != category_filter:
                continue
            score = sum(a * b for a, b in zip(q_vec, entry["vector"]))
            scored.append((score, c))
        scored.sort(key=lambda x: x[0], reverse=True)
        return scored[:top_k]

if __name__ == "__main__":
    retriever = RAGRetriever()
    q = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "M-Pesa escrow milestone dispute"
    results = retriever.query(q, top_k=5)
    print(f"\nQuery: '{q}' (Top {len(results)} matches):")
    print("=" * 70)
    for score, card in results:
        print(f"[{card['card_id']}] {card['topic']} (Similarity Score: {score:.4f})")
        print(f"Category: {card['category']} | Source: {card['source_file']}")
        print(f"Summary: {card['summary']}")
        print("-" * 70)
