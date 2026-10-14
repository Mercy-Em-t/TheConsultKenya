import os
import json
import re
import math
from typing import List, Dict, Any

class FullProjectRAGBuilder:
    def __init__(self, workspace_root: str):
        self.workspace_root = workspace_root
        self.rag_dir = os.path.join(workspace_root, "rag_knowledge")
        self.cards_dir = os.path.join(self.rag_dir, "cards")
        self.index_dir = os.path.join(self.rag_dir, "index")
        os.makedirs(self.cards_dir, exist_ok=True)
        os.makedirs(self.index_dir, exist_ok=True)
        
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

    def clean_text(self, text: str) -> str:
        text = re.sub(r'#+\s*', '', text)
        text = re.sub(r'\*+', '', text)
        text = re.sub(r'`+', '', text)
        text = re.sub(r'\|', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def chunk_markdown_file(self, file_path: str, category: str, base_prefix: str, card_counter: int) -> List[Dict[str, Any]]:
        rel_path = os.path.relpath(file_path, self.workspace_root)
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            raw_content = f.read()

        # Split by major headings (# or ##)
        sections = re.split(r'\n(?=#{1,3}\s+)', raw_content)
        new_cards = []

        for idx, sec in enumerate(sections):
            sec_clean = sec.strip()
            if not sec_clean or len(sec_clean) < 150:
                continue

            # Extract title
            header_match = re.match(r'^(#{1,3}\s+)([^\n]+)', sec_clean)
            topic = header_match.group(2).strip() if header_match else f"{os.path.basename(file_path)} Section {idx+1}"
            topic = re.sub(r'[*_`]', '', topic)

            # Sub-chunk if section is too large (> 3000 chars)
            chunks = []
            if len(sec_clean) > 3000:
                paras = sec_clean.split("\n\n")
                current_chunk = []
                current_len = 0
                for p in paras:
                    current_chunk.append(p)
                    current_len += len(p)
                    if current_len >= 1800:
                        chunks.append("\n\n".join(current_chunk))
                        current_chunk = []
                        current_len = 0
                if current_chunk:
                    chunks.append("\n\n".join(current_chunk))
            else:
                chunks = [sec_clean]

            for sub_idx, chunk_text in enumerate(chunks):
                card_id = f"{base_prefix}-{card_counter:03d}"
                card_counter += 1

                cleaned_content = self.clean_text(chunk_text)
                summary_sentences = re.split(r'(?<=[.!?])\s+', cleaned_content)
                summary = " ".join(summary_sentences[:2]) if summary_sentences else topic
                if len(summary) > 250:
                    summary = summary[:247] + "..."

                # Extract entities/tags
                tags = [f"#{t}" for t in re.findall(r'\b[A-Z][a-zA-Z0-9]{3,}\b', topic)[:4]]
                if f"#{category}" not in tags:
                    tags.append(f"#{category.replace(' ', '')}")

                card = {
                    "card_id": card_id,
                    "category": category,
                    "topic": topic if len(chunks) == 1 else f"{topic} (Part {sub_idx+1})",
                    "source_file": rel_path.replace("\\", "/"),
                    "page_number": idx + 1,
                    "summary": summary,
                    "key_entities": list(set(re.findall(r'\b[A-Z][a-zA-Z0-9]{2,}\b', topic)[:5])),
                    "content": chunk_text[:2500],
                    "grounded_rules": [
                        f"Grounded directly in authoritative project specification: {rel_path.replace(chr(92), '/')}"
                    ],
                    "tags": tags
                }
                new_cards.append(card)

        return new_cards

    def build_corpus(self):
        all_cards = []
        counter = 1

        # 1. Existing baseline knowledge cards (preserve and re-number)
        baseline_file = os.path.join(self.cards_dir, "cards_master.json")
        if os.path.exists(baseline_file):
            with open(baseline_file, "r", encoding="utf-8") as f:
                existing = json.load(f)
                for c in existing:
                    c["card_id"] = f"RAG-BASE-{counter:03d}"
                    counter += 1
                    all_cards.append(c)

        # 2. Ingest Planning Phase
        planning_dir = os.path.join(self.workspace_root, "sad_phase1_planning")
        if os.path.exists(planning_dir):
            p_counter = 1
            for f in sorted(os.listdir(planning_dir)):
                if f.endswith(".md"):
                    cards = self.chunk_markdown_file(os.path.join(planning_dir, f), "Planning & Management", "RAG-PLAN", p_counter)
                    p_counter += len(cards)
                    all_cards.extend(cards)

        # 3. Ingest Use Cases Phase
        use_cases_dir = os.path.join(self.workspace_root, "use_cases")
        if os.path.exists(use_cases_dir):
            uc_counter = 1
            for f in sorted(os.listdir(use_cases_dir)):
                if f.endswith(".md"):
                    cards = self.chunk_markdown_file(os.path.join(use_cases_dir, f), "Use Cases & Functional", "RAG-UC", uc_counter)
                    uc_counter += len(cards)
                    all_cards.extend(cards)

        # 4. Ingest Processes & DFD Phase
        proc_dir = os.path.join(self.workspace_root, "processes")
        if os.path.exists(proc_dir):
            pr_counter = 1
            for f in sorted(os.listdir(proc_dir)):
                if f.endswith(".md"):
                    cards = self.chunk_markdown_file(os.path.join(proc_dir, f), "Process & DFD Architecture", "RAG-DFD", pr_counter)
                    pr_counter += len(cards)
                    all_cards.extend(cards)

        # 5. Ingest Data Modelling & ERD Phase
        ent_dir = os.path.join(self.workspace_root, "entities")
        if os.path.exists(ent_dir):
            e_counter = 1
            for f in sorted(os.listdir(ent_dir)):
                if f.endswith(".md"):
                    cards = self.chunk_markdown_file(os.path.join(ent_dir, f), "Data Modelling & ERD", "RAG-ERD", e_counter)
                    e_counter += len(cards)
                    all_cards.extend(cards)

        # 6. Ingest IEEE SRS Specification
        srs_file = os.path.join(self.workspace_root, "CONSULT_KENYA_IEEE_SRS_V2.md")
        if os.path.exists(srs_file):
            srs_cards = self.chunk_markdown_file(srs_file, "IEEE SRS Specification", "RAG-SRS", 1)
            all_cards.extend(srs_cards)

        print(f"Total structured RAG cards extracted across all phases: {len(all_cards)}")

        # Save cards master
        master_path = os.path.join(self.cards_dir, "cards_master.json")
        with open(master_path, "w", encoding="utf-8") as f:
            json.dump(all_cards, f, indent=2)

        # Save summary markdown
        summary_path = os.path.join(self.cards_dir, "cards_summary.md")
        with open(summary_path, "w", encoding="utf-8") as f:
            f.write("# Master RAG Knowledge Index for Consult Kenya\n\n")
            f.write(f"Total Grounded RAG Knowledge Cards: **{len(all_cards)}**\n\n")
            f.write("| Card ID | Category | Topic | Source Document | Key Entities |\n")
            f.write("| :--- | :--- | :--- | :--- | :--- |\n")
            for c in all_cards:
                entities = ", ".join(c.get("key_entities", [])[:3])
                f.write(f"| **{c['card_id']}** | {c['category']} | {c['topic']} | `{c['source_file']}` | {entities} |\n")

        # Generate Dense Vector Embeddings (256-dim)
        indexed_entries = []
        for c in all_cards:
            full_text = f"{c['topic']} {c['category']} {c['summary']} {c['content']} {' '.join(c.get('tags', []))}"
            vec = self.embed(full_text)
            indexed_entries.append({
                "card": c,
                "vector": vec
            })

        vector_path = os.path.join(self.index_dir, "vector_index.json")
        with open(vector_path, "w", encoding="utf-8") as f:
            json.dump(indexed_entries, f, indent=2)

        print(f"Successfully vectorized and indexed {len(indexed_entries)} cards into {vector_path}")
        self.generate_standalone_retriever()

    def embed(self, text: str) -> List[float]:
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

    def generate_standalone_retriever(self):
        code = '''# Consult Kenya Comprehensive Project RAG Retriever
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
        tokens = re.findall(r'\\b\\w+\\b', text.lower())
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
    print(f"\\nQuery: '{q}' (Top {len(results)} matches):")
    print("=" * 70)
    for score, card in results:
        print(f"[{card['card_id']}] {card['topic']} (Similarity Score: {score:.4f})")
        print(f"Category: {card['category']} | Source: {card['source_file']}")
        print(f"Summary: {card['summary']}")
        print("-" * 70)
'''
        retriever_path = os.path.join(self.rag_dir, "rag_retriever.py")
        with open(retriever_path, "w", encoding="utf-8") as f:
            f.write(code)

if __name__ == "__main__":
    builder = FullProjectRAGBuilder(r"c:\Users\user\Documents\KenyaConsult")
    builder.build_corpus()
