import asyncio
import reflex as rx
from typing import Dict, Any, List
from src.agents.speech_agent import SpeechAnalysisAgent
from src.agents.text_agent import TextScamDetectorAgent
from src.database.db_manager import DatabaseManager

# Initialize backend agents
db_mgr = DatabaseManager()
speech_agent = SpeechAnalysisAgent(db_manager=db_mgr)
text_agent = TextScamDetectorAgent(db_manager=db_mgr)


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

    # Floating AI Bot Popup State
    bot_open: bool = False
    bot_input: str = ""
    bot_messages: List[Dict[str, str]] = [
        {
            "sender": "bot",
            "text": "Hello! I am Cyber Fraud Shield AI. Ask me about voice clone detection, suspicious calls, or reporting fraud."
        }
    ]

    def toggle_bot(self):
        self.bot_open = not self.bot_open

    def set_bot_input(self, val: str):
        self.bot_input = val

    def send_bot_message(self):
        msg = self.bot_input.strip()
        if not msg:
            return
        
        self.bot_messages.append({"sender": "user", "text": msg})
        self.bot_input = ""
        
        # Query backend text agent
        res = text_agent.analyze(msg)
        scam_type = res.get("scam_type", "Standard Query")
        threat = res.get("threat_level", "Info")
        advice = res.get("actionable_advice", "Always verify unexpected callers before providing sensitive info.")
        
        reply = f"🤖 AI Shield Analysis:\nThreat: {scam_type} ({threat})\nRecommendation: {advice}"
        self.bot_messages.append({"sender": "bot", "text": reply})

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
            