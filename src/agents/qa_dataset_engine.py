import re
import os
import pandas as pd
from typing import Dict, Any, Optional, List, Tuple
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DATASET_PATH = Path(__file__).resolve().parent.parent / "model" / "data" / "cybercrime_reporting_chatbot_100_qa.csv"

# Incident question IDs from the 100 Q&A dataset where next-step guidelines should be appended
FINANCIAL_INCIDENT_IDS = {2, 4, 8, 16, 24, 53, 55, 56, 65}
CREDENTIAL_INCIDENT_IDS = {15, 22, 28, 33, 47, 50, 69}

# Emergency guidelines matching the user's reference specification
EMERGENCY_GUIDELINES = {
    "financial_fraud": """

2. **The Golden Hour (Call 1930):** Dial National Cyber Crime Helpline **1930** within 2–3 hours. The Citizen Financial Cyber Fraud Reporting system can freeze money in the fraudster's mule bank before cashout.

3. **Collect Transaction Evidence:** Gather the Bank UTR number, debit reference, recipient account/UPI ID, and debit SMS timestamp.

4. **File Complaint:** Submit full details at **https://cybercrime.gov.in** and present the acknowledgement slip to your branch manager.""",

    "compromised_credentials": """

2. **Account Lockdown:** Contact your bank or app provider immediately to freeze access and revoke active sessions.

3. **Credential Reset:** Change all passwords and PINs from a known clean, secure device.

4. **Report to Authorities:** Report incident details promptly at **https://cybercrime.gov.in** or call **1930**."""
}


class CybercrimeQADatasetEngine:
    """
    Dedicated Intelligent Q&A Engine trained on cybercrime_reporting_chatbot_100_qa.csv.
    Employs multigram TF-IDF vectorization and domain-weighted semantic similarity to match
    user queries to the authoritative 100 cybercrime questions and answers.
    Optimized to return the precise answer for the asked query without unnecessary bloat.
    """

    def __init__(self, dataset_path: Optional[Path] = None):
        self.dataset_path = dataset_path or DATASET_PATH
        self.df: Optional[pd.DataFrame] = None
        self.vectorizer: Optional[TfidfVectorizer] = None
        self.question_vectors = None
        self.qa_pairs: List[Dict[str, Any]] = []
        self._load_and_train()

    def _normalize(self, text: str) -> str:
        """Cleans and standardizes query text for high recall matching."""
        if not text:
            return ""
        t = text.lower().strip()
        t = re.sub(r'[^a-z0-9\s]', ' ', t)
        
        # Strip common conversation filler phrases to reveal core intent
        for filler in [
            "can you tell me about", "tell me about", "i want to know about",
            "please explain to me", "explain to me", "explain", "please explain",
            "what do you mean by", "what can i do if", "what should i do if",
            "what to do if", "how can i", "how do i", "how to", "what is a",
            "what is an", "what is", "what are"
        ]:
            if t.startswith(filler + " "):
                t = t[len(filler) + 1:].strip()
                break

        # Standardize core domain terminology
        t = t.replace("cyber crime", "cybercrime")
        t = t.replace("online fraud", "payment fraud")
        t = t.replace("bank acc", "bank account")
        t = t.replace("otp code", "otp")
        t = t.replace("deep fake", "deepfake")
        t = t.replace("voice clone", "voice spoofing")
        t = t.replace("simswap", "sim swap")
        return re.sub(r'\s+', ' ', t).strip()

    def _load_and_train(self):
        """Loads 100 Q&A dataset and fits TF-IDF semantic index."""
        if not self.dataset_path.exists():
            print(f"[QAEngine] Warning: Dataset not found at {self.dataset_path}")
            return

        try:
            self.df = pd.read_csv(self.dataset_path)
            self.qa_pairs = []
            corpus = []

            for _, row in self.df.iterrows():
                qid = int(row["id"])
                q_text = str(row["question"]).strip()
                ans_text = str(row["answer"]).strip()
                cat = str(row.get("category", "cybercrime_awareness_and_reporting"))
                
                self.qa_pairs.append({
                    "id": qid,
                    "question": q_text,
                    "answer": ans_text,
                    "category": cat
                })

                # Rich representation: repeat normalized and original question with answer context
                clean_q = self._normalize(q_text)
                rich_text = f"{q_text} {q_text} {q_text} {clean_q} {ans_text}"
                corpus.append(rich_text)

            # Fit TF-IDF with unigrams, bigrams, and trigrams
            self.vectorizer = TfidfVectorizer(
                ngram_range=(1, 3),
                sublinear_tf=True,
                stop_words="english",
                min_df=1
            )
            self.question_vectors = self.vectorizer.fit_transform(corpus)
            print(f"[QAEngine] Successfully trained Q&A engine on {len(self.qa_pairs)} authoritative questions from dataset.")
        except Exception as e:
            print(f"[QAEngine] Error loading dataset: {e}")

    def query(self, user_query: str, language: str = "English") -> Optional[Dict[str, Any]]:
        """
        Evaluates user query against the 100 Q&A dataset.
        Returns matched Q&A dict if confidence threshold is met, otherwise None.
        """
        if not user_query or not self.qa_pairs or self.vectorizer is None or self.question_vectors is None:
            return None

        raw_query = user_query.strip().lower()
        clean_q = self._normalize(user_query)
        if not clean_q:
            clean_q = raw_query

        # 1. Exact or near-exact match
        for item in self.qa_pairs:
            orig_q_norm = self._normalize(item["question"])
            if clean_q == orig_q_norm or raw_query == item["question"].lower():
                return self._format_response(item, score=1.0, language=language)

        # 2. Vectorized TF-IDF Cosine Similarity
        search_str = f"{user_query} {clean_q}"
        q_vec = self.vectorizer.transform([search_str])
        sims = cosine_similarity(q_vec, self.question_vectors)[0]

        # 3. Keyword-specific domain routing & boosting
        words = set(re.findall(r'\b\w+\b', clean_q))

        # Direct domain topic overrides for high precision
        if "whatsapp" in words:
            for item in self.qa_pairs:
                if item["id"] == 33:
                    return self._format_response(item, score=0.95, language=language)

        if "aadhaar" in words:
            target_id = 22 if "otp" in words or "stranger" in words or "call" in words else 21
            for item in self.qa_pairs:
                if item["id"] == target_id:
                    return self._format_response(item, score=0.95, language=language)

        if "cybercrime" in words and len(words) <= 3:
            for item in self.qa_pairs:
                if item["id"] == 1:
                    return self._format_response(item, score=0.95, language=language)

        best_idx = int(sims.argmax())
        best_score = float(sims[best_idx])

        # If similarity threshold is met (score >= 0.18)
        if best_score >= 0.18:
            matched_item = self.qa_pairs[best_idx]
            return self._format_response(matched_item, score=best_score, language=language)

        return None

    def _format_response(self, item: Dict[str, Any], score: float, language: str = "English") -> Dict[str, Any]:
        """Formats the response according to user requirements (clean answer + optional guidelines)."""
        qid = item["id"]
        question = item["question"]
        base_answer = item["answer"]
        
        # Determine if additional emergency guidelines should be provided
        append_guidelines = ""
        is_incident = False
        if qid in FINANCIAL_INCIDENT_IDS:
            append_guidelines = EMERGENCY_GUIDELINES["financial_fraud"]
            is_incident = True
        elif qid in CREDENTIAL_INCIDENT_IDS:
            append_guidelines = EMERGENCY_GUIDELINES["compromised_credentials"]
            is_incident = True

        # Multilingual translation for non-English queries
        if language != "English":
            final_text = self._translate_if_needed(base_answer, append_guidelines, language)
        else:
            if is_incident and append_guidelines:
                final_text = f"1. **Immediate Action:** {base_answer}{append_guidelines}"
            else:
                final_text = base_answer

        return {
            "matched_id": qid,
            "matched_question": question,
            "answer": final_text,
            "raw_answer": base_answer,
            "score": round(score, 4),
            "category": item["category"]
        }

    def _translate_if_needed(self, answer: str, guidelines: str, language: str) -> str:
        """Provides localized responses when user converses in Tamil, German, or Japanese."""
        if language == "Tamil":
            text = f"💡 **பதில்:** {answer}"
            if guidelines:
                text += "\n\n🚨 **அவசர உதவி வழிகாட்டுதல்:**\n2. **தங்க நேரம் (1930 அழைப்பு):** பணத்தை முடக்க தேசிய உதவி எண் **1930** அழைக்கவும்.\n3. **ஆதாரங்கள்:** வங்கி UTR எண் மற்றும் குறுஞ்செய்தி சேமிக்கவும்.\n4. **புகார் பதிவு:** அதிகாரப்பூர்வ **https://cybercrime.gov.in** இணையதளத்தில் புகார் அளிக்கவும்."
            return text
        elif language == "German":
            text = f"💡 **Antwort:** {answer}"
            if guidelines:
                text += "\n\n🚨 **Dringende Schritte:**\n2. **Notruf (1930):** Rufen Sie umgehend die Cyber-Helpline 1930 an, um verdächtige Transaktionen zu stoppen.\n3. **Beweise sichern:** UTR-Nummer, Transaktions-ID und Screenshots sammeln.\n4. **Anzeige erstatten:** Offizielle Meldung unter https://cybercrime.gov.in einreichen."
            return text
        elif language == "Japanese":
            text = f"💡 **回答:** {answer}"
            if guidelines:
                text += "\n\n🚨 **緊急ガイドライン:**\n2. **ゴールデンアワー (1930番に通報):** 被害拡大を防ぐため直ちに1930番または銀行へ通報してください。\n3. **証拠収集:** 取引UTR番号、送金先ID、SMSを保存してください。\n4. **被害届の提出:** 公式ポータル https://cybercrime.gov.in から被害届を提出してください。"
            return text
        return answer
