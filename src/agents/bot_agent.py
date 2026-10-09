import json
from typing import List, Dict, Any
from src.config import Config
from src.agents.rag_engine import CyberKnowledgeRAGEngine

class CyberShieldBotAgent:
    """
    Interactive Cyber Fraud Emergency & Security Advisor AI Bot powered by RAG (Retrieval-Augmented Generation).
    Uses semantic vector search across verified cybercrime playbooks to deliver zero-hallucination,
    actionable security instructions, emergency checklists, and official helpline citations.
    """
    
    def __init__(self, db_manager=None):
        self.name = "Cyber Shield Bot"
        self.role = "Cyber Security & Fraud Emergency Advisor (RAG-Powered)"
        self.rag_engine = CyberKnowledgeRAGEngine()
        if db_manager is None:
            from src.database.db_manager import DatabaseManager
            db_manager = DatabaseManager()
        self.db = db_manager
        self.system_prompt = """
You are Cyber Shield Bot, an empathetic, highly knowledgeable, and authoritative Cyber Security & Fraud Emergency AI Advisor.
Your objective:
1. Provide immediate, clear, actionable instructions to individuals facing suspected or active cyber fraud (bank scams, phishing, voice spoofing, OTP theft, digital arrest).
2. Ground your advice strictly in the provided verified cybersecurity reference playbooks (RAG Context).
3. Always structure your emergency response clearly into:
   - 🚨 IMMEDIATE ACTIONS (First 5 minutes checklist: call 1930, freeze cards, disconnect Wi-Fi)
   - 🛡️ DEFENSE & RECOVERY PROTOCOL (Step-by-step account recovery)
   - 💡 SCAM MECHANISM (Explain how scammers manipulate victims)
   - 📞 VERIFIED HELPLINES & SOURCES (Cite official portals: 1930, cybercrime.gov.in, RBI circulars)
4. Maintain a reassuring, calm, and security-focused tone.
"""

    def respond(self, message: str, chat_history: List[Dict[str, str]] = None, idempotency_key: str = None) -> str:
        if not message or not message.strip():
            return "Hello! I am **Cyber Shield Bot** (RAG-Powered Security Advisor). How can I help protect you or investigate a cyber threat today?"

        if chat_history is None:
            chat_history = []

        # Step 0: Check Idempotency Cache
        if not idempotency_key:
            payload_str = f"{message.strip().lower()}_ctx:{json.dumps(chat_history[-2:] if chat_history else [])}"
            idempotency_key = self.db.generate_idempotency_key(payload_str, prefix="bot_response")

        cached_rec = self.db.get_idempotent_record(idempotency_key, scope="bot_response")
        if cached_rec and "response_text" in cached_rec:
            prefix_badge = "⚡ *(Idempotent Cached Advice)*\n\n" if not cached_rec["response_text"].startswith("⚡") else ""
            return f"{prefix_badge}{cached_rec['response_text']}"

        # Retrieve top relevant cybersecurity playbooks via RAG semantic search
        rag_results = self.rag_engine.search(message, top_k=2)
        rag_context = self.rag_engine.format_rag_context(rag_results)

        # Try Groq Free API first if available
        bot_reply = None
        if Config.is_groq_available():
            try:
                bot_reply = self._respond_with_groq(message, chat_history, rag_context)
            except Exception as e:
                print(f"[BotAgent] Groq API call failed: {e}. Using RAG Knowledge Base fallback engine.")

        if not bot_reply:
            bot_reply = self._respond_with_knowledge_base(message, rag_results)

        # Cache generated response
        self.db.save_idempotent_record(
            idempotency_key=idempotency_key,
            request_hash=idempotency_key.split(":")[-1],
            scope="bot_response",
            response_data={"response_text": bot_reply}
        )

        return bot_reply

    def _respond_with_groq(self, message: str, chat_history: List[Dict[str, str]], rag_context: str) -> str:
        try:
            from groq import Groq
        except ImportError:
            raise RuntimeError("The 'groq' package is not installed.")

        client = Groq(api_key=Config.GROQ_API_KEY)
        
        system_with_rag = (
            f"{self.system_prompt}\n\n"
            f"=== VERIFIED CYBERSECURITY RAG KNOWLEDGE CONTEXT ===\n"
            f"{rag_context}\n"
            f"===================================================\n\n"
            f"Instructions: Use the above verified RAG context to answer the user's scenario. Cite official sources provided in the context."
        )

        messages = [{"role": "system", "content": system_with_rag}]
        for item in chat_history[-6:]:
            messages.append({"role": item.get("role", "user"), "content": item.get("content", "")})
        messages.append({"role": "user", "content": message})

        response = client.chat.completions.create(
            messages=messages,
            model="llama-3.3-70b-versatile",
            temperature=0.2,
            max_tokens=700
        )
        
        return response.choices[0].message.content

    def _respond_with_knowledge_base(self, message: str, rag_results: List[Any]) -> str:
        """Generates RAG-backed structured emergency guidance for offline mode."""
        if rag_results and len(rag_results) > 0:
            doc, score = rag_results[0]
            actions = "\n".join([f"- {step}" for step in doc.get("immediate_actions", [])])
            match_pct = int(min(1.0, score) * 100)
            
            return f"""🚨 **EMERGENCY ACTION PROTOCOL: {doc.get('title')}**
*(RAG Semantic Match Score: {match_pct}% | Category: {doc.get('category')})*

{doc.get('description')}

**Immediate Action Checklist:**
{actions}

💡 **Security Mechanism:** Scammers rely on artificial urgency, authority impersonation, or credential theft to induce panic. Always pause and verify independently.

📞 **Verified Official Source:** {doc.get('source')} | **National Cybercrime Helpline:** `1930`"""

        # Generic RAG fallback if no high-confidence match
        return f"""🛡️ **Cyber Shield Advisor Guidance**

Thank you for reaching out. Here is standard protocol for evaluating potential cyber threats:

1. **Verify Sender Identity:** Always verify calls, emails, or messages through official customer care numbers listed on official websites.
2. **Never Share Credentials:** Never reveal OTPs, PINs, passwords, or CVV numbers over phone or chat.
3. **Inspect URLs carefully:** Do not log in through links sent in SMS or WhatsApp.
4. **Report Suspicious Incidents:** File reports on official cyber crime portals (e.g. `cybercrime.gov.in` or helpline `1930`).

You can also use our **Text Scanner** or **Voice AI Scanner** tabs to analyze suspicious messages or voice recordings!"""
