# Cyber Fraud Shield: Speech & Text Analysis AI Assistant

An educational, beginner-friendly walkthrough and interactive chatbot application designed to help users identify and overcome cyber fraud. The project focuses exclusively on:
1. **Speech Analysis:** Voice transcription and AI spoofing/cloned voice detection.
2. **Text Fraud Analysis:** Scanning suspicious text messages, emails, and phone call transcripts for scam indicators.
3. **Interactive Cyber Fraud Bot:** A conversational helper ("Cyber Shield Bot") that analyzes cases, guides users on immediate steps to secure accounts, and teaches preventative security habits.

## User Review Required

> [!IMPORTANT]
> **Demo/Simulation vs. Production Modes:**
> - To make this project run instantly without external keys or a GPU, we will implement a dual-mode configuration:
>   - **Simulation Mode (Default):** Runs local rule-based heuristics and templates to analyze messages, transcribe standard test audio files, detect simulated synthetic voice traits, and power the chatbot using local responses.
>   - **Production Mode:** Enables real API calls (e.g., Groq API for LLM chatbot & text analysis, Hugging Face transformers/Whisper for speech transcription and wav2vec2 spoofing classification).
> - Set up will be simple, controlled via a local `.env` configuration file.

> [!TIP]
> **Streamlit Dashboard Design:**
> The dashboard will use a sleek cybersecurity dark-theme with clear visual panels:
> - **Threat Alert Level:** Visual widgets (Safe, Caution, High Alert, Critical) based on analyzer outputs.
> - **Incident Response Guide:** Custom expandable checklists for common scam types (e.g., Bank Impersonation, Courier Scam, Support Scam).

## Open Questions

None. The scope is now focused specifically on speech, text, and the cyber fraud assistant bot.

## Proposed Changes

We will create a clean workspace inside `C:/Users/mitra/.gemini/antigravity/scratch/cyber_fraud_shield` with the following structure:

---

### [Cyber Fraud Shield Application]

#### [NEW] [requirements.txt](file:///C:/Users/mitra/.gemini/antigravity/scratch/cyber_fraud_shield/requirements.txt)
Specifies dependencies: `streamlit`, `python-dotenv`, `openai`, `groq`, `soundfile`, `numpy`, `matplotlib`.

#### [NEW] [config.py](file:///C:/Users/mitra/.gemini/antigravity/scratch/cyber_fraud_shield/src/config.py)
Configures simulation mode vs. production API keys (Groq, OpenAI, Hugging Face) and stores fallback scam definitions.

#### [NEW] [speech_analyzer.py](file:///C:/Users/mitra/.gemini/antigravity/scratch/cyber_fraud_shield/src/speech_analyzer.py)
Handles voice analysis:
- **Transcription (Whisper):** Converts uploaded speech clips to text.
- **Spoof Detection (wav2vec2):** Evaluates voice audio for signs of synthetic generation or cloning (spectral variance, voice stability). Contains production Hugging Face pipeline + local simulator.

#### [NEW] [text_analyzer.py](file:///C:/Users/mitra/.gemini/antigravity/scratch/cyber_fraud_shield/src/text_analyzer.py)
Scans text messages (SMS, email, chats) for scam indicators:
- Evaluates urgency cues, suspicious links, credential requests, authority impersonations.
- Outputs threat rating, type of scam (e.g., Phishing, Vishing, Tax fraud), and key warning signs.

#### [NEW] [bot.py](file:///C:/Users/mitra/.gemini/antigravity/scratch/cyber_fraud_shield/src/bot.py)
The Cyber Shield conversational bot:
- Maintains context-aware chat history.
- Guides users who have encountered cyber fraud (e.g., banking freezes, phishing response steps, reporting to authorities).
- Orchestrates calling the speech and text engines if the user provides a transcript or file.

#### [NEW] [app.py](file:///C:/Users/mitra/.gemini/antigravity/scratch/cyber_fraud_shield/src/app.py)
Premium Streamlit frontend:
- **Tab 1: Cyber Shield Chatbot:** Full-screen conversational AI assistant with pre-selected panic/emergency buttons (e.g. "I shared my PIN!", "I got a suspicious SMS").
- **Tab 2: Speech AI Scanner:** Drag-and-drop audio uploader to transcribe and run spoof checking.
- **Tab 3: Text Scanner:** Paste message area highlighting scam tactics and listing immediate defense checklists.

#### [NEW] [README.md](file:///C:/Users/mitra/.gemini/antigravity/scratch/cyber_fraud_shield/README.md)
Beginner-friendly step-by-step documentation on files, architecture, how AI works to solve fraud, and guidance on how to run and customize it.

## Verification Plan

### Automated Tests
- Verification scripts to ensure simulation mode and engines output correct formats (JSON analyses and scores).
- Run `python src/bot.py --test` to verify basic chatbot conversational flow.

### Manual Verification
- Launch the Streamlit dashboard: `streamlit run src/app.py`.
- Paste known spam messages (e.g., "Urgent: Your account is locked! Click link...") and check the parsed metrics.
- Chat with Cyber Shield Bot to verify responses for user security panic scenarios.
