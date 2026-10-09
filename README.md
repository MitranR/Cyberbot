# 🛡️ Cyber Fraud Shield: AI-Powered Fraud Defense & Assistant

An interactive web application and multi-agent AI system designed to protect users against cyber fraud, voice cloning, phishing messages, and social engineering attacks.

Built for **HackIndia** with a focus on **100% Free APIs & Free AI Agents** (Groq, Hugging Face, Google Gemini) alongside a zero-dependency local simulation engine.

---

## 🌟 Key Features

1. **🤖 Cyber Shield Emergency Assistant (AI Bot):**
   - Interactive chatbot with pre-configured emergency panic buttons (*"Shared OTP/PIN"*, *"Clicked Fake Link"*, *"Fake Police/Customs Threat"*).
   - Provides immediate step-by-step playbooks to freeze accounts, revoke access, and file cybercrime complaints.

2. **🎙️ Speech & Voice AI Spoof Scanner:**
   - **Voice Transcription (Whisper):** Converts spoken call audio into transcripts.
   - **Synthetic / Cloned Voice Detection:** Analyzes spectral micro-variations, pitch stability, and acoustic artifacts to detect deepfake audio.
   - **Content Fraud Evaluation:** Scans transcription for fraud tactics.

3. **🔍 Text Scam & Phishing Scanner:**
   - Evaluates SMS, emails, and WhatsApp messages.
   - Generates a **Threat Risk Score (0-100)**, classifies threat level (*Safe*, *Caution*, *High Alert*, *Critical Threat*), highlights matched tactics, and gives actionable advice.

4. **⚡ Dual-Engine System:**
   - **Free API Mode:** Integrates free-tier AI APIs (Groq Llama 3.3 70B & Whisper Large v3, Hugging Face, Gemini 1.5 Flash).
   - **Simulation Fallback Engine:** Built-in heuristic engine that works offline without any external keys or GPU requirements.

---

## 🚀 Quick Start (Running the Web App)

### 1. Prerequisite Check
Ensure Python 3.10+ is installed on your system.

### 2. Launch the Application
Run the Streamlit web dashboard directly from your terminal:

```bash
streamlit run src/app.py
```

The web application will automatically open in your browser at `http://localhost:8501`.

---

## 🌐 Running the Reflex Web Frontend

Cyber Fraud Shield includes an institutional-grade Python web frontend built using **Reflex** (`reflex.dev`). It features a two-tier top header ribbon, a live morphing voice waveform, interactive audio upload analysis, and direct Python backend agent integration.

### Launch Reflex Frontend:
```bash
python -m reflex run
```
The Reflex web portal will open at `http://localhost:3000`.

---

## 🔑 Step-by-Step Instructions: Free API Keys & Free AI Agents

To power your AI agents with ultra-fast LLMs and Whisper model inference, follow these step-by-step guides to acquire free API keys.

### 1. Groq Free API Key (Recommended - Ultra Fast)
- **What it provides:** Free access to `Llama 3.3 70B` (Text & Bot Agent) and `Whisper Large v3` (Voice Transcription).
- **Steps:**
  1. Visit [console.groq.com](https://console.groq.com) and create a free account.
  2. Go to **API Keys** → Click **Create API Key**.
  3. Copy your key (starts with `gsk_...`).
  4. Paste into `.env` as `GROQ_API_KEY=gsk_...`.

### 2. Hugging Face Free Token
- **What it provides:** Free access to open-source speech transformers and NLP models.
- **Steps:**
  1. Visit [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens).
  2. Create a free account → Click **New Token** (User Role: Read).
  3. Copy your token (starts with `hf_...`).
  4. Paste into `.env` as `HUGGINGFACE_API_KEY=hf_...`.

### 3. Google Gemini Free API Key
- **What it provides:** Free access to `Gemini 1.5 Flash` / `Gemini 2.0 Flash` for threat reasoning.
- **Steps:**
  1. Visit [aistudio.google.com](https://aistudio.google.com).
  2. Click **Get API Key** → Create Key in a new project.
  3. Copy key and paste into `.env` as `GEMINI_API_KEY=AIza...`.

---

## 🛠️ Environment Configuration

Copy `.env.example` to create your local `.env` file:

```bash
cp .env.example .env
```

Edit `.env` with your API keys:

```env
GROQ_API_KEY=gsk_your_groq_key_here
HUGGINGFACE_API_KEY=hf_your_hf_token_here
GEMINI_API_KEY=AIza_your_gemini_key_here
FORCE_SIMULATION_MODE=False
```

*Note: If keys are left blank, Cyber Fraud Shield automatically runs in built-in **Simulation Fallback Mode**.*

---

## 🏗️ Multi-Agent Architecture

```
                       +-----------------------------------+
                       |    Streamlit Web Application      |
                       |          (src/app.py)             |
                       +-----------------+-----------------+
                                         |
                                         v
                       +-----------------+-----------------+
                       |    Free Agent Orchestrator        |
                       |    (src/agents/orchestrator.py)   |
                       +-------+---------+---------+-------+
                               |         |         |
       +-----------------------+         |         +-----------------------+
       |                               |                               |
       v                               v                               v
+------------------+           +-------------------+           +-------------------+
| Text Scam Agent  |           | Speech & Voice    |           | Cyber Shield Bot  |
| (text_agent.py)  |           | Spoof Agent       |           | (bot_agent.py)    |
|                  |           | (speech_agent.py) |           |                   |
| - Phishing score |           | - Whisper STT     |           | - Emergency advice|
| - Urgency cues   |           | - AI voice spoof  |           | - Banking freeze  |
| - URL scanner    |           | - Spectral checks |           | - Cyber reporting |
+------------------+           +-------------------+           +-------------------+
```

---

## 📂 Project File Structure

```
HackIndia/
├── implementation_plan.md      # Initial implementation plan & roadmap
├── requirements.txt            # Python dependencies (streamlit, groq, openai, etc.)
├── .env.example                # Free API keys template
├── README.md                   # Complete documentation & step-by-step setup guide
└── src/
    ├── __init__.py
    ├── config.py               # Configuration & threat indicator rules
    ├── app.py                  # Streamlit dark-mode web application
    └── agents/
        ├── __init__.py
        ├── text_agent.py       # Fraud text analysis agent
        ├── speech_agent.py     # Voice transcription & AI voice spoof agent
        ├── bot_agent.py        # Cyber Shield emergency advisor AI bot
        └── orchestrator.py     # Multi-agent coordination pipeline
```

---

---

## 📊 Text Fraud ML Model

Cyber Fraud Shield now includes a **trained ML classifier** to detect SMS/text scams with higher accuracy than pure keyword heuristics.

### Dataset
- **Source:** [SMS Spam Collection Dataset](https://www.kaggle.com/datasets/uciml/sms-spam-collection-dataset) (UCI ML Repository)
- **Size:** 5,574 labeled SMS messages (ham/spam)
- **Location:** `src/model/data/sms_spam_dataset.csv`

### Pipeline
- **TF-IDF Vectorizer** with uni-gram & bi-gram features (max 5,000 features)
- **Logistic Regression** classifier
- Train/test split: 80/20, stratified

### Performance
| Metric    | Value  |
|-----------|--------|
| Accuracy  | ~97.9% |
| F1 (spam) | ~0.91  |

### Retraining
To retrain from scratch (e.g., with additional data):
```bash
pip install -r requirements.txt
python -m src.model.train_text_model
```

This regenerates:
- `src/model/artifacts/tfidf_vectorizer.joblib`
- `src/model/artifacts/fraud_classifier.joblib`

### Known Limitation
The dataset skews toward spam-style promotional messages. Legitimate transactional notifications (shipping confirmations, delivery updates, OTP messages) may occasionally receive elevated risk scores. Future work includes augmenting the dataset with more "legitimate notification" examples.

---

## 🚨 Emergency Contacts (India & Global)

- **National Cyber Crime Helpline (India):** `1930`
- **Official Reporting Portal:** [cybercrime.gov.in](https://cybercrime.gov.in)
- **Immediate Action:** If you have shared financial details, call your bank's emergency line to block cards immediately.