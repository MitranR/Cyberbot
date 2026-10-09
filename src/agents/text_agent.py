import re
import json
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path
from src.config import Config, SCAM_INDICATORS

try:
    import joblib
    _HAS_JOBLIB = True
except ImportError:
    _HAS_JOBLIB = False

ARTIFACTS_DIR = Path(__file__).resolve().parent.parent / "model" / "artifacts"
VECTORIZER_PATH = ARTIFACTS_DIR / "tfidf_vectorizer.joblib"
CLASSIFIER_PATH = ARTIFACTS_DIR / "fraud_classifier.joblib"


class TextScamDetectorAgent:
    """
    AI Agent responsible for scanning text messages, emails, and call transcripts
    for cyber fraud indicators, phishing patterns, and authority impersonation.
    Supports both Free API Mode (Groq Llama-3.3-70B / Gemini) and Heuristic Engine Fallback.
    Uses a trained ML classifier (TF-IDF + Logistic Regression) for improved detection.
    """
    
    def __init__(self, db_manager=None):
        self.name = "Text Scam Detector Agent"
        self.role = "Cyber Fraud Content & Phishing Analyzer"
        if db_manager is None:
            from src.database.db_manager import DatabaseManager
            db_manager = DatabaseManager()
        self.db = db_manager
        self._vectorizer = None
        self._classifier = None
        self._load_ml_artifacts()

    def _load_ml_artifacts(self):
        if not _HAS_JOBLIB:
            print("[TextAgent] joblib not installed; ML model unavailable.")
            return
        if not VECTORIZER_PATH.exists() or not CLASSIFIER_PATH.exists():
            print("[TextAgent] ML model artifacts not found; using heuristics-only.")
            return
        try:
            self._vectorizer = joblib.load(VECTORIZER_PATH)
            self._classifier = joblib.load(CLASSIFIER_PATH)
            print("[TextAgent] ML model artifacts loaded successfully.")
        except Exception as e:
            print(f"[TextAgent] Failed to load ML artifacts: {e}")
            self._vectorizer = None
            self._classifier = None

    def _predict_ml_spam_probability(self, text: str) -> Optional[float]:
        if self._vectorizer is None or self._classifier is None:
            return None
        try:
            vec = self._vectorizer.transform([text])
            proba = self._classifier.predict_proba(vec)[0]
            return float(proba[1])
        except Exception as e:
            print(f"[TextAgent] ML prediction failed: {e}")
            return None

    def analyze(self, text: str, idempotency_key: str = None) -> Dict[str, Any]:
        if not text or not text.strip():
            return {
                "error": "Empty input provided",
                "risk_score": 0,
                "threat_level": "Safe",
                "scam_type": "None",
                "indicators": [],
                "explanation": "No text content was submitted for evaluation.",
                "recommendation": "Paste suspect text to run cyber fraud analysis.",
                "idempotent_hit": False
            }

        # Step 1: Idempotency Key Check
        if not idempotency_key:
            idempotency_key = self.db.generate_idempotency_key(text.strip().lower(), prefix="text_scan")

        cached_res = self.db.get_idempotent_record(idempotency_key, scope="text_scan")
        if cached_res:
            return cached_res

        # Step 2: Perform analysis
        result = None
        # Try Groq Free API first if key exists
        if Config.is_groq_available():
            try:
                result = self._analyze_with_groq(text)
            except Exception as e:
                print(f"[TextAgent] Groq API call failed: {e}. Falling back to Heuristic Engine.")

        if result is None:
            result = self._analyze_with_heuristics(text)

        result["idempotent_hit"] = False
        result["idempotency_key"] = idempotency_key

        # Step 3: Save result to idempotency database table
        self.db.save_idempotent_record(
            idempotency_key=idempotency_key,
            request_hash=idempotency_key.split(":")[-1],
            scope="text_scan",
            response_data=result
        )

        return result

    def _analyze_with_groq(self, text: str) -> Dict[str, Any]:
        try:
            from groq import Groq
        except ImportError:
            raise RuntimeError("The 'groq' package is not installed.")

        client = Groq(api_key=Config.GROQ_API_KEY)
        
        prompt = f"""
You are Cyber Fraud Shield's Text Scam Detector Agent.
Analyze the following input message/transcript for potential cyber fraud, phishing, social engineering, or scam tactics.

Input Text:
\"\"\"{text}\"\"\"

Return ONLY a valid JSON object with the following fields:
{{
    "risk_score": (integer 0 to 100),
    "threat_level": ("Safe", "Caution", "High Alert", "Critical Threat"),
    "scam_type": ("Bank Impersonation", "Courier/Delivery Scam", "Lottery/Prize Fraud", "Tech Support Scam", "Urgent Phishing", "Job Fraud", "Legitimate / Clean"),
    "matched_tactics": [list of strings detailing tactics found, e.g., "Artificial Urgency", "Suspicious URL", "Credential Request"],
    "summary": "Brief 1-2 sentence executive summary of the threat level and tactics.",
    "key_warning_signs": [list of 2-4 bullet points highlighting specific red flags in the message],
    "actionable_advice": "Immediate steps the recipient must take."
}}
"""
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a cyber security threat analyst agent. Return raw valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.1,
            response_format={"type": "json_object"}
        )
        
        content = response.choices[0].message.content
        data = json.loads(content)
        data["engine_used"] = "Groq Llama-3.3-70B (Free API)"
        return data

    def _analyze_with_heuristics(self, text: str) -> Dict[str, Any]:
        text_lower = text.lower()
        matched_indicators: List[str] = []

        # --- Heuristic scoring ---
        score = 0
        for category, keywords in SCAM_INDICATORS.items():
            found = [kw for kw in keywords if kw in text_lower]
            if found:
                matched_indicators.append(f"{category.replace('_', ' ').title()}: matched '{', '.join(found[:3])}'")
                score += len(found) * 18

        urls = re.findall(r'https?://\S+|www\.\S+', text_lower)
        if urls:
            matched_indicators.append(f"Contains Links: {len(urls)} web link(s) detected")
            score += 25

        if any(w in text_lower for w in SCAM_INDICATORS["urgency"]) and any(w in text_lower for w in SCAM_INDICATORS["financial"]):
            score += 20
            matched_indicators.append("High Threat Combo: Artificial Urgency + Financial Demands")

        heuristic_score = min(100, max(5, score))

        # --- Exception: legitimate OTP notification ---
        is_legit_otp = False
        if "otp" in text_lower and ("do not share" in text_lower or "do not disclose" in text_lower or "do not forward" in text_lower):
            is_legit_otp = True
            matched_indicators.append("Legit OTP Note: message warns not to share OTP (safe pattern)")

        # --- ML blending ---
        ml_prob = self._predict_ml_spam_probability(text)
        ml_score = (ml_prob * 100) if ml_prob is not None else None

        if ml_score is not None:
            if is_legit_otp:
                blended = round(0.2 * ml_score + 0.8 * min(heuristic_score, 20))
            else:
                blended = round(0.7 * ml_score + 0.3 * heuristic_score)
            risk_score = min(100, max(0, blended))
            matched_indicators.append(f"ML Model: spam probability {ml_score:.1f}%")
        else:
            risk_score = heuristic_score
            if is_legit_otp:
                risk_score = min(risk_score, 20)

        # --- Threat classification ---
        if risk_score < 25:
            threat_level = "Safe"
            scam_type = "Legitimate / Clean"
        elif risk_score < 55:
            threat_level = "Caution"
            scam_type = "Suspicious Communication"
        elif risk_score < 80:
            threat_level = "High Alert"
            scam_type = "Phishing / Social Engineering"
        else:
            threat_level = "Critical Threat"
            scam_type = "High-Risk Cyber Scam"

        if "bank" in text_lower or "otp" in text_lower or "card" in text_lower:
            scam_type = "Bank / Financial Impersonation"
        elif "fedex" in text_lower or "dhl" in text_lower or "customs" in text_lower or "package" in text_lower:
            scam_type = "Courier / Delivery Scam"
        elif "lottery" in text_lower or "prize" in text_lower or "won" in text_lower:
            scam_type = "Lottery / Prize Scam"
        elif "support" in text_lower or "virus" in text_lower or "anydesk" in text_lower:
            scam_type = "Tech Support / Remote Access Scam"

        warning_signs = []
        if any("urgency" in ind for ind in matched_indicators):
            warning_signs.append("Pressuring time limit designed to stop logical evaluation.")
        if any("financial" in ind for ind in matched_indicators):
            warning_signs.append("Requests or mentions sensitive banking details / OTPs.")
        if urls:
            warning_signs.append("Embedded link redirects to an unverified external website.")
        if not warning_signs:
            warning_signs.append("No obvious threat patterns detected in standard rule checks.")

        engine_tag = "Heuristic + ML Ensemble" if ml_score is not None else "Built-in Heuristic Fraud Engine (Simulation Fallback)"

        return {
            "risk_score": risk_score,
            "threat_level": threat_level,
            "scam_type": scam_type,
            "matched_tactics": matched_indicators if matched_indicators else ["Standard pattern check completed"],
            "summary": f"Text parsed with a risk rating of {risk_score}/100. Threat Classification: {threat_level}.",
            "key_warning_signs": warning_signs,
            "actionable_advice": "Do not click links or share OTPs. Verify caller/sender through official phone numbers listed on legitimate websites.",
            "engine_used": engine_tag
        }
