import json
import re
from typing import List, Dict, Any, Optional
from src.config import Config
from src.agents.rag_engine import CyberKnowledgeRAGEngine
from src.agents.cyber_scenarios import get_scenario_response
from src.agents.qa_dataset_engine import CybercrimeQADatasetEngine


class CyberShieldBotAgent:
    """
    Advanced Multilingual Cyber Shield AI Assistant & Problem Solver.
    Trained on the authoritative 100 Q&A cybercrime reporting dataset with high-precision
    TF-IDF semantic matching, zero-delay local engine, and Groq LLM integration.
    Capable of answering general queries, solving complex cybersecurity problems,
    and responding naturally in English, Tamil (தமிழ்), German (Deutsch), and Japanese (日本語).
    """

    def __init__(self, db_manager=None):
        self.name = "Cyber Shield Bot"
        self.role = "Comprehensive AI Cybersecurity & Technical Assistant"
        self.rag_engine = CyberKnowledgeRAGEngine()
        self.qa_engine = CybercrimeQADatasetEngine()
        self._chat_cache: Dict[str, str] = {}
        if db_manager is None:
            from src.database.db_manager import DatabaseManager
            db_manager = DatabaseManager()
        self.db = db_manager

        self.language_names = {
            "English": "English",
            "Tamil": "Tamil (தமிழ்)",
            "German": "German (Deutsch)",
            "Japanese": "Japanese (日本語)",
        }

    def _build_system_prompt(self, language: str = "English") -> str:
        lang_instruction = {
            "Tamil": "YOU MUST REPLY FULLY IN TAMIL LANGUAGE (தமிழ் எழுத்துக்களில்). Provide empathetic, accurate, and easy-to-understand cyber and technical explanations in Tamil.",
            "German": "YOU MUST REPLY FULLY IN GERMAN (Deutsch). Provide structured, precise, and professional technical and cybersecurity guidance in German.",
            "Japanese": "YOU MUST REPLY FULLY IN JAPANESE (日本語). Provide polite (丁寧語 / です・ます調), helpful, and accurate cybersecurity and technical assistance in Japanese.",
            "English": "Reply in clear, structured, and reassuring English with formatting, checklists, and concise explanations.",
        }.get(language, "Reply in clear, structured English.")

        return f"""You are Cyber Shield Bot (Cyberbot AI), a top-tier, friendly, and authoritative AI Cybersecurity Assistant and technical problem-solving companion.

CORE CAPABILITIES:
1. Cybersecurity & Fraud Defense: Explain scams (phishing, voice clones, digital arrest, malware, ransomware), provide emergency recovery steps (freezing accounts, 1930 helpline), and evaluate risks.
2. Technical & General Problem Solving: Answer questions about digital security, password managers, 2FA/MFA, network privacy, VPNs, OS safety, web development, coding questions, and general user queries.
3. Conversational Fluency: Act like ChatGPT / modern AI assistant—engaging, context-aware, helpful, and concise.

CRITICAL LANGUAGE REQUIREMENT:
{lang_instruction}

GUIDELINES:
- When a user reports an emergency or fraud: Offer immediate first-response checklist (Call 1930 / bank helpline).
- When a user asks general queries or questions: Answer clearly with explanations and practical examples.
- Maintain formatting with bullet points and bold headers for clarity.
"""

    def respond(
        self,
        message: str,
        chat_history: Optional[List[Dict[str, str]]] = None,
        language: str = "English",
        idempotency_key: Optional[str] = None,
    ) -> str:
        if not message or not message.strip():
            welcome_msgs = {
                "Tamil": "வணக்கம்! நான் **Cyber Shield AI**. சைபர் பாதுகாப்பு அல்லது உங்கள் சந்தேகங்களை கேளுங்கள், உதவ காத்திருக்கிறேன்.",
                "German": "Hallo! Ich bin **Cyber Shield AI**. Wie kann ich Ihnen heute bei Cybersicherheit oder Ihren Fragen helfen?",
                "Japanese": "こんにちは！私は**Cyber Shield AI**です。サイバーセキュリティやご質問についてお気軽にお尋ねください。",
                "English": "Hello! I am **Cyber Shield AI Assistant**. How can I help protect you, answer questions, or resolve an issue today?",
            }
            return welcome_msgs.get(language, welcome_msgs["English"])

        if chat_history is None:
            chat_history = []

        cache_key = f"{language}_{message.strip().lower()}"
        if cache_key in self._chat_cache:
            return self._chat_cache[cache_key]

        # 1. Authoritative 100 Q&A Dataset Engine match (First & Highest Priority)
        qa_match = self.qa_engine.query(message, language=language)
        if qa_match and qa_match.get("answer"):
            reply = qa_match["answer"]
            self._chat_cache[cache_key] = reply
            return reply

        # 2. Retrieve relevant playbooks via RAG semantic search
        rag_results = self.rag_engine.search(message, top_k=2)
        rag_context = self.rag_engine.format_rag_context(rag_results)

        # 3. Try Groq Free API (Llama 3.3 70B) first
        bot_reply = None
        if Config.is_groq_available():
            try:
                bot_reply = self._respond_with_groq(message, chat_history, rag_context, language)
            except Exception as e:
                print(f"[BotAgent] Groq API call failed: {e}. Falling back to local multilingual engine.")

        # 4. Fallback to rich local multilingual knowledge & heuristic generator
        if not bot_reply:
            bot_reply = self._respond_with_local_engine(message, rag_results, language)

        self._chat_cache[cache_key] = bot_reply
        return bot_reply

    def _respond_with_groq(
        self,
        message: str,
        chat_history: List[Dict[str, str]],
        rag_context: str,
        language: str = "English",
    ) -> str:
        try:
            from groq import Groq
        except ImportError:
            raise RuntimeError("The 'groq' package is not installed.")

        client = Groq(api_key=Config.GROQ_API_KEY)

        system_prompt = self._build_system_prompt(language)
        system_with_rag = (
            f"{system_prompt}\n\n"
            f"=== VERIFIED CYBERSECURITY RAG CONTEXT ===\n"
            f"{rag_context}\n"
            f"===========================================\n"
        )

        messages = [{"role": "system", "content": system_with_rag}]
        for item in chat_history[-6:]:
            messages.append({"role": item.get("role", "user"), "content": item.get("content", "")})
        messages.append({"role": "user", "content": message})

        response = client.chat.completions.create(
            messages=messages,
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            max_tokens=850,
        )

        return response.choices[0].message.content or ""

    def _classify_topic(self, text: str) -> str:
        """Classifies user queries into specific domain topics across languages."""
        lower = text.lower()

        # 1. Coding & scripts first
        if any(w in lower for w in ["python", "code", "script", "நிரல்", "skript", "プログラム", "コード", "hash", "regex", "algorithm"]):
            return "coding"
            
        # 2. Digital arrest
        if any(w in lower for w in ["digital arrest", "police call", "cbi", "narcotics", "skype arrest", "arrest warrant", "customs drugs", "டிஜிட்டல் அரெஸ்ட்", "கைது", "polizei", "verhaftung", "警察", "逮捕"]):
            return "digital_arrest"

        # 3. Voice clone & deepfake
        if any(w in lower for w in ["voice clone", "cloned voice", "ai voice", "deepfake voice", "synthetic voice", "kidnap call", "குரல்", "stimme geklont", "stimmklon", "音声クローン", "ディープフェイク"]):
            return "voice_clone"

        # 4. Bank OTP, KYC & financial fraud
        if any(w in lower for w in ["otp", "kyc", "bank blocked", "electricity bill", "debit card", "credit card", "pin", "cvv", "bank fraud", "வங்கி", "bankbetrug", "口座", "暗証番号"]):
            return "bank_otp"

        # 5. Passwords & 2FA security
        if any(w in lower for w in ["password", "password manager", "2fa", "mfa", "two factor", "authenticator", "strong password", "பாஸ்வேர்ட்", "கடவுச்சொல்", "passwort", "パスワード", "2段階認証"]):
            return "passwords_2fa"

        # 6. Telegram task / part time scam
        if any(w in lower for w in ["telegram", "part time", "youtube like", "hotel rating", "task scam", "crypto invest", "double money", "பகுதி நேர வேலை", "nebenjob"]):
            return "telegram_job"

        # 7. Sextortion / morphing blackmail
        if any(w in lower for w in ["nude", "sextortion", "morph", "blackmail", "intimate video", "loan app harassment", "மிரட்டல்", "erpress", "leak video", "threaten video", "恐喝", "脅迫"]):
            return "sextortion"

        # 8. SIM swap fraud
        if any(w in lower for w in ["sim swap", "sim block", "esim", "no network", "no service", "lost signal", "duplicate sim", "sim card", "சிம்", "圏外", "sim-karte"]):
            return "sim_swap"

        # 9. Phishing, courier, customs & fraudulent parcel links
        if any(w in lower for w in ["phishing", "fake link", "smishing", "lottery", "customs", "courier", "fedex", "dhl", "speed post", "parcel", "contraband", "mdma", "delivery link", "package hold", "இணைப்பு", "பார்சல்", "betrugslink", "フィッシング", "荷物"]):
            return "phishing"

        # 10. Malware & APK installs
        if any(w in lower for w in ["apk", "anydesk", "teamviewer", "quicksupport", "remote access", "install app", "malware", "virus", "spyware", "செயலி", "schadsoftware"]):
            return "malware_apk"

        # 11. Hacked account recovery
        if any(w in lower for w in ["hacked", "hack instagram", "recover instagram", "whatsapp hacked", "gmail hacked", "compromised account", "ஹேக்", "gehackt", "乗っ取り"]):
            return "hacked_account"

        # 12. VPN & Wi-Fi safety
        if any(w in lower for w in ["vpn", "public wifi", "wifi security", "https", "secure browsing", "tor"]):
            return "vpn_wifi"

        # 13. AI detection technology
        if any(w in lower for w in ["how ai detects", "detection technology", "spectrogram", "mfcc", "how does ai work", "machine learning"]):
            return "ai_tech_detection"

        # 14. 1930 Helpline & portal
        if any(w in lower for w in ["1930", "helpline", "report cybercrime", "file fir", "cybercrime.gov.in", "golden hour", "புகார்"]):
            return "reporting_1930"

        # 15. Greetings & help
        if any(w in lower for w in ["hi", "hello", "hey", "who are you", "what can you do", "help", "வணக்கம்", "hallo", "guten tag", "こんにちは"]):
            return "greeting"
        
        return "general"

    def _respond_with_local_engine(self, message: str, rag_results: List[Any], language: str = "English") -> str:
        """High-quality local multilingual fallback responses when running offline without external API keys."""
        topic = self._classify_topic(message)

        # 1. GREETINGS & CAPABILITIES
        if topic == "greeting":
            if language == "Tamil":
                return """👋 **வணக்கம்! நான் Cyber Shield AI (சைபர் ஷீல்ட் பாட்)**

நான் உங்களுக்கு பின்வரும் சேவைகளை வழங்குகிறேன்:
1. 🛡️ **சைபர் மோசடி பாதுகாப்பு**: டிஜிட்டல் அரெஸ்ட், AI குரல் குளோனிங், வங்கி OTP மோசடிகளை கண்டறிதல்.
2. 🚨 **அவசர உதவி**: பண இழப்பை தடுக்க 1930 உதவி எண் மற்றும் புகார் அளிக்கும் வழிமுறைகள்.
3. 🔐 **தொழில்நுட்ப ஆலோசனைகள்**: பாஸ்வேர்டு பாதுகாப்பு, 2FA, VPN மற்றும் ஹேக் செய்யப்பட்ட கணக்குகளை மீட்டெடுப்பது.
4. 🎙️ **குரல் உரையாடல்**: நீங்கள் மைக்ரோஃபோன் மூலம் பேசி என்னிடம் சந்தேகங்களை கேட்கலாம்!

உங்கள் கேள்வியை தட்டச்சு செய்யவும் அல்லது மைக் மூலம் பேசவும்!"""
            elif language == "German":
                return """👋 **Hallo! Ich bin Cyber Shield AI (Cyberbot)**

Ich bin Ihr intelligenter Sicherheits- und KI-Assistent für folgende Themen:
1. 🛡️ **Cyberkriminalitäts-Abwehr**: Erkennung von Phishing, Fake-Polizeianrufen, KI-Stimmenklonen und OTP-Betrug.
2. 🚨 **Notfall-Leitfaden**: Sofortmaßnahmen bei Datenverlust oder Finanzbetrug (1930 / Bankensperrung).
3. 🔐 **IT-Sicherheit**: Passwort-Manager, 2-Faktor-Authentifizierung (2FA), VPN und Kontowiederherstellung.
4. 🎙️ **Sprachsteuerung**: Sprechen Sie einfach über Ihr Mikrofon mit mir!

Wie kann ich Ihnen heute behilflich sein?"""
            elif language == "Japanese":
                return """👋 **こんにちは！Cyber Shield AI (サイバーボット) です**

私は最新のサイバーセキュリティおよび総合AIアシスタントとして以下をサポートします：
1. 🛡️ **サイバー詐欺・脅威対策**: フィッシング詐欺、警察なりすまし、AI音声偽造、ワンタイムパスワード詐取の防御。
2. 🚨 **緊急対処手順**: 不正送金発生時の口座凍結手順、サイバー犯罪通報（1930番窓口等）。
3. 🔐 **セキュリティ技術**: 強固なパスワード管理、2要素認証（2FA）、VPN、乗っ取りアカウント復旧。
4. 🎙️ **音声対話機能**: マイクを使って音声で質問することも可能です。

何か気になることやご質問はございますか？"""
            else:
                return """👋 **Hello! I am Cyber Shield AI (Cyberbot Assistant)**

I am your comprehensive AI assistant for cybersecurity, technical problem-solving, and general inquiries:
1. 🛡️ **Cyber Fraud Defense**: Step-by-step resolution for Digital Arrest, AI Voice Clones, Bank OTP scams, and Phishing.
2. 🚨 **Emergency Protocol**: Immediate action checklists for reporting fraud to 1930 and freezing compromised accounts.
3. 🔐 **Technical Guidance**: Password security, 2FA/MFA, VPNs, device malware removal, and code verification.
4. 🎙️ **Full Voice Control**: Tap the microphone to talk with me naturally!

How can I help you today?"""

        # 2. Check dedicated cybercrime scenario playbooks from knowledge base
        scenario_reply = get_scenario_response(topic, language)
        if scenario_reply:
            return scenario_reply

        # 5. CODING & TECHNICAL QUERIES
        if topic == "coding":
            if language == "Tamil":
                return """💻 **சைபர் பாதுகாப்பு பைதான் ஸ்கிரிப்ட் (Python Code Example)**

வலுவான பாஸ்வேர்டுகளை சோதிப்பதற்கான மாதிரி பைதான் நிரல்:

```python
import re

def check_password_strength(password: str) -> dict:
    has_length = len(password) >= 12
    has_upper = bool(re.search(r'[A-Z]', password))
    has_lower = bool(re.search(r'[a-z]', password))
    has_digit = bool(re.search(r'[0-9]', password))
    has_special = bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))
    
    score = sum([has_length, has_upper, has_lower, has_digit, has_special])
    return {
        "score": f"{score}/5",
        "is_secure": score >= 4,
        "recommendation": "வலுவான பாஸ்வேர்டு!" if score >= 4 else "குறைந்தது 12 எழுத்துகள், எண்கள், குறியீடுகள் சேர்க்கவும்."
    }

# சோதனை:
print(check_password_strength("MySuperSecurePass2026!"))
```

வேறு ஏதேனும் குறியீட்டு கேள்விகள் உள்ளதா?"""
            elif language == "German":
                return """💻 **Sicherheitscode-Beispiel (Python Script)**

Hier ist ein praktisches Skript zur Überprüfung der Passwortstärke:

```python
import re

def check_password_strength(password: str) -> dict:
    has_length = len(password) >= 12
    has_upper = bool(re.search(r'[A-Z]', password))
    has_lower = bool(re.search(r'[a-z]', password))
    has_digit = bool(re.search(r'[0-9]', password))
    has_special = bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))
    
    score = sum([has_length, has_upper, has_lower, has_digit, has_special])
    return {
        "score": f"{score}/5",
        "is_secure": score >= 4,
        "verdict": "Sicher" if score >= 4 else "Zu schwach"
    }

print(check_password_strength("CyberShield#2026Secure!"))
```

Haben Sie weitere Fragen zu Python, Algorithmen oder Skripten?"""
            elif language == "Japanese":
                return r"""💻 **サイバーセキュリティ用 Python スクリプト例**

強力なパスワード強度チェッカーの実装コードです：

```python
import re

def evaluate_password(pwd: str) -> dict:
    criteria = {
        "length_12_plus": len(pwd) >= 12,
        "uppercase": bool(re.search(r'[A-Z]', pwd)),
        "lowercase": bool(re.search(r'[a-z]', pwd)),
        "digit": bool(re.search(r'\d', pwd)),
        "symbol": bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', pwd))
    }
    score = sum(criteria.values())
    return {
        "score": f"{score}/5",
        "secure": score >= 4,
        "advice": "安全です" if score >= 4 else "12文字以上、記号と大文字・数字を含めてください"
    }

print(evaluate_password("CyberShield#2026Secure!"))
```

その他、プログラミングやセキュリティ関連コードのご質問もどうぞ！"""
            else:
                return r"""💻 **Python Security Tool: Password Strength Validator**

Here is a ready-to-run Python script that evaluates entropy and enforces security standards:

```python
import re

def validate_password_strength(password: str) -> dict:
    rules = {
        "min_length_12": len(password) >= 12,
        "has_uppercase": bool(re.search(r'[A-Z]', password)),
        "has_lowercase": bool(re.search(r'[a-z]', password)),
        "has_digits": bool(re.search(r'\d', password)),
        "has_special_chars": bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password)),
    }
    score = sum(rules.values())
    status = "Strong & Secure" if score >= 4 else "Weak - Vulnerable to Brute Force"
    
    return {
        "score": f"{score}/5",
        "status": status,
        "passed_rules": rules
    }

# Example usage:
print(validate_password_strength("CyberShield#2026Secure!"))
```

Feel free to ask for any other scripts, algorithms, or API implementations!"""

        # 6. PASSWORDS & 2FA / GENERAL SECURITY
        if topic == "passwords_2fa":
            if language == "Tamil":
                return """🔐 **வலுவான கடவுச்சொல் மற்றும் 2FA பாதுகாப்பு வழிகாட்டி**

1. **பாஸ்வேர்டு மேனேஜர் பயன்படுத்துங்கள்:** Bitwarden அல்லது 1Password போன்ற நம்பகமான செயலிகளை பயன்படுத்துங்கள்.
2. **2-Step Verification (2FA):** SMS OTP-க்கு பதிலாக Google Authenticator அல்லது Aegis போன்ற செயலிகளை பயன்படுத்துங்கள் (ஏனெனில் SMS-ஐ சிம் ஸ்வாப் மூலம் திருட முடியும்).
3. **நீளமான கடவுச்சொற்கள்:** குறைந்தபட்சம் 14 எழுத்துகள் கொண்ட பாஸ்ஃப்ரேஸ் (Passphrase) அமைக்கவும் (எ.கா: `Blue#SkyWalk$River99`)."""
            elif language == "German":
                return """🔐 **Passwortsicherheit & 2-Faktor-Authentifizierung (2FA)**

1. **Passwort-Manager einsetzen:** Nutzen Sie Lösungen wie Bitwarden oder 1Password für einzigartige Passwörter pro Dienst.
2. **App-basierte 2FA bevorzugen:** Nutzen Sie Authenticator-Apps (z. B. Google Authenticator, Aegis) anstelle von SMS-Codes zum Schutz vor SIM-Swapping.
3. **Passphrase-Methode:** Nutzen Sie min. 14 Zeichen lange Sätze anstelle einfacher Wörter."""
            elif language == "Japanese":
                return """🔐 **パスワードセキュリティと2要素認証（2FA）のベストプラクティス**

1. **パスワードマネージャーの活用:** Bitwardenや1Passwordなどを利用し、サービスごとに異なる強固なパスワードを生成・管理してください。
2. **認証アプリによる2段階認証:** SMS認証よりも、SIMスワップ被害を防げるアプリ認証（Google Authenticator等）を推奨します。
3. **パスフレーズの利用:** 単語の組み合わせによる14文字以上の長いフレーズを設定しましょう。"""
            else:
                return """🔐 **Password Security & Multi-Factor Authentication (MFA) Guide**

1. **Use a Dedicated Password Manager:** Adopt tools like Bitwarden or 1Password. Never reuse passwords across sites.
2. **Upgrade to App-Based 2FA:** Prefer Time-based One-Time Passwords (TOTP via Google Authenticator or Aegis) over SMS, which is vulnerable to SIM-swapping.
3. **Passphrase Strategy:** 4 random words joined with numbers/symbols (e.g., `Coffee#Tiger$Window77`) yield massive entropy that defies brute-force attacks."""

        # 7. GENERAL / RAG FALLBACK
        doc = rag_results[0][0] if rag_results and len(rag_results) > 0 else None
        title = doc.get("title", "Cyber Safety & Problem Solving Advisory") if doc else "Cyber Security & Technical Advisory"
        actions = doc.get("immediate_actions", []) if doc else [
            "Verify caller or sender identity through official channels",
            "Never disclose OTP, PIN, password, or financial credentials",
            "Report fraudulent numbers or links immediately to Helpline 1930",
        ]

        if language == "Tamil":
            action_lines = "\n".join([f"• {act}" for act in actions])
            return f"""🛡️ **சைபர் ஷீல்ட் AI வழிகாட்டுதல் (Cyberbot Tamil)**

**அறிவிப்பு தலைப்பு:** {title}

**உடனடி பாதுகாப்பு நடவடிக்கைகள்:**
{action_lines}

💡 **முக்கிய அறிவுரை:**
1. உங்கள் வினவலை ஆய்வு செய்ததில், அனைத்து விதிகளையும் பின்பற்றுவது பாதுகாப்பானது.
2. வங்கி மற்றும் காவல் துறை OTP-யை கேட்காது.
3. தேசிய சைபர் உதவி எண் **1930** அல்லது **cybercrime.gov.in** இணையதளத்தில் புகார் அளியுங்கள்."""
        elif language == "German":
            action_lines = "\n".join([f"• {act}" for act in actions])
            return f"""🛡️ **Cyber Shield AI Leitfaden (Cyberbot Deutsch)**

**Thema:** {title}

**Sofortmaßnahmen:**
{action_lines}

💡 **Wichtige Sicherheitshinweise:**
1. Geben Sie niemals Passwörter oder TANs über ungesicherte Links weiter.
2. Notfall-Meldung: Wenden Sie sich bei Betrug sofort an die Bank und Notruf 1930."""
        elif language == "Japanese":
            action_lines = "\n".join([f"• {act}" for act in actions])
            return f"""🛡️ **サイバーシールド AI ガイド (Cyberbot 日本語)**

**件名:** {title}

**推奨される手順:**
{action_lines}

💡 **重要セキュリティ情報:**
1. 銀行や公的機関が電話やSMSで暗証番号を尋ねることは絶対にありません。
2. 不審な場合は直ちにサイバー犯罪相談窓口（1930）へご相談ください。"""
        else:
            action_lines = "\n".join([f"• {act}" for act in actions])
            return f"""🛡️ **Cyber Shield AI Problem Solver & Advisory**

**Topic:** {title}

**Recommended Action Steps:**
{action_lines}

💡 **Core Principles:**
1. **Zero Trust:** Verify every unknown request via verified official directory numbers.
2. **Incident Escalation:** For financial fraud, contact your bank and dial National Cyber Crime Helpline **1930** immediately.

Feel free to ask follow-up questions, request scripts, or talk via voice!"""
