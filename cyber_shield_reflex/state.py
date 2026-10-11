import asyncio
import reflex as rx
from typing import Dict, Any, List
from src.agents.speech_agent import SpeechAnalysisAgent
from src.agents.text_agent import TextScamDetectorAgent
from src.agents.bot_agent import CyberShieldBotAgent
from src.database.db_manager import DatabaseManager

# Initialize backend agents
db_mgr = DatabaseManager()
speech_agent = SpeechAnalysisAgent(db_manager=db_mgr)
text_agent = TextScamDetectorAgent(db_manager=db_mgr)
cyber_bot = CyberShieldBotAgent(db_manager=db_mgr)


class State(rx.State):  # type: ignore  # Suppress Pyright rx.State router descriptor type error
    """
    Reflex Reactive Application State.
    Encapsulates all reactive UI variables and handles direct backend invocations
    for voice spoofing scanning, text fraud detection, and sample analysis.
    """
    # Active tab state
    active_tab: str = "speech"
    
    # Processing states
    is_analyzing: bool = False
    analysis_done: bool = False
    uploaded_filename: str = ""
    text_input: str = ""
    
    # Verdict output variables
    verdict: str = "GENUINE"  # "GENUINE", "SPOOFED", "UNCERTAIN"
    synthetic_confidence: int = 12
    voice_nature: str = "✅ Natural Human Voice Signature"
    pitch_stability: str = "Natural Pitch Micro-variations"
    transcription: str = "No audio uploaded yet. Click 'Analyze a Call' or upload a voice file below."
    transcription_engine: str = "Groq Whisper Large v3"
    spoof_engine: str = "Hugging Face (Mitran14/speach-agent)"
    overall_voice_risk_score: int = 15
    threat_level: str = "Safe"
    scam_type: str = "Legitimate / Clean"
    matched_tactics: List[str] = ["Standard acoustic check completed"]
    warning_signs: List[str] = ["No obvious threat patterns detected."]
    actionable_advice: str = "Always verify unknown callers through official bank channels."
    artifacts_detected: List[str] = ["Natural background noise", "Human breath pauses"]
    engine_used: str = "Hugging Face (Mitran14/speach-agent)"
    idempotent_hit: bool = False

    # Complaint Prerequisites & Disclaimer Dialog State
    complaint_modal_open: bool = False
    disclaimer_modal_open: bool = False

    def toggle_complaint_modal(self):
        self.complaint_modal_open = not self.complaint_modal_open

    def proceed_to_complaint(self):
        self.complaint_modal_open = False
        return rx.redirect("/scan")

    def toggle_disclaimer_modal(self):
        self.disclaimer_modal_open = not self.disclaimer_modal_open

    # Multilingual AI Bot State (Voice In, Voice Out, Problem Solver)
    bot_open: bool = False
    bot_input: str = ""
    bot_language: str = "English"  # "English", "Tamil", "German", "Japanese"
    bot_language_display: str = "🇬🇧 English"
    selected_complaint_topic: str = ""
    auto_read_aloud: bool = False
    speak_text: str = ""
    speech_rate: float = 1.0
    bot_messages: List[Dict[str, str]] = [
        {
            "sender": "bot",
            "text": "Hello! I am Cyberbot AI. I can solve cyber problems, answer security questions, and converse with you using voice in English, Tamil, German, or Japanese."
        }
    ]

    def toggle_bot(self):
        self.bot_open = not self.bot_open

    def toggle_auto_read(self):
        self.auto_read_aloud = not self.auto_read_aloud

    def clear_bot_chat(self):
        welcomes = {
            "Tamil": "வணக்கம்! உரையாடல் அழிக்கப்பட்டது. புதிய கேள்வியை கேளுங்கள்.",
            "German": "Hallo! Der Chat wurde zurückgesetzt. Wie kann ich Ihnen helfen?",
            "Japanese": "こんにちは！チャットがリセットされました。ご質問をどうぞ。",
            "English": "Chat cleared. Ask me any cyber question or query!",
        }
        self.bot_messages = [{"sender": "bot", "text": welcomes.get(self.bot_language, welcomes["English"])}]

    def set_bot_input(self, val: str):
        self.bot_input = val

    def set_bot_language(self, lang: str):
        self.bot_language = lang
        lang_display_map = {
            "Tamil": "🇮🇳 தமிழ் (Tamil)",
            "German": "🇩🇪 Deutsch (German)",
            "Japanese": "🇯🇵 日本語 (Japanese)",
            "English": "🇬🇧 English",
        }
        self.bot_language_display = lang_display_map.get(lang, "🇬🇧 English")
        lang_welcomes = {
            "Tamil": "வணக்கம்! மொழி தமிழில் அமைக்கப்பட்டுள்ளது. உங்கள் கேள்வியை தட்டச்சு செய்யவும் அல்லது மைக்ரோஃபோன் மூலம் பேசவும்.",
            "German": "Hallo! Die Sprache wurde auf Deutsch umgestellt. Wie kann ich Ihnen heute helfen?",
            "Japanese": "こんにちは！言語が日本語に設定されました。セキュリティのご質問やご相談をどうぞ。",
            "English": "Language set to English. Ask me any cybersecurity query or use the microphone to talk!",
        }
        greeting = lang_welcomes.get(lang, f"Language switched to {lang}.")
        self.bot_messages.append({"sender": "bot", "text": greeting})
        self.speak_text = greeting
        if self.auto_read_aloud:
            return self.speak_bot_text(greeting)

    def change_language_select(self, val: str):
        """Dropdown handler for switching language."""
        self.bot_language_display = val
        if "Tamil" in val or "தமிழ்" in val:
            lang = "Tamil"
        elif "German" in val or "Deutsch" in val:
            lang = "German"
        elif "Japanese" in val or "日本語" in val:
            lang = "Japanese"
        else:
            lang = "English"
        
        self.set_bot_language(lang)
        return rx.call_script(f"window.currentBotLang = '{lang}';")

    def handle_complaint_select(self, val: str):
        """Dropdown handler for instant complaints / threat scenarios."""
        if not val or not val.strip() or val.startswith("⚡"):
            return
        
        prompt_map = {
            "🚨 1930 Helpline - Report Fraud": "How do I report fraud to national helpline 1930 within the golden hour?",
            "🛑 Digital Arrest - Fake Police": "What should I do if someone calls threatening a digital arrest from police or CBI?",
            "🎙️ Voice Clone - Deepfake Call": "How do I protect against and handle an AI voice cloning scam call?",
            "💳 Bank OTP & KYC Scam": "I accidentally shared my bank OTP with an unknown caller! How do I block my account?",
            "💼 Telegram Task Scheme": "I was scammed by a work from home Telegram like-video prepaid task scheme!",
            "🔞 Sextortion - Video Blackmail": "Someone recorded an explicit video call and is blackmailing to leak it to my contacts!",
            "📱 SIM Swap - Lost Signal": "My phone suddenly lost network signal and shows no service! How do I stop a SIM swap?",
            "📦 FedEx Customs Parcel Hold": "I got a call claiming customs seized a FedEx courier with contraband in my name!",
            "📲 Malicious APK & AnyDesk": "I was tricked into installing an APK and AnyDesk on my phone! How do I secure it?",
            "🔓 Hacked Account Recovery": "How do I recover my hacked Instagram and WhatsApp accounts?",
            "🔐 Strong Password & 2FA": "How to create an uncrackable password and secure my accounts with 2FA?",
            "💻 Python Security Script": "Write a python script to check password strength and entropy",
        }
        query = prompt_map.get(val, val)
        self.selected_complaint_topic = ""
        return self._process_bot_message(query)

    def _process_bot_message(self, msg: str):
        cleaned = msg.strip() if msg else ""
        if not cleaned:
            return
        
        self.bot_messages.append({"sender": "user", "text": cleaned})
        self.bot_input = ""
        
        # Format conversation history
        history = []
        for m in self.bot_messages[-6:]:
            role = "user" if m.get("sender") == "user" else "assistant"
            history.append({"role": role, "content": m.get("text", "")})
        
        # Invoke enhanced multilingual CyberShieldBotAgent
        reply = cyber_bot.respond(cleaned, chat_history=history, language=self.bot_language)
        self.bot_messages.append({"sender": "bot", "text": reply})
        self.speak_text = reply

        if self.auto_read_aloud:
            return self.speak_bot_text(reply)

    def handle_chat_submit(self, form_data: dict):
        """Single-enter and single-click native form submission handler."""
        msg = form_data.get("message", "")
        if not msg:
            msg = self.bot_input
        return self._process_bot_message(msg)

    def send_bot_message(self):
        """Button or script triggered submission."""
        return self._process_bot_message(self.bot_input)

    def submit_voice_message(self, spoken_text: str):
        """Receives spoken transcript from browser Web Speech API and processes it."""
        if spoken_text and spoken_text.strip():
            return self._process_bot_message(spoken_text.strip())

    def send_quick_prompt(self, prompt: str):
        return self._process_bot_message(prompt)

    def speak_bot_text(self, text: str):
        import json
        clean_text = text.replace("*", "").replace("#", "").replace("`", "").replace(">", "").replace("\n", " ")
        return rx.call_script(f"window.cyberBotTTS.speak({json.dumps(clean_text)}, '{self.bot_language}');")

    def stop_bot_speech(self):
        return rx.call_script("window.cyberBotTTS.stopSpeaking();")

    def set_active_tab(self, tab: str):
        self.active_tab = tab

    def set_text_input(self, val: str):
        self.text_input = val

    async def handle_upload(self, files: List[rx.UploadFile]):
        """
        Reflex Event Handler for audio file uploads.
        Reads raw audio bytes and passes directly to speech_agent.analyze_audio.
        """
        if not files:
            return
        
        self.is_analyzing = True
        yield
        
        upload_file = files[0]
        fname = upload_file.filename or "uploaded_audio.wav"
        self.uploaded_filename = fname
        upload_bytes = await upload_file.read()
        
        # Invoke backend speech agent
        result = speech_agent.analyze_audio(upload_bytes, filename=fname)
        self._apply_analysis_result(result)
        
        self.is_analyzing = False
        self.analysis_done = True

    def run_sample_scan(self, sample_type: str):
        """
        Instantly runs analysis on pre-configured test scenarios for instant demonstration.
        """
        self.is_analyzing = True
        
        if sample_type == "cloned_voice":
            # Synthetic / cloned voice sample simulation
            audio_bytes = b"CLONED_VOICE_DEMO_SAMPLE_BYTES_" * 50
            filename = "cloned_voice_demo.wav"
        elif sample_type == "bank_scam":
            # Bank fraud scam sample
            audio_bytes = b"EMERGENCY_BANK_OTP_SCAM_SAMPLE_" * 40
            filename = "bank_scam_urgent.mp3"
        else:
            # Natural human voice sample
            audio_bytes = b"NATURAL_HUMAN_VOICE_SAMPLE_AUDIO" * 45
            filename = "natural_call.wav"

        result = speech_agent.analyze_audio(audio_bytes, filename=filename)
        self.uploaded_filename = filename
        self._apply_analysis_result(result)
        
        self.is_analyzing = False
        self.analysis_done = True

    def run_text_scan(self):
        """
        Runs text-based scam scanning using text_agent.
        """
        if not self.text_input.strip():
            return
            
        self.is_analyzing = True
        
        content_res = text_agent.analyze(self.text_input)
        
        self.overall_voice_risk_score = content_res.get("risk_score", 0)
        self.threat_level = content_res.get("threat_level", "Caution")
        self.scam_type = content_res.get("scam_type", "Suspicious Communication")
        self.matched_tactics = content_res.get("matched_tactics", [])
        self.warning_signs = content_res.get("key_warning_signs", [])
        self.actionable_advice = content_res.get("actionable_advice", "")
        self.engine_used = content_res.get("engine_used", "Text Scam Agent")
        
        risk = self.overall_voice_risk_score
        if risk > 60:
            self.verdict = "SPOOFED"
        elif risk > 35:
            self.verdict = "UNCERTAIN"
        else:
            self.verdict = "GENUINE"
            
        self.is_analyzing = False
        self.analysis_done = True

    def analyze_text_scam(self):
        """Alias for run_text_scan."""
        return self.run_text_scan()

    def run_suspect_text_sample(self, sample: str):
        """Runs text_agent analysis on pre-configured suspect text sample."""
        if sample == "bank_otp":
            self.text_input = "URGENT: Your HDFC bank account is blocked due to unverified KYC. Click http://hdfc-verify-login.net immediately or share OTP 849201 to avoid closure."
        elif sample == "delivery":
            self.text_input = "FedEx Alert: Package #IN-84920 is held at customs due to unpaid fee of Rs. 499. Pay immediately at http://fedex-customs-clear.com to release shipment."
        elif sample == "tech_support":
            self.text_input = "Microsoft Security Warning: Trojan.WIN32 detected on your computer! Call official support at +1-800-555-0199 or download AnyDesk for emergency cleanup."
        else:
            self.text_input = sample
        self.run_text_scan()

    def reset_results(self):
        self.analysis_done = False
        self.uploaded_filename = ""
        self.text_input = ""

    def _apply_analysis_result(self, result: Dict[str, Any]):
        """Applies speech_agent analysis result dictionary to state attributes."""
        self.transcription = result.get("transcription", "")
        self.transcription_engine = result.get("transcription_engine", "")
        self.overall_voice_risk_score = result.get("overall_voice_risk_score", 0)
        self.threat_level = result.get("overall_threat_level", "Caution")
        self.spoof_engine = result.get("voice_spoof_engine", "")
        self.idempotent_hit = result.get("idempotent_hit", False)
        
        voice_metrics = result.get("voice_spoof_metrics", {})
        is_synthetic = voice_metrics.get("is_synthetic", False)
        self.synthetic_confidence = voice_metrics.get("synthetic_confidence", 0)
        self.voice_nature = voice_metrics.get("voice_nature", "")
        self.pitch_stability = voice_metrics.get("pitch_stability", "")
        self.artifacts_detected = voice_metrics.get("artifacts_detected", [])
        
        content_res = result.get("content_analysis", {})
        self.scam_type = content_res.get("scam_type", "None")
        self.matched_tactics = content_res.get("matched_tactics", [])
        self.warning_signs = content_res.get("key_warning_signs", [])
        self.actionable_advice = content_res.get("actionable_advice", "")
        self.engine_used = result.get("voice_spoof_engine", "Hugging Face Engine")
        
        if is_synthetic or self.synthetic_confidence > 60:
            self.verdict = "SPOOFED"
        elif self.synthetic_confidence > 35 or self.overall_voice_risk_score > 50:
            self.verdict = "UNCERTAIN"
        else:
            self.verdict = "GENUINE"
            