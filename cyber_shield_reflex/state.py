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


# Module-level audio cache to store raw bytes in memory without frontend serialization
_uploaded_audio_cache: Dict[str, bytes] = {}


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
    voice_analysis_done: bool = False  # Dedicated for Voice & Audio Scan
    text_analysis_done: bool = False   # Dedicated for SMS & WhatsApp Scan
    analysis_done: bool = False        # General compatibility flag
    uploaded_filename: str = ""
    uploaded_file_size: str = ""
    is_file_ready: bool = False
    show_upload_toast: bool = False
    upload_toast_message: str = ""
    text_input: str = ""
    
    # Verdict output variables (Voice & Audio Scan)
    verdict: str = "GENUINE"  # "GENUINE", "SPOOFED", "UNCERTAIN"
    synthetic_confidence: int = 12
    voice_nature: str = "✅ Natural Human Voice Signature"
    pitch_stability: str = "Natural Pitch Micro-variations"
    transcription: str = "No audio uploaded yet. Click 'Analyze a Call' or upload a voice file below."
    transcription_engine: str = "Groq Whisper Large v3"
    spoof_engine: str = "Hugging Face (Mitran14/speach-agent)"
    overall_voice_risk_score: int = 0
    threat_level: str = "Safe"
    scam_type: str = "Legitimate / Non-Threat Call"
    
    # Cross-Attention Transformer & LwF Methodology Variables (Voice)
    analysis_method: str = "Cross-Attention Transformer & LwF"
    threat_verdict: str = "SAFE / NON-THREAT"
    threat_probability: int = 0
    cross_attention_alignment: float = 85.0
    urgency_score: int = 25
    detected_triggers: List[str] = []
    
    matched_tactics: List[str] = ["Standard acoustic check completed"]
    warning_signs: List[str] = ["No obvious threat patterns detected."]
    actionable_advice: str = "Always verify unknown callers through official bank channels."
    artifacts_detected: List[str] = ["Natural background noise", "Human breath pauses"]
    engine_used: str = "Cross-Attention Transformer & LwF"
    idempotent_hit: bool = False

    # SMS & WhatsApp Message Phishing State (Completely Separate from Voice)
    text_verdict: str = "GENUINE"  # "GENUINE", "SPOOFED", "UNCERTAIN"
    text_scanned_content: str = ""
    text_risk_score: int = 0
    text_threat_probability: int = 0
    text_threat_level: str = "Safe"
    text_scam_type: str = "Legitimate Message"
    text_actionable_advice: str = "No malicious links or coercive phishing indicators detected."
    text_matched_tactics: List[str] = []
    text_warning_signs: List[str] = []
    text_engine_used: str = "NLP Scam Classifier"


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
        
        self.bot_messages = [*self.bot_messages, {"sender": "user", "text": cleaned}]
        self.bot_input = ""
        
        # Format conversation history
        history = []
        for m in self.bot_messages[-6:]:
            role = "user" if m.get("sender") == "user" else "assistant"
            history.append({"role": role, "content": m.get("text", "")})
        
        # Invoke enhanced multilingual CyberShieldBotAgent
        reply = cyber_bot.respond(cleaned, chat_history=history, language=self.bot_language)
        self.bot_messages = [*self.bot_messages, {"sender": "bot", "text": reply}]
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

    async def handle_file_upload(self, files: List[rx.UploadFile]):
        """
        Triggered immediately when an audio file is selected from the device dialog or dropped.
        Reads file bytes into local cache, calculates size, sets visual ready state,
        and displays a pop-up confirmation message for 2.5 to 3 seconds.
        """
        if not files:
            return
        
        upload_file = files[0]
        fname = upload_file.filename or "uploaded_audio.wav"
        self.uploaded_filename = fname
        upload_bytes = await upload_file.read()
        _uploaded_audio_cache[fname] = upload_bytes
        
        # Calculate human-friendly file size
        size_bytes = len(upload_bytes)
        if size_bytes >= 1024 * 1024:
            self.uploaded_file_size = f"{size_bytes / (1024 * 1024):.2f} MB"
        else:
            self.uploaded_file_size = f"{max(size_bytes / 1024, 0.1):.1f} KB"
            
        self.is_file_ready = True
        self.voice_analysis_done = False
        self.analysis_done = False
        self.show_upload_toast = True
        self.upload_toast_message = f"Audio '{fname}' ({self.uploaded_file_size}) is ready for AI analysis."
        
        # Trigger native toast notification
        yield rx.toast.success(f"File uploaded successfully! ({fname})", duration=3000)
        
        # Keep floating pop-up visible for 3 seconds then auto-dismiss
        await asyncio.sleep(3)
        self.show_upload_toast = False

    def dismiss_upload_toast(self):
        """Dismisses the floating upload success toast."""
        self.show_upload_toast = False

    def clear_uploaded_file(self):
        """Clears current selected file and completely resets/dismisses the voice analysis report."""
        if self.uploaded_filename in _uploaded_audio_cache:
            del _uploaded_audio_cache[self.uploaded_filename]
        self.uploaded_filename = ""
        self.uploaded_file_size = ""
        self.is_file_ready = False
        self.show_upload_toast = False
        self.voice_analysis_done = False  # Immediately dismisses voice analysis report!
        self.analysis_done = False
        self.transcription = ""
        self.transcription_engine = ""
        self.overall_voice_risk_score = 0
        self.threat_probability = 0
        self.threat_verdict = "SAFE / NON-THREAT"
        self.scam_type = "Legitimate / Non-Threat Call"
        self.actionable_advice = ""
        return rx.clear_selected_files("audio_upload")

    def clear_voice_report(self):
        """Explicitly dismisses the voice threat analysis report and clears uploaded file."""
        return self.clear_uploaded_file()

    def clear_text_scan(self):
        """Clears the text input and completely dismisses the SMS/text analysis report."""
        self.text_input = ""
        self.text_scanned_content = ""
        self.text_analysis_done = False
        self.text_risk_score = 0
        self.text_threat_probability = 0
        self.text_scam_type = "Legitimate Message"
        self.text_actionable_advice = ""
        self.text_matched_tactics = []
        self.text_warning_signs = []

    async def handle_upload(self, files: List[rx.UploadFile] = []):
        """
        Reflex Event Handler triggered when clicking 'Analyze Uploaded File'.
        Processes the previously uploaded audio or newly provided files.
        """
        upload_bytes = None
        fname = self.uploaded_filename
        
        # Check if files were passed via the button directly
        if files:
            upload_file = files[0]
            fname = upload_file.filename or "uploaded_audio.wav"
            self.uploaded_filename = fname
            upload_bytes = await upload_file.read()
            _uploaded_audio_cache[fname] = upload_bytes
            
            size_bytes = len(upload_bytes)
            if size_bytes >= 1024 * 1024:
                self.uploaded_file_size = f"{size_bytes / (1024 * 1024):.2f} MB"
            else:
                self.uploaded_file_size = f"{max(size_bytes / 1024, 0.1):.1f} KB"
            self.is_file_ready = True
        elif fname and fname in _uploaded_audio_cache:
            upload_bytes = _uploaded_audio_cache[fname]

        if not upload_bytes:
            yield rx.toast.warning("Please upload an audio file first before analyzing!", duration=3000)
            return
        
        self.is_analyzing = True
        yield
        
        # Invoke backend speech agent
        result = speech_agent.analyze_audio(upload_bytes, filename=fname)
        self._apply_analysis_result(result)
        
        self.is_analyzing = False
        self.voice_analysis_done = True
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
        self.voice_analysis_done = True
        self.analysis_done = True

    def run_text_scan(self):
        """
        Runs text-based scam scanning using text_agent into dedicated SMS/text state.
        Never overwrites or interferes with voice analysis report!
        """
        if not self.text_input.strip():
            return
            
        self.is_analyzing = True
        
        content_res = text_agent.analyze(self.text_input)
        
        self.text_scanned_content = self.text_input.strip()
        self.text_risk_score = content_res.get("risk_score", 0)
        self.text_threat_probability = self.text_risk_score
        self.text_threat_level = content_res.get("threat_level", "Caution")
        self.text_scam_type = content_res.get("scam_type", "Suspicious Communication")
        self.text_matched_tactics = content_res.get("matched_tactics", [])
        self.text_warning_signs = content_res.get("key_warning_signs", [])
        self.text_actionable_advice = content_res.get("actionable_advice", "")
        self.text_engine_used = content_res.get("engine_used", "Text Scam Agent")
        
        risk = self.text_risk_score
        if risk > 60:
            self.text_verdict = "SPOOFED"  # High Risk Threat
        elif risk > 35:
            self.text_verdict = "UNCERTAIN"  # Caution
        else:
            self.text_verdict = "GENUINE"  # Clean Message
            
        self.is_analyzing = False
        self.text_analysis_done = True

    def analyze_text_scam(self):
        """Alias for run_text_scan."""
        return self.run_text_scan()

    def run_sample_text_scan(self, sample: str):
        """Runs text_agent analysis on pre-configured test sample scenarios."""
        if sample == "bank_otp":
            self.text_input = "URGENT: Your HDFC bank account is blocked due to unverified KYC. Click http://hdfc-verify-login.net immediately or share OTP 849201 to avoid closure."
        elif sample == "delivery":
            self.text_input = "FedEx Alert: Package #IN-84920 is held at customs due to unpaid fee of Rs. 499. Pay immediately at http://fedex-customs-clear.com to release shipment."
        elif sample == "tech_support":
            self.text_input = "Microsoft Security Warning: Trojan.WIN32 detected on your computer! Call official support at +1-800-555-0199 or download AnyDesk for emergency cleanup."
        else:
            self.text_input = sample
        self.run_text_scan()

    def run_suspect_text_sample(self, sample: str):
        return self.run_sample_text_scan(sample)

    def reset_results(self):
        self.voice_analysis_done = False
        self.text_analysis_done = False
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
        
        # Cross-Attention Transformer & LwF continual learning attributes
        self.analysis_method = result.get("model_method", "Cross-Attention Transformer & LwF")
        self.threat_verdict = result.get("threat_verdict", "SAFE / NON-THREAT")
        self.threat_probability = int(result.get("threat_probability", 15))
        self.scam_type = result.get("scam_type", "Legitimate / Non-Threat Call")
        self.cross_attention_alignment = float(result.get("cross_attention_alignment", 85.0))
        self.urgency_score = int(result.get("urgency_score", 50))
        self.detected_triggers = result.get("detected_triggers", [])
        self.actionable_advice = result.get("actionable_advice", "")
        self.engine_used = self.analysis_method
        
        voice_metrics = result.get("voice_spoof_metrics", {})
        is_synthetic = voice_metrics.get("is_synthetic", False)
        self.synthetic_confidence = voice_metrics.get("synthetic_confidence", 0)
        self.voice_nature = voice_metrics.get("voice_nature", "")
        self.pitch_stability = voice_metrics.get("pitch_stability", "")
        self.artifacts_detected = voice_metrics.get("artifacts_detected", [])
        
        content_res = result.get("content_analysis", {})
        self.matched_tactics = content_res.get("matched_tactics", [])
        self.warning_signs = content_res.get("key_warning_signs", [])
        
        if self.threat_verdict == "THREAT DETECTED":
            self.verdict = "SPOOFED"  # High Risk Threat (Red Banner)
        elif self.threat_verdict == "UNCERTAIN" or (self.overall_voice_risk_score > 35 and self.threat_verdict != "SAFE / NON-THREAT"):
            self.verdict = "UNCERTAIN"  # Caution / Moderate Risk (Amber Banner)
        else:
            self.verdict = "GENUINE"  # Safe / Clean Voice (Green Banner)
            
        self.voice_analysis_done = True
        self.analysis_done = True


            