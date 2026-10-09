import os
from dotenv import load_dotenv

# Load environment variables from .env file if available
load_dotenv()

class Config:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()
    HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "").strip()
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
    FORCE_SIMULATION = os.getenv("FORCE_SIMULATION_MODE", "False").lower() in ("true", "1", "t")

    @classmethod
    def is_groq_available(cls) -> bool:
        return bool(cls.GROQ_API_KEY) and not cls.FORCE_SIMULATION

    @classmethod
    def is_hf_available(cls) -> bool:
        return bool(cls.HUGGINGFACE_API_KEY) and not cls.FORCE_SIMULATION

    @classmethod
    def is_gemini_available(cls) -> bool:
        return bool(cls.GEMINI_API_KEY) and not cls.FORCE_SIMULATION

    @classmethod
    def active_mode(cls) -> str:
        if cls.FORCE_SIMULATION:
            return "Simulation Mode (Forced)"
        active_keys = []
        if cls.GROQ_API_KEY:
            active_keys.append("Groq Free API")
        if cls.HUGGINGFACE_API_KEY:
            active_keys.append("Hugging Face Free API")
        if cls.GEMINI_API_KEY:
            active_keys.append("Gemini Free API")
        
        if active_keys:
            return f"Free API Mode ({', '.join(active_keys)})"
        return "Simulation Mode (Offline Fallback Engine)"

# Scam classification rules & indicators
SCAM_INDICATORS = {
    "urgency": ["urgent", "immediately", "24 hours", "suspended", "blocked", "act now", "warning", "police", "legal action"],
    "financial": ["bank", "transfer", "otp", "pin", "credit card", "debit card", "refund", "lottery", "crypto", "prize", "account locked"],
    "suspicious_links": ["http://", "https://", "bit.ly", "tinyurl", "login-verify", "secure-update", "bank-auth", "click here"],
    "authority_impersonation": ["fedex", "dhl", "customs", "tax department", "irs", "support team", "security department", "whatsapp center"],
    "credential_harvesting": ["password", "verification code", "ssn", "aadhaar", "cvv", "security question"]
}

# Incident Emergency Protocol Playbooks
EMERGENCY_PLAYBOOKS = {
    "Shared OTP / PIN": [
        "🚨 Immediately contact your bank's fraud helpline to block your cards and freeze net banking.",
        "📱 Change online banking passwords and disable UPI/digital wallets linked to the account.",
        "📝 File an official Cyber Crime report at https://cybercrime.gov.in or call national helpline 1930.",
        "🔒 Scan your device for malware or remote control apps (e.g. AnyDesk, TeamViewer)."
    ],
    "Clicked Suspicious Link": [
        "🌐 Disconnect Wi-Fi and mobile data immediately to stop potential data exfiltration.",
        "🔑 Change credentials for all accounts accessed on that device using a separate secure device.",
        "🛡️ Clear browser cache, cookies, and inspect installed browser extensions.",
        "🦠 Run a full antivirus scan on your system."
    ],
    "Simulated Voice / Impersonation Call": [
        "📞 Hang up immediately. Never call back on the number provided in the voice call.",
        "👥 Contact the real family member or organization via a independently verified number.",
        "🚫 Block the incoming caller ID and report as spam.",
        "⚠️ Warn close contacts about target impersonation scam."
    ],
    "Financial Loss / Transfer Sent": [
        "🚨 Call bank immediately to request a payment reversal / chargeback under fraudulent transaction protocol.",
        "📞 Dial National Cybercrime Helpline 1930 (or local financial cyber hotline).",
        "📄 Preserve all evidence: transaction IDs, chat logs, call recordings, and screenshot receipts.",
        "🚔 Register an FIR at the nearest police station or cyber crime cell."
    ]
}
