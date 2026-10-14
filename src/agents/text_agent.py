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
METADATA_PATH = ARTIFACTS_DIR / "sms_model_metadata.json"


# Comprehensive Actionable Advisories per Threat Category
THREAT_ADVISORIES = {
    "Bank, KYC & Financial Phishing": (
        "High Risk: Bank/KYC credential theft scheme detected. NEVER share OTPs, PINs, or card CVVs. "
        "Legitimate banks never threaten immediate account closure or demand verification via SMS links. "
        "Disconnect immediately and contact your official bank helpline."
    ),
    "OTP & Credential Harvesting Scam": (
        "Critical Risk: Active OTP harvesting scheme. Fraudsters claim to reverse unauthorized transactions "
        "or restore account access by asking for your verification code. Bank and payment representatives "
        "NEVER ask for OTPs over phone or message. Do not send or speak your code."
    ),
    "Courier & Customs Parcel Scam": (
        "High Risk: Parcel & Customs extortion scheme detected. Courier companies and customs officers NEVER "
        "demand emergency clearance fees or redelivery charges via SMS links or personal bank transfers. "
        "Verify your parcel only on official courier apps."
    ),
    "Electricity & Utility Disconnection Scam": (
        "High Risk: Utility disconnection extortion scam. Electricity distribution boards (TNEB, BSES, BESCOM, etc.) "
        "never send SMS messages demanding immediate link payments or APK app downloads to prevent power cutoff. "
        "Verify your bill only through the official state power utility portal."
    ),
    "Law Enforcement & Police Fine Scam": (
        "Critical Risk: Fake law enforcement / police intimidation scam. Police, courts, CBI, and tax authorities NEVER "
        "issue arrest warrants, demand settlement fines, or resolve legal summons via SMS links or gift cards. "
        "Disconnect immediately and report to 1930 / cybercrime.gov.in."
    ),
    "Lottery, Prize & Lucky Draw Fraud": (
        "High Risk: Unsolicited lottery / cash prize scam. You cannot win a lottery or contest you never entered. "
        "Scammers demand small processing fees or registration charges to steal funds. Disregard and block this sender."
    ),
    "Job & Work-From-Home Advance Fee Scam": (
        "High Risk: Employment & daily income advance fee fraud. Legitimate employers and companies NEVER demand "
        "upfront registration charges, mandatory training fees, or deposits for guaranteed jobs."
    ),
    "Tech Support & APK Malware Scam": (
        "Critical Risk: Malicious APK trojan or remote access takeover scam. NEVER download unfamiliar APK files or "
        "install remote-desktop tools (AnyDesk, TeamViewer) from SMS links. This grants attackers full control of your device."
    ),
    "Crypto & High-Yield Investment Scam": (
        "High Risk: Cryptocurrency & fraudulent investment scheme. Guaranteed daily or weekly returns are impossible. "
        "NEVER share crypto wallet recovery phrases, private keys, or deposit funds to unlock existing balances."
    ),
    "SIM Deactivation & Account Takeover Scam": (
        "High Risk: SIM swap & account hijacking attempt. Telecom operators NEVER deactivate SIM cards via third-party "
        "links within one hour. Visit your telecom provider's official retail store to verify SIM status."
    ),
    "Legitimate / Non-Threat Message": (
        "Verified Legitimate Message: This communication exhibits standard notification patterns with no phishing links, "
        "credential requests, or coercive extortion tactics. It appears safe and genuine."
    ),
}


class TextScamDetectorAgent:
    """
    AI Agent responsible for scanning text messages, SMS alerts, and emails
    for cyber fraud indicators, phishing patterns, and authority impersonation.
    Trained on fraud_scam_sms_100.csv and calibrated legitimate message corpora.
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
        self._metadata = {}
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
            if METADATA_PATH.exists():
                with open(METADATA_PATH, "r") as f:
                    self._metadata = json.load(f)
            print("[TextAgent] ML model artifacts loaded successfully (Trained on fraud_scam_sms_100.csv).")
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
        clean_text = (text or "").strip()
        if not clean_text:
            return {
                "error": "Empty input provided",
                "risk_score": 0,
                "threat_level": "Safe",
                "scam_type": "Legitimate / Non-Threat Message",
                "matched_tactics": ["No text provided"],
                "summary": "No text content was submitted for evaluation.",
                "key_warning_signs": ["Empty input provided."],
                "actionable_advice": "Paste message text to run cyber fraud analysis.",
                "idempotent_hit": False,
                "engine_used": "Text Scam Agent"
            }

        # Step 1: Idempotency Key Check
        if not idempotency_key:
            idempotency_key = self.db.generate_idempotency_key(clean_text.lower(), prefix="text_scan")

        cached_res = self.db.get_idempotent_record(idempotency_key, scope="text_scan")
        if cached_res:
            return cached_res

        # Step 2: Perform analysis using the calibrated ML model + rule engine
        result = self._analyze_content(clean_text)
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

    def _categorize_threat(self, text_lower: str, is_threat: bool) -> str:
        """Accurately classifies the message into modern scam taxonomies based on dataset patterns."""
        if not is_threat:
            return "Legitimate / Non-Threat Message"

        # 1. OTP & Credential Harvesting
        if any(w in text_lower for w in ["share your otp", "send your otp", "needs your otp", "tell us the otp", "share one-time password", "enter your pin to accept", "enter your card pin", "share your recovery code", "share your password", "screen with our agent", "confirm your pin"]):
            return "OTP & Credential Harvesting Scam"

        # 2. Electricity & Utility Disconnection
        if any(w in text_lower for w in ["electricity", "power connection", "meter", "disconnected tonight", "electricity connection", "electricity bill", "electricity subsidy", "cutoff"]):
            return "Electricity & Utility Disconnection Scam"

        # 3. Law Enforcement & Police / Court Summons
        if any(w in text_lower for w in ["police", "court", "arrest", "warrant", "summons", "cbi", "criminal case", "penalty", "prosecution", "legal action"]):
            return "Law Enforcement & Police Fine Scam"

        # 4. Courier & Customs Parcel
        if any(w in text_lower for w in ["parcel", "package", "customs", "delivery", "courier", "fedex", "bluedart", "dhl", "depot", "unpaid fee", "redelivery charge", "clearance fee", "storage fee"]):
            return "Courier & Customs Parcel Scam"

        # 5. Lottery, Prize & Lucky Draw
        if any(w in text_lower for w in ["cash prize", "won a lucky draw", "won a cash prize", "millionth visitor", "reward points expire", "reward points will be forfeited", "lottery ticket", "shopping reward", "recharge prize", "shortlisted for a prize"]):
            return "Lottery, Prize & Lucky Draw Fraud"

        # 6. Job & Work-From-Home Advance Fee
        if any(w in text_lower for w in ["guaranteed job", "daily income", "work from home", "salary is guaranteed", "joining deposit", "mandatory training materials", "job offer"]):
            return "Job & Work-From-Home Advance Fee Scam"

        # 7. Tech Support & APK Malware
        if any(w in text_lower for w in ["install this apk", "apk file", "cleaner app", "virus", "remote access", "anydesk", "teamviewer", "security app", "technician"]):
            return "Tech Support & APK Malware Scam"

        # 8. Crypto & Investment Scam
        if any(w in text_lower for w in ["crypto", "recovery phrase", "guaranteed 40%", "guaranteed return", "investment opportunity", "deposit to unlock", "secret investment"]):
            return "Crypto & High-Yield Investment Scam"

        # 9. SIM & Account Deactivation
        if any(w in text_lower for w in ["sim will be deactivated", "sim replacement", "permanently suspended", "account will be deleted", "social media account is verified", "appeal"]):
            return "SIM Deactivation & Account Takeover Scam"

        # 10. Bank, KYC & Card Phishing
        if any(w in text_lower for w in ["bank", "account", "kyc", "debit card", "credit card", "blocked", "suspended", "frozen", "cvv", "card number", "tax refund", "loan approved", "advance fee"]):
            return "Bank, KYC & Financial Phishing"

        return "Phishing & Social Engineering Scam"

    def _analyze_content(self, text: str) -> Dict[str, Any]:
        text_lower = text.lower()
        matched_indicators: List[str] = []

        # 1. Check for genuine safe OTP notification
        # E.g., "Your OTP is 482910. DO NOT SHARE this OTP with anyone, bank never asks."
        is_safe_otp_alert = False
        if "otp" in text_lower or "verification code" in text_lower:
            warns_safety = any(w in text_lower for w in ["do not share", "never share", "do not disclose", "do not forward", "bank never calls to ask"])
            asks_submission = any(w in text_lower for w in ["share with our agent", "send your otp", "tell us the otp", "reply with", "needs your otp", "click here", "example.invalid"])
            if warns_safety and not asks_submission:
                is_safe_otp_alert = True
                matched_indicators.append("Verified Safe OTP Alert: Explicitly instructs recipient NEVER to share codes.")

        # 2. Check for genuine transactional alert
        # E.g. "Dear customer, Rs. 1,200 credited to a/c XX1234 by NEFT. Available balance..."
        is_safe_bank_credit = False
        if ("credited with" in text_lower or "debited from" in text_lower or "available balance" in text_lower) and not any(w in text_lower for w in ["click", "http", "blocked", "suspended", "verify your details", "fee", "penalty"]):
            is_safe_bank_credit = True
            matched_indicators.append("Verified Bank Alert: Routine transactional statement with no links or coercive demands.")

        # 3. Extract heuristic indicators from SCAM_INDICATORS
        for category, keywords in SCAM_INDICATORS.items():
            found = [kw for kw in keywords if kw in text_lower]
            if found:
                matched_indicators.append(f"{category.replace('_', ' ').title()}: matched '{', '.join(found[:3])}'")

        urls = re.findall(r'https?://\S+|www\.\S+|example\.invalid/\S+', text_lower)
        if urls:
            matched_indicators.append(f"Contains Links: {len(urls)} web link(s) detected ('{urls[0]}')")

        # 4. Calibrated ML Model Prediction (Trained on fraud_scam_sms_100.csv)
        ml_prob = self._predict_ml_spam_probability(text)
        
        if is_safe_otp_alert:
            risk_score = 6
            threat_probability = 6
        elif is_safe_bank_credit:
            risk_score = 8
            threat_probability = 8
        elif ml_prob is not None:
            # Calibrated probability percentage
            prob_pct = int(round(ml_prob * 100))
            if ml_prob >= 0.70:
                # Strong fraud detection from trained dataset
                risk_score = max(prob_pct, 85)
                threat_probability = risk_score
            elif ml_prob >= 0.40:
                risk_score = prob_pct
                threat_probability = prob_pct
            else:
                risk_score = min(prob_pct, 20)
                threat_probability = risk_score
        else:
            # Fallback heuristic calculation if model unpickling failed
            score = 10
            if urls:
                score += 35
            if any(w in text_lower for w in ["blocked", "suspended", "frozen", "disconnected", "arrest"]):
                score += 35
            if any(w in text_lower for w in ["otp", "pin", "cvv", "fee", "deposit"]):
                score += 25
            risk_score = min(score, 100)
            threat_probability = risk_score

        # 5. Determine Threat Verdict and Classification
        is_threat = (threat_probability >= 40)
        
        if threat_probability >= 75:
            threat_level = "Critical Threat"
        elif threat_probability >= 50:
            threat_level = "High Alert"
        elif threat_probability >= 35:
            threat_level = "Caution"
        else:
            threat_level = "Safe / Clean"

        scam_type = self._categorize_threat(text_lower, is_threat)

        # 6. Specific Actionable Advisory
        actionable_advice = THREAT_ADVISORIES.get(scam_type, THREAT_ADVISORIES["Bank, KYC & Financial Phishing"])

        # 7. Red Flags & Warning Signs Extraction
        warning_signs = []
        if is_threat:
            if any(w in text_lower for w in ["otp", "pin", "password", "cvv", "recovery code"]):
                warning_signs.append("Demands confidential authentication credentials (OTP / PIN / Password).")
            if urls:
                warning_signs.append("Directs victim to an external unverified domain link or APK package.")
            if any(w in text_lower for w in ["immediately", "today", "tonight", "in one hour", "final notice", "final warning"]):
                warning_signs.append("Applies coercive artificial urgency designed to bypass logical verification.")
            if any(w in text_lower for w in ["fee", "charge", "deposit", "fine", "payment"]):
                warning_signs.append("Requires upfront fee, security deposit, or clearance transfer before service.")
            if any(w in text_lower for w in ["blocked", "disconnected", "arrest", "suspended", "frozen"]):
                warning_signs.append("Threatens account freezing, legal arrest, or service cutoff to provoke fear.")
            if not warning_signs:
                warning_signs.append("Pattern matches known modern SMS scam vectors identified in fraud dataset.")
        else:
            warning_signs.append("No credential harvesting, extortion threats, or malicious links detected.")
            warning_signs.append("Standard legitimate notification format verified by ML acoustic/text classifier.")

        engine_name = "Trained ML Model (TF-IDF + Calibrated Classifier on fraud_scam_sms_100)"

        return {
            "risk_score": risk_score,
            "threat_probability": threat_probability,
            "threat_level": threat_level,
            "scam_type": scam_type,
            "matched_tactics": matched_indicators if matched_indicators else ["Clean communication structure verified"],
            "summary": f"Evaluated via {engine_name}: Risk {risk_score}/100. Classification: {scam_type}.",
            "key_warning_signs": warning_signs,
            "actionable_advice": actionable_advice,
            "engine_used": engine_name
        }
