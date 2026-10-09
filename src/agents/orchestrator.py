from typing import Dict, Any
from src.agents.text_agent import TextScamDetectorAgent
from src.agents.speech_agent import SpeechAnalysisAgent
from src.agents.bot_agent import CyberShieldBotAgent
from src.database.db_manager import DatabaseManager
from src.config import Config

class FreeAgentOrchestrator:
    """
    Multi-Agent Orchestrator connecting specialized AI agents:
    - TextScamDetectorAgent (Text & URL Fraud Analysis)
    - SpeechAnalysisAgent (Voice Transcription & Synthetic Spoof Detection)
    - CyberShieldBotAgent (RAG-Powered Conversational Emergency Advisor)
    
    Demonstrates Multi-Agent Collaboration using Free APIs (Groq, HuggingFace, Gemini)
    with 100% end-to-end Data Idempotency.
    """
    def __init__(self, db_manager: DatabaseManager = None):
        if db_manager is None:
            db_manager = DatabaseManager()
        self.db = db_manager
        self.text_agent = TextScamDetectorAgent(db_manager=self.db)
        self.speech_agent = SpeechAnalysisAgent(db_manager=self.db)
        self.bot_agent = CyberShieldBotAgent(db_manager=self.db)

    def get_agent_status(self) -> Dict[str, Any]:
        kb_count = len(self.bot_agent.rag_engine.documents)
        idempotency_stats = self.db.get_idempotency_stats()
        return {
            "mode": Config.active_mode(),
            "rag_documents": kb_count,
            "idempotency_stats": idempotency_stats,
            "agents": [
                {
                    "name": self.text_agent.name,
                    "role": self.text_agent.role,
                    "provider": "Groq Llama-3.3-70B / Heuristic Engine",
                    "free_tier": "100% Free API Available"
                },
                {
                    "name": self.speech_agent.name,
                    "role": self.speech_agent.role,
                    "provider": "Groq Whisper Large v3 / Acoustic Artifact Analyzer",
                    "free_tier": "100% Free API Available"
                },
                {
                    "name": self.bot_agent.name,
                    "role": self.bot_agent.role,
                    "provider": f"Groq Llama-3.3-70B + RAG Vector Engine ({kb_count} Security Playbooks)",
                    "free_tier": "100% Free API Available"
                }
            ]
        }

    def process_full_incident(self, text_input: str = None, audio_bytes: bytes = None, filename: str = "") -> Dict[str, Any]:
        """
        Runs multi-agent investigation across provided text and/or speech inputs idempotently.
        """
        results = {}
        
        if text_input and text_input.strip():
            results["text_investigation"] = self.text_agent.analyze(text_input)
            
        if audio_bytes and len(audio_bytes) > 0:
            results["speech_investigation"] = self.speech_agent.analyze_audio(audio_bytes, filename)

        # Generate aggregated bot advice based on investigation
        summary_prompt = f"Incident investigation findings: {results}. Provide 3 priority emergency safety recommendations."
        results["bot_emergency_guidance"] = self.bot_agent.respond(summary_prompt)
        
        return results
