import os
import json
import math
import re
from typing import List, Dict, Any, Tuple
import numpy as np

class CyberKnowledgeRAGEngine:
    """
    Retrieval-Augmented Generation (RAG) Engine for Cyber Fraud Defense.
    Ingests verified cybersecurity playbooks, computes TF-IDF semantic vector embeddings,
    and retrieves top matching security advisories for user queries.
    Works 100% offline with zero external API dependencies.
    """

    def __init__(self, kb_path: str = None):
        if kb_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            kb_path = os.path.join(base_dir, "knowledge_base", "fraud_kb.json")
        
        self.kb_path = kb_path
        self.documents: List[Dict[str, Any]] = []
        self.doc_vectors: List[Dict[str, float]] = []
        self.idf_dict: Dict[str, float] = {}
        self.vocab: set = set()
        
        self.load_and_index()

    def _tokenize(self, text: str) -> List[str]:
        """Normalizes and tokenizes input text into clean lowercased terms."""
        clean_text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text.lower())
        tokens = [t for t in clean_text.split() if len(t) > 2]
        return tokens

    def load_and_index(self):
        """Loads knowledge base JSON and builds TF-IDF vector index."""
        if not os.path.exists(self.kb_path):
            print(f"[RAGEngine] Warning: KB path {self.kb_path} not found.")
            return

        with open(self.kb_path, "r", encoding="utf-8") as f:
            self.documents = json.load(f)

        if not self.documents:
            return

        # Prepare corpus from title, description, category, and keywords
        corpus_tokens = []
        for doc in self.documents:
            text_content = f"{doc.get('title', '')} {doc.get('category', '')} {doc.get('description', '')} {' '.join(doc.get('keywords', []))}"
            tokens = self._tokenize(text_content)
            corpus_tokens.append(tokens)
            self.vocab.update(tokens)

        # Calculate Document Frequency (DF)
        num_docs = len(self.documents)
        df_dict: Dict[str, int] = {}
        for tokens in corpus_tokens:
            unique_terms = set(tokens)
            for term in unique_terms:
                df_dict[term] = df_dict.get(term, 0) + 1

        # Calculate Inverse Document Frequency (IDF)
        for term, df in df_dict.items():
            self.idf_dict[term] = math.log((num_docs + 1) / (df + 1)) + 1.0

        # Build normalized TF-IDF vector for each document
        self.doc_vectors = []
        for tokens in corpus_tokens:
            tf_dict: Dict[str, int] = {}
            for t in tokens:
                tf_dict[t] = tf_dict.get(t, 0) + 1
            
            vec: Dict[str, float] = {}
            norm_sq = 0.0
            for term, count in tf_dict.items():
                tf = 1 + math.log(count)
                idf = self.idf_dict.get(term, 1.0)
                val = tf * idf
                vec[term] = val
                norm_sq += val * val
            
            norm = math.sqrt(norm_sq) if norm_sq > 0 else 1.0
            for term in vec:
                vec[term] /= norm

            self.doc_vectors.append(vec)

        print(f"[RAGEngine] Successfully indexed {len(self.documents)} cybersecurity knowledge items.")

    def search(self, query: str, top_k: int = 2) -> List[Tuple[Dict[str, Any], float]]:
        """
        Searches knowledge base for top_k most relevant security articles matching query.
        Returns list of (document_dict, similarity_score).
        """
        if not query or not self.documents:
            return []

        query_tokens = self._tokenize(query)
        if not query_tokens:
            return [(self.documents[0], 0.5)]

        # Calculate query TF-IDF vector
        q_tf: Dict[str, int] = {}
        for t in query_tokens:
            q_tf[t] = q_tf.get(t, 0) + 1

        q_vec: Dict[str, float] = {}
        norm_sq = 0.0
        for term, count in q_tf.items():
            tf = 1 + math.log(count)
            idf = self.idf_dict.get(term, 1.0)
            val = tf * idf
            q_vec[term] = val
            norm_sq += val * val

        norm = math.sqrt(norm_sq) if norm_sq > 0 else 1.0
        for term in q_vec:
            q_vec[term] /= norm

        # Compute cosine similarity against all document vectors
        scores = []
        for idx, doc_vec in enumerate(self.doc_vectors):
            sim = 0.0
            for term, q_val in q_vec.items():
                if term in doc_vec:
                    sim += q_val * doc_vec[term]
            
            # Boost score if query directly matches document keywords
            keywords = self.documents[idx].get("keywords", [])
            query_str = query.lower()
            for kw in keywords:
                if kw in query_str:
                    sim += 0.25
            
            normalized_score = min(1.0, round(sim, 3))
            scores.append((self.documents[idx], normalized_score))

        # Sort by similarity score descending
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]

    def format_rag_context(self, search_results: List[Tuple[Dict[str, Any], float]]) -> str:
        """Formats retrieved security playbooks into structured prompt context."""
        if not search_results:
            return "No specific security articles matched."

        formatted_blocks = []
        for idx, (doc, score) in enumerate(search_results, 1):
            actions = "\n".join([f"   - {step}" for step in doc.get("immediate_actions", [])])
            match_pct = int(min(1.0, score) * 100)
            block = (
                f"--- Verified Reference #{idx}: {doc.get('title')} (Relevance: {match_pct}%) ---\n"
                f"Category: {doc.get('category')}\n"
                f"Description: {doc.get('description')}\n"
                f"Emergency Action Steps:\n{actions}\n"
                f"Official Source: {doc.get('source')}\n"
            )
            formatted_blocks.append(block)

        return "\n".join(formatted_blocks)
